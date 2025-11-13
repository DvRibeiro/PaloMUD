from evennia import default_cmds
from .commands_basic import CmdInventory, CmdStats, CmdMemories, CmdAttack

class CharacterCmdSet(default_cmds.CharacterCmdSet):
    """
    CmdSet for the character, adding custom commands.
    """
    def at_cmdset_creation(self):
        """
        Populates the cmdset.
        """
        super().at_cmdset_creation()
        self.add(CmdInventory())
        self.add(CmdStats())
        self.add(CmdMemories())
        self.add(CmdAttack())
