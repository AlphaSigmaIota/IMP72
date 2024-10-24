# Die Funktionen in dieser Datei stammen aus dem GitHub Verzeichnis der AI4Finance-Foundation:
# https://github.com/AI4Finance-Foundation/FinGPT/blob/master/fingpt/FinGPT_Forecaster/prepare_data.ipynb
# Die Funktionen dienen der Generierung der Prompts.

import json
import random
import yfinance
import pandas as pd
from time import sleep
from datetime import datetime, timedelta


def n_weeks_before(date_string, n):
    date = datetime.strptime(date_string, "%Y-%m-%d") - timedelta(days=7 * n)
    return date.strftime("%Y-%m-%d")


def get_stock_data(stock_symbol, steps):
    stock_data = yfinance.download(stock_symbol, steps[0], steps[-1])
    if len(stock_data) == 0:
        raise Exception(f"Aktiendaten zu {stock_symbol} konnten von yfinance nicht abgerufen werden.")

    dates, prices = [], []
    available_dates = stock_data.index.format()

    for date in steps[:-1]:
        for i in range(len(stock_data)):
            if available_dates[i] >= date:
                prices.append(stock_data['Close'].iloc[i])
                dates.append(datetime.strptime(available_dates[i], "%Y-%m-%d"))
                break

    dates.append(datetime.strptime(available_dates[-1], "%Y-%m-%d"))
    prices.append(stock_data['Close'].iloc[-1])

    return pd.DataFrame({
        "Start Date": dates[:-1], "End Date": dates[1:],
        "Start Price": prices[:-1], "End Price": prices[1:]
    })


def get_news(finnhub_client, symbol, data):
    news_list = []

    for end_date, row in data.iterrows():
        start_date = row['Start Date'].strftime('%Y-%m-%d')
        end_date = row['End Date'].strftime('%Y-%m-%d')
        #         print(symbol, ': ', start_date, ' - ', end_date)
        sleep(1)  # control qpm
        weekly_news = finnhub_client.company_news(symbol, _from=start_date, to=end_date)
        if len(weekly_news) == 0:
            raise Exception(f"No company news found for symbol {symbol} from finnhub!")
        weekly_news = [
            {
                "date": datetime.fromtimestamp(n['datetime']).strftime('%Y%m%d%H%M%S'),
                "headline": n['headline'],
                "summary": n['summary'],
            } for n in weekly_news
        ]
        weekly_news.sort(key=lambda x: x['date'])
        news_list.append(json.dumps(weekly_news))

    data['News'] = news_list

    return data


def get_company_prompt(finnhub_client, symbol):
    profile = finnhub_client.company_profile2(symbol=symbol)
    if not profile:
        raise Exception(f"Failed to find company profile for symbol {symbol} from finnhub!")

    company_template = "[Company Introduction]:\n\n{name} is a leading entity in the {finnhubIndustry} sector. Incorporated and publicly traded since {ipo}, the company has established its reputation as one of the key players in the market. As of today, {name} has a market capitalization of {marketCapitalization:.2f} in {currency}, with {shareOutstanding:.2f} shares outstanding." \
                       "\n\n{name} operates primarily in the {country}, trading under the ticker {ticker} on the {exchange}. As a dominant force in the {finnhubIndustry} space, the company continues to innovate and drive progress within the industry."

    formatted_str = company_template.format(**profile)

    return formatted_str


def get_prompt_by_row(symbol, row):
    start_date = row['Start Date'] if isinstance(row['Start Date'], str) else row['Start Date'].strftime('%Y-%m-%d')
    end_date = row['End Date'] if isinstance(row['End Date'], str) else row['End Date'].strftime('%Y-%m-%d')
    term = 'increased' if row['End Price'] > row['Start Price'] else 'decreased'
    head = "From {} to {}, {}'s stock price {} from {:.2f} to {:.2f}. Company news during this period are listed below:\n\n".format(
        start_date, end_date, symbol, term, row['Start Price'], row['End Price'])

    news = json.loads(row["News"])
    news = ["[Headline]: {}\n[Summary]: {}\n".format(
        n['headline'], n['summary']) for n in news if n['date'][:8] <= end_date.replace('-', '') and \
                                                      not n['summary'].startswith(
                                                          "Looking for stock market analysis and research with proves results?")]

    basics = json.loads(row['Basics'])
    if basics:
        basics = "Some recent basic financials of {}, reported at {}, are presented below:\n\n[Basic Financials]:\n\n".format(
            symbol, basics['period']) + "\n".join(f"{k}: {v}" for k, v in basics.items() if k != 'period')
    else:
        basics = "[Basic Financials]:\n\nNo basic financial reported."

    return head, news, basics


def sample_news(news, k=5):
    return [news[i] for i in sorted(random.sample(range(len(news)), k))]


def get_all_prompts_online(finnhub_client, symbol, data, curday):
    company_prompt = get_company_prompt(finnhub_client, symbol)

    prev_rows = []

    for row_idx, row in data.iterrows():
        head, news, _ = get_prompt_by_row(symbol, row)
        prev_rows.append((head, news, None))

    prompt = ""
    for i in range(-len(prev_rows), 0):
        prompt += "\n" + prev_rows[i][0]
        sampled_news = sample_news(
            prev_rows[i][1],
            min(5, len(prev_rows[i][1]))
        )
        if sampled_news:
            prompt += "\n".join(sampled_news)
        else:
            prompt += "No relative news reported."

    period = "{} to {}".format(curday, n_weeks_before(curday, -1))

    info = company_prompt + '\n' + prompt + '\n'
    prompt = info + f"\n\nBased on all the information before {curday}, let's first analyze the positive developments and potential concerns for {symbol}. Come up with 2-4 most important factors respectively and keep them concise. Most factors should be inferred from company related news. " \
                    f"Then make your prediction of the {symbol} stock price movement for next week ({period}). Provide a summary analysis to support your prediction."

    return info, prompt
