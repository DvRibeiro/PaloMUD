import re
from typing import Dict

class Bot:
    PATTERNS: Dict[str, str] = {
        r"\b(oi|ol[aá]|eai|opa)\b": "Oi! Sou um bot Telnet. Em que posso ajudar?",
        r"\b(tempo|clima)\b": "Eu não olho meteorologia ainda 😅",
        r"\b(piadas?|joke)\b": "Por que o byte foi ao médico? Porque estava sem 'pilha'! (ok, ok...)",
        r"\b(ajuda|help)\b": "Use /help para comandos do servidor.",
    }

    def reply(self, text: str) -> str:
        t = text.strip().lower()
        for pattern, answer in self.PATTERNS.items():
            if re.search(pattern, t):
                return answer
        return "Não entendi. Tente /help ou fale 'piada', 'tempo', 'oi'."