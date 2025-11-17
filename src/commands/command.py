"""
Commands

Commands describe the input the account can do to the game.

"""

from evennia.commands.command import Command as BaseCommand

# from evennia import default_cmds


class Command(BaseCommand):
    """
    Base command (you may see this if a child command had no help text defined)

    Note that the class's `__doc__` string is used by Evennia to create the
    automatic help entry for the command, so make sure to document consistently
    here. Without setting one, the parent's docstring will show (like now).

    """

    # Each Command class implements the following methods, called in this order
    # (only func() is actually required):
    #
    #     - at_pre_cmd(): If this returns anything truthy, execution is aborted.
    #     - parse(): Should perform any extra parsing needed on self.args
    #         and store the result on self.
    #     - func(): Performs the actual work.
    #     - at_post_cmd(): Extra actions, often things done after
    #         every command, like prompts.
    #
    pass

import random

from evennia import Command
import random

# commands/inventory.py

from evennia import Command

class CmdInventario(Command):
    """
    Lista os itens no inventário do jogador.

    Uso:
        inventario
    """
    key = "inventario"
    aliases = ["inv"]
    help_category = "Utilidades"

    def func(self):
        inventario = self.caller.db.inventory or []
        
        # Se o inventário for uma lista com objetos
        if not inventario:
            self.caller.msg("Você não possui itens no inventário.")
            return
        
        # Cria uma lista de nomes dos itens
        itens_formatados = []
        for item in inventario:
            nome = item.key
            itens_formatados.append(f"- {nome}")
        
        # Exibe os itens para o jogador
        itens_texto = "\n".join(itens_formatados)
        self.caller.msg(f"Você está carregando:\n{itens_texto}")

class CmdEquipar(Command):
    """
    Equipa um item do seu inventário.

    Uso:
        equipar <item>
    """
    key = "equipar"
    help_category = "Inventário"

    def func(self):
        if not self.args:
            self.caller.msg("Equipar o quê?")
            return
        
        item_name = self.args.strip().lower()
        inventario = self.caller.db.inventory
        
        for item in inventario:
            if item.key.lower() == item_name:
                self.caller.equipar(item)
                return
        
        self.caller.msg("Você não possui esse item para equipar.")

class CmdPegar(Command):
    """
    Pega um item da sala.

    Uso:
        pegar <item>
    """
    key = "pegar"
    help_category = "Inventário"

    def func(self):
        if not self.args:
            self.caller.msg("Pegar o quê?")
            return

        item = self.caller.search(self.args, location=self.caller.location)
        if not item:
            return

        # Move o item para o inventário
        self.caller.adicionar_item(item)
        item.location = None  # tira o item da sala

class CmdAtacar(Command):
    """
    Ataca um inimigo na sala.

    Uso:
        atacar <alvo>

    Exemplo:
        atacar goblin
    """
    key = "atacar"
    help_category = "Combate"

    def func(self):
        if not self.args:
            self.caller.msg("Atacar quem?")
            return
        
        alvo = self.caller.search(self.args)
        if not alvo:
            return
        
        if not hasattr(alvo, "receber_dano"):
            self.caller.msg("Isso não pode ser atacado.")
            return


        # TODO: considerar armas equipadas para dano
        # if self.caller.db.equipado:
        #     dano = random.randint(5, 10)
        #     arma = self.caller.db.equipado.key
        #     self.caller.msg(f"Você usa {arma} e causa {dano} de dano!")
        # else:
        #     dano = random.randint(2, 4)
        #     self.caller.msg(f"Você ataca desarmado e causa {dano} de dano...")

        dano = random.randint(2, 6)  # dano variável
        self.caller.msg(f"|gVocê ataca {alvo.key} e causa {dano} de dano!|n")
        alvo.msg(f"|r{self.caller.key} ataca você e causa {dano} de dano!|n")
        alvo.receber_dano(dano, self.caller)

class CmdFalar(Command):
    key = "falar"
    help_category = "Interação"

    def func(self):
        if not self.args:
            self.caller.msg("Falar com quem?")
            return
        alvo = self.caller.search(self.args)
        if not alvo or not hasattr(alvo, "talk"):
            self.caller.msg("Esse personagem não quer conversar.")
            return
        alvo.talk(self.caller)

class CmdComprar(Command):
    key = "comprar"
    help_category = "Interação"

    def func(self):
        if not self.args:
            self.caller.msg("Comprar o quê?")
            return
        alvo = self.caller.search("mercador")
        if not alvo or not hasattr(alvo, "comprar"):
            self.caller.msg("Não há comerciante aqui.")
            return
        alvo.comprar(self.caller, self.args)

class CmdListarItens(Command):
    key = "listaritens"
    help_category = "Interação"

    def func(self):
        if not self.args:
            self.caller.msg("Indique de qual mercador quer listar os itens")
            return
        alvo = self.caller.search("mercador")
        if not alvo or not hasattr(alvo, "listar_itens"):
            self.caller.msg("Não há mercador aqui.")
            return
        alvo.listar_itens(self.caller)        

class CmdResolver(Command):
    key = "resolver"
    help_category = "Puzzle"

    def func(self):
        if not self.args:
            self.caller.msg("Resolver o quê?")
            return
        armadilha = self.caller.search(self.args)
        if not armadilha or not hasattr(armadilha, "resolver"):
            self.caller.msg("Não há nada para resolver.")
            return
        resposta = yield("Qual é a resposta?")
        armadilha.resolver(self.caller, resposta)

class CmdLembrar(Command):
    key = "lembrar"
    help_category = "Memória"

    def func(self):
        """
        O jogador tenta acessar uma memória perdida.
        """
        self.caller.lembrar()


# -------------------------------------------------------------
#
# The default commands inherit from
#
#   evennia.commands.default.muxcommand.MuxCommand.
#
# If you want to make sweeping changes to default commands you can
# uncomment this copy of the MuxCommand parent and add
#
#   COMMAND_DEFAULT_CLASS = "commands.command.MuxCommand"
#
# to your settings file. Be warned that the default commands expect
# the functionality implemented in the parse() method, so be
# careful with what you change.
#
# -------------------------------------------------------------

# from evennia.utils import utils
#
#
# class MuxCommand(Command):
#     """
#     This sets up the basis for a MUX command. The idea
#     is that most other Mux-related commands should just
#     inherit from this and don't have to implement much
#     parsing of their own unless they do something particularly
#     advanced.
#
#     Note that the class's __doc__ string (this text) is
#     used by Evennia to create the automatic help entry for
#     the command, so make sure to document consistently here.
#     """
#     def has_perm(self, srcobj):
#         """
#         This is called by the cmdhandler to determine
#         if srcobj is allowed to execute this command.
#         We just show it here for completeness - we
#         are satisfied using the default check in Command.
#         """
#         return super().has_perm(srcobj)
#
#     def at_pre_cmd(self):
#         """
#         This hook is called before self.parse() on all commands
#         """
#         pass
#
#     def at_post_cmd(self):
#         """
#         This hook is called after the command has finished executing
#         (after self.func()).
#         """
#         pass
#
#     def parse(self):
#         """
#         This method is called by the cmdhandler once the command name
#         has been identified. It creates a new set of member variables
#         that can be later accessed from self.func() (see below)
#
#         The following variables are available for our use when entering this
#         method (from the command definition, and assigned on the fly by the
#         cmdhandler):
#            self.key - the name of this command ('look')
#            self.aliases - the aliases of this cmd ('l')
#            self.permissions - permission string for this command
#            self.help_category - overall category of command
#
#            self.caller - the object calling this command
#            self.cmdstring - the actual command name used to call this
#                             (this allows you to know which alias was used,
#                              for example)
#            self.args - the raw input; everything following self.cmdstring.
#            self.cmdset - the cmdset from which this command was picked. Not
#                          often used (useful for commands like 'help' or to
#                          list all available commands etc)
#            self.obj - the object on which this command was defined. It is often
#                          the same as self.caller.
#
#         A MUX command has the following possible syntax:
#
#           name[ with several words][/switch[/switch..]] arg1[,arg2,...] [[=|,] arg[,..]]
#
#         The 'name[ with several words]' part is already dealt with by the
#         cmdhandler at this point, and stored in self.cmdname (we don't use
#         it here). The rest of the command is stored in self.args, which can
#         start with the switch indicator /.
#
#         This parser breaks self.args into its constituents and stores them in the
#         following variables:
#           self.switches = [list of /switches (without the /)]
#           self.raw = This is the raw argument input, including switches
#           self.args = This is re-defined to be everything *except* the switches
#           self.lhs = Everything to the left of = (lhs:'left-hand side'). If
#                      no = is found, this is identical to self.args.
#           self.rhs: Everything to the right of = (rhs:'right-hand side').
#                     If no '=' is found, this is None.
#           self.lhslist - [self.lhs split into a list by comma]
#           self.rhslist - [list of self.rhs split into a list by comma]
#           self.arglist = [list of space-separated args (stripped, including '=' if it exists)]
#
#           All args and list members are stripped of excess whitespace around the
#           strings, but case is preserved.
#         """
#         raw = self.args
#         args = raw.strip()
#
#         # split out switches
#         switches = []
#         if args and len(args) > 1 and args[0] == "/":
#             # we have a switch, or a set of switches. These end with a space.
#             switches = args[1:].split(None, 1)
#             if len(switches) > 1:
#                 switches, args = switches
#                 switches = switches.split('/')
#             else:
#                 args = ""
#                 switches = switches[0].split('/')
#         arglist = [arg.strip() for arg in args.split()]
#
#         # check for arg1, arg2, ... = argA, argB, ... constructs
#         lhs, rhs = args, None
#         lhslist, rhslist = [arg.strip() for arg in args.split(',')], []
#         if args and '=' in args:
#             lhs, rhs = [arg.strip() for arg in args.split('=', 1)]
#             lhslist = [arg.strip() for arg in lhs.split(',')]
#             rhslist = [arg.strip() for arg in rhs.split(',')]
#
#         # save to object properties:
#         self.raw = raw
#         self.switches = switches
#         self.args = args.strip()
#         self.arglist = arglist
#         self.lhs = lhs
#         self.lhslist = lhslist
#         self.rhs = rhs
#         self.rhslist = rhslist
#
#         # if the class has the account_caller property set on itself, we make
#         # sure that self.caller is always the account if possible. We also create
#         # a special property "character" for the puppeted object, if any. This
#         # is convenient for commands defined on the Account only.
#         if hasattr(self, "account_caller") and self.account_caller:
#             if utils.inherits_from(self.caller, "evennia.objects.objects.DefaultObject"):
#                 # caller is an Object/Character
#                 self.character = self.caller
#                 self.caller = self.caller.account
#             elif utils.inherits_from(self.caller, "evennia.accounts.accounts.DefaultAccount"):
#                 # caller was already an Account
#                 self.character = self.caller.get_puppet(self.session)
#             else:
#                 self.character = None
