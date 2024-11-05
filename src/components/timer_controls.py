import flet as ft
from typing import Callable

class TimerControls(ft.Container):
    """タイマーのコントロール部分（入力フィールドとボタン）"""
    
    def __init__(
        self,
        on_start: Callable,
        on_reset: Callable,
        initial_minutes: str = "25"
    ):
        """
        タイマーコントロールの初期化
        Args:
            on_start (Callable): 開始/一時停止ボタンのコールバック
            on_reset (Callable): リセットボタンのコールバック
            initial_minutes (str): 初期設定時間（分）
        """
        super().__init__()
        
        # 時間入力フィールド
        self.time_input = ft.TextField(
            value=initial_minutes,
            width=100,
            text_align=ft.TextAlign.RIGHT,
            keyboard_type=ft.KeyboardType.NUMBER,
        )
        
        # 開始/一時停止ボタン
        self.start_button = ft.IconButton(
            icon=ft.icons.PLAY_ARROW,
            icon_color=ft.colors.ON_SURFACE,
            icon_size=32,
            on_click=on_start,
        )
        
        # リセットボタン
        self.reset_button = ft.IconButton(
            icon=ft.icons.REFRESH,
            icon_color=ft.colors.ON_SURFACE,
            icon_size=32,
            on_click=on_reset,
        )
        
        # レイアウトの構築
        self.content = ft.Row(
            controls=[
                self.time_input,
                ft.Text("分", size=16),
                self.start_button,
                self.reset_button
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20,
        )
        
        # マージン設定
        self.margin = ft.margin.only(top=20)
    
    def get_input_minutes(self) -> int:
        """
        入力された分数を取得
        Returns:
            int: 入力された分数（無効な入力の場合は0）
        """
        try:
            return int(self.time_input.value)
        except ValueError:
            return 0
    
    def update_start_button(self, is_running: bool):
        """
        開始/一時停止ボタンの状態を更新
        Args:
            is_running (bool): タイマー実行中かどうか
        """
        self.start_button.icon = (
            ft.icons.PAUSE if is_running else ft.icons.PLAY_ARROW
        )
    
    def disable_controls(self, disabled: bool = True):
        """
        コントロールの有効/無効を切り替え
        Args:
            disabled (bool): 無効にする場合はTrue
        """
        self.time_input.disabled = disabled
        self.start_button.disabled = disabled
        self.reset_button.disabled = disabled