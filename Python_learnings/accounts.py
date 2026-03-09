class Account:
    def __init__(self, name, balance):
        self.name = name
        self.balance = balance
        print(f"Account created for {self.name} with balance {self.balance}")

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            self.show_balance()
        else:
            print("Invalid deposit amount.")

    def withdraw(self, amount):
        if amount > 0 and amount <= self.balance:
            self.balance -= amount
        else:
            print("Insufficient funds or invalid amount. Please give an amount less than or equal to your balance ")
            self.show_balance()

    def show_balance(self):
        print(f"Current balance for {self.name} is {self.balance}")

if __name__ == "__main__":
    tim = Account("Tim", 1000)
    tim.show_balance()
    tim.deposit(500)
    tim.show_balance()
    tim.withdraw(200)
    tim.show_balance()