import logging

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
    logging.info(f"設定ファイル読み取り結果:{config}")
    logging.info(f"コピーキーワード:{file_pattern}")

    return
    # 1. 基準パス構築
    # 2. コピー先のディレクトリ構築(フォルダ作成)
    # 3. Teamsローカルパス配下の探索
    # 4. file_patternに合致するか判定
    # 5. 合致するファイルをコピー先のディレクトの該当の階層にコピー
    # 6. ログ
    # 7. エラー処理
