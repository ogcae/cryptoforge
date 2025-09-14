#| ------------------------------------------ |
__email__   =  "c.ogcae@engineer.com"
__name__    =  "cryptoforge"
__version__ =  "1.0.2"
__author__  =  "ogcae"
#| ------------------------------------------ |

from typing import Optional, List, Union
import hashlib
import secrets

from utils.encoding import (
    string_to_blocks, blocks_to_string, bytes_to_int, int_to_bytes,
    calculate_byte_length, encode_base64, decode_base64
)

from crypto.padding import apply_pkcs1_padding, remove_pkcs1_padding
from utils.math import modular_inverse, fast_modular_exponentiation
from crypto.prime import generate_prime_pair, find_public_exponent
from core.keypair import RSAKeyPair

class RSAEngine:
    def __init__(self):
        self._key_pair: Optional[RSAKeyPair] = None
        self._session_id: str = secrets.token_hex(16)
    
    def generate_key_pair(self, key_size: int = 2048, seed: Optional[int] = None, 
                         secure: bool = True) -> RSAKeyPair:
        """
        Args:
            key_size: Size of the key in bits (default: 2048)
            seed: Random seed for reproducible key generation (optional)
            secure: Use cryptographically secure random generation
        
        Returns:
            RSAKeyPair: Generated key pair
        
        Raises:
            ValueError: If key_size is too small
        """
        if key_size < 512:
            raise ValueError("Key size must be at least 512 bits for security")
        
        if seed is not None and not secure:
            import random
            random.seed(seed)
        
        # generate two large prime numbers
        prime_size = key_size // 2
        p, q = generate_prime_pair(prime_size, secure=secure)
        
        # calculate modulus and totient
        n = p * q
        phi_n = (p - 1) * (q - 1)
        
        # find public exponent
        e = find_public_exponent(phi_n)
        
        # calculate private exponent
        d = modular_inverse(e, phi_n)
        
        # create and store key pair
        self._key_pair = RSAKeyPair((e, n), d, n)
        return self._key_pair
    
    def load_key_pair(self, key_pair: RSAKeyPair) -> None:
        self._key_pair = key_pair
    
    def load_public_key(self, public_key_str: str) -> None:
        self._key_pair = RSAKeyPair.from_public_key_string(public_key_str)
    
    def load_private_key(self, private_key_str: str) -> None:
        self._key_pair = RSAKeyPair.from_private_key_string(private_key_str)
    
    def encrypt_number(self, message: int) -> int:
        if not self._key_pair:
            raise ValueError("No key pair loaded")
        
        if message >= self._key_pair.modulus:
            raise ValueError("Message too large for key size")
        
        e, n = self._key_pair.get_public_key()
        return fast_modular_exponentiation(message, e, n)
    
    def decrypt_number(self, ciphertext: int) -> int:
        if not self._key_pair or self._key_pair.private_key is None:
            raise ValueError("No private key available for decryption")
        
        d, n = self._key_pair.private_key, self._key_pair.modulus
        return fast_modular_exponentiation(ciphertext, d, n)
    
    def encrypt_text(self, message: str, encoding: str = 'utf-8') -> str:
        if not self._key_pair:
            raise ValueError("No key pair loaded")
        
        message_bytes = message.encode(encoding)
        byte_length = calculate_byte_length(self._key_pair.key_size)
        max_message_size = byte_length - 11
        
        if len(message_bytes) > max_message_size:
            raise ValueError(f"Message too long. Maximum size: {max_message_size} bytes")
        
        padded_message = apply_pkcs1_padding(message_bytes, byte_length)
        message_int = bytes_to_int(padded_message)
        encrypted_int = self.encrypt_number(message_int)
        encrypted_bytes = int_to_bytes(encrypted_int, byte_length)
        return encode_base64(encrypted_bytes)
    
    def decrypt_text(self, encrypted_message: str, encoding: str = 'utf-8') -> str:
        if not self._key_pair or self._key_pair.private_key is None:
            raise ValueError("No private key available for decryption")
        
        try:
            encrypted_bytes = decode_base64(encrypted_message)
            encrypted_int = bytes_to_int(encrypted_bytes)
            decrypted_int = self.decrypt_number(encrypted_int)
            
            byte_length = calculate_byte_length(self._key_pair.key_size)
            decrypted_bytes = int_to_bytes(decrypted_int, byte_length)
            message_bytes = remove_pkcs1_padding(decrypted_bytes)
            
            return message_bytes.decode(encoding)
        except Exception as ex:
            raise ValueError(f"Decryption failed: {ex}")
    
    def encrypt_long_text(self, message: str, encoding: str = 'utf-8') -> List[str]:
        if not self._key_pair:
            raise ValueError("No key pair loaded")
        
        byte_length = calculate_byte_length(self._key_pair.key_size)
        max_block_size = byte_length - 11
        
        blocks = string_to_blocks(message, max_block_size, encoding)
        encrypted_blocks = []
        
        for block in blocks:
            padded_block = apply_pkcs1_padding(block, byte_length)
            block_int = bytes_to_int(padded_block)
            encrypted_int = self.encrypt_number(block_int)
            encrypted_bytes = int_to_bytes(encrypted_int, byte_length)
            encrypted_blocks.append(encode_base64(encrypted_bytes))
        
        return encrypted_blocks
    
    def decrypt_long_text(self, encrypted_blocks: List[str], encoding: str = 'utf-8') -> str:
        if not self._key_pair or self._key_pair.private_key is None:
            raise ValueError("No private key available for decryption")
        
        decrypted_blocks = []
        byte_length = calculate_byte_length(self._key_pair.key_size)
        
        for encrypted_block in encrypted_blocks:
            encrypted_bytes = decode_base64(encrypted_block)
            encrypted_int = bytes_to_int(encrypted_bytes)
            decrypted_int = self.decrypt_number(encrypted_int)
            decrypted_bytes = int_to_bytes(decrypted_int, byte_length)
            block_bytes = remove_pkcs1_padding(decrypted_bytes)
            decrypted_blocks.append(block_bytes)
        
        return blocks_to_string(decrypted_blocks, encoding)
    
    def sign_message(self, message: str, encoding: str = 'utf-8', 
                    hash_algorithm: str = 'sha256') -> str:
        if not self._key_pair or self._key_pair.private_key is None:
            raise ValueError("No private key available for signing")
        
        hash_functions = {
            'sha256': hashlib.sha256,
            'sha384': hashlib.sha384,
            'sha512': hashlib.sha512
        }
        
        if hash_algorithm not in hash_functions:
            raise ValueError(f"Unsupported hash algorithm: {hash_algorithm}")
        
        hash_func = hash_functions[hash_algorithm]
        message_hash = hash_func(message.encode(encoding)).digest()
        
        byte_length = calculate_byte_length(self._key_pair.key_size)
        padded_hash = apply_pkcs1_padding(message_hash, byte_length, padding_type='signature')
        
        hash_int = bytes_to_int(padded_hash)
        signature_int = self.decrypt_number(hash_int)
        
        signature_bytes = int_to_bytes(signature_int, byte_length)
        return encode_base64(signature_bytes)
    
    def verify_signature(self, message: str, signature: str, encoding: str = 'utf-8',
                        hash_algorithm: str = 'sha256') -> bool:
        if not self._key_pair:
            raise ValueError("No key pair loaded")
        
        try:
            hash_functions = {
                'sha256': hashlib.sha256,
                'sha384': hashlib.sha384,
                'sha512': hashlib.sha512
            }
            
            if hash_algorithm not in hash_functions:
                return False
            
            signature_bytes = decode_base64(signature)
            signature_int = bytes_to_int(signature_bytes)
            
            decrypted_int = self.encrypt_number(signature_int)
            byte_length = calculate_byte_length(self._key_pair.key_size)
            decrypted_bytes = int_to_bytes(decrypted_int, byte_length)
            
            decrypted_hash = remove_pkcs1_padding(decrypted_bytes, padding_type='signature')
            
            hash_func = hash_functions[hash_algorithm]
            message_hash = hash_func(message.encode(encoding)).digest()
            return decrypted_hash == message_hash
        
        except Exception:
            return False
    
    def get_key_info(self) -> dict:
        if not self._key_pair:
            return {"status": "No key pair loaded"}
        
        e, n = self._key_pair.get_public_key()
        
        key_data = f"{e}:{n}".encode('utf-8')
        fingerprint = hashlib.sha256(key_data).hexdigest()[:16]
        
        return {
            "key_size": self._key_pair.key_size,
            "public_exponent": e,
            "has_private_key": self._key_pair.private_key is not None,
            "fingerprint": fingerprint,
            "session_id": self._session_id
        }
    
    def benchmark_performance(self, iterations: int = 10) -> dict:
        if not self._key_pair:
            raise ValueError("No key pair loaded for benchmarking")
        
        import time
        
        test_message = "Performance benchmark test message"
        
        start_time = time.time()
        for _ in range(iterations):
            encrypted = self.encrypt_text(test_message)
        encrypt_time = (time.time() - start_time) / iterations
        
        if self._key_pair.private_key is not None:
            start_time = time.time()
            for _ in range(iterations):
                self.decrypt_text(encrypted)
            decrypt_time = (time.time() - start_time) / iterations
        else:
            decrypt_time = None
        
        return {
            "key_size": self._key_pair.key_size,
            "iterations": iterations,
            "avg_encrypt_time": encrypt_time,
            "avg_decrypt_time": decrypt_time,
            "encrypt_ops_per_sec": 1.0 / encrypt_time if encrypt_time > 0 else 0,
            "decrypt_ops_per_sec": 1.0 / decrypt_time if decrypt_time and decrypt_time > 0 else 0
        }
    
    @property
    def key_pair(self) -> Optional[RSAKeyPair]:
        return self._key_pair
    
    @property
    def session_id(self) -> str:
        return self._session_id
