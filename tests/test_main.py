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
import sys
import io
import tempfile  # 一時ディレクトリ作成に必要
from pathlib import Path  # Pathオブジェクトの操作に必要
import shutil  # 指定されたディレクトリを再帰的に完全に削除するのに必要
import configparser
from unittest.mock import patch

# テスト用モジュールをインポート
from main import main, load_config


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
        作成した一時ディレクトリ(self.test_dir)を削除
        """
        shutil.rmtree(self.test_dir)

    def test_load_config_success(self):
        """
        有効な設定ファイルが正常に読み込まれることを確認
        """
        config = load_config(self.config_path)
        self.assertIsInstance(config, configparser.ConfigParser)
        self.assertEqual(config["Settings"]["key"], "value")

    # 異常系（エラーが発生するべき状況）のコードパスが正しく実装されていることを保証
    def test_load_config_file_not_found(self):
        """
        設定ファイルが見つからない場合にFileNotFoundErrorが発生することを確認
        """
        with self.assertRaisesRegex(
            FileNotFoundError, r"設定ファイルが見つかりません: .*non_existent.ini"
        ):
            load_config(self.non_existent_path)

    def test_load_config_invalid_format(self):
        """
        INIファイルとして不正な形式の場合、エラーは出さず、
        ファイルを読み込まれないこと(戻り値は[])を確認
        """
        config = load_config(self.invalid_config_path)
        self.assertIsInstance(config, configparser.ConfigParser)
        self.assertFalse(config.sections())  # セクションが読み込まれないことを確認

    # --- main 関数（argparseとロギング、configparserの連携）のテスト ---

    @patch("sys.stderr", new_callable=io.StringIO)  # 標準エラー出力を捕捉
    @patch("sys.stdout", new_callable=io.StringIO)  # 標準出力を捕捉
    @patch("sys.exit")  # sys.exit をモック化してプログラム終了を阻止
    def test_main_arg_parsing_success_with_tree_output(
        self, mock_exit, mock_stdout, mock_stderr
    ):  # 作成時点で-tが標準出力を行わないため、mock_stdoutは使用されない
        """
        全ての引数が正しく指定された場合にmain関数が正常に動作することを確認
        """
        # sys.argv をモック化してコマンドライン引数を設定
        test_args = [
            "main.py",
            "-i",
            str(self.config_path),
            "-f",
            "*.txt",
            "-t",
            str(self.output_file),
        ]
        with patch("sys.argv", test_args):
            main()  # main 関数を実行

            # sys.exit が呼び出されないことを確認（正常系の為呼び出されないことが正）
            mock_exit.assert_not_called()

            # 期待するロギングメッセージが含まれているか確認
            # (ログ出力はstderrに出るようにbasicConfigで設定されている前提)
            stderr_output = mock_stderr.getvalue()
            self.assertIn(f"INIファイル: {self.config_path}", stderr_output)
            self.assertIn("抽出パターン: *.txt", stderr_output)
            self.assertIn(f"ツリー出力先: {self.output_file}", stderr_output)
            self.assertIn(
                "設定ファイルの読み込み完了。セクション: ['Settings']", stderr_output
            )

    @patch("sys.stderr", new_callable=io.StringIO)
    @patch("sys.stdout", new_callable=io.StringIO)
    @patch("sys.exit")
    def test_main_arg_parsing_success_without_tree_output(
        self, mock_exit, mock_stdout, mock_stderr
    ):
        """
        ツリー出力が省略された場合にmain関数が正常に動作することを確認
        """
        test_args = ["main.py", "-i", str(self.config_path), "-f", "*.csv"]
        with patch("sys.argv", test_args):
            main()

            mock_exit.assert_not_called()
            stderr_output = mock_stderr.getvalue()
            self.assertIn("ツリー出力先: 標準出力", stderr_output)

    @patch("sys.stderr", new_callable=io.StringIO)
    @patch("sys.stdout", new_callable=io.StringIO)
    @patch("sys.exit")
    def test_main_missing_required_args(self, mock_exit, mock_stdout, mock_stderr):
        """
        必須引数が不足している場合にSystemExitで終了することを確認
        """
        # -i が不足
        test_args = ["main.py", "-f", "*.txt"]
        with patch("sys.argv", test_args):
            # argparseはsys.exitを呼び出すので、SystemExitを捕捉する
            with self.assertRaises(SystemExit):
                main()
            mock_exit.assert_called_with(2)
            # エラーメッセージが標準エラー出力に含まれているか確認
            stderr_output = mock_stderr.getvalue()
            self.assertIn(
                "the following arguments are required: -i/--ini_file", stderr_output
            )
