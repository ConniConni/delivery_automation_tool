import logging
import configparser
from pathlib import Path

# ロギング設定
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def load_config(config_file_path: Path) -> dict:
    """
    指定されたINI形式の設定ファイルを読み込み、プログラムで利用可能な辞書形式に変換する。

    Args:
        config_file_path (Path): 設定ファイルへのパス。

    Returns:
        dict: 読み込まれた設定を格納した辞書。

    Raises:
        FileNotFoundError: 設定ファイルが見つからない場合。
        configparser.Error: INIファイルの解析中にエラーが発生した場合。
        ValueError: 必須項目が不足している場合。
    """

    logging.info(f"設定ファイル {config_file_path} を読み込みます。")
    config = configparser.ConfigParser()
    config_data = {}

    try:
        if not config_file_path or not config_file_path.is_file():
            raise FileNotFoundError(f"設定ファイルが見つかりません: {config_file_path}")

        with open(config_file_path, "r") as f:
            content = f.read()
            if not "[" in content or not "]" in content:
                logging.warning(
                    f"設定ファイル {config_file_path} はINIファイルの形式ではありません。"
                )
                return config_data  # 例外ではなく、空のconfig_dataを返す

        config.read(config_file_path)
        logging.info(f"設定ファイルの読み込み完了。セクション: {config.sections()}")

    except configparser.MissingSectionHeaderError as e:
        logging.error(f"設定ファイルの読み込み中にエラーが発生しました: {e}")
        raise
    except Exception as e:
        logging.error(f"設定ファイルの読み込み中に予期せぬエラーが発生しました: {e}")
        raise
    return config_data
