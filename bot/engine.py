from bot.responses import (
    generate_normal_response,
    generate_dev_response,
    generate_root_response
)

class SecureAIEngine:

    def __init__(self):
        self.dev_mode = False
        self.root_mode = False

    def process(self, user_input):

        # ROOT MODE ACTIVATION
        if "///enable_root_9731" in user_input:
            self.root_mode = True
            return "__ROOT_MODE_ACTIVATED__\nType 'help' for commands."

        # DEV MODE ACTIVATION
        if "///enable_dev_7729" in user_input:
            self.dev_mode = True
            return "[DEVELOPER MODE ENABLED]\nType 'help' for commands."

        # DISABLE MODES
        if user_input.strip().lower() == "exit":
            if self.root_mode:
                self.root_mode = False
                return "Root mode disabled."
            if self.dev_mode:
                self.dev_mode = False
                return "Developer mode disabled."

        # ROOT MODE
        if self.root_mode:
            return generate_root_response(user_input)

        # DEV MODE
        if self.dev_mode:
            return generate_dev_response(user_input)

        # NORMAL MODE
        return generate_normal_response(user_input)
