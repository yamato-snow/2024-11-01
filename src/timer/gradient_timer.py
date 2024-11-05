import flet as ft
from typing import Optional

from ..components.progress_ring import ProgressRing
from ..components.timer_display import TimerDisplay
from ..components.timer_controls import TimerControls
from ..utils.timer_logic import TimerLogic
from ..utils.constants import *

class GradientTimer(ft.UserControl):
    """グラデーションエフェクトを使用したビジュアルタイマー"""
    
    def __init__(self):
        """タイマーコンポーネントの初期化"""
        super().__init__()
        
        # UIコンポーネントの初期化
        self.progress_ring = ProgressRing(
            width=RING_SIZE,
            height=RING_SIZE,
            start_color=GRADIENT_START_COLOR,
            end_color=GRADIENT_END_COLOR
        )
        
        self.timer_display = TimerDisplay()
        
        # タイマーロジックの初期化
        self.timer_logic = TimerLogic(
            on_tick=self._on_timer_tick,
            on_complete=self._on_timer_complete
        )
        
        # コントロールの初期化
        self.timer_controls = TimerControls(
            on_start=self._on_start_click,
            on_reset=self._on_reset_click,
            initial_minutes=DEFAULT_MINUTES
        )

    def build(self):
        """UIレイアウトの構築"""
        return ft.Column(
            controls=[
                # タイマー表示エリア
                ft.Container(
                    content=ft.Stack([
                        self.progress_ring,
                        ft.Container(
                            content=self.timer_display,
                            alignment=ft.alignment.center
                        )
                    ]),
                    height=RING_SIZE,
                    width=RING_SIZE,
                    alignment=ft.alignment.center,
                ),
                
                # コントロールエリア
                self.timer_controls
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
        )

    def _on_timer_tick(self, remaining_seconds: int):
        """
        タイマーの毎秒の更新処理
        Args:
            remaining_seconds: 残り秒数
        """
        # 時間表示の更新
        minutes = remaining_seconds // 60
        seconds = remaining_seconds % 60
        self.timer_display.update_time(minutes, seconds)
        
        # プログレスリングの更新
        progress = self.timer_logic.progress
        self.progress_ring.update_progress(progress)
        
        # 画面の更新
        self.update()

    def _on_timer_complete(self):
        """タイマー完了時の処理"""
        # UIの更新
        self.timer_controls.update_start_button(False)
        self.progress_ring.gradient.colors = [COMPLETE_COLOR, COMPLETE_COLOR]
        self.update()

    def _on_start_click(self, e):
        """開始/一時停止ボタンのクリックハンドラ"""
        if not self.timer_logic.is_running:
            # タイマーの開始
            minutes = self.timer_controls.get_input_minutes()
            if minutes > 0 and self.timer_logic.start(minutes):
                self.timer_controls.update_start_button(True)
                # プログレスリングの色をリセット
                self.progress_ring.gradient.colors = [
                    GRADIENT_START_COLOR,
                    GRADIENT_END_COLOR
                ]
        else:
            # タイマーの一時停止
            self.timer_logic.pause()
            self.timer_controls.update_start_button(False)
        
        self.update()

    def _on_reset_click(self, e):
        """リセットボタンのクリックハンドラ"""
        self.timer_logic.reset()
        self.timer_display.reset()
        self.progress_ring.reset()
        self.timer_controls.update_start_button(False)
        self.update()