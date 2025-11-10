import logging
import os
import shutil
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

    target_dirs = {
        "030.調査": ["030", "調査", "調査"],
        "040.設計": ["040", "設計", "機能設計書"],
        "050.製造": [
            "050",
            "製造",
        ],  # 製造は具体的なファイル名が少ないので、キーワードを調整
        "060.UD作成": ["060", "UD作成", "単体試験仕様書"],
        "070.UD消化": ["070", "UD消化", "単体試験成績書"],
        "080.SD作成": ["080", "SD作成", "結合試験仕様書"],
        "090.SD消化": ["090", "SD消化", "結合試験成績書", "試験結果報告書"],
    }

    search_root_path = config["teams_root_path"]
    destination_base_dir_path = (
        config["delivery_root_path"]
        / config["delivery_quarter"]
        / config["project_name"]
    )

    os.makedirs(destination_base_dir_path, exist_ok=True)

    for root, _, files in os.walk(search_root_path):
        for file_name in files:
            source_file_path = os.path.join(root, file_name)
            copied = False

            # 各ターゲットディレクトリに対してチェック
            for target_dir_name, keywords in target_dirs.items():
                for keyword in keywords:
                    if keyword.lower() in file_name.lower():  # 大文字小文字を区別しない
                        # 条件1: 各フォルダ(030.調査 ...)に該当のファイルをコピー
                        destination_top_dir = os.path.join(
                            destination_base_dir_path, target_dir_name
                        )
                        os.makedirs(destination_top_dir, exist_ok=True)

                        # 条件3: 各フォルダトップには各フォルダと名称に一致するファイルをコピーする
                        # 例: 030.調査には調査検討書...xlsx
                        # ここでは、ファイル名にフォルダ名（030.調査）が直接含まれるか、
                        # 最初のキーワード（030または調査）が直接ファイル名と一致するかで判定
                        if keyword.lower() in target_dir_name.lower() and (
                            keyword.lower() in file_name.lower()
                            or file_name.lower().startswith(keyword.lower())
                        ):
                            dest_file_path = os.path.join(
                                destination_top_dir, file_name
                            )
                            if not os.path.exists(dest_file_path):
                                shutil.copy2(source_file_path, dest_file_path)
                                print(
                                    f"コピー (トップ): {file_name} -> {destination_top_dir}"
                                )
                                copied = True
                                # 複数のターゲットディレクトリにコピーされる可能性があるのでbreakはしない
                                # break

                        # 条件2: 各フォルダには成果物というフォルダがある
                        # 条件4: 成果物の方も同様
                        # 例)030もしくは調査と入っているファイルは030.調査/成果物配下にコピー
                        # 常に「成果物」フォルダにもコピーを試みる
                        destination_artifact_dir = os.path.join(
                            destination_top_dir, "成果物"
                        )
                        os.makedirs(destination_artifact_dir, exist_ok=True)
                        dest_artifact_file_path = os.path.join(
                            destination_artifact_dir, file_name
                        )

                        # 成果物フォルダへのコピーは、キーワードがファイル名に含まれていれば行う
                        if not os.path.exists(dest_artifact_file_path):
                            shutil.copy2(source_file_path, dest_artifact_file_path)
                            print(
                                f"コピー (成果物): {file_name} -> {destination_artifact_dir}"
                            )
                            copied = True

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
