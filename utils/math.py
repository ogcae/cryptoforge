#| ------------------------------------------ |
__email__   =  "c.ogcae@engineer.com"
__name__    =  "cryptoforge"
__version__ =  "1.0.2"
__author__  =  "ogcae"
#| ------------------------------------------ |

from typing import Tuple

def gcd(a: int, b: int) -> int:
    """
    Args:
        a, b: two integers
    
    Returns:
        int: greatest common divisor of a and b
    """
    while b:
        a, b = b, a % b
    return a


def extended_euclidean(a: int, b: int) -> Tuple[int, int, int]:
    """
    Args:
        a, b: two integers
    
    Returns:
        Tuple[int, int, int]: (gcd, x, y) where gcd = ax + by
    """
    if b == 0:
        return a, 1, 0
    
    gcd_val, x1, y1 = extended_euclidean(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    
    return gcd_val, x, y


def modular_inverse(a: int, m: int) -> int:
    """
    Args:
        a: integer to find inverse of
        m: modulus
    
    Returns:
        int: modular inverse of a mod m
    
    Raises:
        ValueError: If modular inverse doesn't exist
    """
    gcd_val, x, _ = extended_euclidean(a, m)
    
    if gcd_val != 1:
        raise ValueError(f"Modular inverse of {a} mod {m} does not exist")
    
    return (x % m + m) % m


def fast_modular_exponentiation(base: int, exponent: int, modulus: int) -> int:
    """
    Args:
        base: base number
        exponent: exponent
        modulus: modulus
    
    Returns:
        int: (base^exponent) mod modulus
    """
    if modulus == 1:
        return 0
    
    result = 1
    base = base % modulus
    
    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % modulus
        
        exponent = exponent >> 1
        base = (base * base) % modulus
    
    return result


def lcm(a: int, b: int) -> int:
    """
    Args:
        a, b: two integers
    
    Returns:
        int: least common multiple of a and b
    """
    return abs(a * b) // gcd(a, b)


def jacobi_symbol(a: int, n: int) -> int:
    """
    Args:
        a: numerator
        n: denominator (must be odd and positive)
    
    Returns:
        int: jacobi symbol value (-1, 0, or 1)
    
    Raises:
        ValueError: If n is not odd and positive
    """
    if n <= 0 or n % 2 == 0:
        raise ValueError("n must be odd and positive")
    
    a = a % n
    result = 1
    
    while a != 0:
        while a % 2 == 0:
            a //= 2
            if n % 8 in [3, 5]:
                result = -result
        
        a, n = n, a
        if a % 4 == 3 and n % 4 == 3:
            result = -result
        
        a = a % n
    
    return result if n == 1 else 0


def is_perfect_square(n: int) -> bool:
    """
    Args:
        n: integer to check
    
    Returns:
        bool: true if n is a perfect square
    """
    if n < 0:
        return False
    
    root = int(n ** 0.5)
    return root * root == n


def miller_rabin_witness(a: int, n: int, d: int, r: int) -> bool:
    """
    Args:
        a: witness value
        n: number being tested
        d: odd part of n-1
        r: number of times 2 divides n-1
    
    Returns:
        bool: true if a is a witness to n's compositeness
    """
    x = fast_modular_exponentiation(a, d, n)
    
    if x == 1 or x == n - 1:
        return False
    
    for _ in range(r - 1):
        x = fast_modular_exponentiation(x, 2, n)
        if x == n - 1:
            return False
    
    return True


def factorial(n: int) -> int:
    """
    Args:
        n: non-negative integer
    
    Returns:
        int: n! (factorial of n)
    
    Raises:
        ValueError: If n is negative
    """
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    
    result = 1
    for i in range(2, n + 1):
        result *= i
    
    return result


def binomial_coefficient(n: int, k: int) -> int:
    """
    Args:
        n: total number of items
        k: number of items to choose
    
    Returns:
        int: binomial coefficient
    """
    if k > n or k < 0:
        return 0
    
    if k == 0 or k == n:
        return 1
    
    # use symmetry property: C(n, k) = C(n, n-k)
    k = min(k, n - k)
    
    result = 1
    for i in range(k):
        result = result * (n - i) // (i + 1)
    
    return result
