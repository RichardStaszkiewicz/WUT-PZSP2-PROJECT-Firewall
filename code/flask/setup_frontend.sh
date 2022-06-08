#!bin/bash
echo ""
echo "Skrypt instalacyjny do frontu z flaska"

echo "Zostanie uruchomiona instalacja pakietów z pliku requirements.txt"
echo ""
pip install -r requirements.txt


#EKSPERYMENTALNE, OBOWIAZKOWE PRZY INSTALACJI pip install flask
echo "Uruchamiam eksport ustawien flask"
export FLASK_APP=hello.py
export FLASK_ENV=development

echo "WERSJE ZAINSTALOWANE:"
echo ""
echo `flask --version`
echo ""