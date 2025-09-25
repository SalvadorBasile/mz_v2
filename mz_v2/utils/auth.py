import bcrypt
import jwt
from typing import Optional
from datetime import datetime, timezone, timedelta


#Sistema de Encriptacion de password
class AuthManager:
    SECRET_KEY = "admin123"

    @staticmethod
    def hash_password(password: str) -> str:
        #Convertimos el password en un hash seguro
        password_bytes = password.encode('utf-8')
        #Generar un salt (ingrediente extra para mayor seguridad)
        salt = bcrypt.gensalt()
        #Crear el hash
        hash_bytes = bcrypt.hashpw(password_bytes, salt)
        return hash_bytes.decode('utf-8')
    
    @staticmethod
    def verify_password(password: str, hash: str) -> bool:
        #Verifica si el password coincide con el hash
        return bcrypt.checkpw(password.encode('utf-8'), hash.encode('utf-8'))
    
#Sistema de Sesiones y Tokens
    @staticmethod
    def create_token(user_id: int) -> str:
        #Crea un token de sesion para el usuario
        payload = {
            'user_id': user_id,
            'exp': datetime.now(timezone.utc) + timedelta(hours=2) #El token expira en 2 horas
        }

        return jwt.encode(payload, AuthManager.SECRET_KEY, algorithm='HS256')
    
    @staticmethod
    def verify_token(token: str) -> Optional[int]:
        #Verifica un token y devuelve el user_id si es valido
        try:
            payload = jwt.decode(token, AuthManager.SECRET_KEY, algorithms=['HS256'])
            return payload['user_id']
        except jwt.ExpiredSignatureError:
            return None #Token expirado
        except jwt.InvalidTokenError:
            return None #Token invalido