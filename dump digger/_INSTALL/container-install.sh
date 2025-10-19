#!/bin/sh
apt-get update -y
apt install ./pstotext_1.9-6build1_amd64.deb -y

# we need to install textract this way because pip wont let you do so for some reason
git clone https://github.com/deanmalmgren/textract
cp -r textract/textract /usr/lib/python3/dist-packages/textract
rm -rf textract

cat requirements.txt | xargs -I {} pip3 install {} --break-system-packages --no-cache --root-user-action=ignore
cat requirements.txt | xargs -I {} pip install {} --break-system-packages --no-cache --root-user-action=ignore


# reinstall six
pip3 uninstall six
pip uninstall six

pip3 install six --break-system-packages --no-cache --root-user-action=ignore
pip install six --break-system-packages --no-cache --root-user-action=ignore


# ZHOR_Modules install
git clone https://github.com/SpeWnz/ZHOR_Modules /usr/lib/python3/dist-packages/ZHOR_Modules
cat /usr/lib/python3/dist-packages/ZHOR_Modules/requirements.txt | xargs -I {} pip3 install {} --break-system-packages --no-cache --root-user-action=ignore
cat /usr/lib/python3/dist-packages/ZHOR_Modules/requirements.txt | xargs -I {} pip install {} --break-system-packages --no-cache --root-user-action=ignore