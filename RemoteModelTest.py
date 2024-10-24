import requests
from config import Config

config = Config()


def combine_prompt():
    SYSTEM_PROMPT = "You are a seasoned stock market analyst. Your task is to list the positive developments and " \
                    "potential concerns for companies based on relevant news and basic financials from the past weeks, " \
                    "then provide an analysis and prediction for the companies' stock price movement for the upcoming " \
                    "week. Your answer format should be as follows:\n\n" \
                    "[Positive Developments]:\n1. ...\n\n" \
                    "[Potential Concerns]:\n1. ...\n\n" \
                    "[Prediction & Analysis]:\n...\n"
    prompt = """
    [Company Introduction]:

    NVIDIA Corp is a leading entity in the Semiconductors sector. Incorporated and publicly traded since 1999-01-22, the company has established its reputation as one of the key players in the market. As of today, NVIDIA Corp has a market capitalization of 1706799.59 in USD, with 2470.00 shares outstanding.

    NVIDIA Corp operates primarily in the US, trading under the ticker NVDA on the NASDAQ NMS - GLOBAL MARKET. As a dominant force in the Semiconductors space, the company continues to innovate and drive progress within the industry.

    From 2024-01-10 to 2024-01-17, NVDA's stock price increased from 543.50 to 560.53. Company news during this period are listed below:

    [Headline]: 1 Magnificent Artificial Intelligence (AI) Stock Down 71% You'll Wish You'd Bought on the Dip in 2024
    [Summary]: This unique cloud company is bringing artificial intelligence to small businesses.

    [Headline]: History Tells Us the Nasdaq Is About to Surge: 1 Stock to Buy Before It Does
    [Summary]: Some macroeconomic pressures could lessen this year, helping one of the market's hottest growth stocks rocket even higher.

    [Headline]: History Says the Nasdaq Will Soar in 2024: My Top 10 Growth Stocks to Buy Before It Does
    [Summary]: Investors are cheering last year's stock market recovery, but it could be just the beginning.

    [Headline]: IMF managing director on AI's impact: New social safety nets may be needed
    [Summary]: New research from the IMF sheds light on the profound impacts to global economies as generative AI becomes more pronounced.

    [Headline]: Here's How Much a $1000 Investment in Nvidia Made 10 Years Ago Would Be Worth Today
    [Summary]: Why investing for the long run, especially if you buy certain popular stocks, could reap huge rewards.

    From 2024-01-17 to 2024-01-24, NVDA's stock price increased from 560.53 to 613.62. Company news during this period are listed below:

    [Headline]: Supermicro Stock Surges As AI Computing Boom Continues
    [Summary]: Shares of Supermicro, a major maker of computer servers, shot up more than 30% to a record high after the company said revenue for its recently ended quarter would be far higher than initially expected.  The company is among the big beneficiaries of surging investment in computing infrastructure for artificial intelligence.  AI chips made by Nvidia and its peers reside in servers that Supermicro and other manufacturers produce.

    [Headline]: US STOCKS-S&P 500 notches first record high close in 2 years; chipmakers soar
    [Summary]: The S&P 500 posted a record high close on Friday for the first time in two years, fueled by a rally in chipmakers and other heavyweight technology stocks on optimism around artificial intelligence.  The benchmark's close confirmed that the S&P 500 has been in a bull market since it closed at its low on Oct. 12, 2022, according to one measure which also puts that date as the end of a bear market.  In a selloff between its record high close of 4,796.56 on Jan. 3, 2022 and its low in October 2022, the S&P 500 tumbled 25%.

    [Headline]: Why America’s controls on sales of AI tech to China are so leaky
    [Summary]: For increasingly hawkish lawmakers, that’s a problem

    [Headline]: History Says the Nasdaq Will Roar Higher in 2024: 2 Revolutionary AI Stocks to Buy Before It Does
    [Summary]: Nvidia and Alphabet could be among the biggest winners in an AI-driven Nasdaq rally.

    [Headline]: Why Western Digital Stock—Not Nvidia—Is Morgan Stanley’s Top Chip Pick
    [Summary]: The semiconductor analyst still has an overweight rating on Nvidia, but says Western Digital offers the best risk-reward opportunity.

    From 2024-01-24 to 2024-01-31, NVDA's stock price increased from 613.62 to 615.27. Company news during this period are listed below:

    [Headline]: Juniper (JNPR) Enhances Learning Experience in JCU Singapore
    [Summary]: James Cook University Singapore associates with Juniper (JNPR) to deploy transformative blended learning experience on campus, backed by AI-driven networks.

    [Headline]: Earnings Season Kicks Into High Gear With Magnificent 7 Reports
    [Summary]: Big tech kicks off peak earnings season - Microsoft, Alphabet, Amazon, Apple, and Meta.

    [Headline]: Snowflake's High Growth Days Could Be Numbered
    [Summary]: 

    [Headline]: NVIDIA Corp. stock rises Tuesday, outperforms market
    [Summary]: Shares of NVIDIA Corp. inched 0.49% higher to $627.74 Tuesday, on what proved to be an all-around mixed trading session for the stock market, with the Dow...

    [Headline]: Will Nvidia Be Worth More Than Microsoft by 2030?
    [Summary]: The graphics giant has been growing at a much faster pace than Microsoft, but can it sustain that momentum?

    From 2024-01-31 to 2024-02-06, NVDA's stock price increased from 615.27 to 682.23. Company news during this period are listed below:

    [Headline]: Why Nvidia Stock Joined the Tech Party Today
    [Summary]: Strong earnings reports from Amazon and Meta were good news for Nvidia.

    [Headline]: Meta stock jumps 20% after earnings in biggest market-cap jump in stock market history
    [Summary]: Shares of Meta soared Friday after the company reported a beat on earnings and guidance and announced new shareholder initiatives.

    [Headline]: Stocks close in the red, but Nvidia closes at new record
    [Summary]: Market indices (^DJI, ^IXIC, ^GSPC) close Monday lower, while semiconductor manufacturer Nvidia (NVDA) — among other stocks — close at a record high. Yahoo Finance's Jared Blikre examines the sector action and Chinese markets after the closing bell. For more expert insight and the latest market action, click here to watch this full episode of Yahoo Finance Live. Editor's note: This article was written by Luke Carberry Mogan.

    [Headline]: Cisco and NVIDIA to Help Enterprises Quickly and Easily Deploy and Manage Secure AI Infrastructure
    [Summary]: CISCO LIVE EMEA -- Cisco and NVIDIA today announced plans to deliver AI infrastructure solutions for the data center that are easy to deploy and manage, enabling the massive computing power that enterprises need to succeed in the AI era.

    [Headline]: Dow Jones Rises As Tesla Stock Downgraded; Palantir Soars 25% On Surging AI Demand
    [Summary]: The Dow Jones rose Tuesday, as Tesla stock slid on an analyst downgrade. Palantir stock soared 25% on surging AI demand.

    [Basic Financials]:

    No basic financial reported.

    Based on all the information before {curday}, let's first analyze the positive developments and potential concerns for {symbol}. Come up with 2-4 most important factors respectively and keep them concise. Most factors should be inferred from company-related news. Then make your prediction of the {symbol} stock price movement for next week ({period}). Provide a summary analysis to support your prediction.

    """

    B_INST, E_INST = "[INST]", "[/INST]"
    B_SYS, E_SYS = "<<SYS>>\n", "\n<</SYS>>\n\n"

    prompt = B_INST + B_SYS + SYSTEM_PROMPT + E_SYS + prompt + E_INST
    return prompt


def query_model():
    url = f"{config.ngrok_url}/predict"  # Ersetzen Sie dies durch die tatsächliche ngrok URL
    print(f"Run: {url}")
    headers = {
        'Content-Type': 'application/json',
        'ngrok-skip-browser-warning': 'true'
    }
    prompt = combine_prompt()
    print(prompt)
    body = {
        'prompt': combine_prompt()
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


# Beispielverwendung
result = query_model()
if result:
    print("Antwort vom Modell:", result)
else:
    print("Keine gültige Antwort erhalten.")
