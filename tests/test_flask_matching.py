import pytest
import re
from subprocess import Popen, PIPE
import signal
from time import sleep
import requests
import json

@pytest.fixture
def url():
    ''' A generator that starts the server and returns the url for the server '''    
    server = Popen(["python3", "src/server.py"], stderr=PIPE, stdout=PIPE)    
    sleep(1)
    
    # Local url for flask server is set to port 6200. Change this if port is changed
    local_url = 'http://127.0.0.1:6200'
    if local_url:
        yield local_url
        # Terminate the server
        server.send_signal(signal.SIGINT)
        waited = 0
        while server.poll() is None and waited < 5:
            sleep(0.1)
            waited += 0.1
        if server.poll() is None:
            server.kill()

def test_matching(url):
  ''' Test 100% match '''
  trade = 'Earthworks'
  unit_of_measure = 'M3'
  response = requests.post(f"{url}/match", json={
        "trade" : trade,
        'unit_of_measure': unit_of_measure,
  })

  payload  = response.json()
  assert payload['best_match'] == {"trade": "Earthworks", "unit_of_measure": "M3", "rate": 50.0}
  assert payload['similarity_score'] == 1.0
  assert response.status_code == 200

def test_partial_match(url):
  ''' Test partial  match '''
  trade = 'paint'
  unit_of_measure = 'HouR'
  response = requests.post(f"{url}/match", json={
        "trade" : trade,
        'unit_of_measure': unit_of_measure,
  })

  payload  = response.json()
  assert payload['best_match'] == {"trade": "Painting", "unit_of_measure": "HOURS", "rate": 55.0}
  assert payload['similarity_score'] == 0.83
  assert response.status_code == 200

def test_no_match(url):
      ''' Test No match '''
      trade = 'dog'
      unit_of_measure = 'cat'
      response = requests.post(f"{url}/match", json={
            "trade" : trade,
            'unit_of_measure': unit_of_measure,
      })
      payload  = response.json()
      assert payload['best_match'] == {"trade": "No Match", "unit_of_measure": "", "rate": 0}
      assert payload['similarity_score'] == 0
      assert payload['message'] == "No match found. Check the trade name for spellling errors. Use abbreviations for unit of measure with more than 4 letters and capitalize the abbreviations"
      assert response.status_code == 200

def test_no_trade(url):
  ''' Test No Trade input '''
  unit_of_measure = 'M2'
  response = requests.post(f"{url}/match", json={
        'unit_of_measure': unit_of_measure,
  })
  payload  = response.json()
  assert payload['error'] == "Invalid Request"
  assert payload['message'] == "Trade name is missing"
  assert response.status_code == 400

def test_no_unit_of_measure(url):
  ''' Test No Unit of Measure input '''
  trade = 'paint'
  response = requests.post(f"{url}/match", json={
    "trade" : trade,
  })
  payload  = response.json()
  assert payload['error'] == "Invalid Request"
  assert payload['message'] == "Unit of Measure is missing"
  assert response.status_code == 400

def test_empty_trade(url):
  ''' Test Empty Trade input '''
  trade = ''
  unit_of_measure = 'M2'
  response = requests.post(f"{url}/match", json={
        "trade" : trade,
        'unit_of_measure': unit_of_measure,
  })
  payload  = response.json()
  assert payload['error'] == "Invalid Request"
  assert payload['message'] == "Trade name cannot be empty"
  assert response.status_code == 400

def test_empty_unit_of_measure(url):
    ''' Test Empty Unit of Measure input '''
    trade = 'paint'
    unit_of_measure = ''
    response = requests.post(f"{url}/match", json={
          "trade" : trade,
          'unit_of_measure': unit_of_measure,
    })
    payload  = response.json()
    assert payload['error'] == "Invalid Request"
    assert payload['message'] == "Unit of Measure name cannot be empty"
    assert response.status_code == 400

def test_user_typo(url):
    ''' Test for user typos '''
    trade = 'eletrial'
    unit_of_measure = 'EAh'
    response = requests.post(f"{url}/match", json={
          "trade" : trade,
          'unit_of_measure': unit_of_measure,
    })
    payload  = response.json()
    assert payload['best_match'] == {"trade": "Electrical", "unit_of_measure": "EACH", "rate": 45.0}
    assert payload['similarity_score'] == 0.88
    assert response.status_code == 200
