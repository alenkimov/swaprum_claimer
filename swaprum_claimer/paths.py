from pathlib import Path


SCRIPT_DIR = Path(__file__).parent
BASE_DIR = SCRIPT_DIR.parent
ABI_DIR = SCRIPT_DIR / "abi"
OUTPUT_DIR = BASE_DIR / "output"
PRIVATE_KEYS_TXT = BASE_DIR / "private_keys.txt"
PUBLIC_KEYS_TXT = BASE_DIR / "public_keys.txt"
