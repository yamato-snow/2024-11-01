import flet as ft

class TimerDisplay(ft.Container):
    """タイマーの時間表示コンポーネント"""
    
    def __init__(self):
        """タイマー表示の初期化"""
        super().__init__()
        
        self.time_text = ft.Text(
            value="00:00",
            size=48,
            weight=ft.FontWeight.BOLD,
            color=ft.colors.ON_SURFACE,
        )
        
        # コンテナの設定
        self.content = self.time_text
        self.alignment = ft.alignment.center
        
    def update_time(self, minutes: int, seconds: int):
        """
        表示時間の更新
        Args:
            minutes (int): 分
            seconds (int): 秒
        """
        self.time_text.value = f"{minutes:02d}:{seconds:02d}"

    def reset(self):
        """表示をリセット"""
        self.time_text.value = "00:00"