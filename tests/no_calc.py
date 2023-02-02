#this is a simple test
from src.trial_function import * 
import pytest

@pytest.fixture
def zero_bank_account():
    return Account()

@pytest.fixture
def filled_account():
    return Account(580)

@pytest.mark.parametrize("x, y, result",[
    (5, 3, 8),
    (152,7,159),
    (75,62,578)
    ])
def test_adding(x, y, result):
    print('testing add')
    #following assert can be used for checking the logic
    assert adding(x,y) == result 

#there is no need to call the above function for the test to run

def test_multi():
    assert multi(3,12) == 36 
    
def test_devid():
    assert devid(12,3) == 4

def test_subt():
    assert subt(17,3) == 14

#The above three tests will be auto-discovered by pytest when executed from the
#project root directory
def test_new_bank_account(filled_account):
    assert filled_account.balance == 580

def test_withdraw_account(filled_account):
    filled_account.withdraw(5)
    assert filled_account.balance == 575

def test_deposit_account(zero_bank_account):
    zero_bank_account.deposit(25)
    assert zero_bank_account.balance == 25
@pytest.mark.parametrize("x, y, result",[
    (500, 300, 208),
    (152,7,145),
    (75,62,13)
    ])
def test_bank_txn(zero_bank_account, x, y, result):
    zero_bank_account.deposit(x)
    zero_bank_account.withdraw(y)
    assert zero_bank_account.balance == result

def test_raise_exception(filled_account):
    with pytest.raises(Exception):
        filled_account.withdraw(1000)
