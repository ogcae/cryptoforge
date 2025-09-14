#| ------------------------------------------ |
__email__   =  "c.ogcae@engineer.com"
__name__    =  "cryptoforge"
__version__ =  "1.0.2"
__author__  =  "ogcae"
#| ------------------------------------------ |

from utils.encoding import encode_base64, decode_base64, serialize_key_data, deserialize_key_data
from typing import Tuple, Optional
import json

class RSAKeyPair:
    def __init__(self, public_key: Tuple[int, int], private_key: Optional[int] = None, 
                 modulus: Optional[int] = None):
        """
        Args:
            public_key: Tuple of (e, n) where e is public exponent, n is modulus
            private_key: Private exponent d (optional)
            modulus: Modulus n (optional, derived from public_key if not provided)
        """
        self.public_key = public_key
        self.private_key = private_key
        self.modulus = modulus if modulus is not None else public_key[1]
    
    @property
    def key_size(self) -> int:
        """Returns the key size in bits."""
        return self.modulus.bit_length()
    
    def get_public_key(self) -> Tuple[int, int]:
        """Returns the public key as (e, n)."""
        return self.public_key
    
    def get_private_key(self) -> Optional[int]:
        """Returns the private key exponent."""
        return self.private_key
    
    def has_private_key(self) -> bool:
        """Returns True if this key pair includes the private key."""
        return self.private_key is not None
    
    def export_public_key(self) -> str:
        """Exports the public key as a base64-encoded JSON string."""
        e, n = self.public_key
        key_data = {
            "type": "RSA_PUBLIC_KEY",
            "e": e,
            "n": n,
            "key_size": self.key_size
        }
        return serialize_key_data(key_data)
    
    def export_private_key(self) -> str:
        """Exports the private key as a base64-encoded JSON string."""
        if self.private_key is None:
            raise ValueError("No private key available for export")
        
        e, n = self.public_key
        key_data = {
            "type": "RSA_PRIVATE_KEY",
            "e": e,
            "n": n,
            "d": self.private_key,
            "key_size": self.key_size
        }
        return serialize_key_data(key_data)
    
    def export_key_pair(self) -> dict:
        """Exports both keys as a dictionary."""
        result = {
            "public_key": self.export_public_key()
        }
        
        if self.private_key is not None:
            result["private_key"] = self.export_private_key()
        
        return result
    
    @classmethod
    def from_public_key_string(cls, key_string: str) -> 'RSAKeyPair':
        """Creates a key pair from a public key string."""
        try:
            key_data = deserialize_key_data(key_string)
            
            if key_data.get("type") != "RSA_PUBLIC_KEY":
                raise ValueError("Invalid public key format")
            
            e = key_data["e"]
            n = key_data["n"]
            
            return cls((e, n))
        
        except Exception as ex:
            raise ValueError(f"Failed to import public key: {ex}")
    
    @classmethod
    def from_private_key_string(cls, key_string: str) -> 'RSAKeyPair':
        """Creates a key pair from a private key string."""
        try:
            key_data = deserialize_key_data(key_string)
            
            if key_data.get("type") != "RSA_PRIVATE_KEY":
                raise ValueError("Invalid private key format")
            
            e = key_data["e"]
            n = key_data["n"]
            d = key_data["d"]
            
            return cls((e, n), d, n)
        
        except Exception as ex:
            raise ValueError(f"Failed to import private key: {ex}")
    
    @classmethod
    def from_key_pair_dict(cls, key_dict: dict) -> 'RSAKeyPair':
        """Creates a key pair from a dictionary containing both keys."""
        public_key_pair = cls.from_public_key_string(key_dict["public_key"])
        
        if "private_key" in key_dict:
            private_key_pair = cls.from_private_key_string(key_dict["private_key"])
            public_key_pair.private_key = private_key_pair.private_key
        
        return public_key_pair
    
    def __str__(self) -> str:
        """String representation of the key pair."""
        key_type = "Key Pair" if self.has_private_key() else "Public Key"
        return f"RSA {key_type} ({self.key_size} bits)"
    
    def __repr__(self) -> str:
        """Detailed representation of the key pair."""
        e, n = self.public_key
        return (f"RSAKeyPair(public_key=({e}, {n}), "
                f"private_key={'***' if self.private_key else None}, "
                f"key_size={self.key_size})")
