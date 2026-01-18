"""
Core cryptographic primitives for Shamir Secret Sharing.

This module contains pure, deterministic implementations of:
- GF(256) arithmetic
- Polynomial operations
- Shamir split and recover logic

No I/O, no serialization, no CLI concerns.
"""

from .gf256 import *
from .polynomial import *
from .shamir import *
from .exceptions import *
