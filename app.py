import backend
import datetime
import streamlit as st
from config import Config

config = Config()

# Seitentitel
st.set_page_config(page_title="FinGPT Finanzmarkttrends Vorhersage", layout="wide")

# Titel und Beschreibung
st.title("FinGPT Finanzmarkttrends Vorhersage")
st.write("Vorhersage von Finanzmarkttrends mit FinGPT und Nachrichtenanalyse.")

# Layout mit zwei Spalten
col1, col2 = st.columns(2)

# Eingabebereich für die Parameter in der ersten Spalte
with col1:
    st.subheader("Parametrisierung")

    selected_stock = st.selectbox("Auswahl einer DOW30 Aktie:", config.dow_30)

    prediction_date = st.date_input("Auswahl des Datums für die Vorhersage:",
                                    min_value=datetime.date.today() + datetime.timedelta(days=-60),
                                    max_value=datetime.date.today())

    weeks_of_news = st.slider("Weeks of historical news to consider:", 1, 4, 2)

    if st.button("Vorhersage"):
        with st.spinner("Analysiere Finanzmarktnachrichten..."):
            info, prediction = backend.predict_trend(selected_stock, prediction_date, weeks_of_news)

        # Ergebnisse darstellen in der zweiten Spalte
        with col2:
            st.subheader("Vorhersage des Finanzmarkttrends:")
            st.write(f"Vorhersage für die Aktie {selected_stock} für den {prediction_date}:")
            st.write(f"{prediction}")

            st.subheader("Nachrichtenartikel, die als Basis für die Vorhersage dienten:")

            # Bereich mit Nachrichtenartikeln ausklappbar machen
            with st.expander("Nachrichtenartikel anzeigen"):
                st.write(info)

# Warnung am Ende hinzufügen.
st.caption("Warnung: Dieses Tool dient nur zu Demonstrationszwecken und sollte nicht für finanzielle Entscheidungen "
           "verwendet werden.")
