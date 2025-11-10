import logging
import os
from pathlib import Path


logger = logging.getLogger(__name__)


def process_files(config: dict, file_pattern: str):
    """
    基準パスを構築し、指定されたファイルパターンに合致するファイルをTeamsパスから探し、コピーする。

    Args:
        config (dict): 設定ファイルの読み込み結果
        file_pattern (str): コマンドライン引数で指定したファイルパターンの文字列

    Returns:
        delivery_base_path (Path): 基準パス
    """

    search_root_path = config["teams_root_path"]
    destination_base_dir_path = (
        config["delivery_root_path"]
        / config["delivery_quarter"]
        / config["project_name"]
    )

    os.makedirs(destination_base_dir_path, exist_ok=True)
    logging.info(f"探索先ルートバス:{search_root_path}")
    logging.info(f"コピー先ベースディレクトリパス:{destination_base_dir_path}")
    logging.info(f"コピーキーワード:{file_pattern}")

    return
    # 1. 基準パス構築
    # 2. コピー先のディレクトリ構築(フォルダ作成)
    # 3. Teamsローカルパス配下の探索
    # for文
    # 現在の階層で、条件に一致するファイルがあるか判定
    # 再帰的に実施
    # 基準パス配下の全てのフォルダで実施
    # 4. file_patternに合致するか判定
    # 5. 合致するファイルをコピー先のディレクトの該当の階層にコピー
    # 6. ログ
    # 7. エラー処理
