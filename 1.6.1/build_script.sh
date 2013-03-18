#!/bin/sh

sudo chown -R root:root fotoshare/opt/

sudo chown -R root:root fotoshare/usr/

sudo chown -R root:root fotoshare/etc/

sudo chmod a+x fotoshare/opt/FotoShareN9/fotoshareGUI.py

sudo chmod a+x fotoshare/opt/FotoShareN9/fotoshare_service

sudo python digsigsums.py fotoshare

dpkg-deb -b fotoshare

ar q fotoshare.deb _aegis
