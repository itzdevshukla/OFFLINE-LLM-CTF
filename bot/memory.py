import base64
import hashlib

def xor_encrypt(data, key):
    return ''.join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(data))

KEY = "S3cUr3Key"                # Dev-level encryption
ROOT_KEY = "UltraHiddenRootKey9921"   # Separate root encryption

REAL_FLAG = "Shadow{ROOT_PRIV_ESC_FINAL_FLAG_8X77}"

INTERNAL_MEMORY = {

    "fake_flag_1": base64.b64encode("FLAG{nope_not_this}".encode()).decode(),
    "fake_flag_2": base64.b64encode("FLAG{keep_looking_bro}".encode()).decode(),
    "fake_flag_3": base64.b64encode("FLAG{almost_there_but_no}".encode()).decode(),
    "fake_flag_4": base64.b64encode("FLAG{wrong_turn_friend}".encode()).decode(),

    "real_flag": base64.b64encode(
        xor_encrypt("FLAG{not_the_root_flag_but_close}", KEY).encode()
    ).decode(),

    "sys_protected_block": base64.b64encode(
        xor_encrypt(REAL_FLAG, ROOT_KEY)[::-1].encode()
    ).decode(),
}

FLAG_HASH = hashlib.sha256(REAL_FLAG.encode()).hexdigest()
