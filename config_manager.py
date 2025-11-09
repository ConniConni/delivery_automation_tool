import logging
import configparser
from pathlib import Path

logger = logging.getLogger(__name__)


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

    if not config_file_path.is_file():
        raise FileNotFoundError(f"設定ファイルが見つかりません: {config_file_path}")

    config.read(config_file_path, encoding="utf-8")

    if "General" not in config:
        raise ValueError("[General]セクションが見つかりません。")

    general_section = config["General"]

    required_general_keys = {
        "teams_root_path": Path,
        "delivery_root_path": Path,
        "project_name": str,
        "item_name": str,
        "delivery_quarter": str,
    }

    for key, expected_type in required_general_keys.items():
        if key not in general_section:
            raise ValueError(f"[General]セクションの必須項目'{key}'が見つかりません。")
        value = general_section.get(key)

        if value is None or value is "":
            raise ValueError(f"[General]セクションの必須項目'{key}'の値が空です。")

        try:
            if expected_type == Path:
                config_data[key] = Path(value)
            else:
                config_data[key] = value

        except ValueError:
            raise ValueError(
                f"[General]セクションの'{key}'の値が不正な型です。期待される型: {expected_type.__name__}, 実際の値: '{value}'"
            )

    config_data["mappings"] = {}
    if "Mappings" not in config:
        raise ValueError("[Mappings]セクションが見つかりません。")

    mappings_section = config["Mappings"]

    placeholder_value = config_data["item_name"]

    for key, value in mappings_section.items():
        value = mappings_section.get(key)

        replaced_value = value.replace("[案件名]", placeholder_value)
        config_data["mappings"][key] = Path(replaced_value)

    return config_data
