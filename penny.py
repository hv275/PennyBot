import random
import discord
import threading
import numpy as np

class Session:
    """ Represents a round of pennying"""
    def __init__(self):
        self.players = []

    def penny(self, offenceName, defenceName, vchannels):
        """ A pennying event
        
        offence player is attacking the defence player"""
        offence = self.get_player(offenceName)
        defence = self.get_player(defenceName)

        if self.same_channel_check(offenceName, defenceName, vchannels):
        
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
                    offence.pennys -= 1
                    defence.pennys += 1
                    defence.defences += 1
                    defence.defencestat += offence.prob
                    print(offence)
                    print(defence)
                    print(f"{offence.name} tried to penny {defence.name}, but missed.")
                    return f"{offence.name} tried to penny {defence.name}, but missed."
                else:
                    # Attempt succeeded
                    offence.pennys -= 1
                    offence.attacks += 1
                    defence.pennys += 1
                    if defence.blocking is True:
                        defence.defencestat += 1.5*offence.prob
                        print(f"{offence.name} tried to penny {defence.name}, but {defence.name}"
                              f" was holding their glass!")
                        return (f"{offence.name} tried to penny {defence.name}, but {defence.name}"
                              f" was holding their glass!")
                    else:
                        offence.attackstat += 1.0-offence.prob
                        defence.defencestat += offence.prob/3.0 #review the mechanics as very basic atm, we want to compare attack/defense ideally
                        print(offence)
                        print(defence)
                        print(f"{offence.name} pennied {defence.name}!")
                        return f"{offence.name} pennied {defence.name}!"
        else:
            print(f"{offence.name} tried to penny {defence.name}, but target is sat too far. You have to be sat the the same table")
            return f"{offence.name} tried to penny {defence.name}, but target is sat too far. You have to be sat the the same table"


    def snipe(self, offenceName, defenceName, vchannels):
        """ A sniping event
        
        offence player is attacking the defence player"""
        offence = self.get_player(offenceName)
        defence = self.get_player(defenceName)

        if self.same_channel_check(offenceName, defenceName, vchannels):
        
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
                if random.random() < 0.2:
                    # Attempt failed
                    print(f"{offence.name} tried to snipe {defence.name}, "
                          f"but missed.")
                    offence.pennys -= 1
                    defence.pennys += 1
                    defence.defences += 1
                    defence.defencestat += offence.prob
                    print(offence)
                    print(defence)
                    return f"{offence.name} tried to snipe {defence.name}, but missed."
                else:
                    # Attempt succeeded
                    offence.pennys -= 1
                    offence.attacks += 1
                    defence.pennys += 1
                    offence.attackstat += 1.0-offence.prob
                    defence.defencestat += offence.prob/0.3 #the way this stuff will affect the snipe ability
                    print(offence)
                    print(defence)
                    print(f"{offence.name} sniped {defence.name}!")
                    return f"{offence.name} sniped {defence.name}!"
        else:
            print(f"{offence.name} tried to snipe {defence.name}, but target is sat too far. You have to be sat the the same table")
            return f"{offence.name} tried to snipe {defence.name}, but target is sat too far. You have to be sat the the same table"



    def block(self, playerName):
        print(" Session.block() called")
        player = self.get_player(playerName)
        player.block()
            

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
                print("Player found")
                return player
        print("Player not found")
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
        self.attackstat = 1.0 # attack level
        self.defencestat = 1.0 #defense level
        self.prob = 0.5 #should really be linked to Session and worked out by using a formular with attack and defence
        self.snipesuccess = 0.1 #success for a successful snipe, need formulae to scale
        self.level = 1 + np.floor(np.log2(self.attackstat + self.defencestat)) #formula for level (to be reviewed) (Note:floor rounds down)
        self.pennys = 10  # All players start with 10 pennies
        self.attacks = 0  # Record of all attempts at pennying
        self.defences = 0  # Record of all attempts on this player
        self.blocking = False
        self.on_cooldown = False
        print("Setting up timers")
        self.t1 = threading.Timer(5, self.reset_block)
        self.t2 = threading.Timer(10, self.reset_cooldown)
        print("  Timers set")

    def block(self):
        print(" Player.block() called")
        if self.on_cooldown is True:
            return "That ability is on cooldown - you'll need to wait"
        else:
            self.on_cooldown = True
            self.blocking = True
            print("Starting timers")
            print(f"  Block_pre = {self.blocking}")
            self.t1.start()
            print("  t1 started")
            print(f"  Cooldown_pre = {self.on_cooldown}")
            self.t2.start()
            print("  t2 started")
            return "Blocking glass for 30 seconds"

    def reset_block(self):
        self.blocking = False
        print(f"Blocking_post = {self.blocking}")
        self.t1 = threading.Timer(5, self.reset_block)

    def reset_cooldown(self):
        self.on_cooldown = False
        print(f"Cooldown_post = {self.on_cooldown}")
        self.t2 = threading.Timer(10, self.reset_cooldown)

    #for easier printing of function
    def __repr__(self):
        return f"""
        Name: {self.name}
        Attackstat: {str(self.attackstat)}
        Defencestat: {str(self.defencestat)}
        Level: {str(self.level)}
        Attacks: {str(self.attacks)}
        Defences: {str(self.defences)}"""
        
