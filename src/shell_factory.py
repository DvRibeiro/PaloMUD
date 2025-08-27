from server_state import ServerState
from bot import Bot
from shell import Shell

class ShellFactory:
    @staticmethod
    def return_shell():
        server_state = ServerState()
        bot = Bot()
        return Shell(server_state, bot)