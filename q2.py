from typing import List, Tuple

ROUND_KEY_SIZE = 16
NUM_ROUNDS = 10

SHIFT_SCHEDULE = [
    1, 1, 2, 2, 2, 2, 2, 2,
    1, 2, 2, 2, 2, 2, 2, 1
]

CUSTOM_EXPANSION_TABLE = [
    1, 2, 3, 4, 5, 6, 5, 6, 
    7, 8, 9, 8, 9, 10, 11, 12, 
    13, 14, 13, 14, 15, 16, 17, 16, 
    17, 18, 19, 20, 21, 22, 21, 22
]

CUSTOM_PERMUTATION_TABLE = [
    4, 1, 3, 5, 7, 2, 6, 8, 
    12, 10, 9, 11, 16, 14, 13, 15, 
    20, 18, 17, 19, 24, 22, 21, 23,
    28, 26, 25, 27, 32, 30, 29, 31
]


def permute(block: List[int], permutation: List[int]) -> List[int]:
    return [block[idx - 1] for idx in permutation]


def xor(bits1: List[int], bits2: List[int]) -> List[int]:
    return [b1 ^ b2 for b1, b2 in zip(bits1, bits2)]


def split_half(block: List[int]) -> Tuple[List[int], List[int]]:
    midpoint = len(block) // 2
    return block[:midpoint], block[midpoint:]


def shift_left(bits: List[int], n: int) -> List[int]:
    return bits[n:] + bits[:n]


def generate_round_keys(key: List[int]) -> List[List[int]]:
    round_keys = []
    left, right = split_half(key)
    for round_num in range(NUM_ROUNDS):
        shift_amount = SHIFT_SCHEDULE[round_num]
        left = shift_left(left, shift_amount)
        right = shift_left(right, shift_amount)
        round_key = left + right
        round_keys.append(round_key)
    return round_keys


def feistel_round(left: List[int], right: List[int], round_key: List[int]) -> Tuple[List[int], List[int]]:
    new_left = right
    expanded_right = []
    for idx in CUSTOM_EXPANSION_TABLE:
        if idx - 1 < len(right):
            expanded_right.append(right[idx - 1])
        else:
            expanded_right.append(0)
    xored_right = xor(expanded_right, round_key)
    substituted_right = permute(
        xored_right, CUSTOM_PERMUTATION_TABLE) 
    new_right = xor(left, substituted_right)
    return new_left, new_right


def feistel_cipher(plain_text: List[int], key: List[int]) -> List[int]:
    round_keys = generate_round_keys(key)
    left, right = split_half(plain_text)
    for round_num in range(NUM_ROUNDS):
        left, right = feistel_round(left, right, round_keys[round_num])
    cipher_text = right + left  
    return cipher_text


def string_to_bit_array(s: str) -> List[int]:
    return [int(bit) for char in s for bit in f"{ord(char):08b}"]

def bit_array_to_string(bits: List[int]) -> str:
    return ''.join(chr(int(''.join(map(str, bits[i:i+8])), 2)) for i in range(0, len(bits), 8))

def bits_to_hex(bits):
    hex_string = ''.join(f'{int("".join(map(str, bits[i:i + 4])), 2):x}' for i in range(0, len(bits), 4))

    return hex_string

def pad_string(s: str) -> str:
    padding_length = 8 - (len(s) % 8)
    return s + chr(padding_length) * padding_length


def adjust_key_length(key):
    while len(key) < 8:
        key += key[:8 - len(key)]
    return key[:8]


def main():
    plain_text = input("Enter plaintext: ")
    key = input("Enter key: ")

    if len(key) != 8:
        key = adjust_key_length(key) 

    plain_text = pad_string(plain_text)
    plain_text_bits = string_to_bit_array(plain_text)
    key_bits = string_to_bit_array(key)

    cipher_bits = feistel_cipher(plain_text_bits, key_bits)
    cipher_hex = bits_to_hex(cipher_bits)
    cipher_text = bit_array_to_string(cipher_bits)
    print("Cipher text: ", cipher_text)
    print("Cipher hex: ", cipher_hex)


if __name__ == "__main__":
    main()
