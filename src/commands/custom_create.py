from evennia import default_cmds, create_object, search_object
from typeclasses.characters import Character

class CmdCustomCreate(default_cmds.CmdCreate):
    """
    Sobrescreve o comando 'create' padrão para também gerar um personagem.
    """

    def func(self):
        super().func()

        if not self.account:
            return

        entrada = search_object("Entrada")
        if not entrada:
            self.account.msg("❌ Erro: Sala 'Entrada' não encontrada.")
            return
        entrada = entrada[0]

        # Cria o personagem automaticamente
        char = create_object(
            Character,
            key=self.account.key,
            location=entrada,
            home=entrada
        )

        # Vincula o personagem à conta
        self.account.db._last_puppet = char
        self.account.db._last_puppet_dbref = char.dbref

        # Faz o jogador já entrar com esse personagem
        self.account.puppet_object(session=self.session, obj=char)
        self.account.msg(f"🎮 Personagem '{char.key}' criado e posicionado em {entrada.key}!")
