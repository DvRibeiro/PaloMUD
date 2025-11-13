from evennia import DefaultCharacter

class NPC(DefaultCharacter):
    """
    Classe base para Personagens Não-Jogadores (NPCs).
    """
    def at_object_creation(self):
        """
        Chamado na criação do NPC.
        """
        super().at_object_creation()
        self.db.strength = 3
        self.db.vitality = 5
        self.db.max_hp = self.db.vitality * 8
        self.db.hp = self.db.max_hp
        self.db.hostile = True

    def at_gothit(self, attacker):
        """
        Chamado quando o NPC é atingido em combate.
        """
        if not self.db.hp or self.db.hp <= 0:
            return

        if self.db.hostile:
            # Contra-ataque
            damage = self.db.strength
            attacker.msg(f"{self.key} counter-attacks for {damage} damage.")
            self.location.msg(f"{self.key} counter-attacks {attacker.key}.", exclude=[self, attacker])
            
            if hasattr(attacker.db, "hp"):
                attacker.db.hp -= damage
                if attacker.db.hp <= 0:
                    attacker.msg("You have been defeated!")
                    self.msg(f"You defeated {attacker.key}!")
                    attacker.location.msg(f"{attacker.key} collapses to the ground, defeated.", exclude=[self, attacker])
                    attacker.delete()

