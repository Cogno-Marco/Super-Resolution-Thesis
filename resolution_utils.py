from typing import Tuple
import math

def input_vars() -> Tuple[int, int, int]:
    repeat = "n"
    choose = "m"
    k,r,f = 0,0,0
    execute = False
    while (choose != "m" or choose != "f" and execute == False):
        choose = input("Variables set manually or by formula? [M/F]: ").lower()
        
        # manual variable setting
        if choose == "m":
            while repeat == "n":
                k = int(input("Enter the camera size: "))
                r = int(input("Enter the target resolution: "))
                f = int(input("Enter how many photos per offset: "))
                print(f"The total photos are {r*f}")
                repeat = input("Proceed? [Y/N] \n").lower()
            execute = True
        
        # calculated variable setting based on input parameters
        elif choose == "f":
            while repeat == 'n':
                r = int(input("Enter the target resolution: "))
                error = float(input("Enter the probability of error [0 - 1]: "))

                f = round(-12 * r * math.log(error / 2)) # theoric photo per offset, calcolated in the thesis
                k = round(-24 * math.pow(r,4) * math.log(error)) # theoric camera size, calculated in the thesis

                # print the numbers
                print(f"The camera size is {k}")
                print(f"The photos per offset are {f}")
                print(f"The total photos are {r*f}")
                repeat = input("Proceed? [Y/N] \n").lower()
            execute = True
        else:
            print("Incorrect typing, please try again")
    
    return k,r,f