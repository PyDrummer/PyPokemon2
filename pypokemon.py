import random as rd
#import time i was going to implement a time feature but didnt.

# I need to go back and fix the dictionary with the types cause the type advantages aren't working correctly
#type_advantages={ 
#     'fire' : 'grass',
#    'water' : 'fire',
#    'grass' : 'water'}

class Pokemon:
    def __init__(self, name, level, el_type, atk_type, is_knocked_out = False, exp = 0):
        self.name = name
        self.level = level
        self.health = level * 5
        self.max_health = level * 5
        self.el_type = el_type
        self.atk_type = atk_type
        self.is_knocked_out = is_knocked_out
        self.exp = exp

    def __repr__(self):
        return "Pokemon info, {}, current level: {} type: {}, maximun health: {}, current health: {}.\n".format(self.name, self.level, self.el_type, self.max_health, self.health)

    def lose_health(self, dmg):
        self.health -= dmg
        if self.health <= 0:
            self.knock_out()

    def gain_health(self, heal):
        if heal + self.health >= self.max_health:
            self.health = self.max_health
            print({f"{self.name} is at max health!"})
        else:
            self.health += heal
            print(f"{self.name} gained {heal} health!")

    def knock_out(self):
        if self.health <= 0:
            self.is_knocked_out = True
            print(f"{self.name} is knocked out!")

# i'm planning to add a revive feature later.
#    def revive(self, revive):
#        if self.is_knocked_out:
#            self.health += self.level * 2
#            print(f"{self.name} revived by {self.revive} hp!")
#        else:
#            print(f"{self.name} can't be revived right now!")

    def attack(self, enemy):
        if self.is_knocked_out:
            print(f"{self.name} cannot attack. {self.name} is knocked out!")
            return
        dmg = 0
        if self.el_type == 'water' and enemy.el_type == 'fire':
            dmg += self.level * 2
        elif self.el_type == 'water' and enemy.el_type == 'grass':
            dmg += self.level / 2
        elif self.el_type == 'fire' and enemy.el_type == 'grass':
            dmg += self.level * 2
        elif self.el_type == 'fire' and enemy.el_type == 'water':
            dmg += self.level / 2
        elif self.el_type == 'grass' and enemy.el_type == 'water':
            dmg += self.level * 2
        elif self.el_type == 'grass' and enemy.el_type == 'fire':
            dmg += self.level / 2
        else:
            dmg = self.level
        print(f"{self.name} attacked {enemy.name} and dealt {dmg} damage!")
        enemy.lose_health(dmg)
        if enemy.health > 0:
            print(f"{enemy.name} has {enemy.health} health left!")
        if enemy.health <= 0:
            print(f"{enemy.name} defeated!")
            self.gain_exp(1)
            print(f"{self.name} gained EXP!")

    def gain_exp(self, exp):
        self.exp += exp
        if self.exp >= 3:
            self.level += 1
            print(f"{self.name} leveled up to level {self.exp}!")


class Trainer:
    def __init__(self, name, belt):
        self.name = name
        self.belt = belt

    def get_avg_level(self):
        return sum(slot.level for slot in self.belt) / len(self.belt)

    def has_pokemon(self):
        for pkm in self.belt:
            if not pkm.is_knocked_out:
                return True
        return False

    def swap_pokemon(self):
        self.view_pokemon()
        print("[number] to change leader, or [Enter] to close")
        selection = input()
        if selection in [str(i + 1) for i in range(len(self.belt))]:
            if not self.belt[int(selection) - 1].is_knocked_out:
                self.set_active_pokemon(int(selection) - 1)
            else:
                self.swap_pokemon
        elif self.belt[0].is_knocked_out:
            self.swap_pokemon()

    def set_active_pokemon(self, selection):
        self.belt.insert(0, self.belt.pop(self.belt.index(self.belt[selection])))

    def view_pokemon(self):
        print(f"{self.name}'s Pokemon:")
        for idx, pkm in enumerate(self.belt):
            is_ko = ''
            if pkm.is_knocked_out == True:
                is_ko = " - fainted!"
            print(f"{pkm.name}, Level: {pkm.level}, Current health: {pkm.health}, Max Health: {pkm.max_health} {is_ko}")

#variables

player = Trainer("missingno", [])
opponent_names = ["Brock", "Misty", "Lt. Surge", "Erika", "Koga", "Sabrina", "Blaine", "Giovanni"]
dex = [{"Name": "Bulbasaur", 'el_type': 'grass', "attack_type": 'grass'},
       {"Name": "Charmander", 'el_type': 'fire', "attack_type": 'fire'},
       {"Name": "Squirtle", 'el_type': 'water', "attack_type": 'water'}]

#functions

def display_belt(player, pokemon):
    print(player.name, end='-')
    for slot in player.belt:
        if slot.is_knocked_out:
            print("[/]", end=' ')
        else:
            print("[_]", end=' ')
    print(f"\n%s  Lv.%d  %d/%d HP" % (pokemon.name, pokemon.level, pokemon.health, pokemon.max_health))


def opponent_trainer():
    belt = []
    level = 0
    for slot in range(rd.randint(1, 6)):
        rand_pkm = rd.choice(dex)
        level = player.get_avg_level() + rd.randint(-2, 2)
        belt.append(Pokemon(rand_pkm["Name"], level, rand_pkm['el_type'], rand_pkm["attack_type"]))
    return Trainer(rd.choice(opponent_names), belt)


def battle():
    opponent = opponent_trainer()

    #battle starts
    player_pkm = player.belt[0]
    print(f"Go, {player_pkm.name}!")
    opponent_pkm = opponent.belt[0]
    print(f"{opponent.name} sends out {opponent_pkm.name}!")

    #battle loop
    while opponent.has_pokemon() and player.has_pokemon():
        print()
        display_belt(opponent, opponent_pkm)
        display_belt(player, player_pkm)
        choice = input("1) Attack\n2) Switch\n ")
        if choice == '1':
            player_pkm.attack(opponent_pkm)
            if opponent_pkm.is_knocked_out:
                if opponent.has_pokemon():
                    opponent_pkm = rd.choice([pk for pk in opponent.belt if (not pk.is_knocked_out)])
                    print(f"{opponent.name} sends out {opponent_pkm.name}!")
                else:
                    continue
            opponent_pkm.attack(player_pkm)
            if player_pkm.is_knocked_out:
                print("Choose next Pokemon!")
                player.swap_pokemon()
                player_pkm = player.belt
        elif choice == '2':
            player.swap_pokemon()
            player_pkm = player.belt[0]
    if not player.has_pokemon():
        print(f"{player.name} is out of usable Pokemon! {player.name} loses.")
    elif not opponent.has_pokemon():
        print(f"{player.name} defeated {opponent.name}!")
    return True


def main():
    print("Welcome to my small version of Pokemon! Let's start with your name, adventurer!")
    player.name = input()
    print(f"So, you're name is {player.name}.")
    print(f"Pokemon is all about battling! Since picking just one is difficult you can start with all three!")
    player.belt.extend([Pokemon("Bulbasaur", 5, ['grass'], ['grass']), Pokemon("Charmander", 5, ['fire'], ['fire']), Pokemon("Squirtle", 5, ['water'], ['water'])])
    print(f"*You attach the 3 pokemon to your belt and are ready to fight*")

    playing = True
    while playing:
        choice = input(f"\nSo, {player.name} what would you like to do?\n"
                       "1) Trainer Battle\n"
                       "2) Check your Pokemon\n"
                       "3) Quit\n")
        if (choice == '1'):
            playing = battle()
        elif (choice == '2'):
            player.view_pokemon()
        elif (choice == '3'):
            playing = False

main()
