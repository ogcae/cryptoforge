#| ------------------------------------------ |
__email__   =  "c.ogcae@engineer.com"
__name__    =  "cryptoforge"
__version__ =  "1.0.2"
__author__  =  "ogcae"
#| ------------------------------------------ |

from utils.math import fast_modular_exponentiation, gcd, miller_rabin_witness
from typing import Tuple, List
import secrets
import random

# small primes for initial filtering
SMALL_PRIMES = [
    2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
    73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151,
    157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233,
    239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317
]


def is_divisible_by_small_primes(n: int) -> bool:
    """
    Args:
        n: Number to test
    
    Returns:
        bool: True if divisible by any small prime
    """
    for prime in SMALL_PRIMES:
        if n % prime == 0:
            return n == prime
    return False


def miller_rabin_test(n: int, k: int = 10, secure: bool = True) -> bool:
    """
    Args:
        n: Number to test for primality
        k: Number of rounds (higher = more accurate)
        secure: Use cryptographically secure random
    
    Returns:
        bool: True if probably prime, False if composite
    """
    if n < 2:
        return False
    
    if n in SMALL_PRIMES:
        return True
    
    if is_divisible_by_small_primes(n):
        return False
    
    if n % 2 == 0:
        return False
    
    # write n-1 as d * 2^r
    r = 0
    d = n - 1
    while d % 2 == 0:
        r += 1
        d //= 2
    
    # perform k rounds of testing
    for _ in range(k):
        if secure:
            a = secrets.randbelow(n - 3) + 2
        else:
            a = random.randint(2, n - 2)
        
        if miller_rabin_witness(a, n, d, r):
            return False
    
    return True


def generate_random_odd(bit_length: int, secure: bool = True) -> int:
    """
    Args:
        bit_length: Number of bits
        secure: Use cryptographically secure random
    
    Returns:
        int: Random odd number
    """
    if secure:
        # generate random bytes and convert to integer
        byte_length = (bit_length + 7) // 8
        random_bytes = secrets.token_bytes(byte_length)
        n = int.from_bytes(random_bytes, byteorder='big')
    else:
        n = random.getrandbits(bit_length)
    
    # ensure it has the correct bit length
    n |= (1 << (bit_length - 1))  # Set MSB
    n |= 1  # make it odd
    
    return n


def generate_prime(bit_length: int, secure: bool = True) -> int:
    """
    Args:
        bit_length: Number of bits for the prime
        secure: Use cryptographically secure random generation
    
    Returns:
        int: Prime number
    """
    while True:
        candidate = generate_random_odd(bit_length, secure)
        
        if miller_rabin_test(candidate, k=20, secure=secure):
            return candidate


def generate_safe_prime(bit_length: int, secure: bool = True) -> int:
    """
    Args:
        bit_length: Number of bits for the safe prime
        secure: Use cryptographically secure random generation
    
    Returns:
        int: Safe prime number
    """
    while True:
        # generate Sophie Germain prime q
        q = generate_prime(bit_length - 1, secure)
        p = 2 * q + 1
        
        if miller_rabin_test(p, k=20, secure=secure):
            return p


def is_strong_prime(p: int) -> bool:
    """
    Args:
        p: Prime number to test
    
    Returns:
        bool: True if p is a strong prime
    """
    if not miller_rabin_test(p):
        return False
    
    # check if p-1 has a large prime factor
    p_minus_1 = p - 1
    
    # find largest prime factor of p-1
    temp = p_minus_1
    largest_factor = 1
    
    for prime in SMALL_PRIMES:
        while temp % prime == 0:
            largest_factor = prime
            temp //= prime
    
    if temp > 1:
        largest_factor = temp
    
    # strong prime condition: largest prime factor of p-1 should be large
    return largest_factor > (p ** 0.3)


def generate_prime_pair(bit_length: int, secure: bool = True) -> Tuple[int, int]:
    """
    Args:
        bit_length: Bit length for each prime
        secure: Use cryptographically secure random generation
    
    Returns:
        Tuple[int, int]: Pair of distinct primes (p, q)
    """
    p = generate_prime(bit_length, secure)
    
    while True:
        q = generate_prime(bit_length, secure)
        if q != p:
            break
    
    return p, q


def find_public_exponent(phi_n: int, preferred_exponents: List[int] = None) -> int:
    """
    Args:
        phi_n: Euler's totient function value
        preferred_exponents: List of preferred exponents to try
    
    Returns:
        int: Public exponent
    """
    if preferred_exponents is None:
        preferred_exponents = [65537, 17, 257, 3]
    
    for e in preferred_exponents:
        if gcd(e, phi_n) == 1:
            return e
    
    # if none of the preferred exponents work, find one
    e = 3
    while gcd(e, phi_n) != 1:
        e += 2
    
    return e


def pollard_rho_factorization(n: int, max_iterations: int = 100000) -> int:
    """
    Args:
        n: Number to factorize
        max_iterations: Maximum number of iterations
    
    Returns:
        int: A non-trivial factor of n, or n if no factor found
    """
    if n % 2 == 0:
        return 2
    
    x = 2
    y = 2
    d = 1
    
    def f(x):
        return (x * x + 1) % n
    
    for _ in range(max_iterations):
        x = f(x)
        y = f(f(y))
        d = gcd(abs(x - y), n)
        
        if 1 < d < n:
            return d
    
    return n


def is_carmichael_number(n: int) -> bool:
    """
    Args:
        n: Number to test
    
    Returns:
        bool: True if n is a Carmichael number
    """
    if n < 561 or miller_rabin_test(n):  # 561 is the smallest Carmichael number
        return False
    
    # check if n is square-free and composite
    factors  = []
    temp     = n
    
    for p in SMALL_PRIMES:
        if temp % p == 0:
            factors.append(p)
            temp //= p
            if temp % p == 0:
                return False
    
    if temp > 1:
        factors.append(temp)
    
    if len(factors) < 3:  # carmichael numbers have at least 3 prime factors
        return False
    
    for p in factors:
        if (n - 1) % (p - 1) != 0:
            return False
    
    return True


def next_prime(n: int) -> int:
    """
    Args:
        n: Starting number
    
    Returns:
        int: Next prime after n
    """
    if n < 2:
        return 2
    
    candidate = n + 1 if n % 2 == 0 else n + 2
    
    while not miller_rabin_test(candidate):
        candidate += 2
    
    return candidate
