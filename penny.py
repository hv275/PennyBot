import random
import discord
import threading

class Session:
    """ Represents a round of pennying"""
    def __init__(self):
        self.players = []

    def penny(self, offenceName, defenceName, vchannels):
        """ A pennying event
           
        offence player is attacking the defence player"""
        if self.same_channel_check(offenceName, defenceName, vchannels):
            offence = self.get_player(offenceName)
            defence = self.get_player(defenceName)
        
            # check offence is registered in the game
            if offence not in self.players:
                print("Player not registered - please sign in "
                      "before trying to penny someone.")
                return "Player not registered"
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
                    print(f"{offence.name} pennied {defence.name}!")
                    return f"{offence.name} pennied {defence.name}!"
                    offence.pennys -= 1
                    offence.attacks += 1
                    defence.pennys += 1
                    defence.defences += 1
        else:
            return "Target too far to penny. You have to be sat the the same table"

    def block(self, playerName):
        player = self.get_player(playerName)
        if player.on_cooldown is True:
            return "That ability is on cooldown - you'll need to wait"
        else:
            cooldown_timer = True
            blocking = True
            print("  Setting up timers")
            t1 = threading.Timer(30, reset_block(player))
            t2 = threading.Timer(120, reset_cooldown(player))
            print("  Starting timers")
            t1.start()
            t2.start()
            return "Blocking glass for 30 seconds"
            
    def reset_cooldown(self, player):
        player.on_cooldown = False

    def reset_block(self, player):
        player.block = False

    def add_player(self, name):
        """ Add a player to the game"""
        for player in self.players:
            print(f"Debug: {name} checked against {player.name}")
            if name == player.name:
                print("You're already in the game!")
                return "You're already in the game!"
        self.players.append(Player(name))
        print(f"{name} has joined the game!")
        return f"{name} has joined the game!"

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

    def cashinjection(self, player_name, num):
        player = self.get_player(player_name)
        player.pennys += int(num)
        return(f"{player.name} was given {num} pennies. New balance: {player.pennys}")

    def same_channel_check(self, offense, defense, vchannels):
        print("test")
        for channel in vchannels:
            print(channel)
            members = channel.members
            for i in members:
                if i.display_name==offense:
                    for j in members:
                        if j.display_name == defense:
                            return True
        return False





class Player:
    """ A person playing along"""
    def __init__(self, name):
        self.name = name
        self.pennys = 10  # All players start with 10 pennies
        self.attacks = 0  # Record of all attempts at pennying
        self.defences = 0  # Record of all attempts on this player
        self.blocking = False
        self.on_cooldown = False
