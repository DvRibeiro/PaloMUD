import telnetlib3

class Session:
    def __init__(self, reader: telnetlib3.TelnetReader, writer: telnetlib3.TelnetWriter, nickname: str):
        self.reader = reader
        self.writer = writer
        self.nickname = nickname
        self.PROMPT = ">> "

    async def send(self, text: str) -> None:
        """Envia texto para o cliente (UTF-8)."""
        self.writer.write(text + "\r\n")
        await self.writer.drain()

    async def send_no_lb(self, text: str) -> None:
            """Envia texto para o cliente (UTF-8)."""
            self.writer.write(text)
            await self.writer.drain()        

    async def prompt(self) -> None:
        """Mostra o prompt no cliente."""
        self.writer.write(self.PROMPT)
        await self.writer.drain()