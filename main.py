import keyboard
import time
import winsound
import wave
from scipy.io import wavfile

#=========================================
# Variables for the *beep* sound.
#=========================================

frequency = 2500
duration = 100
dd_frequency = 1000
dot_duration = 100
dash_duration = 300

###########################################
# The function below takes a list as a    #
# parameter, which is coded in 0s and 1s, #
# and decodes it using morse code.        #
###########################################

def decoder(encoded_list):
    """
        DASH = 0
        DOT  = 1

        MORSE TREE:
                                    <- DASH         DOT ->
                                  ___________START__________
                                /                           \
                              T                              E
                             / \                            / \
                           /    \                         /    \
                         /       \                      /       \
                       /          \                   /          \
                     /             \                /             \
                    M              N               A               I
                   / \            / \             / \             / \
                 /    \         /    \          /    \          /    \
               O      G       K       D       W       R       U       S
              / \    / \     / \     / \     / \     / \     / \     / \
             -  .   Q   Z   Y   C   X   B   J   P       L   -   F   V   H

    :return: None
    """
    morse_tree = [
        [
            [
                ["-","-","O"],  #0000,0001,0002
                ["Q","Z","G"],  #0010,0011,0012
                "M"],           #002
            [
                ["Y","C","K"],  #0100,0101,0102
                ["X","B","D"],  #0110,0111,0112
                "N"],           #012
            "T"],               #02
        [
            [
                ["J","P","W"],  #1000,1001,1002
                ["-","L","R"],  #1010,1011,1012
                "A"],           #102
            [
                ["-","F","U"],  #1100,1101,1102
                ["V","H","S"],  #1110,1111,1112
                "I"],           #112
            "E"]                #12
    ]

    command_string = "morse_tree"
    i = 0
    while i < 4:
        if encoded_list[i] == 2:
            command_string += "[" + str(encoded_list[i]) + "]"
            break
        command_string += "[" + str(encoded_list[i]) + "]"
        i += 1
    letter = eval(command_string)
    return letter

###############################################################
#  This function decodes a WAV file (which is coded in morse) #
###############################################################

def user_input():

    dot = input("Please select the dot button, by pressing it: ")
    dash = input("Please select the dash button, by pressing it: ")

    letter = []
    text = ""
    sum_of_blank = 0
    while True:
        if keyboard.is_pressed("q"):
            break
        elif keyboard.is_pressed(dot) and len(letter) < 4 and sum_of_blank > 0:
            sum_of_blank = 0
            letter.append(1)
            winsound.Beep(dd_frequency, dot_duration)
        elif keyboard.is_pressed(dash) and len(letter) < 4 and sum_of_blank > 0:
            sum_of_blank = 0
            letter.append(0)
            winsound.Beep(dd_frequency, dash_duration)
        else:
            if len(letter) > 0 and sum_of_blank > 15:
                if len(letter) < 4:
                    letter.append(2)
                text += decoder(letter)
                winsound.Beep(frequency, duration)
                letter = []
                sum_of_blank = 0
            if sum_of_blank > 35:
                print()
                winsound.Beep(frequency, duration)
                text += " "
                sum_of_blank = 0
            sum_of_blank += 1
        time.sleep(0.05)
    print()
    print(text)
    return None

#################################################
# This function decodes only WAV file.          #
#################################################

def file_decoder(file_name = "/Users/Lucky Luke/morsecode.wav"):

#This function decodes only WAV file

    with wave.open(file_name, "rb") as something:
        samp, data = wavfile.read(file_name)


    first = 0
    second = - 1
    i = 1
    while first + 50 > second:
        j = i
        temp = data[i]
        s = 0
        while s < 10:
            if data[i] == temp:
                s += 1
            else:
                s = 0
            i += 1
        if first == 0 and i - j > 100:
            first = i - j
        elif i - j > 100:
            second = i - j
        if first - 50 > second and second != -1:
            first, second = second, first
    dot_dash = (first + second)/2
    morse_code = []
    text = ""
    temp = data[0]
    l = 0
    s = 0
    for k in range(len(data)):
        if data[k] == temp:
            s += 1
        else:
            s = 0
        temp = data[k]
        if s > 10 and s < dot_dash:
            if k - l > 100:
                if k-l - 50 < first:
                    morse_code.append(1)
                else:
                    morse_code.append(0)
            l = k
        elif s > dot_dash and s < second*2:
            if morse_code != []:
                morse_code.append(2)
                text += decoder(morse_code)
                morse_code = []
            l = k
        elif s > second*2:
            text += " "
            s = 0
            l = k
    print(text)
    return None

#=======================================================
# MAIN PROGRAM
#=======================================================

print("1. Decode a WAV file\n2. Input code by user\n3. Exit")
mode = input()
while mode != "1" and mode != "2" and mode != "3":
    print("Incorrect input. Please type one of the following numbers => 1, 2, 3")
    mode = input()
if mode == "1":
    print("Type the path of the file you want to decode.")
    file_path = input()
    file_decoder(file_path)
elif mode == "2":
    print("If you want to quit press 'q'.")
    user_input()

