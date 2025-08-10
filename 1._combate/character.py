import random

class Character:
    def __init__(self, name, hp, base_damage, parry_prob, crit_prob):
        self.name = name
        self.hp = hp
        self.base_damage = base_damage
        self.parry_prob = parry_prob
        self.crit_prob = crit_prob
        self.bonus_damage_turns = 0
        self.shield_turns = 0
        self.skill_uses = {}
    
    def is_alive(self):
        return self.hp > 0
    
    def attack(self, other):
        if self.bonus_damage_turns > 0:
            damage = (self.base_damage * 2)
            self.bonus_damage_turns -= 1
        else:
            damage = self.base_damage
        
        if random.random() <= self.crit_prob:
            damage *= 2
            print(f":o ¡Crítico de {self.name}!")
        
        other.hurt(damage)

    def hurt(self, damage):
        if self.shield_turns > 0:
            print(f"🛡 {self.name} bloqueó el ataque (escudo activo)")
            self.shield_turns -= 1
            return
        
        if random.random() <= self.parry_prob:
            print(f"⚡ {self.name} hizo parry y evitó el daño!")
            return
        
        self.hp -= damage
        print(f"¡Ay! {self.name} recibió {damage} de daño. HP restante: {self.hp}")
    
    def heal(self, amount):
        self.hp += amount
        print(f":D {self.name} se curó {amount} HP. HP actual: {self.hp}")
    
    def activate_skill(self, skill_name, target=None):
        if skill_name not in self.skill_uses or self.skill_uses[skill_name] <= 0:
            print(f" {self.name} no puede usar la habilidad {skill_name} (ya no tienes usos!)")
            return False
        
        if skill_name == "curar":
            self.heal(30)
        elif skill_name == "daño extra":
            self.bonus_damage_turns = 3
            print(f"{self.name} activó daño extra por 3 turnos")
        elif skill_name == "escudo":
            self.shield_turns = 2
            print(f"🛡 {self.name} activó escudo por 2 turnos")
        elif skill_name == "ataque poderoso" and target:
            damage = self.base_damage * 3
            target.hurt(damage)
        else:
            print("No tienes esa habilidad XD")
            return False
        
        self.skill_uses[skill_name] -= 1
        return True


class Rogue(Character):
    def __init__(self, name):
        super().__init__(name, 100, 15, 0.2, 0.4)
        self.skill_uses = {"daño extra": 2, "curar": 1}


class Tank(Character):
    def __init__(self, name):
        super().__init__(name, 200, 10, 0.3, 0.1)
        self.skill_uses = {"escudo": 2, "ataque poderoso": 1}


class Wizard(Character):
    def __init__(self, name):
        super().__init__(name, 120, 12, 0.1, 0.3)
        self.skill_uses = {"curar": 2, "daño extra": 1}


class Paladin(Character):
    def __init__(self, name):
        super().__init__(name, 150, 14, 0.15, 0.25)
        self.skill_uses = {"escudo": 1, "curar": 1}
