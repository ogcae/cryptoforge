from typing import Union
import secrets

def apply_pkcs1_padding(message: bytes, target_length: int, 
                       padding_type: str = 'encryption') -> bytes:
    """
    PKCS#1
    
    Args:
        message: Message bytes to pad
        target_length: Target length after padding
        padding_type: 'encryption' or 'signature'
    
    Returns:
        bytes: Padded message
    
    Raises:
        ValueError: If message is too long or parameters are invalid
    """
    if len(message) > target_length - 11:
        raise ValueError(f"Message too long for padding. Max: {target_length - 11} bytes")
    
    if target_length < 11:
        raise ValueError("Target length must be at least 11 bytes")
    
    #           0x00 || BT || PS || 0x00 || M
    #   BT = 0x02 for encryption, 0x01 for signature
    
    if padding_type == 'encryption':
        block_type = 0x02
        padding_length = target_length - len(message) - 3
        padding_bytes = bytearray()
        
        for _ in range(padding_length):
            byte_val = 0
            while byte_val == 0:
                byte_val = secrets.randbits(8)
            padding_bytes.append(byte_val)
        
        padding_string = bytes(padding_bytes)
    
    elif padding_type == 'signature':
        block_type = 0x01
        # use 0xFF (B)
        padding_length = target_length - len(message) - 3
        padding_string = bytes([0xFF] * padding_length)
    
    else:
        raise ValueError("padding_type must be 'encryption' or 'signature'")

    padded = bytes([0x00, block_type]) + padding_string + bytes([0x00]) + message
    
    if len(padded) != target_length:
        raise ValueError(f"Padding error: expected {target_length}, got {len(padded)}")
    
    return padded


def remove_pkcs1_padding(padded_message: bytes, 
                        padding_type: str = 'encryption') -> bytes:
    """
    PKCS#1
    Args:
        padded_message: Padded message bytes
        padding_type: 'encryption' or 'signature'
    
    Returns:
        bytes: Original message without padding
    
    Raises:
        ValueError: If padding is invalid or corrupted
    """
    if len(padded_message) < 11:
        raise ValueError("Padded message too short")
    
    # check first byte (should be 0x00)
    if padded_message[0] != 0x00:
        raise ValueError("Invalid padding: first byte must be 0x00")
    
    # check block type
    expected_bt = 0x02 if padding_type == 'encryption' else 0x01
    if padded_message[1] != expected_bt:
        raise ValueError(f"Invalid padding: wrong block type {padded_message[1]:02x}")
    
    # find 0x00
    separator_index = -1
    for i in range(2, len(padded_message)):
        if padded_message[i] == 0x00:
            separator_index = i
            break
    
    if separator_index == -1:
        raise ValueError("Invalid padding: separator not found")
    
    # check minimum padding length
    padding_length = separator_index - 2
    if padding_length < 8:
        raise ValueError("Invalid padding: padding string too short")
    
    # validate padding string
    if padding_type == 'encryption':
        for i in range(2, separator_index):
            if padded_message[i] == 0x00:
                raise ValueError("Invalid padding: zero byte in encryption padding")
    
    elif padding_type == 'signature':
        # for signature 0xFF
        for i in range(2, separator_index):
            if padded_message[i] != 0xFF:
                raise ValueError("Invalid padding: non-0xFF byte in signature padding")
    
    # extract original message
    message = padded_message[separator_index + 1:]
    
    if len(message) == 0:
        raise ValueError("Invalid padding: empty message")
    
    return message


def validate_padding_parameters(message_length: int, key_size: int, 
                               padding_type: str = 'encryption') -> bool:
    """
    Args:
        message_length: Length of message in bytes
        key_size: RSA key size in bits
        padding_type: Type of padding to apply
    
    Returns:
        bool: True if padding is possible
    """
    byte_length = (key_size + 7) // 8
    max_message_length = byte_length - 11
    
    return message_length <= max_message_length


def calculate_max_message_size(key_size: int) -> int:
    """
    Args:
        key_size: RSA key size in bits
    
    Returns:
        int: Maximum message size in bytes
    """
    byte_length = (key_size + 7) // 8
    return byte_length - 11


def generate_padding_string(length: int, padding_type: str = 'encryption') -> bytes:
    """
    Args:
        length: Length of padding string needed
        padding_type: 'encryption' or 'signature'
    
    Returns:
        bytes: Padding string
    """
    if length < 8:
        raise ValueError("Padding string must be at least 8 bytes")
    
    if padding_type == 'encryption':
        # generate non-zero random bytes
        padding_bytes = bytearray()
        for _ in range(length):
            byte_val = 0
            while byte_val == 0:
                byte_val = secrets.randbits(8)
            padding_bytes.append(byte_val)
        return bytes(padding_bytes)
    
    elif padding_type == 'signature':
        # 0xFF (B)
        return bytes([0xFF] * length)
    
    else:
        raise ValueError("padding_type must be 'encryption' or 'signature'")


def verify_padding_integrity(padded_message: bytes) -> dict:
    """
    Args:
        padded_message: Padded message to analyze
    
    Returns:
        dict: Analysis results including validity and details
    """
    result = {
        'valid': False,
        'length': len(padded_message),
        'block_type': None,
        'padding_length': 0,
        'message_length': 0,
        'errors': []
    }
    
    if len(padded_message) < 11:
        result['errors'].append("Message too short for PKCS#1 padding")
        return result
    
    # check first byte
    if padded_message[0] != 0x00:
        result['errors'].append(f"Invalid first byte: 0x{padded_message[0]:02x}")
    
    # get block type
    result['block_type'] = padded_message[1]
    if result['block_type'] not in [0x01, 0x02]:
        result['errors'].append(f"Invalid block type: 0x{result['block_type']:02x}")
    
    # find separator
    separator_index = -1
    for i in range(2, len(padded_message)):
        if padded_message[i] == 0x00:
            separator_index = i
            break
    
    if separator_index == -1:
        result['errors'].append("Separator byte not found")
        return result
    
    result['padding_length'] = separator_index - 2
    result['message_length'] = len(padded_message) - separator_index - 1
    
    # check minimum padding length
    if result['padding_length'] < 8:
        result['errors'].append("Padding string too short")
    
    # validate padding bytes
    if result['block_type'] == 0x02:  # Encryption
        for i in range(2, separator_index):
            if padded_message[i] == 0x00:
                result['errors'].append("Zero byte found in encryption padding")
                break
    
    elif result['block_type'] == 0x01:  # Signature
        for i in range(2, separator_index):
            if padded_message[i] != 0xFF:
                result['errors'].append("Non-0xFF byte found in signature padding")
                break
    
    result['valid'] = len(result['errors']) == 0
    return result