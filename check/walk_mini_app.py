import os
import shutil

src = "/Users/koni/Desktop/delivery_automation_tool/check/walk_base_sample"
dst = "/Users/koni/Desktop/delivery_automation_tool/check/walk_copy_place"

for root, dirs, files in os.walk(src):
    for file in files:
        src_file = os.path.join(root, file)
        # srcから見た相対パスを取得し、コピー先のパスを作成
        rel_path = os.path.relpath(src_file, src)
        dst_file = os.path.join(dst, rel_path)

        # コピー先のディレクトリがなければ作成
        os.makedirs(os.path.dirname(dst_file), exist_ok=True)

        # ファイルをコピー
        shutil.copy2(src_file, dst_file)
        print(f"Copied {src_file} to {dst_file}")
