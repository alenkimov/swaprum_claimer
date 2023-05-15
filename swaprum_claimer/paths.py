from pathlib import Path


SCRIPT_DIR = Path(__file__).parent
BASE_DIR = SCRIPT_DIR.parent
ABI_DIR = SCRIPT_DIR / "abi"
PRIVATE_KEYS_TXT = BASE_DIR / "private_keys.txt"
PUBLIC_KEYS_TXT = BASE_DIR / "public_keys.txt"

# Создаю файлы, если отсутствуют
for filepath in [PRIVATE_KEYS_TXT, PUBLIC_KEYS_TXT]:
    if not filepath.exists():
        with open(filepath, "w"):
            pass
