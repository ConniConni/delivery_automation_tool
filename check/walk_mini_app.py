import os
import shutil

src = "/Users/koni/Desktop/delivery_automation_tool/check/walk_base_sample"
dst = "/Users/koni/Desktop/delivery_automation_tool/check/walk_copy_place"

for root, dirs, files in os.walk(src):
    if os.path.basename(root) == "成果物":
        target_dir = os.path.join(dst, os.path.relpath(root, src))
        for dir_name in dirs:
            subdir_path = os.path.join(root, dir_name)
            # サブディレクトリ配下全てのファイルを成果物直下へコピー
            for sub_root, _, sub_files in os.walk(subdir_path):
                for file in sub_files:
                    src_file = os.path.join(sub_root, file)
                    dst_file = os.path.join(target_dir, file)
                    shutil.copy2(src_file, dst_file)
        # もし直接「成果物」直下にもファイルがある場合はそちらもコピー
        for file in files:
            src_file = os.path.join(root, file)
            dst_file = os.path.join(target_dir, file)
            shutil.copy2(src_file, dst_file)
