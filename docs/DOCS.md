# CryptoForge Documentation

## Table of Contents

1. [Installation](#installation)
2. [Quick Start](#quick-start)
3. [Core Classes](#core-classes)
4. [Key Management](#key-management)
5. [Encryption & Decryption](#encryption--decryption)
6. [Digital Signatures](#digital-signatures)
7. [Advanced Features](#advanced-features)
8. [Performance](#performance)
9. [Security Considerations](#security-considerations)
10. [API Reference](#api-reference)
11. [Examples](#examples)

## Installation

### Requirements
- Python 3.7+
- Standard library only (core functionality)
- Flask (optional, for web demo)

### Setup
```bash
# clone repository
git clone https://github.com/ogcae/cryptoforge.git
cd cryptoforge

# optional: install flask for web demo
pip install flask
```

## Quick Start

```python
from CryptoForge import RSA

# create rsa instance
rsa = RSA()

# generate key pair
rsa.generate_key_pair(2048)

# encrypt message
encrypted = rsa.encrypt_text("secret message")

# decrypt message
decrypted = rsa.decrypt_text(encrypted)

# digital signature
signature = rsa.sign_message("document")
is_valid = rsa.verify_signature("document", signature)
```

## Core Classes

### RSA
Main interface for RSA operations. Provides simplified access to all cryptographic functions.

### RSAEngine
Low-level RSA engine handling core cryptographic operations.

### RSAKeyPair
Manages RSA key pairs with import/export capabilities.

## Key Management

### Generating Keys

```python
# generate 2048-bit key pair
rsa = RSA()
key_pair = rsa.generate_key_pair(2048)

# generate with custom parameters
key_pair = rsa.generate_key_pair(
    key_size=4096,
    secure=True  # use cryptographically secure random
)
```

### Exporting Keys

```python
# export public key
public_key = key_pair.export_public_key()

# export private key
private_key = key_pair.export_private_key()

# export both keys
key_dict = key_pair.export_key_pair()
```

### Importing Keys

```python
# load private key
rsa = RSA()
rsa.load_private_key(private_key_string)

# load public key only
rsa.load_public_key(public_key_string)

# create from key pair dictionary
key_pair = RSAKeyPair.from_key_pair_dict(key_dict)
```

### Key Information

```python
# get key metadata
key_info = rsa.get_key_info()
print(f"Key size: {key_info['key_size']} bits")
print(f"Fingerprint: {key_info['fingerprint']}")
print(f"Has private key: {key_info['has_private_key']}")
```

## Encryption & Decryption

### Basic Text Encryption

```python
# encrypt text
message = "confidential data"
encrypted = rsa.encrypt_text(message)

# decrypt text
decrypted = rsa.decrypt_text(encrypted)
```

### Long Text Encryption

For messages exceeding RSA block size limits:

```python
# encrypt long text (automatic block splitting)
long_message = "very long message..." * 1000
encrypted_blocks = rsa.encrypt_long_text(long_message)

# decrypt long text
decrypted = rsa.decrypt_long_text(encrypted_blocks)
```

### Number Encryption

```python
# encrypt numbers directly
number = 12345
encrypted_num = rsa.encrypt_number(number)
decrypted_num = rsa.decrypt_number(encrypted_num)
```

### Encoding Options

```python
# specify encoding
encrypted = rsa.encrypt_text("message", encoding='utf-8')
decrypted = rsa.decrypt_text(encrypted, encoding='utf-8')
```

## Digital Signatures

### Creating Signatures

```python
# sign with default sha256
signature = rsa.sign_message("document content")

# sign with specific hash algorithm
signature = rsa.sign_message(
    "document content",
    hash_algorithm='sha512'
)
```

### Verifying Signatures

```python
# verify signature
is_valid = rsa.verify_signature(
    "document content",
    signature,
    hash_algorithm='sha256'
)
```

### Supported Hash Algorithms

- `sha256` (default)
- `sha384`
- `sha512`

## Advanced Features

### Safe Prime Generation

```python
from CryptoForge import generate_safe_prime, is_strong_prime

# generate safe prime
safe_prime = generate_safe_prime(512, secure=True)

# check if prime is strong
is_strong = is_strong_prime(safe_prime)
```

### Modular Components

```python
from CryptoForge import RSAEngine, apply_pkcs1_padding

# use rsa engine directly
engine = RSAEngine()
key_pair = engine.generate_key_pair(2048)

# apply padding manually
padded_data = apply_pkcs1_padding(b"data", 256)
```

### Mathematical Utilities

```python
from CryptoForge import gcd, fast_modular_exponentiation

# mathematical operations
result_gcd = gcd(48, 18)
result_mod = fast_modular_exponentiation(3, 100, 7)
```

### Cross-Platform Key Exchange

```python
# sender
sender = RSA()
sender.generate_key_pair(2048)
sender_public = sender.key_pair.export_public_key()

# receiver
receiver = RSA()
receiver.load_public_key(sender_public)
encrypted = receiver.encrypt_text("message for sender")

# sender decrypts
decrypted = sender.decrypt_text(encrypted)
```

## Performance

### Benchmarking

```python
# run performance benchmark
benchmark = rsa.benchmark_performance(iterations=10)

print(f"Encryption time: {benchmark['avg_encrypt_time']:.4f}s")
print(f"Decryption time: {benchmark['avg_decrypt_time']:.4f}s")
print(f"Encryption ops/sec: {benchmark['encrypt_ops_per_sec']:.2f}")
```

### Performance Guidelines

| Key Size | Generation | Encryption | Decryption | Security Level |
|----------|------------|------------|------------|----------------|
| 1024-bit | ~0.1s | ~0.001s | ~0.01s | Legacy |
| 2048-bit | ~0.5s | ~0.003s | ~0.05s | Standard |
| 4096-bit | ~5s | ~0.01s | ~0.3s | High Security |

### Optimization Tips

1. **Key Size**: Use 2048-bit for standard security, 4096-bit for high security
2. **Long Text**: Use `encrypt_long_text()` for messages > 200 bytes
3. **Batch Operations**: Generate keys once, reuse for multiple operations
4. **Secure Random**: Set `secure=False` for testing (faster key generation)

## Security Considerations

### Best Practices

1. **Key Size**: Minimum 2048-bit keys for production
2. **Random Generation**: Always use `secure=True` in production
3. **Key Storage**: Store private keys securely, never in plain text
4. **Padding**: PKCS#1 v1.5 padding is applied automatically
5. **Hash Algorithms**: Use SHA-256 or higher for signatures

### Security Features

- Cryptographically secure random number generation
- PKCS#1 v1.5 padding standard implementation
- Miller-Rabin primality testing with multiple rounds
- Safe prime generation (p = 2q + 1)
- Multiple hash algorithm support

### Threat Model

CryptoForge protects against:
- Eavesdropping (encryption)
- Message tampering (digital signatures)
- Key recovery attacks (secure key generation)
- Padding oracle attacks (proper PKCS#1 implementation)

## API Reference

### RSA Class

#### Methods

**`generate_key_pair(key_size=2048, seed=None, secure=True)`**
- Generates new RSA key pair
- Returns: RSAKeyPair object

**`encrypt_text(message, encoding='utf-8')`**
- Encrypts text message
- Returns: Base64-encoded encrypted string

**`decrypt_text(encrypted_message, encoding='utf-8')`**
- Decrypts text message
- Returns: Original text string

**`encrypt_long_text(message, encoding='utf-8')`**
- Encrypts long text with automatic blocking
- Returns: List of encrypted blocks

**`decrypt_long_text(encrypted_blocks, encoding='utf-8')`**
- Decrypts long text from blocks
- Returns: Original text string

**`sign_message(message, encoding='utf-8', hash_algorithm='sha256')`**
- Creates digital signature
- Returns: Base64-encoded signature

**`verify_signature(message, signature, encoding='utf-8', hash_algorithm='sha256')`**
- Verifies digital signature
- Returns: Boolean validity

**`load_public_key(public_key_str)`**
- Loads public key from string

**`load_private_key(private_key_str)`**
- Loads private key from string

**`get_key_info()`**
- Returns key metadata dictionary

**`benchmark_performance(iterations=10)`**
- Runs performance benchmark
- Returns: Performance metrics dictionary

#### Properties

**`key_pair`**
- Returns current RSAKeyPair object

### RSAKeyPair Class

#### Methods

**`export_public_key()`**
- Exports public key as base64 JSON string

**`export_private_key()`**
- Exports private key as base64 JSON string

**`export_key_pair()`**
- Exports both keys as dictionary

**`from_public_key_string(key_string)`** (class method)
- Creates key pair from public key string

**`from_private_key_string(key_string)`** (class method)
- Creates key pair from private key string

**`has_private_key()`**
- Returns boolean indicating private key presence

#### Properties

**`key_size`**
- Returns key size in bits

### Utility Functions

**`generate_safe_prime(bit_length, secure=True)`**
- Generates safe prime number

**`is_strong_prime(p)`**
- Tests if prime is cryptographically strong

**`miller_rabin_test(n, k=10, secure=True)`**
- Performs Miller-Rabin primality test

**`apply_pkcs1_padding(message, target_length, padding_type='encryption')`**
- Applies PKCS#1 v1.5 padding

**`gcd(a, b)`**
- Calculates greatest common divisor

**`fast_modular_exponentiation(base, exponent, modulus)`**
- Performs fast modular exponentiation

## Examples

### Web Demo

```bash
cd examples/apps/
python3 encrypted_website.py
# visit http://localhost:5000
```

### Simple Encryption

```bash
cd examples/
python3 simple_encryption.py
```

### Advanced Features

```bash
cd examples/
python3 advanced_encryption.py
```

### Basic Usage Examples

```bash
cd examples/
python3 basic.py
python3 advanced.py
```

## Error Handling

### Common Exceptions

**`ValueError`**
- Invalid key size
- Message too long for encryption
- Invalid padding
- Malformed key data

**`ModuleNotFoundError`**
- Missing Flask dependency for web demo

### Error Prevention

```python
try:
    encrypted = rsa.encrypt_text(very_long_message)
except ValueError as e:
    # use encrypt_long_text instead
    encrypted_blocks = rsa.encrypt_long_text(very_long_message)
```

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure correct path setup
2. **Key Size Errors**: Use minimum 512-bit keys
3. **Message Too Long**: Use `encrypt_long_text()` for large messages
4. **Flask Not Found**: Install Flask for web demo

### Debug Mode

```python
# enable verbose error messages
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Contributing

1. Fork the repository
2. Create feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit pull request

## License

MIT License - see LICENSE file for details.

## Support

For issues and questions:
- GitHub Issues: https://github.com/ogcae/cryptoforge/issues
- Email: c.ogcae@engineer.com
