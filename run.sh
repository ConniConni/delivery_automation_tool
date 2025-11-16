# !/bin/sh

echo "#### コピー開始 ####"
python main.py

echo "#### config.ini修正 ####"
sed -i '' 's|/Users/koni/Desktop/delivery_automation_tool/check/walk_base_sample/マイグレ|/Users/koni/Desktop/delivery_automation_tool/check/walk_base_sample/サンプル2|g' config.ini
echo "#### コピー開始 ####"
python main.py

sed -i '' 's|/Users/koni/Desktop/delivery_automation_tool/check/walk_base_sample/サンプル2|/Users/koni/Desktop/delivery_automation_tool/check/walk_base_sample/マイグレ|g' config.ini

echo "#### ツリー出力 ####"
cd /Users/koni/Desktop/copy_teams
tree > tree.txt