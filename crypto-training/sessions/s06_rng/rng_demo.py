#!/usr/bin/env python3
import os, random

print('os.urandom(8):', os.urandom(8).hex())
print('os.urandom(8):', os.urandom(8).hex())

# Broken: predictable PRNG
random.seed(0)
print('random.random():', random.random())
print('random.random():', random.random())

print('\nLesson: use os.urandom / secrets, not random.seed for security-sensitive values.')
