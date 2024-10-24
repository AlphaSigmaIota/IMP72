import backend


selected_stock = "AAPL"
prediction_date = "2024-10-22"
weeks_of_news = 4

company_prompt = backend.construct_prompt(selected_stock, prediction_date, weeks_of_news, False)

print(company_prompt)
