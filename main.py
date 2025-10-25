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


# ロギング設定
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def main(config_file="config.ini"):
    """
    iniファイルとコマンド引数を解析し、内容を表示する関数
    """
    config = configparser.ConfigParser()
    config.read(config_file)

    parser = argparse.ArgumentParser(description="*説明*:xxxxxxxxxxx")

    parser.add_argument(
        "-i",
        "--ini_file",
        dest="config_file_path",
        help="設定ファイルへのパス",
        required=True,
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
    )

    args = parser.parse_args()
