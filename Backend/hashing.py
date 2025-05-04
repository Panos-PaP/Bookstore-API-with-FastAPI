from passlib.context import CryptContext


class Hash():
    pwd_cipher = CryptContext(schemes=["sha256_crypt"], deprecated="auto")

    @staticmethod
    def hashPwd(password: str):
        return Hash.pwd_cipher.hash(password)

    @staticmethod
    def verify_password(plainPwd, hashedPwd):
       return Hash.pwd_cipher.verify(plainPwd, hashedPwd)