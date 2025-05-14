import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from datetime import datetime
import zipfile
import base64

# C# 头部数据
C_SHARP_HEADER = bytes([0, 1, 0, 0, 0, 255, 255, 255, 255, 1, 0, 0, 0, 0, 0, 0, 0, 6, 1, 0, 0, 0])

# AES密钥
AES_KEY = 'UKu52ePUBwetZ9wNX88o54dnfKRu0T1l'.encode('utf-8')

class SaveFileUtils:
    """存档文件处理工具类"""
    
    @staticmethod
    def generate_length_prefixed_string(length):
        """Generate LengthPrefixedString as per C# implementation"""
        length = min(0x7FFFFFFF, length)  # maximum value
        bytes_list = []
        for i in range(4):
            if length >> 7 != 0:
                bytes_list.append(length & 0x7F | 0x80)
                length >>= 7
            else:
                bytes_list.append(length & 0x7F)
                length >>= 7
                break
        if length != 0:
            bytes_list.append(length)
        return bytes(bytes_list)

    @staticmethod
    def add_header(data):
        """Add C# header to data"""
        length_data = SaveFileUtils.generate_length_prefixed_string(len(data))
        new_data = bytearray(len(data) + len(C_SHARP_HEADER) + len(length_data) + 1)
        
        # 添加固定头部
        new_data[:len(C_SHARP_HEADER)] = C_SHARP_HEADER
        # 添加长度前缀
        new_data[len(C_SHARP_HEADER):len(C_SHARP_HEADER) + len(length_data)] = length_data
        # 添加数据
        new_data[len(C_SHARP_HEADER) + len(length_data):-1] = data
        # 添加结束字节
        new_data[-1] = 11
        
        return bytes(new_data)

    @staticmethod
    def remove_header(data):
        """Remove C# header from data"""
        # 移除固定头部和结束字节
        data = data[len(C_SHARP_HEADER):-1]
        
        # 移除长度前缀
        length_count = 0
        for i in range(5):
            length_count += 1
            if (data[i] & 0x80) == 0:
                break
        
        return data[length_count:]

    @staticmethod
    def decrypt_save(encrypted_data):
        """Decrypt save file"""
        try:
            # 创建AES-ECB解密器
            cipher = Cipher(
                algorithms.AES(AES_KEY),
                modes.ECB(),
                backend=default_backend()
            )
            decryptor = cipher.decryptor()
            
            # 移除头部
            data = SaveFileUtils.remove_header(encrypted_data)
            
            # Base64解码
            data = base64.b64decode(data)
            
            # AES解密
            decrypted = decryptor.update(data) + decryptor.finalize()
            
            # 移除PKCS7填充
            padding_length = decrypted[-1]
            decrypted = decrypted[:-padding_length]
            
            # 解码为字符串
            return decrypted.decode('utf-8')
        except Exception as e:
            raise Exception(f"Failed to decrypt save file: {str(e)}")

    @staticmethod
    def encrypt_save(save_data):
        """Encrypt save data"""
        try:
            # 创建AES-ECB加密器
            cipher = Cipher(
                algorithms.AES(AES_KEY),
                modes.ECB(),
                backend=default_backend()
            )
            encryptor = cipher.encryptor()
            
            # 添加PKCS7填充
            data = save_data.encode('utf-8')
            padding_length = 16 - (len(data) % 16)
            padded_data = data + bytes([padding_length] * padding_length)
            
            # AES加密
            encrypted = encryptor.update(padded_data) + encryptor.finalize()
            
            # Base64编码
            encoded = base64.b64encode(encrypted)
            
            # 添加头部
            return SaveFileUtils.add_header(encoded)
        except Exception as e:
            raise Exception(f"Failed to encrypt save file: {str(e)}")

    @staticmethod
    def create_backup(save_files, save_dir):
        """Create a zip backup of save files"""
        try:
            # 创建备份文件名（使用当前日期和时间）
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = os.path.join(save_dir, f"hk_save_backup_{timestamp}.zip")
            
            # 创建zip文件
            with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for filepath in save_files:
                    if os.path.exists(filepath):
                        # 使用相对路径存储文件
                        arcname = os.path.basename(filepath)
                        zipf.write(filepath, arcname)
            
            print(f"\nCreated backup: {os.path.basename(backup_path)}")
            return True
        except Exception as e:
            print(f"Warning: Failed to create backup: {str(e)}")
            return False 