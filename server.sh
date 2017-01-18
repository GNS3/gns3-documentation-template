set -e

echo "Compile CSS"
cd theme/style
lessc index.less index.css
cd -

echo "Start server"
python3 server.py
