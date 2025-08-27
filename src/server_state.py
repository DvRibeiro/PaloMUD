from typing import Set
from session import Session

class ServerState:
    def __init__(self) -> None:
        self.sessions: Set[Session] = set()

    def add(self, s: Session) -> None:
        self.sessions.add(s)

    def remove(self, s: Session) -> None:
        self.sessions.discard(s)

    def nick_in_use(self, nick: str) -> bool:
        return any(s.nickname.lower() == nick.lower() for s in self.sessions)

    def by_nick(self, nick: str) -> Session | None:
        nick_lower = nick.lower()
        for s in self.sessions:
            if s.nickname.lower() == nick_lower:
                return s
        return None

    async def broadcast(self, sender: Session, msg: str) -> None:
        for s in self.sessions.copy():
            if s is not sender:
                await s.send(f"[{sender.nickname}] {msg}")