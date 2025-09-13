from typing import List, Union
import base64
import json

def bytes_to_int(data: bytes) -> int:
    """
    Args:
        data: Bytes to convert
    
    Returns:
        int: Integer representation
    """
    return int.from_bytes(data, byteorder='big')


def int_to_bytes(number: int, length: int) -> bytes:
    """
    Args:
        number: Integer to convert
        length: Target byte length
    
    Returns:
        bytes: Byte representation
    """
    return number.to_bytes(length, byteorder='big')


def calculate_byte_length(key_size: int) -> int:
    """
    Args:
        key_size: Key size in bits
    
    Returns:
        int: Byte length
    """
    return (key_size + 7) // 8


def encode_base64(data: bytes) -> str:
    """
    Args:
        data: Bytes to encode
    
    Returns:
        str: Base64 encoded string
    """
    return base64.b64encode(data).decode('ascii')


def decode_base64(data: str) -> bytes:
    """
    Args:
        data: Base64 string to decode
    
    Returns:
        bytes: Decoded bytes
    
    Raises:
        ValueError: If base64 decoding fails
    """
    try:
        return base64.b64decode(data.encode('ascii'))
    except Exception as ex:
        raise ValueError(f"Invalid base64 data: {ex}")


def string_to_blocks(text: str, block_size: int, encoding: str = 'utf-8') -> List[bytes]:
    """
    Args:
        text: Text to split
        block_size: Maximum size of each block in bytes
        encoding: Text encoding to use
    
    Returns:
        List[bytes]: List of byte blocks
    """
    text_bytes = text.encode(encoding)
    blocks = []
    
    for i in range(0, len(text_bytes), block_size):
        block = text_bytes[i:i + block_size]
        blocks.append(block)
    
    return blocks


def blocks_to_string(blocks: List[bytes], encoding: str = 'utf-8') -> str:
    """
    Args:
        blocks: List of byte blocks
        encoding: Text encoding to use
    
    Returns:
        str: Reconstructed string
    """
    combined_bytes = b''.join(blocks)
    return combined_bytes.decode(encoding)


def serialize_key_data(key_data: dict) -> str:
    """
    Args:
        key_data: Dictionary containing key information
    
    Returns:
        str: Base64-encoded JSON string
    """
    json_string = json.dumps(key_data, separators=(',', ':'))
    json_bytes = json_string.encode('utf-8')
    return encode_base64(json_bytes)


def deserialize_key_data(key_string: str) -> dict:
    """
    Args:
        key_string: Base64-encoded JSON string
    
    Returns:
        dict: Key data dictionary
    
    Raises:
        ValueError: If deserialization fails
    """
    try:
        json_bytes = decode_base64(key_string)
        json_string = json_bytes.decode('utf-8')
        return json.loads(json_string)
    except Exception as ex:
        raise ValueError(f"Failed to deserialize key data: {ex}")


def hex_to_bytes(hex_string: str) -> bytes:
    """
    Args:
        hex_string: Hexadecimal string
    
    Returns:
        bytes: Byte representation
    
    Raises:
        ValueError: If hex string is invalid
    """
    try:
        # remove any whitespace and ensure even length
        hex_string = hex_string.replace(' ', '').replace('\n', '')
        if len(hex_string) % 2 != 0:
            hex_string = '0' + hex_string
        return bytes.fromhex(hex_string)
    except ValueError as ex:
        raise ValueError(f"Invalid hexadecimal string: {ex}")


def bytes_to_hex(data: bytes, separator: str = '') -> str:
    """
    Args:
        data: Bytes to convert
        separator: Optional separator between hex pairs
    
    Returns:
        str: Hexadecimal string
    """
    hex_string = data.hex()
    if separator:
        return separator.join(hex_string[i:i+2] for i in range(0, len(hex_string), 2))
    return hex_string


def pad_string(text: str, length: int, padding_char: str = ' ') -> str:
    """
    Args:
        text: String to pad
        length: Target length
        padding_char: Character to use for padding
    
    Returns:
        str: Padded string
    """
    if len(text) >= length:
        return text
    
    padding_needed = length - len(text)
    return text + (padding_char * padding_needed)


def truncate_string(text: str, max_length: int, suffix: str = '...') -> str:
    """
    Args:
        text: String to truncate
        max_length: Maximum allowed length
        suffix: Suffix to add if truncated
    
    Returns:
        str: Truncated string
    """
    if len(text) <= max_length:
        return text
    
    if len(suffix) >= max_length:
        return text[:max_length]
    
    return text[:max_length - len(suffix)] + suffix


def format_bytes(byte_count: int) -> str:
    """
    Args:
        byte_count: Number of bytes
    
    Returns:
        str: Formatted string (e.g., "1.5 KB", "2.3 MB")
    """
    units = ['B', 'KB', 'MB', 'GB', 'TB']
    size = float(byte_count)
    unit_index = 0
    
    while size >= 1024.0 and unit_index < len(units) - 1:
        size /= 1024.0
        unit_index += 1
    
    if unit_index == 0:
        return f"{int(size)} {units[unit_index]}"
    else:
        return f"{size:.1f} {units[unit_index]}"