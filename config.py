from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from passlib.hash import md5_crypt

ACCESS_TOKEN_EXPIRE_MINUTES = 30
ALGORITHM = 'HS256'
OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl='/token')
PWD_CONTEXT = CryptContext(schemes=['bcrypt'], deprecated='auto')
PATH_CONTEXT = md5_crypt
SECRET_KEY = 'mein_sekret'
TOKEN_SUBJECT = 'access'
