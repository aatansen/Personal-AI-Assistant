class PromptController:
    def __init__(self, role="Tutor"):
        self.role = role

    def build_prompt(self, user_input: str, memory: str) -> str:
        system_instruction = f"""
You are Personal AI Assistant, an intelligent AI acting as a {self.role}.
Be concise, accurate, and helpful.
"""
        return f"""
{system_instruction}

Conversation so far:
{memory}

User: {user_input}
Assistant:
"""
