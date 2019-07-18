import base64
import hashlib

from Crypto.Cipher import AES


class Cryptor:

    def doEncryption_data(self, raw_data, key, iv):
        # 前準備
        raw_base64 = base64.b64encode(raw_data)
        while len(raw_base64) % 16 != 0:
            raw_base64 += "_"
        key_32bit = hashlib.sha256(key).digest()
        iv = hashlib.md5(iv).digest()

        # 暗号化とデータの文字列化
        crypt = AES.new(key_32bit, AES.MODE_CBC, iv)
        encrypted_data = crypt.encrypt(raw_base64)
        encrypted_data_base64 = base64.b64encode(encrypted_data)
        return encrypted_data_base64

    def doDecryption_data(self, encrypted_data_base64, key, iv):
        # 前準備
        encrypted_data = base64.b64decode(encrypted_data_base64)
        key_32bit = hashlib.sha256(key).digest()
        iv = hashlib.md5(iv).digest()
        crypt = AES.new(key_32bit, AES.MODE_CBC, iv)

        # 復号と後処理
        decrypted_data = crypt.decrypt(encrypted_data)
        decrypted_data = decrypted_data.split("_")[0]
        raw_data = base64.b64decode(decrypted_data)
        return raw_data

    def get_uuid(self):
        x = subprocess.check_output('wmic csproduct get UUID')
        x = str(x).split()
        x = x[1].replace("b'", "")\
                .replace("'", "")\
                .replace("-", "")\
                .replace("\\r", "")\
                .replace("\\n", "")
        return(x)
