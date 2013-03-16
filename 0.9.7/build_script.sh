#!/usr/bash

cp fotoshareGUI.py fotoshare_deb/opt/FotoShareN9/fotoshareGUI.py
cp fotoshare_service fotoshare_deb/opt/FotoShareN9/fotoshare_service

cp qml/main.qml fotoshare_deb/opt/FotoShareN9/qml/main.qml
cp qml/MainPage.qml fotoshare_deb/opt/FotoShareN9/qml/MainPage.qml
cp qml/SettingsPage.qml fotoshare_deb/opt/FotoShareN9/qml/SettingsPage.qml


sudo chown -R root:root fotoshare_deb/opt/

sudo chown -R root:root fotoshare_deb/usr/

sudo chown -R root:root fotoshare_deb/etc/

sudo chmod a+x fotoshare_deb/opt/FotoShareN9/fotoshareGUI.py

sudo chmod a+x fotoshare_deb/opt/FotoShareN9/fotoshare_service

python digsigsums.py fotoshare_deb

dpkg-deb -b fotoshare_deb

ar q fotoshare_deb.deb _aegis


