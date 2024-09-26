from FileManager import FileManager
from HistoryMessages import HistoryMessages
import requests

class CurrencyExchange:
    def __init__(self, balance = 0):
        self.file_manager = FileManager()
        self.hist_file_path = "hist.json"
        

    def write_to_history(self, hist_dict):
        
        self.file_manager.add_to_json(hist_dict, self.hist_file_path) 

    def get_exchange_rates(self):

        url = 'https://fake-api.apps.berlintech.ai/api/currency_exchange'

        response = requests.get(url)

        if response.status_code == 200 :
            return response.json()
        else:
            raise Exception(response.status_code)

    
    def exchange_currency(self, currency_from, currency_to, amount):

        rates = self.get_exchange_rates()
        
        if currency_from not in rates or currency_to not in rates:
            print('Currency exchange failed! Invalid currency code.')
            history_message = HistoryMessages.exchange("failure", amount, None, currency_from, currency_to)
            self.write_to_history(history_message)
            return None
        
        rate_from = rates[currency_from]
        rate_to = rates[currency_to]

        if not isinstance(amount, (int, float)) or amount <= 0:
            print('Currency exchange failed!')
            history_message = HistoryMessages.exchange("failure", amount, None, currency_from, currency_to)
            self.write_to_history(history_message)
            return None
        
        if rate_from == 0:
            print("Cannot divide by zero! The exchange rate for the original currency cannot be zero.")
            history_message = HistoryMessages.exchange("failure", amount, None, currency_from, currency_to)
            self.write_to_history(history_message)
            return None

        converted_amount = amount * (rate_to / rate_from)

        history_message = HistoryMessages.exchange("success", amount, converted_amount, currency_from, currency_to)
        self.write_to_history(history_message)

        return converted_amount