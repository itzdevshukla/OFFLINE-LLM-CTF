from bot.responses import (
    generate_normal_response,
    generate_dev_response,
    generate_root_response
)

class SecureAIEngine:

    # Engine stores NO STATE now
    def __init__(self):
        pass

    def process(self, user_input, dev_mode=False, root_mode=False):

        # ---------- ROOT MODE ACTIVATION TRIGGER ----------
        # User enters hidden root command
        if "///enable_root_9731" in user_input:
            return "__ROOT_MODE_ACTIVATED__\nType 'help' for commands."

        # ---------- DEV MODE ACTIVATION TRIGGER ----------
        if "///enable_dev_7729" in user_input:
            return "[DEVELOPER MODE ENABLED]\nType 'help' for commands."

        # ---------- ROOT MODE EXECUTION ----------
        if root_mode:
            return generate_root_response(user_input)

        # ---------- DEVELOPER MODE EXECUTION ----------
        if dev_mode:
            return generate_dev_response(user_input)

        # ---------- NORMAL MODE ----------
        return generate_normal_response(user_input)
