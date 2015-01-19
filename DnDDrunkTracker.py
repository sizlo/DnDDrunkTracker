# ==============================================================================
# Imports
# ------------------------------------------------------------------------------
import random
import os

# ==============================================================================
# Globals
# ------------------------------------------------------------------------------
gModifiers = {
  "str": 0,
  "dxt": 0,
  "con": 0,
  "int": 0,
  "wis": 0,
  "cha": 0,
  "ext": 0
}

gDrinkDCs = {
  "l": 5,
  "light": 5,
  "m": 10,
  "medium": 10,
  "s": 15,
  "strong": 15
}

gSize = "medium"

gSizeModifers = {
  "s": -1,
  "small" : -1,
  "m": 0,
  "medium": 0,
  "l": 1,
  "large": 1
}

gDrunkLevel = 0
gMaxDrunkLevel = 6
gFailedSavingThrows = 0
gMaxFailedSavingThrows = 3
gSavingThrowDC = 15



# ==============================================================================
# getInt
# Take an integer from user input
# ------------------------------------------------------------------------------
def getInt(message):
  try:
    strVal = raw_input(message)
    return int(strVal)
  except ValueError:
    print("%s is not an integer, try again" % (strVal))
    return getInt(message)

# ==============================================================================
# getModifiers
# Take input from user for all current stat modifiers
# ------------------------------------------------------------------------------
def getModifiers():
  global gModifiers

  gModifiers["str"] = getInt("Enter your current strength modifer > ")
  gModifiers["dxt"] = getInt("Enter your current dexterity modifer > ")
  gModifiers["con"] = getInt("Enter your current constitution modifer > ")
  gModifiers["int"] = getInt("Enter your current intelligence modifer > ")
  gModifiers["wis"] = getInt("Enter your current wisdom modifer > ")
  gModifiers["cha"] = getInt("Enter your current charisma modifer > ")
  gModifiers["ext"] = getInt("Enter any extra modifier for drinking > ")

# ==============================================================================
# getSize
# Get the size of the character from user input
# ------------------------------------------------------------------------------
def getSize():
  global gSize

  sizes = ["s", "small", "m", "medium", "l", "large"]
  size = raw_input("Enter your characters size (small, medium, large) > ")
  while size not in sizes:
    print("%s is not a valid size, try again" % (size))
    size = raw_input("Enter your characters size (small, medium, large) > ")
  gSize = size

# ==============================================================================
# printModifiers
# Print the current stored modifiers for all stats
# ------------------------------------------------------------------------------
def printModifiers():
  print("Str: %+d, Dxt: %+d, Con: %+d, Int: %+d, Wis: %+d, Cha: %+d" % (
    gModifiers["str"],
    gModifiers["dxt"],
    gModifiers["con"],
    gModifiers["int"],
    gModifiers["wis"],
    gModifiers["cha"]))

# ==============================================================================
# getDrinkStrength
# Get the strength of drink from the user
# ------------------------------------------------------------------------------
def getDrinkStrength():
  drinkStrengths = ["l", "light", "m", "medium", "s", "strong"]
  drinkStrength = raw_input("Enter strength of drink taken (light, medium, strong) > ")
  while drinkStrength not in drinkStrengths:
    print("%s is not a valid strength, try again" % (drinkStrength))
    drinkStrength = raw_input("Enter strength of drink taken (light, medium, strong) > ")
  return drinkStrength

# ==============================================================================
# rollD20
# Generate a random number from 1 to 20
# ------------------------------------------------------------------------------
def rollD20():
  roll =  random.randint(1, 20)
  return roll

# ==============================================================================
# updateModifiers
# Update stat modifiers based on drunk level
# ------------------------------------------------------------------------------
def updateModifiers():
  global gModifiers

  if gDrunkLevel == 1:
    gModifiers["cha"] += 2
  elif gDrunkLevel == 2:
    gModifiers["cha"] += 1
    gModifiers["dxt"] -= 1
  elif gDrunkLevel == 3:
    gModifiers["cha"] += 1
    gModifiers["dxt"] -= 1
    gModifiers["wis"] -= 1
  elif gDrunkLevel == 4:
    gModifiers["dxt"] -= 1
    gModifiers["wis"] -= 1
  elif gDrunkLevel == 5:
    gModifiers["dxt"] -= 1
    gModifiers["wis"] -= 1
  elif gDrunkLevel == 6:
    gModifiers["cha"] -= 4
    gModifiers["dxt"] -= 1
    gModifiers["wis"] -= 1

# ==============================================================================
# takeDrink
# Handle one instance of the character taking a drink
# ------------------------------------------------------------------------------
def takeDrink():
  global gDrunkLevel
  global gDrinkDCs

  drinkStrength = getDrinkStrength()
  drinkDC = gDrinkDCs[drinkStrength]

  roll = rollD20()
  roll += gModifiers["con"]
  roll += gSizeModifers[gSize]
  roll += gModifiers["ext"]

  print("")
  if roll <= drinkDC:
    gDrunkLevel += 1
    updateModifiers()
    print("You feel yourself getting drunker")
    raw_input("Press enter to continue")
  else:
    print("You don't notice any difference")
    raw_input("Press enter to continue")

  gDrinkDCs["l"] += 1
  gDrinkDCs["light"] += 1
  gDrinkDCs["m"] += 1
  gDrinkDCs["medium"] += 1
  gDrinkDCs["s"] += 1
  gDrinkDCs["strong"] += 1

# ==============================================================================
# attemptSavingThrow
# Ask the user to roll a d20 and enter the result, apply this as a const saving
# throw
# ------------------------------------------------------------------------------
def attemptSavingThrow():
  global gFailedSavingThrows

  print("On your turn roll a saving throw with a D20")
  roll = getInt("Enter your roll (without modifiers) > ")
  roll += gModifiers["con"]
  if roll <= gSavingThrowDC:
    gFailedSavingThrows += 1

# ==============================================================================
# printStatus
# Prints the current modifiers and drunk status of the character
# ------------------------------------------------------------------------------
def printStatus():
  clearTerminal()
  print("Current status:")
  printModifiers()
  print("")

# ==============================================================================
# clearTerminal
# Clears the text displayed on the terminal we are running on
# ------------------------------------------------------------------------------
def clearTerminal():
  os.system('cls' if os.name == 'nt' else 'clear')

# ==============================================================================
# main
# ------------------------------------------------------------------------------
if __name__ == "__main__":
  try:
    getModifiers()
    getSize()

    while gDrunkLevel < gMaxDrunkLevel:
      printStatus()
      takeDrink()

    lastFailedSavingThrows = gFailedSavingThrows
    while gFailedSavingThrows < gMaxFailedSavingThrows:
      printStatus()
      attemptSavingThrow()

      print("")
      if gFailedSavingThrows != lastFailedSavingThrows:
        if gFailedSavingThrows == 1:
          print("********** You have vomited **********")
        elif gFailedSavingThrows == 2:
          print("********** You have fallen over **********")
        elif gFailedSavingThrows == 3:
          print("********** You have passed out **********")
        raw_input("Press enter to continue")
      else:
        print("Nothing happens")
        raw_input("Press enter to continue")

      lastFailedSavingThrows = gFailedSavingThrows
  except KeyboardInterrupt:
    print("")