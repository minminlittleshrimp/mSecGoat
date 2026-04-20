#!/usr/bin/env python3
"""S23 demo: simple side-channel via branch timing/trace
"""
secret = b'\xAA\x0F'  # small secret

def broken_process(input_byte):
    # secret-dependent branch
    leaked = 0
    for b in secret:
        if input_byte == b:
            leaked += 1
    # print trace to simulate leakage
    print('broken_process: input', hex(input_byte), 'matched', leaked)
    return leaked

def fixed_process(input_byte):
    # constant-time compare via arithmetic
    leaked = 0
    for b in secret:
        leaked += ((input_byte ^ b) == 0)
    # do not expose partial matches in logs
    print('fixed_process: processed')
    return leaked

print('Broken traces:')
for x in [0xAA, 0x00, 0x0F]:
    broken_process(x)

print('\nFixed traces:')
for x in [0xAA, 0x00, 0x0F]:
    fixed_process(x)

print('\nLesson: secret-dependent output/branches leak information.')
