import logging
import os
import shutil


logger = logging.getLogger(__name__)


def process_files(path_config: dict):
    """
    基準パスを構築し、指定されたファイルパターンに合致するファイルをTeamsパスから探し、コピーする。

    Args:
        config (dict): 設定ファイルの読み込み結果

    Returns:
        なし
    """

    # 設定情報
    config = {
        "030.調査": {
            "top_level_matcher": ["調査検討書_"],
            "artifact_matcher": [
                "030_レビューチェックリスト_",
                "レビュー記録表_調査",
            ],
        },
        "040.設計": {
            "top_level_matcher": ["機能設計書_"],
            "artifact_matcher": ["040_レビューチェックリスト_", "レビュー記録表_設計"],
        },
        "050.製造": {
            "top_level_matcher": [],
            "artifact_matcher": ["050_レビューチェックリスト_", "レビュー記録表_CD"],
        },
        "060.UD作成": {
            "top_level_matcher": ["単体試験仕様書_"],
            "artifact_matcher": [
                "060_レビューチェックリスト_",
                "レビュー記録表_UD作成",
            ],
        },
        "070.UD消化": {
            "top_level_matcher": ["単体試験成績書_"],
            "artifact_matcher": [
                "070_レビューチェックリスト_",
                "レビュー記録表_UD消化",
            ],
        },
        "080.SD作成": {
            "top_level_matcher": ["結合試験仕様書_"],
            "artifact_matcher": [
                "080_レビューチェックリスト_",
                "レビュー記録表_SD作成",
            ],
        },
        "090.SD消化": {
            "top_level_matcher": ["結合試験成績書_", "試験結果報告書_"],
            "artifact_matcher": [
                "090_レビューチェックリスト_",
                "レビュー記録表_SD消化",
            ],
        },
    }

    # コピー元とコピー先のベースパス
    # 環境に合わせてパスを適宜変更してください
    src_base = path_config["teams_root_path"]
    dst_base = path_config["delivery_root_path"]

    logging.info(f"--- ファイルコピーを開始します ---")
    logging.info(f"探索先ルートバス:{src_base}")

    # コピー先ベースディレクトリをまず作成
    os.makedirs(dst_base, exist_ok=True)

    # os.walkでコピー元ディレクトリツリーを走査
    for root, _, files in os.walk(src_base):
        # src_baseからの相対パスを取得
        relative_path = os.path.relpath(root, src_base)
        path_parts = relative_path.split(os.sep)

        # 「対象ディレクトリ」のキーを特定 (例: "010.調査")
        target_folder_key = None
        if path_parts and path_parts[0] in config:
            target_folder_key = path_parts[0]

        # 対象ディレクトリではない場合、このパス以下のファイルは処理しない
        if (
            target_folder_key is None and relative_path != "."
        ):  # '.'はsrc_base自体なので、その中のファイルは処理対象
            continue

        # ファイルの処理
        for file_name in files:
            src_file_path = os.path.join(root, file_name)
            file_name_lower = file_name.lower()  # マッチングのために小文字化

            # コピー済みフラグ
            copied = False

            # 2.1. 対象ディレクトリ直下のドキュメントファイル (トップレベルドキュメント) のコピー
            # rootがsrc_base/010.調査 のようなパスで、その中にファイルがある場合
            if relative_path == target_folder_key and target_folder_key:
                matchers = config[target_folder_key].get("top_level_matcher", [])
                for matcher in matchers:
                    if file_name_lower.startswith(matcher.lower()):
                        # コピー先のディレクトリパスを作成 (例: dst_base/010.調査)
                        dst_dir = os.path.join(dst_base, target_folder_key)
                        os.makedirs(
                            dst_dir, exist_ok=True
                        )  # ディレクトリがなければ作成

                        dst_file_path = os.path.join(dst_dir, file_name)
                        if not os.path.exists(
                            dst_file_path
                        ):  # ファイルが既に存在しなければコピー
                            shutil.copy2(src_file_path, dst_file_path)
                            print(f"コピー (トップレベル): {file_name} -> {dst_dir}")
                        copied = True
                        break
                if copied:  # コピーされたら次のファイルへ
                    continue

            # 2.2. 「成果物」ディレクトリ内の特定ファイルのコピー (フラット化)
            # パスに「成果物」が含まれ、かつ対象のフォルダキーが特定されている場合
            # path_partsのどこかに"成果物"が含まれていればOK（例: "010.調査/成果物/内部"）
            if "成果物" in path_parts and target_folder_key:
                matchers = config[target_folder_key].get("artifact_matcher", [])
                for matcher in matchers:
                    if file_name_lower.startswith(matcher.lower()):
                        # コピー先のディレクトリパスを作成 (例: dst_base/010.調査/成果物)
                        dst_dir = os.path.join(dst_base, target_folder_key, "成果物")
                        os.makedirs(
                            dst_dir, exist_ok=True
                        )  # ディレクトリがなければ作成

                        dst_file_path = os.path.join(dst_dir, file_name)
                        if not os.path.exists(
                            dst_file_path
                        ):  # ファイルが既に存在しなければコピー
                            shutil.copy2(src_file_path, dst_file_path)
                            print(f"コピー: {file_name} -> {dst_dir}")
                        copied = True
                        break
                if copied:  # コピーされたら次のファイルへ
                    continue

            # どのルールにも合致しなかったファイルはコピーしない (要件2.1と2.2の注意点、要件3)
            if not copied:
                # デバッグのために、コピーされなかったファイルをログに出すことも可能
                # print(f"スキップ: {file_name} in {relative_path} (ルールに合致しないため)")
                pass

    logging.info(f"コピー先ベースディレクトリパス:{dst_base}")
    logging.info("--- ファイルコピーが完了しました ---")

    return
