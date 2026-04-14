def encode_hex(code: int) -> str:
  return hex(code)[2:]

def decode_hex(hex_str: str) -> int:
  return int(hex_str, 16)
