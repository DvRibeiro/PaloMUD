from session import Session
from server_state import ServerState

class CMDUtil:
    def __init__(self, server: ServerState) -> None:
        self.server = server
        self.COMMANDS = {
            "help": self.cmd_help,
            "nick": self.cmd_nick,
            "say": self.cmd_say,
            "who": self.cmd_who,
            "whisper": self.cmd_whisper,
            "quit": self.cmd_quit,
        }

    async def handle_command(self, session: Session, line: str) -> None:        
        parts = line[1:].split()  # remove '/'
        if not parts:
            await session.send("Digite /help para ajuda.")
            return
        cmd, args = parts[0].lower(), parts[1:]
        handler = self.COMMANDS.get(cmd)
        if not handler:
            await session.send("Comando desconhecido. Tente /help.")
            return
        await handler(session, args)   

    async def cmd_help(self, session: Session, args: list[str]) -> None:
        await session.send("Comandos:")
        for command in [
            "/help                      - este menu.",
            "/nick <nome>               - muda seu apelido",
            "/say <mensagem>            - fala com todos",
            "/who                       - lista conectados",
            "/whisper <alvo> <mensagem> - sussurra para alguém",
            "/quit                      - sai",
        ]:
            await session.send(command)

    async def cmd_nick(self, session: Session, args: list[str]) -> None:
        if not args:
            await session.send("Uso: /nick <nome>")
            return
        new = args[0][:32]
        if self.server.nick_in_use(new):
            await session.send("Esse nick já está em uso.")
            return
        old = session.nickname
        session.nickname = new
        await session.send(f"Você agora é '{new}'.")
        await self.server.broadcast(session, f"{old} agora é {new}.")
        print(f">> [NICK_CHANGE] de {old} para {new}.")

    async def cmd_say(self, session: Session, args: list[str]) -> None:
        if not args:
            await session.send("Uso: /say <mensagem>")
            return
        await self.server.broadcast(session, " ".join(args))

    async def cmd_who(self, session: Session, args: list[str]) -> None:
        nicks = sorted(s.nickname for s in self.server.sessions)
        await session.send(f"Conectados ({len(nicks)}): " + ", ".join(nicks))

    async def cmd_whisper(self, session: Session, args: list[str]) -> None:
        if len(args) < 2:
            await session.send("Uso: /whisper <alvo> <mensagem>")
            return
        target_nick, message = args[0], " ".join(args[1:])
        target = self.server.by_nick(target_nick)
        if not target:
            await session.send("Alvo não encontrado.")
            return
        await target.send(f"[whisper de {session.nickname}] {message}")
        await session.send(f"[whisper para {target.nickname}] {message}")

    async def cmd_quit(self, session: Session, args: list[str]) -> None:
        await session.send("Até mais!")
        # Fechar o writer encerra a sessão
        session.writer.close()                 