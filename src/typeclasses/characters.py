"""
Characters

Characters are (by default) Objects setup to be puppeted by Accounts.
They are what you "see" in game. The Character class in this module
is setup to be the "default" character type created by the default
creation commands.

"""

from evennia import DefaultCharacter
from evennia import create_script
from typeclasses.skills import Skill

from .objects import ObjectParent


class Character(ObjectParent, DefaultCharacter):
    """
    The Character just re-implements some of the Object's methods and hooks
    to represent a Character entity in-game.

    See mygame/typeclasses/objects.py for a list of
    properties and methods available on all Object child classes like this.

    """
    def at_object_creation(self):
            super().at_object_creation()
            self.db.level = 1
            self.db.inventory = []   # lista de itens no inventário
            self.db.equipado = None  # item atualmente equipado

            self.db.memories = []  # Lista de habilidades esquecidas

            memoria_2 = create_script(Skill, obj=self)
            memoria_2.db.skill_name = "Foco Espiritual"
            memoria_2.db.desc = "Você recorda técnicas de concentração que regeneram energia."
            memoria_2.db.effect = "cura leve"

            self.db.memories = [memoria_2]

    def ganhar_experiencia(self, xp):
        # Recupera ou inicializa o XP
        xp_atual = self.db.xp or 0
        self.db.xp = xp_atual + xp

        # Recupera ou inicializa o nível
        level_atual = self.db.level or 1

        # Verifica se deve subir de nível
        if self.db.xp >= level_atual * 10:
            self.db.level = level_atual + 1
            self.msg(f"|gVocê alcançou o nível {self.db.level}!|n")
            self.lembrar()  # Chama algum método extra (caso exista)


    def adicionar_item(self, item):
        self.db.inventory.append(item)
        self.msg(f"|gVocê adquiriu: {item}|n")        
        #TODO > LISTAR KEY DO ITEM self.msg(f"|gVocê adquiriu: {item.key}|n")

    def equipar(self, item):
        if item not in self.db.inventory:
            self.msg("Você não possui esse item.")
            return

        self.db.equipado = item
        self.msg(f"|yVocê equipou: {item.key}|n")        

    def lembrar(self):
        """
        Desbloqueia uma nova habilidade esquecida conforme o nível atual.
        """
        locked = [m for m in self.db.memories if not m.db.unlocked]
        if not locked:
            self.msg("Você já se lembra de todas as suas habilidades passadas.")
            return
        
        skill = locked[0]
        skill.db.unlocked = True
        self.msg(f"Você se recorda de algo... '{skill.db.skill_name}'!")
        self.msg(skill.db.desc)    

from evennia import DefaultObject
import random

class NPC(DefaultObject):
    def at_object_creation(self):
        # Lista de diálogos possíveis
        self.db.dialogos = [
            "Bem-vindo, aventureiro. Dizem que há um tesouro escondido adiante.",
            "Os ventos sopram como se algo estivesse por vir...",
            "Já encontrou a saída deste labirinto subterrâneo?",
            "Sábios dizem que o silêncio também é uma resposta.",
        ]
        self.db.desc = "Um velho sábio com olhos atentos."

    def talk(self, caller):
        # Escolhe aleatoriamente um dos diálogos
        dialogo = random.choice(self.db.dialogos)
        caller.msg(f"{self.key} diz: {dialogo}")

class Comerciante(NPC):
    def at_object_creation(self):
        super().at_object_creation()
        self.db.dialogo = "Tenho algumas poções à venda."
        self.db.itens = {"poção": 10}  # ← agora armazenado em self.db

    def listar_itens(self, caller):
        itens = self.db.itens or {}
        if not itens:
            caller.msg(f"{self.key} não tem nada à venda no momento.")
            return
        lista = ", ".join([f"{item} ({preco} moedas)" for item, preco in itens.items()])
        caller.msg(f"{self.key} diz: Tenho os seguintes itens à venda: {lista}")    

    def comprar(self, caller, item):
        itens = self.db.itens or {}

        if not item:
            caller.msg("Comprar o quê?")
            return

        # Normaliza entrada e chaves
        item = item.strip().lower()
        itens_normalizados = {nome.lower(): preco for nome, preco in itens.items()}

        if item not in itens_normalizados:
            caller.msg("Não vendo isso.")
            return

        caller.adicionar_item(item.title())  # adiciona como texto, no futuro pode virar um objeto
        preco = itens_normalizados[item]
        caller.msg(f"Você compra {item} por {preco} moedas.")

