import flet as ft
from .gradient_timer import GradientTimer
from ..utils.constants import *

class TimerApp:
    """タイマーアプリケーションのメインクラス"""
    
    def __init__(self, page: ft.Page):
        """
        アプリケーションの初期化
        Args:
            page: Fletページオブジェクト
        """
        self.page = page
        self._configure_page()
        self._init_ui()

    def _configure_page(self):
        """ページの基本設定を行う"""
        # ウィンドウ設定
        self.page.title = WINDOW_TITLE
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.bgcolor = ft.colors.with_opacity(0.95, ft.colors.BLACK)
        
        # ウィンドウサイズ設定
        self.page.window.width = WINDOW_WIDTH
        self.page.window.height = WINDOW_HEIGHT
        self.page.padding = WINDOW_PADDING

    def _init_ui(self):
        """UIコンポーネントの初期化と配置"""
        # タイマーインスタンスの作成
        timer = GradientTimer()
        
        # ページにタイマーを追加
        self.page.add(
            ft.Container(
                content=timer,
                alignment=ft.alignment.center,
                expand=True,
            )
        )

    @staticmethod
    def create(page: ft.Page) -> 'TimerApp':
        """
        アプリケーションのファクトリメソッド
        Args:
            page: Fletページオブジェクト
        Returns:
            TimerAppインスタンス
        """
        return TimerApp(page)