import flet as ft
import logging
from timer.timer_app import TimerApp

# ロギングの設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main(page: ft.Page):
    """
    アプリケーションのメインエントリーポイント
    Args:
        page: Fletページオブジェクト
    """
    try:
        # アプリケーションの作成
        app = TimerApp.create(page)
        logger.info("アプリケーションが正常に起動しました")
        
    except Exception as e:
        # エラーハンドリング
        logger.error(f"アプリケーションの起動中にエラーが発生しました: {str(e)}")
        # エラーメッセージをUI上に表示
        page.add(
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text(
                            "エラーが発生しました",
                            size=20,
                            color=ft.colors.RED_500,
                        ),
                        ft.Text(str(e)),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                alignment=ft.alignment.center,
                expand=True,
            )
        )

if __name__ == "__main__":
    try:
        ft.app(target=main)
    except Exception as e:
        logger.critical(f"アプリケーションが予期せぬエラーで終了しました: {str(e)}")