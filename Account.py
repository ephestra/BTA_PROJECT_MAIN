import json
from FileManager import FileManager
from HistoryMessages import HistoryMessages

class Account:
    def __init__(self, balance = 0):
        self.balance = balance
        self.file_manager = FileManager()
        self.hist_file_path = "hist.json"
        

    def write_to_history(self, hist_dict):
        self.file_manager 

        with open(self.hist_file_path, "a") as file:
            json.dump(hist_dict, file)
            file.write("\n")
    
    def deposit(self, amount):
        try:
            amount = float(amount)
        except ValueError:
            print("Invalid amount for deposit!")
            history_message = HistoryMessages.deposit("failure", amount, self.balance)
            self.write_to_history(history_message)
            return

        if amount <= 0:
            print('Invalid amount for deposit!')
            history_message = HistoryMessages.deposit("failure", amount, self.balance)
            self.write_to_history(history_message)
            return
        
        self.balance += amount
        history_message = HistoryMessages.deposit("success", amount, self.balance)
        self.write_to_history(history_message)


    def debit(self, amount):
        if not isinstance(amount, (int, float)) or amount <= 0:
            print("Invalid amount for debit!")
            history_message = HistoryMessages.debit("failure", amount, self.balance)
            self.write_to_history(history_message)
            return 
        
        if self.balance >= amount:
            self.balance -= amount
            history_message = HistoryMessages.debit("success", amount, self.balance)
            self.write_to_history(history_message)
        else:
            print('Invalid amount for debit!') 
            history_message = HistoryMessages.debit("failure", amount, self.balance)
            self.write_to_history(history_message)
    def get_balance(self):
        return self.balance

    def dict_to_string(self, dict):
        if dict["operation_type"] != "exchange":
            return f'type: {dict["operation_type"]} status: {dict["status"]} amount: {dict["amount_of_deposit"]} balance: {dict["total_balance"]}'
        else:
            return f'type: {dict["operation_type"]} status: {dict["status"]} pre exchange amount: {dict["pre_exchange_amount"]} exchange amount: {dict["exchange_amount"]} currency from: {dict["currency_from"]} currency to: {dict["currency_to"]}'
        

    def get_history(self):
        history_list = []
        with open(self.hist_file_path, "r") as file:
            lines = file.readlines()
            if not lines:  # Handle empty file
                return "No transaction history available."
            for line in lines:
                try:
                    hist_dict = json.loads(line.strip())
                    history_list.append(self.dict_to_string(hist_dict) + "\n")
                except json.JSONDecodeError:
                    print("Error decoding JSON from history file.")
        return "".join(history_list)
