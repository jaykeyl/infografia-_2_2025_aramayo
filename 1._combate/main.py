import random
from character import Rogue, Tank, Wizard, Paladin

# personajes disponibles
character_classes = {
    "rogue": Rogue,
    "tank": Tank,
    "wizard": Wizard,
    "paladin": Paladin
}

# creando jugadores al inicio del juego
players = []
while True:
    try:
        num_players = int(input("¿Cuántos jugadores tendremos hoy? (mínimo 2): "))
        if num_players < 2:
            print("⚠ Debe haber al menos 2 jugadores para iniciar el juego >:c.")
            continue
        break
    except ValueError:
        print("⚠ Ingresa un número válido.")

for i in range(num_players):
    print(f"\nJugador {i+1}:")
    name = input("¿Cuál será el nombre de tu personaje?: ")
    
    print("Personajes disponibles:")
    for c in character_classes.keys():
        print(f"- {c}")
    
    chosen_class = ""
    while chosen_class not in character_classes:
        chosen_class = input("Elige tu personaje: ").lower()
    
    player = character_classes[chosen_class](name)
    players.append(player)

# preguntamos cuantos turnos quieren los jugadores
while True:
    try:
        num_turns = int(input("\nNúmero de turnos (mínimo 1): "))
        if num_turns < 1:
            print("⚠ Debe haber al menos 1 turno.")
            continue
        break
    except ValueError:
        print("⚠ Ingresa un número válido.")

# inicia la pelea
for turn in range(num_turns):
    print(f"\n===== TURNO {turn+1} =====")
    alive_players = [p for p in players if p.is_alive()]
    if len(alive_players) <= 1:
        break

    random.shuffle(alive_players)
    for attacker in alive_players:
        if not attacker.is_alive():
            continue
        
        print(f"\n¡Es el turno de {attacker.name} con {attacker.hp} de salud! ")
        choice = input("¿Quieres usar una habilidad? (s/n): ").lower()
        if choice == "s":
            print("Habilidades disponibles:", attacker.skill_uses)
            skill = input("Elige habilidad: ").lower()
            target = None
            if skill == "ataque poderoso":
                possible_targets = [p for p in alive_players if p != attacker]
                for idx, t in enumerate(possible_targets):
                    print(f"{idx+1}. {t.name} (HP: {t.hp})")
                try:
                    target_choice = int(input("Elige tu objetivo: ")) - 1
                    target = possible_targets[target_choice]
                except (ValueError, IndexError):
                    print("⚠ ¡Ese objetivo no existe! Pierdes el turno.")
                    continue
            attacker.activate_skill(skill, target)
            continue 
        
       # cuando le toca el turno a un personaje elige a quien atacar
        possible_targets = [p for p in alive_players if p != attacker]

        print("\nElige a quien quieres atacar (No puedes atacarte a ti mismo :p ):")
        for idx, t in enumerate(possible_targets):
            print(f"{idx+1}. {t.name} (HP: {t.hp})")

        try:
            target_choice = int(input("Ingresa el número de tu objetivo: ")) - 1
            target = possible_targets[target_choice]
        except (ValueError, IndexError):
            print("⚠ ¡No hay ese número en la lista! Pierdes el turno.")
            continue

        attacker.attack(target)

#despues del numero de turnos, damos el mensaje final 
alive_players = [p for p in players if p.is_alive()]
if len(alive_players) == 1:
    print(f"\n{alive_players[0].name} es el ganador con {alive_players[0].hp} HP restante!")
else:
    print("\n¡Nadie murió! El combate termina en empate.")
