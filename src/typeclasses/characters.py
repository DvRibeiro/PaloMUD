"""
Characters

Characters are (by default) Objects setup to be puppeted by Accounts.
They are what you "see" in game. The Character class in this module
is setup to be the "default" character type created by the default
creation commands.

"""

from evennia import DefaultCharacter
from commands.cmdset_character import CharacterCmdSet

class Character(DefaultCharacter):
    def at_object_creation(self):
        """
        Chamado quando o personagem é criado pela primeira vez.
        """
        super().at_object_creation()
        self.cmdset.add_default(CharacterCmdSet, permanent=True)

        # Atributos base do personagem
        self.db.strength = 5
        self.db.dexterity = 5
        self.db.intelligence = 5
        self.db.vitality = 5

        # Atributos derivados
        self.db.max_hp = self.db.vitality * 10
        self.db.hp = self.db.max_hp

        # Inventário e Memórias
        self.db.inventory = []
        self.db.memories = []

        # Descrição inicial
        self.db.desc = "Uma figura sem uma identidade clara, um recomeço em branco."

    def return_appearance(self, looker, **kwargs):
        """
        Define como o personagem é descrito.
        """
        if not looker:
            return ""
        
        # Adiciona a descrição e o estado de saúde
        text = super().return_appearance(looker, **kwargs)
        health_status = f"\n|cSaúde:|n {self.db.hp}/{self.db.max_hp}"
        return text + health_status
