# !/bin/sh

echo "#### コピー開始 ####"
python walk_mini_app.py

echo "#### config.ini修正 ####"
sed -i '' 's|/Users/koni/Desktop/base_teams/マイグレ|/Users/koni/Desktop/base_teams/サンプル2|g' config.ini
echo "#### コピー開始 ####"
python walk_mini_app.py

sed -i '' 's|/Users/koni/Desktop/base_teams/サンプル2|/Users/koni/Desktop/base_teams/マイグレ|g' config.ini

echo "#### ツリー出力 ####"
cd /Users/koni/Desktop/copy_teams
tree > tree.txt