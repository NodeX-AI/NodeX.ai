# services/encryption.py
import os
import base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from config.config import AES_KEY
from utils.logger import logger

class MessageEncryptor:
    def __init__(self, key_b64: str = None):
        key_b64 = AES_KEY
        
        if not key_b64:
            raise ValueError("❌ Ключ шифрования не найден в .env")
        
        try:
            self.key = base64.urlsafe_b64decode(key_b64.encode()) # декодируем ключ в бинарный вид
            if len(self.key) != 32:
                raise ValueError("Ключ должен быть 32 байта для AES-256")
            self.aesgcm = AESGCM(self.key) # создаем объект для шифрования
        except Exception as e:
            raise ValueError(f"Неверный ключ шифрования: {e}")
    
    def encrypt(self, plaintext: str) -> str:
        try:
            nonce = os.urandom(12) # nonce (number used once) - случайное число для каждого шифрования (96 бит)
            encrypted = self.aesgcm.encrypt(nonce, plaintext.encode(), None)
            return base64.urlsafe_b64encode(nonce + encrypted).decode()
        except Exception as e:
            logger.error(f"❌ Ошибка шифрования: {e}")
            return plaintext
    
    def decrypt(self, encrypted_text: str) -> str:
        try:
            data = base64.urlsafe_b64decode(encrypted_text.encode())
            nonce, encrypted = data[:12], data[12:]
            decrypted = self.aesgcm.decrypt(nonce, encrypted, None)
            return decrypted.decode()
        except Exception as e:
            logger.error(f"❌ Ошибка расшифровки: {e}")
            return "Не удалось расшифровать"

encryptor = MessageEncryptor()