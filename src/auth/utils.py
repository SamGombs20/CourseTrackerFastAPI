from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def verify_password(plain_pwd:str, hashed_pwd:str)->bool:
    #Verify plain password against hashed password
    return pwd_context.verify(plain_pwd, hashed_pwd)

def get_password_hash(password:str)->str:
    #Generate password hash froma plain password
    return pwd_context.hash(password)
