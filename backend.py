
import finnhub
import requests
import streamlit as st

from config import Config
from ai4FinanceFoundationFunctions import *

config = Config()


finnhub_client = finnhub.Client(api_key=config.finnhub_key)


B_INST, E_INST = "[INST]", "[/INST]"
B_SYS, E_SYS = "<<SYS>>\n", "\n<</SYS>>\n\n"


def construct_prompt(ticker, curday, n_weeks, use_basics):
    try:
        steps = [n_weeks_before(curday, n) for n in range(n_weeks + 1)][::-1]
    except Exception:
        raise st.Error(f"Invalid date {curday}!")

    data = get_stock_data(ticker, steps)
    data = get_news(finnhub_client, ticker, data)
    data['Basics'] = [json.dumps({})] * len(data)

    info, prompt = get_all_prompts_online(finnhub_client, ticker, data, curday)

    prompt = B_INST + B_SYS + config.system_prompt + E_SYS + prompt + E_INST

    return info, prompt


def query_model(prompt):
    url = f"{config.ngrok_url}/predict"  # Ersetzen Sie dies durch die tatsächliche ngrok URL
    print(f"Run: {url}")
    headers = {
        'Content-Type': 'application/json',
        'ngrok-skip-browser-warning': 'true'
    }
    print(prompt)
    body = {
        'prompt': prompt
    }

    try:
        response = requests.post(url, json=body, headers=headers)
        response.raise_for_status()  # Wird einen Fehler auslösen, wenn der Status-Code nicht 200 ist
        return response.json()['answer']
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        print(f"Response status code: {response.status_code}")
        print(f"Response content: {response.text}")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error occurred: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"An error occurred while making the request: {req_err}")
    except KeyError as key_err:
        print(f"Key error in response JSON: {key_err}")
        print(f"Response content: {response.text}")
    except Exception as err:
        print(f"An unexpected error occurred: {err}")

    return None


def predict_trend(stock, date, weeks):
    # Diese Funktion erstellt die Vorhersage des Finanzmarkttrends für eine ausgewählte DOW30 Aktie.
    info, prompt = construct_prompt(stock, date.strftime("%Y-%m-%d"), weeks, False)

    answer = query_model(prompt)

    print("Prediction completed.")
    print(f"info: {info}")
    print(f"answer: {answer}")
    return info, answer
