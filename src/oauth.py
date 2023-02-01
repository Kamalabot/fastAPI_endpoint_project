from jose import JWTError, jwt
from .databaseORM import get_db
from . import models
from sqlalchemy.orm import Session
import configparser
from datetime import datetime, timedelta
from .comm_schema import TokenData
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

sec_reader = configparser.ConfigParser()
sec_reader.read_file(open('calter.config'))

SECRET_KEY = sec_reader["OAUTH"]["SECRET"]
ALGORITHM = sec_reader["OAUTH"]["ALGO"]
EXPIRES = sec_reader["OAUTH"]["EXPIRATION"]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login',auto_error=False)
Depends(oauth2_scheme)
def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes = int(EXPIRES))
    
    to_encode.update({"exp":expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def verify_access_token(token:str, cred_exception):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(payload)

        id = payload.get("user_id")
    
        if id is None:
            raise cred_exception

        token_data = TokenData(id=id)
    except JWTError:
        raise cred_exception

    return token_data

def get_current_user(token:str = Depends(oauth2_scheme),db: Session = Depends(get_db)):
    print(f'in get_c {token}')
    cred_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                   detail='Could not validate',
                                   headers={"WWW-Authenticate":"Bearer"})
    token = verify_access_token(token, cred_exception)
    user = db.query(models.User).filter(models.User.email == token.username).first
    return user
