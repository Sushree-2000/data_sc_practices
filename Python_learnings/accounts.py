import datetime
import pytz

class Account:
    @staticmethod
    def _current_time(self):
        utc_time = pytz.utc.localize(datetime.datetime.utcnow())
        return utc_time.astimezone(pytz.timezone('US/Eastern'))
    def __init__(self, name, balance):
        self.name = name
        self.balance = balance
        print(f"Account created for {self.name} with balance {self.balance}")
        self.show_balance()

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            self.show_balance()

            self.transaction_list.append((Account._current_time(), amount))
        else:
            print("Invalid deposit amount.")

    def withdraw(self, amount):
        if amount > 0 and amount <= self.balance:
            self.balance -= amount
            self.transaction_list.append((Account._current_time(), -amount))
        else:
            print("Insufficient funds or invalid amount. Please give an amount less than or equal to your balance ")
            self.show_balance()

    def show_balance(self):
        print(f"Current balance for {self.name} is {self.balance}")

    def show_transactions(self):
        for date, amount in self.transaction_list:
            if amount>0:
                trans_type = "Deposit"
            else:                
                trans_type = "Withdrawal"   
                amount*= -1
            print("{:6} {} on {} (local time: {})".format(amount, trans_type, date, date.astimezone(pytz.timezone('US/Eastern'))))

if __name__ == "__main__":
    tim = Account("Tim", 1000)
    tim.show_balance()
    tim.deposit(500)
    tim.show_balance()
    tim.withdraw(200)
    tim.show_balance()

    steph = Account("Steph", 2000)
    steph.deposit(1000)
    steph.withdraw(500)
    steph.show_balance()
    steph.show_transactions()
    steph.show_balance()