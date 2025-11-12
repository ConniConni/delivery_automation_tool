import os
import shutil

config = {
    "010.調査": {
        "top_level_matcher": ["調査検討書_"],
        "artifact_matcher": [
            "010_レビューチェックリスト_",
            "レビュー記録表_調査_",
        ],
    },
    "020.設計": {
        "top_level_matcher": ["機能設計書_"],
        "artifact_matcher": ["020_レビューチェックリスト_", "レビュー記録表_設計_"],
    },
    "030.UD作成": {
        "top_level_matcher": ["単体試験仕様書_"],
        "artifact_matcher": ["030_レビューチェックリスト_", "レビュー記録表_UD作成_"],
    },
}


src_base = (
    "/Users/koni/Desktop/delivery_automation_tool/check/walk_base_sample/サンプル"
)
dst_base = "/Users/koni/Desktop/delivery_automation_tool/check/walk_copy_place/サンプル"

print(f"--- ファイルコピーを開始します ---")
print(f"コピー元ベース: {src_base}")
print(f"コピー先ベース: {dst_base}\n")


os.makedirs(dst_base, exist_ok=True)


for root, _, files in os.walk(src_base):

    relative_path = os.path.relpath(root, src_base)
    path_parts = relative_path.split(os.sep)

    target_folder_key = (
        path_parts[0] if path_parts and path_parts[0] in config else None
    )

    if target_folder_key is None:
        if relative_path != ".":
            continue

    for file_name in files:
        src_file_path = os.path.join(root, file_name)
        file_name_lower = file_name.lower()

        copied = False

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
                    break

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
                    break

        if not copied:
            pass

print("\n--- ファイルコピーが完了しました ---")
