
#This part takes care of the password hashing
from passlib.context import CryptContext
passwd_context = CryptContext(schemes=["bcrypt"], deprecated='auto')

def hasher(passwd:str):
    return passwd_context.hash(passwd)

