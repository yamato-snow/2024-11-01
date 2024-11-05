from datetime import datetime
import threading
from typing import Callable, Optional
import time

class TimerLogic:
    """タイマーの基本ロジックを管理するクラス"""
    
    def __init__(
        self,
        on_tick: Callable[[int], None],
        on_complete: Callable[[], None]
    ):
        """
        タイマーロジックの初期化
        Args:
            on_tick: 毎秒呼び出されるコールバック関数。残り秒数が渡される
            on_complete: タイマー完了時に呼び出されるコールバック関数
        """
        self.on_tick = on_tick
        self.on_complete = on_complete
        
        # タイマーの状態管理
        self._is_running = False
        self._total_seconds = 0
        self._remaining_seconds = 0
        self._start_time: Optional[datetime] = None
        self._timer_thread: Optional[threading.Thread] = None
        self._lock = threading.Lock()  # スレッドセーフな操作のため

    def start(self, minutes: int) -> bool:
        """
        タイマーを開始する
        Args:
            minutes: 設定する分数
        Returns:
            bool: 開始に成功した場合True
        """
        with self._lock:
            if self._is_running or minutes <= 0:
                return False
                
            # 新規開始の場合
            if self._remaining_seconds == 0:
                self._total_seconds = minutes * 60
                self._remaining_seconds = self._total_seconds
                
            self._start_time = datetime.now()
            self._is_running = True
            
            # タイマースレッドの開始
            self._timer_thread = threading.Thread(
                target=self._update_timer,
                daemon=True
            )
            self._timer_thread.start()
            return True

    def pause(self):
        """タイマーを一時停止する"""
        with self._lock:
            if self._is_running:
                self._is_running = False
                if self._timer_thread:
                    self._timer_thread.join(0.1)
                self._timer_thread = None

    def reset(self):
        """タイマーをリセットする"""
        with self._lock:
            self._is_running = False
            if self._timer_thread:
                self._timer_thread.join(0.1)
            self._timer_thread = None
            self._total_seconds = 0
            self._remaining_seconds = 0
            self._start_time = None

    def _update_timer(self):
        """タイマー更新のメインループ（別スレッドで実行）"""
        while self._is_running:
            with self._lock:
                if not self._start_time:
                    break
                    
                # 経過時間の計算
                elapsed = datetime.now() - self._start_time
                self._remaining_seconds = max(
                    0,
                    self._total_seconds - int(elapsed.total_seconds())
                )
                
                # コールバックの呼び出し
                self.on_tick(self._remaining_seconds)
                
                # タイマー完了チェック
                if self._remaining_seconds <= 0:
                    self._is_running = False
                    self.on_complete()
                    break
            
            time.sleep(0.1)  # CPU負荷軽減

    @property
    def is_running(self) -> bool:
        """タイマーが実行中かどうか"""
        return self._is_running

    @property
    def remaining_seconds(self) -> int:
        """残り秒数を取得"""
        return self._remaining_seconds

    @property
    def progress(self) -> float:
        """
        進行度を取得（0.0 〜 1.0）
        完了時もしくは未開始時は0.0を返す
        """
        if self._total_seconds == 0:
            return 0.0
        return self._remaining_seconds / self._total_seconds