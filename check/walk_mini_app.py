import os
import shutil

# ---【1. 設定（ハードコーディング部分）】---
# ターゲットフォルダとその中のファイルに関するルールを定義
# 各ターゲットフォルダについて、その直下にコピーするファイルと
# その「成果物」サブフォルダにコピーするファイルのルールを明確にします。
config = {
    # 010.調査 フォルダに関する設定
    "010.調査": {
        "top_level_matcher": [
            "調査検討書_"
        ],  # 010.調査 直下にコピーするファイルのプレフィックス
        "artifact_matcher": [
            "010_レビューチェクリスト_",
            "レビュー記録表_調査_",
        ],  # 010.調査/成果物/ にコピーするファイルのプレフィックス
    },
    # 020.設計 フォルダに関する設定
    "020.設計": {
        "top_level_matcher": ["機能設計書_"],
        "artifact_matcher": ["020_レビューチェクリスト_", "レビュー記録表_設計_"],
    },
    # 030.試験 フォルダに関する設定
    "030.UD作成": {
        "top_level_matcher": ["単体試験仕様書_"],
        "artifact_matcher": ["030_レビューチェクリスト_", "レビュー記録表_UD作成_"],
    },
    # メモ
    # 各工程フォルダの"top_level_matcher"は 調査*_ 機能設計書_ 単体試験仕様書_などで良さそう
    # ただし、上記のファイルはコピー元には成果物階層にも同じものがあるためそれらをコピーしないような制御が必要
    # 成果物フォルダも、現在のように複数指定することで解決が可能か
}

# ---【2. パスの設定】---
src_base = (
    "/Users/koni/Desktop/delivery_automation_tool/check/walk_base_sample/サンプル"
)
dst_base = "/Users/koni/Desktop/delivery_automation_tool/check/walk_copy_place/サンプル"

print(f"--- ファイルコピーを開始します ---")
print(f"コピー元ベース: {src_base}")
print(f"コピー先ベース: {dst_base}\n")

# コピー先ベースディレクトリが存在しない場合は作成
os.makedirs(dst_base, exist_ok=True)

# ---【3. ファイルをコピーするメインロジック】---
# os.walk によるファイル走査の for ループ
for root, _, files in os.walk(src_base):
    # 現在のディレクトリの相対パスを取得（例: サンプル/010.調査/成果物/内部）
    # この相対パスを使って、どのルールが適用されるべきかを判断します
    relative_path = os.path.relpath(root, src_base)
    print(f"relative_path: {relative_path}")
    path_parts = relative_path.split(os.sep)  # パスをスラッシュで分割
    print(f"path_parts: {path_parts}")

    # 現在処理しているフォルダのキー (例: "010.調査") を特定
    # path_partsの最初の要素が "010.調査" のようなターゲットフォルダ名
    print(f"path_parts[0]:{path_parts[0]}")
    print(f"path_parts:{path_parts}")

    target_folder_key = (
        path_parts[0] if path_parts and path_parts[0] in config else None
    )
    print(f"target_folder_key:{target_folder_key}")

    if target_folder_key is None:
        # 設定にないディレクトリの場合はスキップ
        if relative_path != ".":  # ルートディレクトリ自体はスキップしない
            continue

    # 各ディレクトリ内のファイルを走査する for ループ
    for file_name in files:
        src_file_path = os.path.join(root, file_name)
        file_name_lower = file_name.lower()  # 判定のため小文字化

        copied = False  # このファイルがコピーされたかどうかのフラグ

        # --- コピー先の決定とコピー処理 ---

        # ターゲットフォルダの直下 (例: サンプル/010.調査/) にコピーする場合
        # 現在のパスがターゲットフォルダ自体 (例: "サンプル/010.調査") であることを確認
        if relative_path == target_folder_key and target_folder_key:
            matchers = config[target_folder_key].get("top_level_matcher", [])
            for matcher in matchers:
                if file_name_lower.startswith(matcher.lower()):
                    dst_dir = os.path.join(dst_base, target_folder_key)
                    os.makedirs(dst_dir, exist_ok=True)
                    dst_file_path = os.path.join(dst_dir, file_name)
                    if not os.path.exists(dst_file_path):
                        shutil.copy2(src_file_path, dst_file_path)
                        print(f"コピー (トップ): {file_name} -> {dst_dir}")
                    copied = True
                    break  # 一致するマッチャーが見つかったら終了

        # ターゲットフォルダの「成果物」サブフォルダ (例: サンプル/010.調査/成果物/) にコピーする場合
        # 現在のパスが「成果物」サブフォルダ、またはその下の「内部」「外部」である場合
        if "成果物" in path_parts and target_folder_key:
            matchers = config[target_folder_key].get("artifact_matcher", [])
            for matcher in matchers:
                if file_name_lower.startswith(matcher.lower()):
                    dst_dir = os.path.join(dst_base, target_folder_key, "成果物")
                    os.makedirs(dst_dir, exist_ok=True)
                    dst_file_path = os.path.join(dst_dir, file_name)
                    if not os.path.exists(dst_file_path):
                        shutil.copy2(src_file_path, dst_file_path)
                        print(f"コピー (成果物): {file_name} -> {dst_dir}")
                    copied = True
                    break  # 一致するマッチャーが見つかったら終了

        if not copied:
            # print(f"スキップ (コピールール不一致): {file_name} (in {root})")
            pass  # スキップログは通常は大量になるのでコメントアウト

print("\n--- ファイルコピーが完了しました ---")
