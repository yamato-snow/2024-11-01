import flet as ft
import time
from datetime import datetime
import threading

class GradientTimer:
    """グラデーションエフェクトを使用したビジュアルタイマークラス"""
    
    def __init__(self, page: ft.Page):
        """
        タイマーの初期化
        Args:
            page (ft.Page): Fletページオブジェクト
        """
        # ページとタイマーの状態管理用の変数
        self.page = page
        self.is_running = False          # タイマー実行状態
        self.total_seconds = 0           # 設定された合計秒数
        self.remaining_seconds = 0       # 残り秒数
        self.start_time = None          # 開始時刻
        self.timer_thread = None        # タイマー実行用スレッド
        
        # プログレスリングの基本設定
        # プログレスリングとは、進行状況を円形で表示するUI要素です
        self.progress_ring = ft.Container(
            # コンテナのサイズ設定
            width=300,      # 横幅を300ピクセルに設定
            height=300,     # 高さを300ピクセルに設定
            
            # 角の丸み設定
            # border_radiusを width/2 (この場合は150) にすることで完全な円形になります
            # 例：100x100のコンテナなら border_radius=50 で円形になります
            border_radius=150,
            
            # グラデーションの設定
            # LinearGradientは直線的なグラデーションを作成します
            gradient=ft.LinearGradient(
                # グラデーションの開始位置と終了位置を指定
                begin=ft.alignment.top_center,    # 上中央から開始
                end=ft.alignment.bottom_center,   # 下中央で終了
                
                # グラデーションの色を指定
                # 配列の最初の色から最後の色にグラデーション変化します
                colors=[
                    "#FF6B6B",  # 開始色: 明るい赤色
                    "#4ECDC4"   # 終了色: ターコイズブルー
                ],
            ),
            
            # アニメーション設定
            # アニメーションを適用することで、値が変更されたときに滑らかに変化します
            animate=ft.animation.Animation(
                300,         # アニメーションの継続時間（ミリ秒）
                "easeInOut"  # アニメーションの種類：始めと終わりがなめらかな動き
            ),
            
            # クリッピング設定
            # コンテナからはみ出た要素の処理方法を指定します
            # HARD_EDGE: はみ出た部分を完全に切り取ります
            clip_behavior=ft.ClipBehavior.HARD_EDGE,
        )

        # タイマー時間表示用テキスト
        self.time_display = ft.Text(
            "00:00",
            size=48,
            weight=ft.FontWeight.BOLD,
            color=ft.colors.ON_SURFACE,
        )
        
        # 開始/一時停止ボタン
        self.start_button = ft.IconButton(
            icon=ft.icons.PLAY_ARROW,
            icon_color=ft.colors.ON_SURFACE,
            icon_size=32,
            on_click=self.toggle_timer,
        )
        
        # リセットボタン
        self.reset_button = ft.IconButton(
            icon=ft.icons.REFRESH,
            icon_color=ft.colors.ON_SURFACE,
            icon_size=32,
            on_click=self.reset_timer,
        )
        
        # 時間入力フィールド
        self.time_input = ft.TextField(
            value="25",
            width=100,
            text_align=ft.TextAlign.RIGHT,
            keyboard_type=ft.KeyboardType.NUMBER,
        )
        
        # メインのレイアウト構築
        # ft.Columnを使用して要素を縦方向に配置する垂直レイアウトを作成
        self.layout = ft.Column(
            controls=[
                # 1. タイマー表示エリア: プログレスリングとタイマー表示の組み合わせ
                ft.Container(
                    # ft.Stackを使用して複数の要素を z-index（重なり順）で配置
                    # 後に追加された要素ほど前面に表示される
                    content=ft.Stack([
                        # プログレスリング（背景として配置）
                        # self.progress_ringは円形のプログレスインジケータ
                        # アニメーションやグラデーションなどの視覚的効果を持つ
                        self.progress_ring,

                        # タイマーの数値表示（前面に配置）
                        ft.Container(
                            # self.time_displayは時間を表示するテキストウィジェット
                            content=self.time_display,
                            # コンテナ内でtime_displayを中央に配置
                            alignment=ft.alignment.center,
                        )
                    ]),
                    # このコンテナ全体のサイズを固定
                    height=300,  # プログレスリングの表示高さ
                    width=300,   # プログレスリングの表示幅
                    # Stack全体をコンテナの中央に配置
                    alignment=ft.alignment.center,
                ),
                
                # 2. コントロールエリア: 入力フィールドとボタン類
                ft.Container(
                    # ft.Rowを使用して要素を横方向に配置する水平レイアウトを作成
                    content=ft.Row(
                        [
                            # 時間入力用のテキストフィールド
                            self.time_input,    
                            # 単位「分」の表示（テキストサイズ16で表示）
                            ft.Text("分", size=16),
                            # 開始/一時停止ボタン
                            self.start_button,  
                            # リセットボタン
                            self.reset_button   
                        ],
                        # Row内の要素を水平方向の中央に配置
                        alignment=ft.MainAxisAlignment.CENTER,
                        # 各要素間の間隔を20ピクセルに設定
                        spacing=20,
                    ),
                    # コントロールエリア全体の上部に20ピクセルの余白を追加
                    # これにより、タイマー表示エリアとの間に適切な空間を作る
                    margin=ft.margin.only(top=20),
                ),
            ],
            # Column内の要素を水平方向（副軸）の中央に配置
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            # Column内の要素を垂直方向（主軸）の中央に配置
            alignment=ft.MainAxisAlignment.CENTER,
        )

    def update_timer(self):
        """タイマーの更新を行うメソッド（別スレッドで実行）"""
        while self.is_running:
            if not self.start_time:
                break
                
            # 経過時間の計算
            elapsed = datetime.now() - self.start_time
            self.remaining_seconds = max(0, self.total_seconds - int(elapsed.total_seconds()))
            
            # プログレスリングの高さを更新（視覚的なフィードバック）
            progress = self.remaining_seconds / self.total_seconds
            height = int(300 * progress)
            self.progress_ring.height = height
            
            # 時間表示の更新
            minutes = self.remaining_seconds // 60
            seconds = self.remaining_seconds % 60
            self.time_display.value = f"{minutes:02d}:{seconds:02d}"
            
            # タイマー完了チェック
            if self.remaining_seconds <= 0:
                self.timer_complete()
                break
                
            self.page.update()
            time.sleep(0.1)  # CPUの負荷を下げるために短い待機を入れる

    def toggle_timer(self, e):
        """開始/一時停止の切り替えを行うメソッド"""
        if not self.is_running:
            self.start_timer(e)
        else:
            self.pause_timer(e)

    def start_timer(self, e):
        """タイマーを開始するメソッド"""
        if not self.is_running:
            try:
                # 入力値の検証
                minutes = int(self.time_input.value)
                if minutes <= 0:
                    raise ValueError
                
                # タイマーの初期設定
                if self.remaining_seconds == 0:
                    self.total_seconds = minutes * 60
                    self.remaining_seconds = self.total_seconds
                self.start_time = datetime.now()
                self.is_running = True
                self.start_button.icon = ft.icons.PAUSE
                self.page.update()
                
                # 別スレッドでタイマーを実行
                self.timer_thread = threading.Thread(target=self.update_timer, daemon=True)
                self.timer_thread.start()
            except ValueError:
                # 無効な入力の場合のエラー処理
                pass

    def pause_timer(self, e):
        """タイマーを一時停止するメソッド"""
        self.is_running = False
        self.start_button.icon = ft.icons.PLAY_ARROW
        if self.timer_thread:
            self.timer_thread.join(0.1)
        self.page.update()

    def timer_complete(self):
        """タイマー完了時の処理を行うメソッド"""
        self.is_running = False
        self.start_button.icon = ft.icons.PLAY_ARROW
        self.progress_ring.gradient.colors = ["#4ECDC4", "#4ECDC4"]  # 完了時の色変更
        self.page.update()

    def reset_timer(self, e):
        """タイマーをリセットするメソッド"""
        # タイマーの停止とスレッドのクリーンアップ
        self.is_running = False
        if self.timer_thread:
            self.timer_thread.join(0.1)
            
        # UI要素のリセット
        self.remaining_seconds = 0
        self.start_time = None
        self.start_button.icon = ft.icons.PLAY_ARROW
        self.time_display.value = "00:00"
        self.progress_ring.height = 300
        self.progress_ring.gradient.colors = ["#FF6B6B", "#4ECDC4"]
        self.page.update()

class TimerApp:
    def __init__(self, page: ft.Page):
        # ベースとなるページの設定
        self.page = page
        
        #=========================================
        # 1. プログレスリング（グラデーション円）の設定
        #=========================================
        self.progress_ring = ft.Container(
            # サイズ設定：幅と高さを同じにして円形の基本形を作る
            width=300,
            height=300,
            
            # 完全な円形にするために、border_radiusを幅の半分に設定
            border_radius=150,
            
            # グラデーションの設定
            gradient=ft.LinearGradient(
                # グラデーションの方向を上から下に設定
                begin=ft.alignment.top_center,    # 開始位置: 上中央
                end=ft.alignment.bottom_center,   # 終了位置: 下中央
                
                # グラデーションの色設定
                colors=[
                    "#FF6B6B",  # 上部の色（赤系）
                    "#4ECDC4"   # 下部の色（青緑系）
                ],
                
                # グラデーションの位置制御（これが重要！）
                # stops=[0.0, 1.0] の場合：通常のグラデーション
                # 数値を変更することで、グラデーションの位置が変化
                stops=[0.0, 1.0]  
            ),
            
            # アニメーションの設定：色の変化を滑らかに
            animate=ft.animation.Animation(300, "easeInOut"),
        )

        #=========================================
        # 2. タイマー更新時の処理を簡略化
        #=========================================
        def update_timer(self):
            """
            1秒ごとに呼び出される更新処理
            """
            if self.is_running and self.remaining_time > 0:
                # 進行度を計算（0.0 から 1.0 の範囲）
                progress = 1 - (self.remaining_time / self.total_time)
                
                # グラデーションを更新
                self.progress_ring.gradient.stops = [progress, 1.0]
                self.progress_ring.update()
                
                # 残り時間を1秒減らす
                self.remaining_time -= 1
                
                # 表示を更新
                self.update_display()
                
                # 次の更新をスケジュール（1秒後）
                self.page.after(1000, self.update_timer)

def main(page: ft.Page):
    """メインアプリケーション関数"""
    # アプリケーションの基本設定
    page.title = "Gradient Task Timer"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = ft.colors.with_opacity(0.95, ft.colors.BLACK)
    page.window.width = 400
    page.window.height = 600
    page.padding = 20
    
    # タイマーインスタンスの作成と配置
    timer = GradientTimer(page)
    page.add(
        ft.Container(
            content=timer.layout,
            alignment=ft.alignment.center,
            expand=True,
        )
    )

if __name__ == "__main__":
    ft.app(target=main)