import asyncio
from constants_util import NAME_VERSION
from session import Session
from server_state import ServerState
from cmd_util import CMDUtil
from bot import Bot

class Shell:
    def __init__(self, server: ServerState, bot: Bot):
        self.server = server
        self.bot = bot

    async def login(self, session: Session, reader) -> None:
        await session.send(f"\r\nBem-vindo ao {NAME_VERSION}!")
        await session.send("Antes de começar, escolha um nickname:")

        while True:
            try:
                await session.send_no_lb("Digite seu nick: ")
                nick = await reader.readline()
                
                # se o cliente fechou a conexão
                if not nick:
                    await session.close()
                    return  # sai do login
                
                nick = nick.rstrip("\r\n").strip()
                
                if not nick:
                    continue
                if self.server.nick_in_use(nick):
                    await session.send("Esse nick já está em uso, tente outro.")
                    continue

                session.nickname = nick
                break
            
            except (asyncio.IncompleteReadError, ConnectionResetError):
                await session.close()
                return    

    async def welcome(self, session: Session) -> None:
        msg = ("\r\n"
            f"Bem-vindo ao {NAME_VERSION}, {session.nickname}!\r\n"
            "Comandos: /help, /nick <nome>, /say <msg>, /who, /whisper <alvo> <msg>, /quit\r\n"
            "Dica: mensagens sem / vão para o BOT.\r\n"
        )
        await session.send(msg)

    async def broadcast_safe(self, msg: str) -> None:
        for s in self.server.sessions.copy():
            try:
                await s.send(msg)
            except Exception:
                pass       

    async def shell(self, reader, writer):
        peername = writer.get_extra_info("peername")  # IP e porta do cliente
        session = Session(reader=reader, writer=writer, nickname=None)
        cmd_util = CMDUtil(self.server) 

        try:
            await self.login(session, reader)      
            self.server.add(session)

            print(f">> [ENTROU] {session.nickname} de {peername}. Total conectados: {len(self.server.sessions)}")

            await self.welcome(session)
            await self.server.broadcast(session, f"{session.nickname} entrou.")
            await session.prompt()

            while True:
                line = await reader.readline()
                if not line:
                    break  # cliente saiu
                line = line.rstrip("\r\n").strip()
                if not line:
                    await session.prompt()
                    continue

                if line.startswith("/"):
                    await cmd_util.handle_command(session, line)
                else:
                    # Envia para o bot
                    answer = self.bot.reply(line)
                    await session.send(f"[BOT] {answer}")

                # Se writer foi fechado por /quit, pare o loop
                if writer.is_closing():
                    break

                await session.prompt()

        finally:
            peername = writer.get_extra_info("peername")  # IP e porta do cliente
            nickname = session.nickname
            self.server.remove(session)
            print(f">> [SAIU] {nickname} de {peername}. Total conectados: {len(self.server.sessions)}")                        
            await self.broadcast_safe(f"{session.nickname} saiu.")