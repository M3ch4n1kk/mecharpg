import random
import math
import json
from time import sleep
import pygame

pygame.init()
pygame.mixer.init()
damage_sound = pygame.mixer.Sound("media/damage.wav")
damage_sound.set_volume(0.2)


biome = 0
enemy = 0
ehp = 0
enemyAlive = False
block = False

p_inv = {"pinespag":3,"explcard":3} # player inventory

p_st = {"hp":100,"maxhp":100,"armor":1,"strength":1,"xp":99999,"lvl":0,"lvlnext":25} # player stats


def save(): # saves game data
    data = open("data/playerdata.json", "w")
    data = json.dump(p_st, data)


def load(): # loads game data on startup
    data = open("data/playerdata.json", "r")
    p_st = json.load(data)


def xpsystem():
    global p_st
    while p_st["xp"] >= p_st["lvlnext"]:
        p_st["lvl"] += 1
        p_st["strength"] += 0.1
        p_st["maxhp"] = round(p_st["maxhp"]*1.1)
        p_st["hp"] = p_st["maxhp"]
        p_st["xp"] -= p_st["lvlnext"]
        p_st["lvlnext"] = round(p_st["lvlnext"]*1.5)
        print("Your level is now {lvl}!\n".format(**p_st))


def plaindlg():
    input("\nThe lush green grass dances in motion as the gust of wind brushes itself against the empty hills.")
    input("You keep walking as you see the nearest town getting engulfed by the horizon behind you.")
    input("Suddenly, a silhoulette appears front of you.")

def mountdlg():
    input("\nThe peaks reach far out into the sky. Fortunately, you're almost at the top.")
    input("You feel a sharp blizzard cutting your face, but that doesn't stop you from climbing any further.")
    input("After reaching the top of the tall cliff, you find a giant cave opening.\n")

def mountdlg2():
    input("As you venture deeper into the cave, some strange crystals on the walls start to glow.")
    input("The cave lits up, revealing an unidentified entity.")
    input("You have no other choice than to fight it.\n")


def spawn():
    choice = input("Will you approach it? (y/n)\n")
    if choice == "y":
        if biome == 0:
            enemy = 0

            if enemy == 0:
                enemyAlive = True
                global p_st,p_inv,block
                ehp = 200
                input("\nYou encountered a GIANT SLIME! 💀\n")

                while(enemyAlive):
                    action = input("Fight | Item | Block | Info >\n")
                    if action == "fight":
                        input("\nYou attacked the slime.")
                        dmg = math.trunc(random.randrange(120,150)*p_st["strength"])
                        ehp -= dmg

                        if (ehp)<0:
                            ehp = 0
                        
                        sleep(0.5)
                        damage_sound.play()
                        input(f"You dealt {dmg} damage! {ehp}/200\n")
                        if (ehp)>0:
                            pass
                        else:
                            p_st["xp"] += 100
                            input("You won! You gained 100 XP!\n")
                            xpsystem()
                            input()
                            enemyAlive = False

                    elif action == "item":
                        item = input("\nPineSpag ({p_inv[pinespag]}) | ExplCard ({p_inv[explcard]})> ")
                        if item == "pinespag":
                            if p_inv["pinespag"]>0:
                                p_inv["pinespag"] -= 1
                                p_st["hp"] += 80

                                if p_st["hp"]>p_st["maxhp"]:
                                    p_st["hp"] = p_st["maxhp"]

                                input("You ate Pineapple Spaghetti. You restored 80 health. {hp}/{maxhp}".format(**p_st))
                                if p_st["hp"]==p_st["maxhp"]:
                                    input("Your health has been maxed out.\n")

                            else:
                                input("You don't have any Pineapple Spaghetti left.\n")
                        
                    elif action == "block":
                        block = True
                        input("You blocked the next attack.\n")
                    elif action == "info":
                        input("- Giant Slime -\nAlthough a mere couple strikes with a sword can do the job, their blow is quite devastating.\nHP: 200\nATK: 40\n")
                    else:
                        input(f"There's no '{action}' option.\n")
                        
                    if enemyAlive == True:
                        input("Giant Slime attacks you.")
                        if block == False:
                            dmg = 40
                        else:
                            dmg = math.trunc(40*0.3)
                        p_st["hp"] -= dmg
                        if p_st["hp"]<0:
                            p_st["hp"] = 0
                        input(f"You took {dmg} damage!" + " {hp}/{maxhp}\n".format(**p_st))
                        block = False
                        if p_st["hp"]>0:
                            pass
                        else:
                            input("You died!\n")
                            input("Exiting...")
                            sleep(1)
    elif choice == "n":
        input("You decided not to approach the thing.\n")
    else:
        input("Invalid option. Please choose one of the options to the right.\n")
        spawn()

def stat_gui():
    global p_st
    input("--- Player Statistics ---\nHealth: {hp}\nLevel: {lvl}\nExperience: {xp}\nNext Level: {lvlnext}\nArmor: {armor}\nStrength: {strength}\n".format(**p_st))


# game start

load()
xpsystem()
welcome = input("Welcome to M3ch4n1kk's RPG test! Would you like to play? (y/n)\n")

if welcome == "y":
    input("\nYou went through a portal, not knowing where you'll end up.")
    biome = 0
    if biome == 0:
        input("\n--- Biome: Plains ---")
        plaindlg()
        spawn()
        
    elif biome == 1:
        input("--- Biome: Mountains ---")
        mountdlg()
        choice = input("Go inside the cave? (yes/no) ")
        if choice == "yes":
            mountdlg2()
        else:
            input("You decide not to go in.")
            input("Your hand slips from the cliff's edge, and fall to the ground.\nYou Died!")



    elif biome == 2:
        input("--- Biome: Forest ---")
        spawn()



    else:
        input("--- Biome: Underworld ---")

        
    

elif welcome == "n":
    input("See you next time then!")

else:
    input("I didn't quite get that. Try restarting the program.")


def savegame():
    savegame = input("Would you like to save your game? (y/n)")

    if savegame == "y":
        save()
        print("Saving...")
        sleep(1)

    elif savegame == "n":
        print ("Closing...")
        sleep(1)

    else:
        print("Invalid option. Please choose one of the options to the right")
        savegame()

savegame()