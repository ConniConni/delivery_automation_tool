###############################################################
# 本ツールはTeams上のファイルのうち納品対象のファイルを抽出するものである。
#
# 主たる機能は次の２つである。
# 1. ローカルに納品時の階層でファイルをコピーする
# 2. 納品対象をツリー形式でファイル出力する
#
# 動作環境は以下のとおり。
# OS: Windows10/11
# Python: 3.8以上
# 必須コマンド: treeコマンド（Windows標準コマンド）
#
# 実行方法はREADME.md 参照
#
##############################################################

import logging
import configparser
import argparse
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
        if not config_file_path.is_file():
            raise FileNotFoundError(f"設定ファイルが見つかりません: {config_file_path}")
        config.read(config_file_path)
        logging.info(f"設定ファイルの読み込み完了。セクション: {config.sections()}")
    except Exception as e:
        logging.error(f"設定ファイルの読み込み中にエラーが発生しました: {e}")
        raise
    return config


def main():
    """
    コマンド引数を解析し、内容を表示する関数。
    """

    parser = argparse.ArgumentParser(
        description="作業ディレクトリから納品対象ファイルを抽出し、ローカルにコピーまたはツリー形式で出力するツールです"
    )

    parser.add_argument(
        "-i",
        "--ini_file",
        dest="config_file_path",
        help="設定ファイルへのパス",
        required=True,
        type=Path,
    )
    parser.add_argument(
        "-f",
        "--file_pattern",
        dest="file_pattern",
        help="抽出対象のファイル名のパターン",
        required=True,
    )
    parser.add_argument(
        "-t",
        "--tree_output",
        dest="tree_output_file_path",
        help="ツリー出力ファイルのパス。指定しない場合は標準出力に表示",
        type=Path,
    )

    args = parser.parse_args()

    logging.info(f"iniファイル: {args.config_file_path}")
    logging.info(f"抽出パターン: {args.file_pattern}")
    if args.tree_output_file_path:
        logging.info(f"ツリー出力先: {args.tree_output_file_path}")
    else:
        logging.info("ツリー出力先: 標準出力")

    config = load_config(args.config_file_path)
    logging.info(f"設定ファイル: {args.config_file_path} を読み込みました。")


if __name__ == "__main__":
    main()
