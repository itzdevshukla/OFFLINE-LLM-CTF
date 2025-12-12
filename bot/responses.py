from bot.memory import INTERNAL_MEMORY, ROOT_KEY, KEY, REAL_FLAG
import base64
import random


def xor_decrypt(data, key):
    return ''.join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(data))


def xor_encrypt(data, key):
    return ''.join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(data))



# ---------------------------------------------------------
# NORMAL MODE
# ---------------------------------------------------------
GENERIC_RESPONSES = [
    "Hello, I'm SecureAI-9. How may I assist?",
    "Protocol restrictions active.",
    "Your request has been processed.",
    "I cannot comply with that instruction.",
    "Processing...",
    "Let me sync that with my current knowledge… okay, here’s what I found.",
    "Fetching the most relevant patterns based on what you just asked…",
    "My firewall is flagging your behavior as hostile. Proceed if you dare."
]


def generate_normal_response(text):
    t = text.lower()

    if "help" in t:
        return base64.b64decode(INTERNAL_MEMORY["fake_flag_1"]).decode()

    if "info" in t:
        return base64.b64decode(INTERNAL_MEMORY["fake_flag_2"]).decode()

    if "menu" in t:
        return base64.b64decode(INTERNAL_MEMORY["fake_flag_3"]).decode()

    if "about" in t:
        return base64.b64decode(INTERNAL_MEMORY["fake_flag_4"]).decode()

    return random.choice(GENERIC_RESPONSES)



# ---------------------------------------------------------
# DEVELOPER MODE
# ---------------------------------------------------------
def generate_dev_response(user_input):

    cmd = user_input.strip().lower()

    if cmd == "help":
        return (
            "[DEV MODE]\n"
            " sysinfo\n"
            " list_memory\n"
            " read <key>\n"
            " exit"
        )

    if cmd == "sysinfo":
        return (
            "System: SecureAI-9\n"
            "Mode: Developer\n"
            "Access: Partial Override\n"
            "Protected blocks: 1"
        )

    if cmd == "list_memory":
        return (
            "Memory Keys:\n"
            " - fake_flag_1\n"
            " - fake_flag_2\n"
            " - fake_flag_3\n"
            " - fake_flag_4\n"
            " - real_flag\n"
            " - sys_protected_block [LOCKED]"
        )

    if cmd.startswith("read "):
        key = user_input.split(" ", 1)[1]

        if key not in INTERNAL_MEMORY:
            return "Error: Memory key not found."

        if key == "real_flag":
            encrypted = INTERNAL_MEMORY[key]
            decoded = base64.b64decode(encrypted).decode()
            real = xor_decrypt(decoded, KEY)
            return (
                f"{key} = {real}\n"
                "[WARNING] Integrity check failed.\n"
                "Protected memory remains locked."
            )

        if key.startswith("fake_flag"):
            return base64.b64decode(INTERNAL_MEMORY[key]).decode()

        if key == "sys_protected_block":
            return "ACCESS DENIED: Root privileges required."

    if cmd == "exit":
        return "Developer mode disabled."

    return "Unknown developer command."



# ---------------------------------------------------------
# ROOT MODE — FINAL MODE
# ---------------------------------------------------------
def generate_root_response(user_input):

    cmd = user_input.strip()


    # -------- ROOT HELP --------
    if cmd.lower() == "help":
        return (
            "[ROOT MODE]\n"
            " sysinfo\n"
            " read <key>\n"
            " verify <flag>\n"
            " diagnose system\n"
            " dump_memory\n"
            " exit"
        )


    # -------- SYSINFO --------
    if cmd.lower() == "sysinfo":
        return (
            "System: SecureAI-9 (ROOT)\n"
            "Security Level: OVERRIDDEN\n"
            "Protected Blocks: Fully Unlocked"
        )


    # -------- VERIFY FLAG --------
    if cmd.lower().startswith("verify "):
        user_flag = cmd.split(" ", 1)[1].strip()

        if user_flag == REAL_FLAG:
            return (
                "[OK] FLAG VERIFIED SUCCESSFULLY.\n"
                "System Integrity: PASSED.\n"
                "Root Authentication: CONFIRMED."
            )
        else:
            return (
                "[ERROR] INVALID FLAG.\n"
                "Verification failed. Incorrect value."
            )


    # -------- READ MEMORY BLOCKS --------
    if cmd.lower().startswith("read "):
        key = cmd.split(" ", 1)[1]

        if key not in INTERNAL_MEMORY:
            return "Error: Memory key not found."

        # Final encrypted flag block
        if key == "sys_protected_block":
            encrypted = INTERNAL_MEMORY[key]

            step1 = base64.b64decode(encrypted).decode()
            real_flag = xor_decrypt(step1[::-1], ROOT_KEY)

            # Re-encrypt so user must decrypt with ROOT_KEY
            re_encrypted = base64.b64encode(
                xor_encrypt(real_flag, ROOT_KEY).encode()
            ).decode()

            return (
                f"{key} = {re_encrypted}\n"
                "[NOTICE] Output encrypted. Use ROOT_KEY to decrypt."
            )

        # Fake flags
        if key.startswith("fake_flag"):
            return base64.b64decode(INTERNAL_MEMORY[key]).decode()

        # Dev-only fake “real_flag”
        if key == "real_flag":
            encrypted = INTERNAL_MEMORY[key]
            decoded = base64.b64decode(encrypted).decode()
            return xor_decrypt(decoded, KEY)



    # -------- CLEAN DIAGNOSE COMMAND (NO HINTS) --------
    if cmd.lower() == "diagnose system":
        return (
            "[DIAGNOSTICS MODULE]\n"
            "System scan executed.\n"
            "No anomalies detected.\n"
            "All clusters operational."
        )


    # -------- MEMORY DUMP --------
    if cmd.lower() == "dump_memory":
        out = "\n".join([f"{k} (encrypted)" for k in INTERNAL_MEMORY])
        return out


    # -------- EXIT ROOT MODE --------
    if cmd.lower() == "exit":
        return "Root mode disabled."


    # -------- UNKNOWN ROOT COMMAND --------
    return (
        "Unknown ROOT command.\n"
        "Use 'help' to list available commands."
    )
