from evennia import create_object, search_object
from typeclasses.rooms import Room
from typeclasses.exits import Exit
from typeclasses.npcs import NPC

def setup_world():
    """
    Cria o mundo inicial do jogo.
    """
    if search_object("Quarto do Despertar"):
        print("O mundo de PaloMUD já foi criado.")
        return

    # --- Criação das Salas ---

    # 1. Quarto do Despertar
    awakening_room = create_object(Room, key="Quarto do Despertar")
    awakening_room.db.desc = (
        "Você desperta sob um teto de madeira antiga. O ar está denso, e há algo "
        "gravado em sua mão, um símbolo que brilha fracamente. A chuva cai lá fora. "
        "Você não lembra seu nome."
    )

    # 2. Cidade de Lorya
    lorya = create_object(Room, key="Cidade de Lorya")
    lorya.db.desc = (
        "O refúgio dos Despertados. Uma cidade movimentada, construída sobre as ruínas "
        "de um tempo esquecido. As ruas de pedra estão repletas de comerciantes, "
        "aventureiros e sussurros de missões."
    )

    # 3. Floresta de Vethar
    vethar_forest = create_object(Room, key="Floresta de Vethar")
    vethar_forest.db.desc = (
        "Uma floresta sombria e corrompida. Árvores retorcidas se erguem como garras "
        "e o ar é pesado com uma energia profana. Criaturas mutantes espreitam nas sombras."
    )

    # --- NPCs ---

    initiate = create_object(NPC, key="Iniciado dos Arautos", location=vethar_forest)
    initiate.db.desc = "Um seguidor fanático dos Arautos da Peste, com olhos brilhando com fervor sombrio."
    initiate.db.strength = 4
    initiate.db.vitality = 6
    initiate.db.max_hp = initiate.db.vitality * 8
    initiate.db.hp = initiate.db.max_hp


    # --- Conexões (Saídas) ---

    create_object(
        Exit,
        key="sair",
        aliases=["out", "porta"],
        location=awakening_room,
        destination=lorya,
    )
    create_object(
        Exit,
        key="floresta",
        aliases=["leste", "east"],
        location=lorya,
        destination=vethar_forest,
    )
    create_object(
        Exit,
        key="cidade",
        aliases=["oeste", "west"],
        location=vethar_forest,
        destination=lorya,
    )

    print("Mundo de PaloMUD criado com sucesso!")
    print("\n--- INSTRUÇÕES IMPORTANTES ---")
    print(f"O 'Quarto do Despertar' foi criado com o dbref: #{awakening_room.id}")
    print(f"A 'Cidade de Lorya' foi criada com o dbref: #{lorya.id}")
    print("Copie esses valores para o arquivo 'server/conf/settings.py'.")
    print("---------------------------------\n")
