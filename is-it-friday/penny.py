import random

class Session:
    """ Represents a round of pennying"""
    def __init__(self):
        self.players = []

    def penny(self, offence, defence):
        """ A pennying event

        offence player is attacking the defence player"""

        # check offence is registered in the game
        if offence not in self.players:
            print("Player not registered - please sign in "
                  "before trying to penny someone.")
        # check defence is registered in the game
        elif defence not in self.players:
            print("Player not registered - make sure your "
                  "target has signed in.")

        # check offence has a penny
        elif offence.pennys <= 0:
            print("Insufficient funds! Go find some pennys "
                  "before you come back!")
        else:
            if random.random() < 0.5:
                # Attempt failed
                print(f"{offence.name} tried to penny {defence.name}, "
                      f"but missed.")
                offence.pennys -= 1
                defence.pennys += 1
            else:
                # Attempt succeeded
                print(f"{offence.name} pennied {defence.name}!")
                offence.pennys -= 1
                offence.attacks += 1
                defence.pennys += 1
                defence.defences += 1

    def add_player(self, name):
        """ Add a player to the game"""
        for player in self.players:
            print(f"Debug: {name} checked against {player.name}")
            if name == player.name:
                print("You're already in the game!")
                return
        self.players.append(Player(name))
        print(f"{name} has joined the game!")
        return

    def remove_player(self, name):
        for player in self.players:
            if name == player.name:
                self.players.remove(player)
                print(f"{name} has been removed")
                return
        print(f"{name} could not be found")
        return

class Player:
    """ A person playing along"""
    def __init__(self, name):
        self.name = name
        self.pennys = 10  # All players start with 10 pennies
        self.attacks = 0  # Record of all attempts at pennying
        self.defences = 0  # Record of all attempts on this player
