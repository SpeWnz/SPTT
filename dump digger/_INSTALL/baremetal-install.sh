#!/bin/sh
sudo apt-get update -y
sudo apt-get install libxml2-dev libxslt1-dev antiword unrtf poppler-utils tesseract-ocr flac ffmpeg lame libmad0 libsox-fmt-mp3 sox libjpeg-dev swig -y
sudo apt install ./pstotext_1.9-6build1_amd64.deb -y

# we need to install textract this way because pip wont let you do so for some reason
git clone https://github.com/deanmalmgren/textract
sudo cp -r textract/textract /usr/lib/python3/dist-packages/textract
rm -rf textract

cat requirements.txt | xargs -I {} pip3 install {} --break-system-packages --no-cache --root-user-action=ignore
cat requirements.txt | xargs -I {} pip install {} --break-system-packages --no-cache


# reinstall six
pip3 uninstall six
pip uninstall six

pip3 install six --break-system-packages
pip install six --break-system-packages