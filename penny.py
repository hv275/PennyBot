import random

class Session:
    """ Represents a round of pennying"""
    def __init__(self):
        self.players = []

    def penny(self, offenceName, defenceName):
        """ A pennying event

        offence player is attacking the defence player"""
        offence = self.get_player(offenceName)
        defence = self.get_player(defenceName)
        
        # check offence is registered in the game
        if offence not in self.players:
            print("Player not registered - please sign in "
                  "before trying to penny someone.")
            return "error"
        # check defence is registered in the game
        elif defence not in self.players:
            print("Player not registered - make sure your "
                  "target has signed in.")
            return "Player not registered"
        # check offence has a penny
        elif offence.pennys <= 0:
            print("Insufficient funds! Go find some pennies "
                  "before you come back!")
            return "Insufficient funds! Go find some pennies before you come back!"
        else:
            if random.random() < 0.5:
                # Attempt failed
                print(f"{offence.name} tried to penny {defence.name}, "
                      f"but missed.")
                offence.pennys -= 1
                defence.pennys += 1
                return f"{offence.name} tried to penny {defence.name}, but missed."
            else:
                # Attempt succeeded
                print(f"@{offence.name} pennied @{defence.name}!")
                return f"@{offence.name} pennied @{defence.name}!"
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
                return "You're already in the game!"
        self.players.append(Player(name))
        print(f"@{name} has joined the game!")
        return f"@{name} has joined the game!"

    def remove_player(self, name):
        for player in self.players:
            if name == player.name:
                self.players.remove(player)
                print(f"{name} has been removed")
                return f"{name} has been removed"
        print(f"{name} could not be found")
        return f"{name} could not be found"

    def get_player(self, playerName):
        print(f"Name is '{playerName}', type {type(playerName)}")
        for player in self.players:
            print(f"  Checking '{player.name}', type {type(player.name)}")
            if playerName == player.name:
                return player
        return None

    """if we need to show who is in the game"""
    def playershow(self):
        playerlist = []
        for player in self.players:
            playerlist.append(player.name)
        return(playerlist)
            
    def get_balance(self, playerName):
        player = self.get_player(playerName)
        return f"You have {player.pennys}p"

class Player:
    """ A person playing along"""
    def __init__(self, name):
        self.name = name
        self.pennys = 10  # All players start with 10 pennies
        self.attacks = 0  # Record of all attempts at pennying
        self.defences = 0  # Record of all attempts on this player
