# !/bin/sh

echo "#### コピー開始 ####"
python walk_mini_app.py

echo "#### ツリー出力 ####"
tree ./walk_copy_place/マイグレ > tree.txt
