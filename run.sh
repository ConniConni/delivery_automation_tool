# !/bin/sh

echo "#### コピー開始 ####"
python main.py

echo "#### config.ini修正 ####"
sed -i '' 's|/Users/koni/Desktop/walk_base_sample/マイグレ|/Users/koni/Desktop/walk_base_sample/サンプル2|g' config.ini
cat ./config.ini
echo "#### コピー開始 ####"
python main.py

sed -i '' 's|/Users/koni/Desktop/walk_base_sample/サンプル2|/Users/koni/Desktop/walk_base_sample/マイグレ|g' config.ini

echo "#### ツリー出力 ####"
cd /Users/koni/Desktop/copy_teams
tree > tree.txt