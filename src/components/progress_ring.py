import flet as ft

class ProgressRing(ft.Container):
    """グラデーションエフェクトを持つ円形のプログレスインジケータ"""
    
    def __init__(
        self,
        width: int = 300,
        height: int = 300,
        start_color: str = "#FF6B6B",
        end_color: str = "#4ECDC4"
    ):
        """
        プログレスリングの初期化
        Args:
            width (int): リングの幅
            height (int): リングの高さ
            start_color (str): グラデーション開始色
            end_color (str): グラデーション終了色
        """
        super().__init__()
        
        # コンテナの基本設定
        self.width = width
        self.height = height
        self.border_radius = width // 2  # 完全な円形にするため
        
        # グラデーションの設定
        self.gradient = ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=[start_color, end_color],
        )
        
        # アニメーション設定
        self.animate = ft.animation.Animation(
            duration=300,
            curve="easeInOut"
        )
        
        # クリッピング設定
        self.clip_behavior = ft.ClipBehavior.HARD_EDGE

    def update_progress(self, progress: float):
        """
        プログレスの更新
        Args:
            progress (float): 0.0から1.0の間の進行度
        """
        self.height = int(self.width * progress)

    def reset(self):
        """プログレスリングをリセット"""
        self.height = self.width