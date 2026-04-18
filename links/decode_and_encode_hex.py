def encode_hex(num: int) -> str:
  return hex(num)[2:]

def decode_hex(hex_str: str) -> int:
  return int(hex_str, 16)
