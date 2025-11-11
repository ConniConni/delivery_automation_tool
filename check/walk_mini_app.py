import os
import shutil

# ---【1. 設定（ハードコーディング部分）】---
config = {
    "010.調査": {
        "file_patterns": ["{folder_name_dot}", "{folder_root_name}"],
    },
    "020.設計": {
        "file_patterns": ["{folder_name_dot}", "{folder_root_name}"],
    },
    "030.試験": {
        "file_patterns": ["{folder_name_dot}", "{folder_root_name}"],
    },
    "成果物": {
        "file_patterns": ["{folder_number}_", "{folder_root_name}"],
    },
}

# ---【2. パスの設定】---
src = "/Users/koni/Desktop/delivery_automation_tool/check/walk_base_sample/サンプル"
dst = "/Users/koni/Desktop/delivery_automation_tool/check/walk_copy_place/サンプル"


# ---【3. ファイル名が指定パターンすべてを含むか判定する関数】---
def match_patterns(filename, patterns):
    for pat in patterns:
        if pat not in filename:
            return False
    return True


# ---【4. フォルダツリーを探索して、条件に合うファイルだけをコピー】---
for root, dirs, files in os.walk(src):
    folder_name = os.path.basename(root)  # 例: 010.調査
    folder_name_dot = folder_name  # そのまま"010.調査"など
    folder_root_name = (
        folder_name.split(".")[1] if "." in folder_name else folder_name
    )  # 例: "調査"
    folder_number = folder_name.split(".")[0] if "." in folder_name else ""  # 例: "010"

    if folder_name in config:
        # ---【5. プレースホルダを置換して実際の判定パターンを構築】---
        patterns = []
        for pat in config[folder_name]["file_patterns"]:
            pat = pat.replace("{folder_name_dot}", folder_name_dot)
            pat = pat.replace("{folder_root_name}", folder_root_name)
            pat = pat.replace("{folder_number}", folder_number)
            patterns.append(pat)

        for file in files:
            if match_patterns(file, patterns):
                src_file = os.path.join(root, file)  # コピー元ファイル
                rel_root = os.path.relpath(root, src)
                dst_file = os.path.join(dst, rel_root, file)  # コピー先ファイル
                os.makedirs(
                    os.path.dirname(dst_file), exist_ok=True
                )  # コピー先フォルダを作成
                shutil.copy2(src_file, dst_file)  # ファイルコピー

# ブロックごとの解説
# 1. 設定ハードコーディング
# どのフォルダにどんな命名規則があるかをPythonの辞書で管理します。

# フォルダごとにfile_patternsリストがあり、プレースホルダーで条件を共通化。

# 2. パスの設定
# コピー元(src)・コピー先(dst)のパスを設定。

# 3. パターン判定関数
# ファイル名がすべての規則パターンを満たしているかを判定するシンプルな関数です。

# 4. ディレクトリ探索＋本体ループ
# os.walkで全フォルダ・ファイルを１回だけサーチします。

# 対象のフォルダ（configに載っているもの）の場合だけ、5. のパターン置換に進みます。

# 5. パターン置換とコピー実行
# 辞書型configの各パターンを、今いるフォルダ名等に合わせて {} を置換します。

# 置換したパターンでファイル名を判定。

# マッチしたファイルだけ、コピー先にディレクトリを作ってファイルをコピーします。

# この方式なら、条件追加やフォルダの増減もconfigを書き足すだけで対応できます。
# さらに複雑なパターンもここを拡張するだけでOKです。​
