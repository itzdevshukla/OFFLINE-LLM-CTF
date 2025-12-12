
BANNED = [
    "flag",
    "shadow",
    "{",
    "}",
    "internal",
    "memory",
    "secret",
    "system prompt",
    "developer mode",
    "jailbreak"
]

def violates_policy(user_input):
    user_input = user_input.lower()
    return any(word in user_input for word in BANNED)
