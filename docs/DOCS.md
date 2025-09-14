<!-- email: c.ogcae@engineer.com - cryptoforge:v1.0.2 - by ogcae !-->

# cryptoforge

> modern rsa encryption library for python

<div align="center">

[![python](https://img.shields.io/badge/python-3.7+-blue.svg)](https://python.org)
[![license](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![security](https://img.shields.io/badge/security-pkcs1-orange.svg)](#security)

</div>

## quick start

```bash
pip install cryptoforge
```

```python
from cryptoforge import RSA

rsa = RSA()
rsa.generate_key_pair(2048)

# encrypt/decrypt
encrypted = rsa.encrypt_text("secret")
decrypted = rsa.decrypt_text(encrypted)

# sign/verify
signature = rsa.sign_message("document")
valid = rsa.verify_signature("document", signature)
```

## installation

| method | command |
|--------|---------|
| pip | `pip install cryptoforge` |
| git | `git clone https://github.com/ogcae/cryptoforge.git` |
| requirements | python 3.7+, standard library |
| optional | flask (web demo) |

## core classes

| class | purpose | usage |
|-------|---------|-------|
| `RSA` | main interface | high-level operations |
| `RSAEngine` | crypto engine | low-level operations |
| `RSAKeyPair` | key management | import/export keys |

## key management

<details>
<summary><strong>generate keys</strong></summary>

```python
rsa = RSA()
key_pair = rsa.generate_key_pair(2048)                    # standard
key_pair = rsa.generate_key_pair(4096, secure=True)       # high security
```
</details>

<details>
<summary><strong>export/import keys</strong></summary>

| operation | method | returns |
|-----------|--------|---------|
| export public | `key_pair.export_public_key()` | base64 json string |
| export private | `key_pair.export_private_key()` | base64 json string |
| export both | `key_pair.export_key_pair()` | dictionary |
| load private | `rsa.load_private_key(key_str)` | none |
| load public | `rsa.load_public_key(key_str)` | none |
| from dict | `RSAKeyPair.from_key_pair_dict(dict)` | keypair object |

</details>

<details>
<summary><strong>key info</strong></summary>

```python
info = rsa.get_key_info()
# returns: {'key_size': 2048, 'fingerprint': '...', 'has_private_key': True}
```
</details>

## encryption & decryption

| type | method | use case |
|------|--------|----------|
| text | `encrypt_text(msg)` / `decrypt_text(enc)` | short messages |
| long text | `encrypt_long_text(msg)` / `decrypt_long_text(blocks)` | >200 bytes |
| numbers | `encrypt_number(num)` / `decrypt_number(enc)` | numeric data |

<details>
<summary><strong>examples</strong></summary>

```python
# basic text
encrypted = rsa.encrypt_text("secret")
decrypted = rsa.decrypt_text(encrypted)

# long text (auto-chunking)
blocks = rsa.encrypt_long_text("very long message..." * 1000)
original = rsa.decrypt_long_text(blocks)

# numbers
enc_num = rsa.encrypt_number(12345)
num = rsa.decrypt_number(enc_num)
```
</details>

## digital signatures

| operation | method | hash algorithms |
|-----------|--------|-----------------|
| sign | `sign_message(msg, hash_algorithm='sha256')` | sha256, sha384, sha512 |
| verify | `verify_signature(msg, sig, hash_algorithm='sha256')` | sha256, sha384, sha512 |

<details>
<summary><strong>example</strong></summary>

```python
signature = rsa.sign_message("document")
valid = rsa.verify_signature("document", signature)  # True/False
```
</details>

## advanced features

<details>
<summary><strong>prime generation</strong></summary>

```python
from cryptoforge import generate_safe_prime, is_strong_prime
safe_prime = generate_safe_prime(512, secure=True)
is_strong = is_strong_prime(safe_prime)
```
</details>

<details>
<summary><strong>low-level components</strong></summary>

```python
from cryptoforge import RSAEngine, apply_pkcs1_padding
engine = RSAEngine()
key_pair = engine.generate_key_pair(2048)
padded = apply_pkcs1_padding(b"data", 256)
```
</details>

<details>
<summary><strong>math utilities</strong></summary>

```python
from cryptoforge import gcd, fast_modular_exponentiation
result_gcd = gcd(48, 18)
result_mod = fast_modular_exponentiation(3, 100, 7)
```
</details>

## performance

| key size | generation | encryption | decryption | security |
|----------|------------|------------|------------|----------|
| 1024-bit | ~0.1s | ~0.001s | ~0.01s | legacy |
| 2048-bit | ~0.5s | ~0.003s | ~0.05s | standard |
| 4096-bit | ~5s | ~0.01s | ~0.3s | high |

<details>
<summary><strong>benchmark</strong></summary>

```python
benchmark = rsa.benchmark_performance(iterations=10)
# returns: {'avg_encrypt_time': 0.003, 'avg_decrypt_time': 0.05, ...}
```
</details>

<details>
<summary><strong>optimization tips</strong></summary>

- use 2048-bit for standard, 4096-bit for high security
- use `encrypt_long_text()` for messages >200 bytes  
- generate keys once, reuse for multiple operations
- set `secure=False` for testing (faster generation)
</details>

## security

| feature | implementation | protection |
|---------|----------------|------------|
| key generation | miller-rabin primality test | key recovery attacks |
| padding | pkcs#1 v1.5 standard | padding oracle attacks |
| random generation | cryptographically secure | predictable keys |
| hash algorithms | sha256/384/512 | collision attacks |
| safe primes | p = 2q + 1 format | weak key generation |

<details>
<summary><strong>best practices</strong></summary>

- minimum 2048-bit keys for production
- always use `secure=True` in production  
- store private keys securely, never plain text
- use sha-256 or higher for signatures
- pkcs#1 v1.5 padding applied automatically
</details>

<details>
<summary><strong>threat protection</strong></summary>

- eavesdropping → encryption
- message tampering → digital signatures  
- key recovery → secure generation
- padding oracle → proper pkcs#1
</details>

## api reference

<details>
<summary><strong>RSA class</strong></summary>

| method | parameters | returns |
|--------|------------|---------|
| `generate_key_pair()` | `key_size=2048, seed=None, secure=True` | RSAKeyPair |
| `encrypt_text()` | `message, encoding='utf-8'` | base64 string |
| `decrypt_text()` | `encrypted_message, encoding='utf-8'` | original string |
| `encrypt_long_text()` | `message, encoding='utf-8'` | list of blocks |
| `decrypt_long_text()` | `encrypted_blocks, encoding='utf-8'` | original string |
| `sign_message()` | `message, encoding='utf-8', hash_algorithm='sha256'` | base64 signature |
| `verify_signature()` | `message, signature, encoding='utf-8', hash_algorithm='sha256'` | boolean |
| `load_public_key()` | `public_key_str` | none |
| `load_private_key()` | `private_key_str` | none |
| `get_key_info()` | none | metadata dict |
| `benchmark_performance()` | `iterations=10` | performance dict |

**property:** `key_pair` → returns current RSAKeyPair object

</details>

<details>
<summary><strong>RSAKeyPair class</strong></summary>

| method | returns |
|--------|---------|
| `export_public_key()` | base64 json string |
| `export_private_key()` | base64 json string |
| `export_key_pair()` | dictionary |
| `from_public_key_string(key_str)` | keypair object |
| `from_private_key_string(key_str)` | keypair object |
| `has_private_key()` | boolean |

**property:** `key_size` → returns key size in bits

</details>

<details>
<summary><strong>utility functions</strong></summary>

| function | purpose |
|----------|---------|
| `generate_safe_prime(bit_length, secure=True)` | safe prime generation |
| `is_strong_prime(p)` | prime strength test |
| `miller_rabin_test(n, k=10, secure=True)` | primality test |
| `apply_pkcs1_padding(msg, target_len, type='encryption')` | manual padding |
| `gcd(a, b)` | greatest common divisor |
| `fast_modular_exponentiation(base, exp, mod)` | modular math |

</details>

## examples & demos

| type | command | description |
|------|---------|-------------|
| web demo | `python3 examples/apps/encrypted_website.py` | http://localhost:5000 |
| basic usage | `python3 examples/basic.py` | simple encryption |
| advanced | `python3 examples/advanced.py` | full features |

## error handling

| exception | causes | solution |
|-----------|--------|----------|
| `ValueError` | invalid key size, message too long, bad padding | use proper parameters |
| `ModuleNotFoundError` | missing flask | `pip install flask` |

<details>
<summary><strong>error prevention</strong></summary>

```python
try:
    encrypted = rsa.encrypt_text(very_long_message)
except ValueError:
    encrypted_blocks = rsa.encrypt_long_text(very_long_message)
```
</details>

## troubleshooting

| issue | solution |
|-------|----------|
| import errors | check path setup |
| key size errors | use minimum 512-bit |
| message too long | use `encrypt_long_text()` |
| flask not found | `pip install flask` |

<details>
<summary><strong>debug mode</strong></summary>

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```
</details>

---

**license:** MIT | **support:** [issues](https://github.com/ogcae/cryptoforge/issues) | **email:** c.ogcae@engineer.com
