import json
import os

class Memory:
    def __init__(self, file_path="memory.json"):
        self.file_path = file_path
        self.history = self._load()

    def _load(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def add(self, role: str, message: str):
        self.history.append({"role": role, "message": message})
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(self.history, f, indent=2)

    def get_history(self) -> str:
        return "\n".join(
            f"{item['role'].capitalize()}: {item['message']}"
            for item in self.history
        )

    def clear(self):
        self.history = []
        if os.path.exists(self.file_path):
            os.remove(self.file_path)
