import pytest
from src.matching import bestMatch


def test_matching():
  ''' Test 100% match '''
  trade = 'Earthworks'
  unit_of_measure = 'M3'
  response  = bestMatch(trade, unit_of_measure)
  assert response['best_match'] == {"trade": "Earthworks", "unit_of_measure": "M3", "rate": 50.0}
  # Similarity score may change if changes are made in the algorithm
  assert response['similarity_score'] == 1.0

def test_partial_match():
  ''' Test partial match '''
  trade = 'paint'
  unit_of_measure = 'HouR'
  response  = bestMatch(trade, unit_of_measure)
  assert response['best_match'] == {"trade": "Painting", "unit_of_measure": "HOURS", "rate": 55.0}
  assert response['similarity_score'] > 0.8
  # Similarity score may change if changes are made in the algorithm
  assert response['similarity_score'] == 0.83

def test_no_match():
  ''' Test No match '''
  trade = 'dog'
  unit_of_measure = 'cat'
  response  = bestMatch(trade, unit_of_measure)
  assert response['best_match'] == {"trade": "Joinery", "unit_of_measure": "EACH", "rate": 200.0}
  # Threshold for no match is < 0.6
  assert response['similarity_score'] < 0.6
  # Similarity score may change if changes are made in the algorithm
  assert response['similarity_score'] == 0.24

def test_abbrieviation():
  ''' Test Abbrieviation '''
  trade = 'Painting'
  unit_of_measure = 'linear metre'
  response  = bestMatch(trade, unit_of_measure)
  assert response['best_match'] == {"trade": "Painting", "unit_of_measure": "LM", "rate": 16.0}
  assert response['similarity_score'] > 0.9
  # Similarity score may change if changes are made in the algorithm
  assert response['similarity_score'] == 0.96

def test_abbrieviation2():
  ''' Test Abbrieviation 2 '''
  trade = 'bricklaying'
  unit_of_measure = 'Metres 2'
  response  = bestMatch(trade, unit_of_measure)
  assert response['best_match'] == {"trade": "Bricklaying", "unit_of_measure": "M2", "rate": 75.0}
  assert response['similarity_score'] > 0.9
  # Similarity score may change if changes are made in the algorithm
  assert response['similarity_score'] == 0.94

def test_trade_wrong_casing():
  ''' Test when trade user input does not have correct casing i.e no upper case start and lower case end '''
  trade = 'paIntIng'
  unit_of_measure = 'LM'
  response  = bestMatch(trade, unit_of_measure)
  assert response['best_match'] == {"trade": "Painting", "unit_of_measure": "LM", "rate": 16.0}
  assert response['similarity_score'] > 0.9
  # Similarity score may change if changes are made in the algorithm
  assert response['similarity_score'] == 0.99

def test_UOM_wrong_casing():
  ''' Test UOM wrong casing i.e not all uppercase '''
  trade = 'Electrical'
  unit_of_measure = 'eaCh'
  response  = bestMatch(trade, unit_of_measure)
  assert response['best_match'] == {"trade": "Electrical", "unit_of_measure": "EACH", "rate": 45.0}
  assert response['similarity_score'] > 0.9
  # Similarity score may change if changes are made in the algorithm
  assert response['similarity_score'] == 0.99

