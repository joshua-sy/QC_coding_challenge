import json
from thefuzz import fuzz, process

commonUserMeasurementInput = ['LINEAR METRE', 'METRE 2', 'METRE 3', 'METRE']

def bestMatch(trade, unit_of_measure):
  items = []
  # Reading item.json database
  with open('items.json', 'r') as file:
    items = json.load(file)
  
  bestSimilarityScore = 0
  bestMatch = {}
  abbrieviationDeductions = 0
  # If unit of measure (UOM) has a space or has more than 4 characters, this means that the user did not give an abbrieviation of the UOM
  # We will be turning their inputted UOM into an abbrieviation
  if (" " in unit_of_measure) or len(unit_of_measure) > 4:
    # We will find possible names based on their input of common measurements with spaces
    # We take the top commonUserMeasurementInput score
    similarityUserMeasurementInput = process.extract(unit_of_measure, commonUserMeasurementInput, limit=1)[0]
    # We then give a deduction based on the score
    # The higher the score, the more similar the input is to one of the commonUserMeasurementInput and thus the lesser the deduction -> min deduction is 5 for 100% similarity
    abbrieviationDeductions += (100 - similarityUserMeasurementInput[1]) + 5

    abbrieviation = createAbbrieviations(unit_of_measure)
    unit_of_measure = abbrieviation['unit_of_measure']
    # Add abbrieviation deductions calculated by createAbbrieviations
    abbrieviationDeductions += abbrieviation['deductions']
  
  # Looping through the item.json database
  for item in items:
    if item['trade'] == trade:
      # If trade names are equal, then set the similarity score of trade name to 100%
      similarityTradeScore = 100
    # If trade names are equal both are lowercase, then set the similarity score of trade name to 99%
    elif item['trade'].lower() == trade.lower():
      similarityTradeScore = 99
    else:
      # Find similarity score of trade name
      # Set both to lowercase so letter casing does not affect similarity score
      similarityTradeScore = fuzz.ratio(trade.lower(), item['trade'].lower())
    
    if item['unit_of_measure'] == unit_of_measure:
      # If UOM names are equal, then set similarity score to 100% - abbrieviationDeductions
      similarityUOMScore = 100 - abbrieviationDeductions
    elif item['unit_of_measure'].upper() == unit_of_measure.upper():
      # Set the similarity UOM score to 99% - abbrieviationDeductions if the unit of measure is the same to unit of meausre in the database when we set it to uppercase
      similarityUOMScore = 99 - abbrieviationDeductions
    else:
      # Use fuzzy search to determine similarity score of user UOM to database UOM
      # Set to uppercase so user inputted UOM casing does not affect score
      similarityUOMScore = round(fuzz.ratio(unit_of_measure.upper(), item['unit_of_measure']), 2) - abbrieviationDeductions
      
      #  Give a higher score if both unit of measure inputted by user has number and the unit of measure in the database has numbers
      #  Rare/Harder for user to accidentally type a number
      if has_numbers(unit_of_measure) is True and has_numbers(item['unit_of_measure']) is True:
        similarityUOMScore += 5

    # Rounds the combined similarity score to 2 decimal places
    similarityScore = round((similarityTradeScore + similarityUOMScore) / 200, 2)
    if similarityScore > bestSimilarityScore:
      bestSimilarityScore = similarityScore
      bestMatch = item
  

  return {
    "best_match": bestMatch,
    "similarity_score": bestSimilarityScore
  }

# We create an abbrieviation based on user inputted UOM
def createAbbrieviations(unit_of_measure):
  splitted_unit_of_measure = unit_of_measure.split(' ')
  result = {
    "unit_of_measure": '',
    "deductions": 0
  }
  print(splitted_unit_of_measure)
  for word in splitted_unit_of_measure:
    # Checks for empty spaces that the user may input
    if len(word) > 0:
      # Check if it is a digit
      # If so we add it to our new abbrieviation but no deduction is given
      if word[0].isdigit():
        result['unit_of_measure'] += word[0]
      # If the character is lower case, we give them a deduction
      # e.g linear Metre -> l is lowercase and therefore a deduction is given
      elif word[0].islower():
        result['unit_of_measure'] += word[0].upper()
        result['deductions'] += 1
      else:
        result['unit_of_measure'] += word[0]
  return result

# Returns true if a word contains a number character
# Returns False otherwise
def has_numbers(word):
    return any(char.isdigit() for char in word)



