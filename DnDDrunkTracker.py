# ==============================================================================
# Imports
# ------------------------------------------------------------------------------
import random
import os
import ConfigParser
import sys

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

gConfigFileName = "DnDDrunkTracker.cfg"

# ==============================================================================
# getFullConfigPath
# ------------------------------------------------------------------------------
def getFullConfigPath():
  ourDir = os.path.dirname(os.path.realpath(__file__))
  configPath = ourDir + "/" + gConfigFileName
  return configPath  

# ==============================================================================
# readConfig
# Reads modifiers and size from config file if it exists
# ------------------------------------------------------------------------------
def readConfig():
  global gModifiers
  global gSize

  configPath = getFullConfigPath()
  
  # If we don't have a config file bail
  if not os.path.isfile(configPath):
    return False

  try:
    config = ConfigParser.RawConfigParser()
    config.read(configPath)

    gModifiers["str"] = config.getint("modifiers", "str")
    gModifiers["dxt"] = config.getint("modifiers", "dxt")
    gModifiers["con"] = config.getint("modifiers", "con")
    gModifiers["int"] = config.getint("modifiers", "int")
    gModifiers["wis"] = config.getint("modifiers", "wis")
    gModifiers["cha"] = config.getint("modifiers", "cha")
    gModifiers["ext"] = config.getint("modifiers", "ext")

    gSize = config.get("size", "size")
    # Ensure size is valid
    sizes = ["s", "small", "m", "medium", "l", "large"]
    if gSize not in sizes:
      print("Config file contains invalid size, re-enter your character")
      print("")
      return False
  except:
    # If anything went wrong reding the config then fail this function
    # The user will be asked for their character again
    print("Something went wrong reading the config file, re-enter your character")
    print("")
    return False

  return True

# ==============================================================================
# writeConfig
# Write modifiers and size to a config file
# ------------------------------------------------------------------------------
def writeConfig():
  config = ConfigParser.RawConfigParser()
  config.add_section("size")
  config.set("size", "size", gSize)
  config.add_section("modifiers")
  config.set("modifiers", "str", gModifiers["str"])
  config.set("modifiers", "dxt", gModifiers["dxt"])
  config.set("modifiers", "con", gModifiers["con"])
  config.set("modifiers", "int", gModifiers["int"])
  config.set("modifiers", "wis", gModifiers["wis"])
  config.set("modifiers", "cha", gModifiers["cha"])
  config.set("modifiers", "ext", gModifiers["ext"])

  configPath = getFullConfigPath()
  with open(configPath, 'wb') as configfile:
    config.write(configfile)

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
def printModifiers(includeExtra=False):
  print("Str: %+d, Dxt: %+d, Con: %+d, Int: %+d, Wis: %+d, Cha: %+d" % (
    gModifiers["str"],
    gModifiers["dxt"],
    gModifiers["con"],
    gModifiers["int"],
    gModifiers["wis"],
    gModifiers["cha"]))
  if includeExtra:
    print("Extra: %+d" % (gModifiers["ext"]))

# ==============================================================================
# getDrinkDC
# Ask for the strength of a drink and any temp modifiers
# Return the drinks DC
# ------------------------------------------------------------------------------
def getDrinkDC():
  drinkStrengths = ["l", "light", "m", "medium", "s", "strong"]
  userInput = raw_input("Enter strength of drink taken (light, medium, strong) followed by any temporary constitution or drink buffs from magic, potions etc > ")
  parts = userInput.split()

  # Make sure we didn't get too maby inputs
  if len(parts) > 2 or len(parts) < 1:
    print("You entered %d items when 1 or 2 are expected, try again" % (len(parts)))
    return getDrinkDC()

  # Make sure we got a valid strength
  strength = parts[0]
  if strength not in drinkStrengths:
    print("%s is not a drink strength, try again" % (strength))
    return getDrinkDC()
  
  # If we got a modifier make sure its valid
  modifier = 0
  if len(parts) > 1:
    modifierStr = parts[1]
    try:
      modifier = int(modifierStr)
    except ValueError:
      print("%s is not an integer, try again" % (modifierStr))
      return getDrinkDC()
  
  drinkDC = gDrinkDCs[strength] - modifier
  return drinkDC

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

  drinkDC = getDrinkDC()

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

  print("On your turn roll a consitution saving throw with a D20")
  roll = getInt("Enter your roll without your constitution modifier but with any temporary constitution or drink buffs from magic, potions etc > ")
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
    if "--resetConfig" not in sys.argv and readConfig():
      print("Character read from config file %s" % (getFullConfigPath()))
      print("Run with --resetConfig argument to change this")
    else:
      getModifiers()
      getSize()
      writeConfig()
      print("")
      print("Character written to config file %s" % (getFullConfigPath()))
    print("")
    printModifiers(includeExtra=True)
    print("Size: %s" % (gSize))
    print("")
    raw_input("Press enter to continue")

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