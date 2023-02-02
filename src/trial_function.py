#this module is going to be a simple function
def adding(num1: int, num2: int):
    return num1 + num2

def multi(num1: int, num2: int):
    return num1 * num2

def devid(num1: int, num2: int):
    return num1 / num2

def subt(num1: int, num2: int):
    return num1 - num2

class InsufficientFunds(Exception):
    pass

class Account():
    def __init__(self, starting_balance = 0):
        self.balance = starting_balance

    def deposit(self, amount):
        self.balance += amount
        
    def withdraw(self, amount):
        if amount > self.balance:
            raise InsufficientFunds('Not that much available')
        self.balance -= amount

    def collect_interest(self):
        self.balance *= 1.1


