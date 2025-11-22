import bcrypt
from SLLACK.api.logger import logger
from fastapi import HTTPException

class Hash:

    def encode_password(password: str):
        try:
            password_bytes = password.encode("utf-8")
            password_salt = bcrypt.gensalt()
            encoded_password = bcrypt.hashpw(password_bytes, password_salt)
            return encoded_password.decode("utf-8")
        except Exception as e:
            logger.error(f"Password encoding error: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to process password")

    def verify(hashed_password, plain_password):
        try:
            passbytes = plain_password.encode("utf-8")
            encoded_password = hashed_password.encode("utf-8")
            return bcrypt.checkpw(passbytes, encoded_password)
        except Exception as e:
            logger.error(f"Password verification error: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to verify password")
