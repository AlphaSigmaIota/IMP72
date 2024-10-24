# IMP72 - Umsetzung eines Business Use Cases mit FinGPT

### Konfiguration
In der config.ini müssen zwei Werte hinterlegt werden: 
- FINNHUB_KEY: Dieser erfordert eine Registrierung bein FinnHub
- NGROK_URL: Dieser wird zur Laufzeit des Notebooks IMP_RunModel.ipynb generiert und muss im nachgang händisch eingetragen werden, bevor die Streamlit Applikation gestartet wird.

### Aufbau der API zum FinGPT-Modell
Das Juypter Notebook IMP_RunModel.ipynb im Verzeichnis API kann in einem beliebigen Notebook basieren Cloude Dienst ausgeführt werden. z.B. in Google Colab.

Hier müssen zur Laufzeit des Notebooks zwei Tokens (Hugginface und ngrok) angegeben werden. Die Links wo diese Tokens angefordert werden können sind im Notebook hinterlegt.

Zum Testen, ob die API entsprechend funktioniert (nicht vergessen in der config.ini die URL einzutragen) kann die Datei RemoteModelTest.py ausgeführt werden.

### Starten der Streamlit App
Zunächst müssen die python reqirements installiert werden. Hierfür kann folgender Befehl im Terminal ausgeführt werden: 
- pip install -r requirements.txt

Zum Starten der Streamlit App muss anschließend im Terminal der folgende Befehl ausgeführt werden: 
- streamlit run app.py

### Verwendete Hilfsfunktionen
In der Datei ai4FinanceFoundationFunctions.py sind die Funktionen der AI4Finance Foundation enthalten und minimal auf den hier vorliegenden Anwendungsfall angepasst.

Zum Testen, ob die Promptgenerierung mit den verwendeten Methoden funktioniert und Daten an der FinnHub API erfolgreich abgerufen werden können, kann die Datei PromptGeneratorTest.py ausgeführt werden.