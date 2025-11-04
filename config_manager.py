import logging
import configparser
from pathlib import Path

# ロギング設定
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def load_config(config_file_path: Path):
    """
    指定された設定ファイルを読み込み、ConfigParseオブジェクトを返す。
    """

    logging.info(f"設定ファイル {config_file_path} を読み込みます。")
    config = configparser.ConfigParser()
    try:
        if not config_file_path or not config_file_path.is_file():
            raise FileNotFoundError(f"設定ファイルが見つかりません: {config_file_path}")

        with open(config_file_path, "r") as f:
            content = f.read()
            if not "[" in content or not "]" in content:
                logging.warning(
                    f"設定ファイル {config_file_path} はINIファイルの形式ではありません。"
                )
                return config  # 例外ではなく、空のconfigを返す

        config.read(config_file_path)
        logging.info(f"設定ファイルの読み込み完了。セクション: {config.sections()}")

    except configparser.MissingSectionHeaderError as e:
        logging.error(f"設定ファイルの読み込み中にエラーが発生しました: {e}")
        raise
    except Exception as e:
        logging.error(f"設定ファイルの読み込み中に予期せぬエラーが発生しました: {e}")
        raise
    return config
