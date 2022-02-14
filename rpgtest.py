import random
import math
import json
from time import sleep
import pygame
import os
from cryptography.fernet import Fernet
import base64

def clear():
    os.system('cls')


enemy = 0
ehp = 0
edmg = 0
e_info = ""
enemyAlive = False
block = False

p_data = {"hp":100,"maxhp":100,"resistance":1,"strength":1,"xp":0,"lvl":1,"lvlnext":25,"pinespag":3,"explcard":3,"audio_music":50,"audio_sfx":50,"biome":0} # player save data
recovery_data = p_data


pygame.init()
pygame.mixer.init()
damage_sound = pygame.mixer.Sound("media/damage.wav")
damage_sound.set_volume(p_data["audio_sfx"]/200)


def save(): # saves game data
    data = open("data/playerdata.json", "w")
    data = json.dump(p_data, data)


def load(): # loads game data on startup
    global p_data
    data = open("data/playerdata.json", "r")
    p_data = json.load(data)

def quit():
    clear()
    savegame = input("\nWould you like to save your game? (y/n)\n")

    if savegame.lower() == "y":
        save()
        print("\nSaving...")
        sleep(1)
        exit()

    elif savegame.lower() == "n":
        print ("\nClosing...")
        sleep(1)
        exit()

    else:
        print("\nInvalid option. Please choose one of the options to the right")
        quit()


def xpsystem():
    global p_data
    while p_data["xp"] >= p_data["lvlnext"]:
        p_data["lvl"] += 1
        p_data["strength"] *= 1.1
        p_data["maxhp"] = round(p_data["maxhp"]*1.1)
        p_data["xp"] -= p_data["lvlnext"]
        p_data["lvlnext"] = round(p_data["lvlnext"]*1.5)
        input("\nYour level is now {lvl}!".format(**p_data))


def plaindlg():
    input("The lush green grass dances in motion as the gust of wind brushes itself against the empty hills.")
    input("You keep walking as you see the nearest town getting engulfed by the horizon behind you.")
    clear()

def mountdlg():
    input("The peaks reach far out into the sky. Fortunately, you're almost at the top.")
    input("You feel a sharp blizzard cutting your face, but that doesn't stop you from climbing any further.")
    input("After reaching the top of the tall cliff, you find a giant cave opening.")

def mountdlg2():
    input("As you venture deeper into the cave, some strange crystals on the walls start to glow.")
    input("The cave lits up, revealing an unidentified entity.")
    input("You have no other choice than to fight it.")


def seed():
    seed = random.randint(0,1)
    if seed == 0:
        input("You see an enemy in the distance.")
        spawn()

    elif seed == 1:
        input("You found an item!")
        if p_data["biome"] == 0:
            item = 0 # random.randint(0,1)
            if item == 0:
                p_data["pinespag"] += 1
                input("You found a Pineapple Spaghetti!")
                clear()
            
            else:
                input("Nevermind, it was just the wind.")
                clear()


def spawn():
    global p_data,block,ehp,e_info,edmg
    choice = input("Will you approach it? (y/n)\n")
    if choice.lower() == "y":
        if p_data["biome"] == 0:
            enemy = 0

            if enemy == 0:
                ehp = 200
                edmg = 40
                e_info = f"\n--- Giant Slime ---\nAlthough a mere couple strikes with a sword can do the job, their blow is quite devastating.\nHP: 200\nATK: 40\n"
                input("\nYou encountered a GIANT SLIME!\n")

                while(ehp>0):
                    action()
                        
                    if ehp>0:
                        input("Giant Slime attacks you.")
                        if block == False:
                            dmg = edmg
                        else:
                            dmg = math.trunc(str(edmg*0.3))
                        p_data["hp"] -= dmg
                        if p_data["hp"]<0:
                            p_data["hp"] = 0
                        sleep(0.5)
                        damage_sound.play()
                        input(f"You took {dmg} damage!" + " {hp}/{maxhp}\n".format(**p_data))
                        block = False
                        if p_data["hp"]>0:
                            pass
                        else:
                            ehp = 0
                            input("You died!\n")
                            print("Closing...")
                            exit()
            else:
                input("\nNevermind, there was nothing.")
                clear

        elif p_data["biome"] == 1:
            enemy = 0


    elif choice.lower() == "n":
        input("\nYou decided not to approach the thing.")

    else:
        input("\nSyntax error: not a valid option.")
        spawn()


def action():
    isRunning = True
    while(isRunning):
        clear()
        action = input("Fight | Item | Block | Info >\n")
        if action.lower() == "fight" or action == "1":
            action_fight()
            isRunning = False

        elif action.lower() == "item" or action == "2":
            action_item()
            
        elif action.lower() == "block" or action == "3":
            action_block()
            isRunning = False

        elif action.lower() == "info" or action == "4":
            action_info()

        else:
            input(f"\nThere's no '{action}' option.\n")

def action_fight():
    global ehp,isRunning
    clear()
    input("You attacked the slime.")
    dmg = math.trunc(random.randrange(80,100)*(p_data["strength"]))
    ehp -= dmg

    if ehp<0:
        ehp = 0
    
    sleep(0.5)
    damage_sound.play()
    input(f"You dealt {dmg} damage! {ehp}/200\n")
    if ehp>0:
        pass

    else:
        isRunning = False
        p_data["xp"] += 50
        input("You won! You gained 50 XP!")
        xpsystem()


def action_item():
    global isRunning
    clear()
    item = input("PineSpag ({pinespag}) | ExplCard ({explcard}) > ".format(**p_data))
    if item.lower() == "pinespag":
        if p_data["pinespag"]>0:
            p_data["pinespag"] -= 1
            p_data["hp"] += 200

            if p_data["hp"]>p_data["maxhp"]:
                p_data["hp"] = p_data["maxhp"]

            clear()
            input("You ate Pineapple Spaghetti. You recovered 200 HP. {hp}/{maxhp}".format(**p_data))
            if p_data["hp"] == p_data["maxhp"]:
                input("Your health has been maxed out.\n")
                isRunning = False

        else:
            clear()
            input("You don't have any Pineapple Spaghetti left.\n")

    elif item.lower() == "explcard":
        input("This item has no use yet. ;-;")

    elif item == "":
        clear()

def action_block():
    global block
    block = True
    clear()
    input("You blocked the next attack.\n")

def action_info():
    global ehp
    input(e_info)


def menu_gui():
    isRunning = True
    while (isRunning):
        clear()
        action = input("--- Menu ---\nStats | Items | Shop\nExplore | Settings | Quit > ")

        if action.lower() == "stats":
            stat_gui()

        elif action.lower() == "items":
            inv_gui()

        elif action.lower() == "shop":
            input("\nShop closed...")

        elif action.lower() == "explore":
            isRunning = False
            input("\nYou decided to explore a bit more...\n")
            sleep(1)
            seed()
        
        elif action.lower() == "settings":
            settings = input("\n--- Settings ---\nAudio | Save > ")

            if settings.lower() == "audio":
                clear()
                set_audio = input("\n--- Audio Settings ---\nMusic: {audio_music}\nSFX: {audio_sfx}\n> ".format(**p_data))

                if set_audio.lower() == "music":
                    p_data["audio_music"] = int(input("Change music volume: "))
                    input("\nMusic set to {audio_music}".format(**p_data))
                    clear()

                elif set_audio.lower() == "sfx":
                    p_data["audio_sfx"] = int(input("Change SFX volume: "))
                    input("\nSFX set to {audio_sfx}".format(**p_data))
                    clear()
            elif settings.lower() == "save":
                savegame()

            elif settings == "":
                pass

            else:
                input("Invalid option.")

        elif action == "quit":
            quit()

        else:
            input("\nSyntax error: not a valid option.")


def stat_gui():
    input("\n--- Player Statistics ---\nHealth: {hp}/{maxhp}\nLevel: {lvl}\nExperience: {xp}\nNext Level: {lvlnext}\nResistance: ".format(**p_data) + ((p_data["resistance"]-1)*10) +"\nStrength: " + ((p_data["strength"]-1)*10) + "\n")

def inv_gui():
    input("\nPineSpag ({pinespag}) | ExplCard ({explcard}) > ".format(**p_data))

def savegame():
    saveRunning = True
    while(saveRunning):
        clear()
        savegame = input("\n--- Save Settings ---\nSave Game | Delete Save | Close > ")

        if savegame.lower() == "save":
            save()
            input("\nGame saved!")

        elif savegame.lower() == "delete":
            yesno = input("\nAre you sure you want to permanently delete your save data? (y/n)\n")

            if yesno.lower() == "y":
                print ("\nDeleting save file...")
                sleep(1)
                data = open("data/playerdata.json", "w")
                data = json.dump(recovery_data, data)
                input("Save file successfully deleted!")
                print("Closing...")
                sleep(1)
                exit()

            elif yesno.lower() == "n":
                pass

            else:
                input("\nInvalid option.")

        elif savegame == "":
            saveRunning = False

        else:
            input("\nInvalid option. Please choose one of the options above.")



# game start

load()
xpsystem()
clear()
welcome = input("Welcome to M3ch4n1kk's RPG test v0.2.0(alpha)! Would you like to play? (y/n)\n")

if welcome.lower() == "y":
    input("\nYou went through a portal, not knowing where you'll end up...\n")
    clear()
    sleep(1)
    p_data["biome"] = 0
    if p_data["biome"] == 0:
        input("--- Biome: Plains ---\n")
        gameRunning = True
        while(gameRunning):
            menu_gui()


    elif p_data["biome"] == 1:
        input("--- Biome: Mountains ---")
        mountdlg()
        choice = input("Go inside the cave? (y/n) ")
        if choice.lower() == "y":
            mountdlg2()
            gameRunning = True
            while(gameRunning):
                menu_gui()

        elif choice.lower() == "n":
            input("\nYou decide not to go in.")
            input("Your hand slips from the cliff's edge, and fall to the ground.\nYou Died!")
            quit()



    elif p_data["biome"] == 2:
        input("--- Biome: Forest ---")
        spawn()



    else:
        input("--- Biome: Underworld ---")


elif welcome.lower() == "n":
    input("\nSee you next time then!")

else:
    input("\nI didn't quite get that. Try restarting the program.")
    exit()

quit()