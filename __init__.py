from engine.rsa import RSAEngine
from core.keypair import RSAKeyPair
from utils.math import (
    gcd, extended_euclidean, modular_inverse, fast_modular_exponentiation,
    lcm, jacobi_symbol, is_perfect_square, factorial, binomial_coefficient
)
from utils.encoding import (
    bytes_to_int, int_to_bytes, calculate_byte_length, encode_base64, decode_base64,
    string_to_blocks, blocks_to_string, serialize_key_data, deserialize_key_data,
    hex_to_bytes, bytes_to_hex, format_bytes
)
from crypto.prime import (
    miller_rabin_test, generate_prime, generate_safe_prime, is_strong_prime,
    generate_prime_pair, find_public_exponent, next_prime
)
from crypto.padding import (
    apply_pkcs1_padding, remove_pkcs1_padding, validate_padding_parameters,
    calculate_max_message_size, verify_padding_integrity
)

__email__   =  "c.ogcae@engineer.com"
__name__    =  "cryptoforge"
__version__ =  "1.0.2"
__author__  =  "ogcae"

class RSA:
    def __init__(self):
        self._engine = RSAEngine()
    
    def generate_key_pair(self, key_size: int = 2048, seed: int = None, secure: bool = True) -> RSAKeyPair:
        """Generate RSA key pair."""
        return self._engine.generate_key_pair(key_size, seed, secure)
    
    def load_key_pair(self, key_pair: RSAKeyPair) -> None:
        """Load existing key pair."""
        self._engine.load_key_pair(key_pair)
    
    def load_public_key(self, public_key_str: str) -> None:
        """Load public key from string."""
        self._engine.load_public_key(public_key_str)
    
    def load_private_key(self, private_key_str: str) -> None:
        """Load private key from string."""
        self._engine.load_private_key(private_key_str)
    
    def encrypt_number(self, message: int) -> int:
        """Encrypt numeric message."""
        return self._engine.encrypt_number(message)
    
    def decrypt_number(self, ciphertext: int) -> int:
        """Decrypt numeric ciphertext."""
        return self._engine.decrypt_number(ciphertext)
    
    def encrypt_text(self, message: str, encoding: str = 'utf-8') -> str:
        """Encrypt text message."""
        return self._engine.encrypt_text(message, encoding)
    
    def decrypt_text(self, encrypted_message: str, encoding: str = 'utf-8') -> str:
        """Decrypt text message."""
        return self._engine.decrypt_text(encrypted_message, encoding)
    
    def encrypt_long_text(self, message: str, encoding: str = 'utf-8') -> list:
        """Encrypt long text in blocks."""
        return self._engine.encrypt_long_text(message, encoding)
    
    def decrypt_long_text(self, encrypted_blocks: list, encoding: str = 'utf-8') -> str:
        """Decrypt long text from blocks."""
        return self._engine.decrypt_long_text(encrypted_blocks, encoding)
    
    def sign_message(self, message: str, encoding: str = 'utf-8', hash_algorithm: str = 'sha256') -> str:
        """Create digital signature."""
        return self._engine.sign_message(message, encoding, hash_algorithm)
    
    def verify_signature(self, message: str, signature: str, encoding: str = 'utf-8', hash_algorithm: str = 'sha256') -> bool:
        """Verify digital signature."""
        return self._engine.verify_signature(message, signature, encoding, hash_algorithm)
    
    def get_key_info(self) -> dict:
        """Get key information."""
        return self._engine.get_key_info()
    
    def benchmark_performance(self, iterations: int = 10) -> dict:
        """Benchmark RSA performance."""
        return self._engine.benchmark_performance(iterations)
    
    @property
    def key_pair(self) -> RSAKeyPair:
        """Get current key pair."""
        return self._engine.key_pair

    @staticmethod
    def GCD(a: int, b: int) -> int:
        """Legacy GCD method."""
        return gcd(a, b)
    
    @staticmethod
    def ExtendedEuclid(a: int, b: int) -> tuple:
        """Legacy Extended Euclidean method."""
        return extended_euclidean(a, b)
    
    @staticmethod
    def FastModExp(base: int, exponent: int, modulus: int) -> int:
        """Legacy fast modular exponentiation method."""
        return fast_modular_exponentiation(base, exponent, modulus)

__all__ = [
    'RSA', 'RSAEngine', 'RSAKeyPair',
    'gcd', 'extended_euclidean', 'modular_inverse', 'fast_modular_exponentiation',
    'lcm', 'jacobi_symbol', 'is_perfect_square', 'factorial', 'binomial_coefficient',
    'bytes_to_int', 'int_to_bytes', 'calculate_byte_length', 'encode_base64', 'decode_base64',
    'string_to_blocks', 'blocks_to_string', 'serialize_key_data', 'deserialize_key_data',
    'hex_to_bytes', 'bytes_to_hex', 'format_bytes',
    'miller_rabin_test', 'generate_prime', 'generate_safe_prime', 'is_strong_prime',
    'generate_prime_pair', 'find_public_exponent', 'next_prime',
    'apply_pkcs1_padding', 'remove_pkcs1_padding', 'validate_padding_parameters',
    'calculate_max_message_size', 'verify_padding_integrity'
]