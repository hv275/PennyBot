import random
import discord
import threading
import numpy as np
import math

class Session:
    """ Represents a round of pennying"""
    def __init__(self):
        self.players = []
    def penny(self, offenceName, defenceName, vchannels):
        """ A pennying event
        
        offence player is attacking the defence player
        """
        offence = self.get_player(offenceName)
        defence = self.get_player(defenceName)
        print(f"Penny event: {offenceName} ==> {defenceName}")
        if self.same_channel_check(offenceName, defenceName, vchannels):
        
            # check offence is registered in the game
            if offence not in self.players:
                print("Player not registered - please sign in "
                      "before trying to penny someone.\n")
                return ("Player not registered - please sign in "
                        "before trying to penny someone.")

            # check defence is registered in the game
            elif defence not in self.players:
                print("Player not registered - make sure your "
                      "target has signed in.\n")
                return ("Player not registered - make sure your "
                      "target has signed in.")

            # check offence has a penny
            elif offence.pennys <= 0:
                print("Insufficient funds! Go find some pennies "
                      "before you come back!")
                return ("Insufficient funds! Go find some pennies "
                      "before you come back!")

            elif offence.p_cooldown is True:
                print("Hold on a bit! You're going too quick!\n")
                return "Hold on a bit! You're going too quick!"

            else:
                offence.blocking = False
                prob = self.probability((offence.attackstat - defence.defencestat))
                print(f"Probability of success: {prob:.4f}")
                if random.random() < (1-prob): #all of our probabilities were the wrong way round
                    # Attempt failed
                    offence.p_wait()
                    offence.pennys -= 1
                    defence.pennys += 1
                    defence.defences += 1
                    defence.defencestat += prob
                    print(offence)
                    print(defence)
                    print(f"{offence.name} tried to penny {defence.name}, but missed.\n")
                    return f"{offence.name} tried to penny {defence.name}, but missed."
                else:
                    # Attempt succeeded
                    offence.pennys -= 1
                    offence.attacks += 1
                    defence.pennys += 1
                    if defence.blocking is True:
                        offence.p_wait()
                        defence.defencestat += 1.5*prob
                        print(f"{offence.name} tried to penny
                              f"{defence.name}, but {defence.name}"
                              f" was holding their glass!\n")
                        return (f"{offence.name} tried to penny "
                                f"{defence.name}, but {defence.name}"
                                f" was holding their glass!")
                    else:
                        offence.attackstat += 1.0-prob
                        defence.defencestat += prob/3.0 
                        print(offence)
                        print(defence)
                        print(f"{offence.name} pennied {defence.name}\n!")
                        return f"{offence.name} pennied {defence.name}!"
        else:
            print(f"{offence.name} tried to penny {defence.name}, "
                  f"but target is sat too far. You have to be sat "
                  f"the the same table.\n")
            return (f"{offence.name} tried to penny {defence.name}, "
                  f"but target is sat too far. You have to be sat "
                  f"the the same table.")


    def snipe(self, offenceName, defenceName, vchannels):
        """ A sniping event
        
        offence player is attacking the defence player"""
        offence = self.get_player(offenceName)
        defence = self.get_player(defenceName)
        print(f"Snipe event: {offenceName} ==> {defenceName}")

        if self.same_channel_check(offenceName, defenceName, vchannels):
        
            # check offence is registered in the game
            if offence not in self.players:
                print("Player not registered - please sign in "
                      "before trying to penny someone.\n")
                return ("Player not registered - please sign in "
                        "before trying to penny someone.")
            # check defence is registered in the game
            elif defence not in self.players:
                print("Player not registered - make sure your "
                      "target has signed in.\n")
                return ("Player not registered - make sure your "
                        "target has signed in.")

            # check offence has a penny
            elif offence.pennys <= 0:
                print("Insufficient funds! Go find some pennies "
                      "before you come back!\n")
                return "Insufficient funds! Go find some pennies before you come back!"
            elif offence.level < 3:
                print("Level not high enough. Available from level 3 and above.\n")
                return "Level not high enough. Available from level 3 and above."
            elif offence.p_cooldown is True:
                print("Hold on a bit! You're going too quick!\n")
                return "Hold on a bit! You're going too quick!"
            else:
                offence.blocking = False
                print(f"Probability of succes: {offence.snipesuccess}")
                if random.random() > offence.snipesuccess:
                    offence.p_wait()
                    # Attempt failed
                    print(f"{offence.name} tried to snipe {defence.name}, "
                          f"but missed.\n")
                    offence.pennys -= 1
                    defence.pennys += 1
                    defence.defences += 1
                    #print(offence)
                    #print(defence)
                    return f"{offence.name} tried to snipe {defence.name}, but missed."
                else:
                    # Attempt succeeded
                    offence.pennys -= 1
                    offence.attacks += 1
                    defence.pennys += 1
                    offence.attackstat += 3*(1.0-offence.snipesuccess)
                    #print(offence)
                    #print(defence)
                    print(f"{offence.name} sniped {defence.name}!\n")
                    return f"{offence.name} sniped {defence.name}!"
        else:
            print(f"{offence.name} tried to snipe {defence.name}, "
                  f"but target is sat too far. You have to be sat "
                  f"the the same table\n")
            return f"{offence.name} tried to snipe {defence.name}, "
                  f"but target is sat too far. You have to be sat "
                  f"the the same table")


    def block(self, playerName):
        print(" Session.block() called")
        player = self.get_player(playerName)
        player.block()
            

    def add_player(self, name):
        """ Add a player to the game"""
        for player in self.players:
            print(f"Debug: {name} checked against {player.name}")
            if name == player.name:
                print("You're already in the game!\n")
                return "You're already in the game!"
        self.players.append(Player(name))
        print(f"{name} has joined the game!\n")
        return f"{name} has joined the game!"

    def remove_player(self, name):
        for player in self.players:
            if name == player.name:
                self.players.remove(player)
                print(f"{name} has been removed\n")
                return f"{name} has been removed"
        print(f"{name} could not be found\n")
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
        scorelist = []
        for player in self.players:
            playerlist.append(player)
        return(playerlist)
            
    def get_balance(self, playerName):
        player = self.get_player(playerName)
        return f"You have {player.pennys}p"

    def cashinjection(self, player_name, num):
        player = self.get_player(player_name)
        player.pennys += int(num)
        return(f"{player.name} was given {num} pennies. New balance: {player.pennys}")


    def give(self,giver,reciever, amount):
        benefactor = self.get_player(giver)
        urchin = self.get_player(reciever)
        amount = int(amount)
        if benefactor != None and urchin != None:
            if benefactor.pennys >= amount:
                benefactor.pennys -= int(amount)
                urchin.pennys += amount
                return(f"{benefactor.name} has kindly given {urchin.name} {str(amount)}p.")
            else:
                return "You do nat have enough pennies for this. Find some more"
        else:
            return "Player not found, check that the name is correct and that they are in the game"


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

    def probability(self, x):
        #adjust constansts for scaling, current set up seems reasonable
        #b is probabolity for when attack and defense are eqaul
        #a affects how quickly the probability grows with disparity
        b=0.55
        a=0.2
        return (b*np.exp(a*x))/(b*np.exp(a*x)-b+1)

    def check(self, offenceName, defenceName):
        #checks the player stats and prints them out
        offence = self.get_player(offenceName)
        defence = self.get_player(defenceName)
        if offence == None:
            return f"{offenceName}, you haven't joined the game yet!"
        elif defence == None:
            return f"{defenceName} is not in the game yet."
        else offence != None and defence != None:
            print(f"""
            Here is information on the target
            Name:        {defence.name}
            Attackstat:  {defence.attackstat:.2f}
            Defencestat: {defence.defencestat:.2f}
            Level:       {defence.level:.0f}
            Attacks:     {defence.attacks}
            Defences:    {defence.defences}\n""")

            return f"""
            Here is information on the target
            Name:        {defence.name}
            Attackstat:  {defence.attackstat:.2f}
            Defencestat: {defence.defencestat:.2f}
            Level:       {defence.level:.0f}
            Attacks:     {defence.attacks}
            Defences:    {defence.defences}"""






class Player:
    """ A person playing along"""
    def __init__(self, name):
        self.name = name
        self.attackstat = 1.0 # attack level
        self.defencestat = 1.0 #defense level
        self.pennys = 10  # All players start with 10 pennies
        self.attacks = 0  # Record of all attempts at pennying
        self.defences = 0  # Record of all attempts on this player
        self.blocking = False
        self.on_cooldown = False
        self.p_cooldown = False
        print("Setting up timers")
        self.t1 = threading.Timer(30, self.reset_block)
        self.t2 = threading.Timer(120, self.reset_cooldown)
        self.t3 = threading.Timer(10, self.reset_penny)
        print("  Timers set")

    #storing level as a property so it auto updated, usage same as a normal property
    @property
    def level(self):
        return np.floor(1 + math.log((self.attackstat + self.defencestat),2)) #formula for level using log base 2 (Note:floor rounds down)

    #used for score sorting purposes
    @property
    def purelevel(self):
        return (1 + math.log((self.attackstat + self.defencestat),2))


    @property
    def snipesuccess(self):
        #test to optimise
        b=0.2
        a=0.2
        return (b*np.exp(a*self.attackstat))/(b*np.exp(a*self.attackstat)-b+1)


    def block(self):
        print(f"Player.block() called by {self.name}")
        if self.on_cooldown is True:
            print("  That ability is on cooldown - you'll need to wait"
            return "That ability is on cooldown - you'll need to wait"
        else:
            self.on_cooldown = True
            self.blocking = True
            print("  Starting timers")
            print(f"  Block_pre = {self.blocking}")
            self.t1.start()
            print("  t1 started")
            print(f"  Cooldown_pre = {self.on_cooldown}")
            self.t2.start()
            print("  t2 started")
            return "Blocking glass for 30 seconds"

    def p_wait(self):
        print(f"{self.name} on Penny Cooldown")
        self.p_cooldown = True
        self.t3.start()

    def reset_penny(self):
        self.p_cooldown = False
        print(f"        {self.name} Penny Cooldown done")
        self.t3 = threading.Timer(10, self.reset_penny)

    def reset_block(self):
        self.blocking = False
        print(f"        {self.name}: blocking done")
        self.t1 = threading.Timer(30, self.reset_block)

    def reset_cooldown(self):
        self.on_cooldown = False
        print(f"        {self.name}: block cooldown done")
        self.t2 = threading.Timer(120, self.reset_cooldown)

    #for easier printing of function
    def __repr__(self):
        return f"""
        Name: {self.name}
        Attackstat: {str(self.attackstat)}
        Defencestat: {str(self.defencestat)}
        Level: {str(self.level)}
        Attacks: {str(self.attacks)}
        Defences: {str(self.defences)}"""
        
