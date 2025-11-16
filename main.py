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
import sys
import argparse
import configparser
from pathlib import Path

import config_manager
import file_processor

# ロギング設定
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


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
        type=Path,
        default="/Users/koni/Desktop/delivery_automation_tool/config.ini",
    )

    args = parser.parse_args()

    if not args.config_file_path:
        logging.error("設定ファイルへのパスが指定されていません。")
        sys.exit(1)

    logging.info(f"iniファイル: {args.config_file_path}")

    try:
        config = config_manager.load_config(args.config_file_path)

    except FileNotFoundError as e:
        logging.error(e)
        sys.exit(1)
    except ValueError as e:
        logging.error(e)
        sys.exit(1)
    except configparser.MissingSectionHeaderError as e:
        logging.error(f"ファイルの読み込み中にエラーが発生しました。:{e}")
        sys.exit(1)
    except Exception as e:
        logging.error(f"ファイルの読み込み中に予期せぬエラーが発生しました。:{e}")
        sys.exit(1)

    file_processor.process_files(config)


if __name__ == "__main__":
    main()
