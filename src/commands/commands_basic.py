from evennia import default_cmds

class CmdInventory(default_cmds.MuxCommand):
    """
    Exibe o inventário do jogador.
    """
    key = "inventory"
    aliases = ["inv"]

    def func(self):
        """
        Executa o comando.
        """
        items = self.caller.db.inventory or []
        if not items:
            self.caller.msg("You don't have anything in your inventory.")
        else:
            item_list = ", ".join(obj.key for obj in items)
            self.caller.msg(f"You carry: {item_list}")

class CmdStats(default_cmds.MuxCommand):
    """
    Exibe as estatísticas do personagem.
    """
    key = "stats"
    aliases = ["status", "score"]

    def func(self):
        """
        Executa o comando.
        """
        caller = self.caller
        table = self.styled_table(
            "|wAtributo|n", "|wValor|n"
        )
        table.add_row("Força", str(caller.db.strength))
        table.add_row("Destreza", str(caller.db.dexterity))
        table.add_row("Inteligência", str(caller.db.intelligence))
        table.add_row("Vitalidade", str(caller.db.vitality))
        table.add_row("-" * 15, "-" * 8)
        table.add_row("HP", f"{caller.db.hp}/{caller.db.max_hp}")
        
        self.caller.msg(f"|cEstatísticas de {caller.key}|n\n{table}")

class CmdMemories(default_cmds.MuxCommand):
    """
    Exibe as memórias recuperadas.
    """
    key = "memories"

    def func(self):
        """
        Executa o comando.
        """
        memories = self.caller.db.memories or []
        if not memories:
            self.caller.msg("You haven't recovered any memories yet.")
        else:
            self.caller.msg("|cMemórias Recuperadas:|n")
            for memory in memories:
                self.caller.msg(f"- {memory}")

class CmdAttack(default_cmds.MuxCommand):
    """
    Inicia um ataque contra um alvo.
    """
    key = "attack"
    aliases = ["atk", "hit"]

    def func(self):
        """
        Executa o comando de ataque.
        """
        if not self.args:
            self.caller.msg("Attack whom?")
            return

        target = self.caller.search(self.args.strip())
        if not target:
            return

        # Calcula o dano
        damage = self.caller.db.strength

        # Mensagem para o atacante e o alvo
        self.caller.msg(f"You attack {target.key} for {damage} damage.")
        target.msg(f"{self.caller.key} attacks you for {damage} damage.")

        # Aplica o dano
        if hasattr(target.db, "hp"):
            target.db.hp -= damage
            if target.db.hp <= 0:
                target.msg("You have been defeated!")
                self.caller.msg(f"You defeated {target.key}!")
                # Aqui poderíamos adicionar loot, XP, etc.
                target.location.msg(f"{target.key} collapses to the ground, defeated.", exclude=[self.caller, target])
                target.delete()
                return

        # Permite que o alvo contra-ataque
        if hasattr(target, "at_gothit"):
            target.at_gothit(self.caller)
