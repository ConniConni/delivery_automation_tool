###############################################################
#
#
# 実行ディレクトリ
# delivery_automation_tool
#
# 以下でもOK
# python tests/test_main.py
#
# 実行コマンド
# python -m unittest discover tests
#
#   python -m: 指定されたモジュールをスクリプトとして実行するPythonの機能
#              ここでは unittest を実行
#   discover:  unittest コマンドのサブコマンド
#              指定されたディレクトリとそのサブディレクトリを再帰的に
#              走査しテストファイルを探索
#   tests:     discoverサブコマンドに渡す引数
#              テストファイルの探索開始のルートディレクトリを指定
#
##############################################################

import unittest
import tempfile  # 一時ディレクトリ作成に必要
from pathlib import Path  # Pathオブジェクトの操作に必要
import shutil  # 指定されたディレクトリを再帰的に完全に削除するのに必要


class TestMainFunctions(unittest.TestCase):
    """
    tempfile.mkdtemp() で一時ディレクトリを作ることで、実際のファイルシステムを汚さずにテスト実施
    """

    def setUp(self):
        # 一時ディレクトリの作成
        self.test_dir = Path(tempfile.mkdtemp())

        # パスを結合して、テストで使用するパスを設定
        self.config_path = self.test_dir / "test_config.ini"
        self.invalid_config_path = self.test_dir / "invalid_config.ini"
        self.non_existent_path = self.test_dir / "non_existent.ini"
        self.output_file = self.test_dir / "output.txt"

        # 有効な設定ファイルの作成
        with open(self.config_path, "w") as f:
            f.write("[Settings]\n")
            f.write("key = value\n")

        # 不正な設定ファイルの作成
        with open(self.invalid_config_path, "w") as f:
            f.write("これはINIファイルではありません")

    def tearDown(self):
        """
        各テスト実行後に実行されるクリーンアップ処理
        作成した一時ディレクトリ(self.test_dir)を削除する
        """
        shutil.rmtree(self.test_dir)
