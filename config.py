import configparser


class Config:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')

    @property
    def start_date(self):
        return self.config['DEFAULT']['START_DATE']

    @property
    def end_date(self):
        return self.config['DEFAULT']['END_DATE']

    @property
    def data_dir(self):
        return f"./data/{self.start_date}_{self.end_date}"

    @property
    def dow_30(self):
        return self.config['DEFAULT']['DOW_30'].split(',')

    @property
    def finnhub_key(self):
        return self.config['DEFAULT']['FINNHUB_KEY']

    @property
    def ngrok_url(self):
        return self.config['DEFAULT']['NGROK_URL']

    @property
    def api_key(self):
        return self.config['DEFAULT']['OPENAI_KEY']

    @property
    def wandb_api_key(self):
        return self.config['WANDB']['WANDB_API_KEY']

    @property
    def wandb_project(self):
        return self.config['WANDB']['WANDB_PROJECT']

    @property
    def company_template(self):
        return self.config['PROMPT']['COMPANY_TEMPLATE']

    @property
    def system_prompt(self):
        return self.config['PROMPT']['SYSTEM_PROMPT']
