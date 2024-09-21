# QC Coding Challenge 

## How to run the program
Make sure all packages are install by running the following command:
```
pip3 install -r requirements.txt
```

Run the server by:

    python3 src/server.py
  
  This should run the server at port 6200 unless port number has been changed. (See server.py if port number has been changed)

## Suggestion
Use postman to test the API or add more tests to the test_flask_matching.py file. Add the link produced by flask when running server.py into postman. Set it to POST. Add input in Body using raw JSON. 

NOTE: The match call should be done on the match route. For example:
```
http://127.0.0.1:6200/match
```

## How to run tests
To run tests, run the following command:
```
pytest -v tests
```

This should run all the tests in the tests folder. There are currently only 2 files which test the match algorithm and the api requests.

## Running Coverage
We use coverage to check that all sections of the code has been executed. This helps in testing to ensure that all the sections of the code has been executed and tested.

To run coverage, run the following command:
```
coverage run -m pytest tests
```

To get the coverage report in your terminal, run the following command:
```
coverage report  
```

The coverage report that can be viewed in an HTML file, run the follow command:
```
coverage html 
```
## theFuzz
We have used the theFuzz library to get a similarity score but what is theFuzz? theFuzz library is a fuzzy string matching algorithm that determines the closeness of two strings using the Levenshtien edit distance. It finds the edit distance by finding the minimum number of edits. The four types of edit include:
- Insert (add a letter)
- Delete (remove a letter)
- Switch (change one letter to another)
- Replace (change one letter to another)

It then gives a score out of 100 to determine the closeness of two strings. If the score is near 100, then this means that the two strings are very close/similar. If the score is near 0, then this means that the two strings are not close/similar.



## Trade Name Similarity algorithm and reasoning
When we find a trade name in items.json that is equal to the user inputted trade name, then we set the similarity score to 100 to indicate a 100% match.

When the trade name is similar to items.json trade name when we set the both to lower case, then we set the similarity score to 99 giving a deduction for incorrect capitalization.

For other cases, we use fuzzy string match to get a score. We set the strings to lowercase because capitalizations will affect the score. i.e M != m and will therefore trigger an edit resulting in a lower score. Trade names are not case sensitive and therefore wrong capitalization and casing should not affect the score. 

similarity score for joins is 50/100 for Joinery when not turning the trade variable and item['trade'] variable to lower.
similarity score for joins is 67/100 for Joinery when  turning the trade variable and item['trade'] variable to lower. 

We set all the trade to lower case because we do not care about casing for trade
All trade names is not name specific or anything
theFuzz fuzzy search algorithm is case specific. meaning lowercase letters are not equal to upper case letters and thus lowering the score.

E.g
similarity score for joins is 50/100 for Joinery when not turning the trade variable and item['trade'] variable to lower.
similarity score for joins is 67/100 for Joinery when  turning the trade variable and item['trade'] variable to lower. Prefferred since joins and joinery is quite similar and joins could be a slang or shortcut for joinery


## Unit of Measurement (UOM) Similarity algorithm and reasoning
When we find a UOM in items.json that is equal to the user inputted UOM, then we set the similarity score to 100 to indicate a 100% match.

When the UOM is similar to items.json UOM when we set the user UOM to upper case, then we set the similarity score to 99 giving a deduction for incorrect capitalization.

For other cases, we use fuzzy string match to get a score. We set the strings to uppercase because capitalizations will affect the score. i.e M != m and will therefore trigger an edit resulting in a lower score. UOM are not case sensitive and therefore wrong capitalization should not affect the score. 

### Abbrieviation
We make an abbrieviation for the user UOM if the user has inputted a UOM that contains spaces or if it more than 4 characters. This is so if user does not input an abbrieviation of the UOM but is a viable UOM, they are not heavily penalised for it. 
For example, Linear Metre is the same as LM but comparing Linear Metre and LM into the fuzzy string match algorithm will yield a very low similarity score. By making an abbrieviation of Linear Metre into LM, we can get an a higher similarity score.

An abbrieviation deduction is added to the similarity score if an abbrieviation is made. An abbrieviation deduction is calculated by checking if inputted UOM is similar to a list of common user measurement inputs that are not abbrieviated using fuzzy string matching. It takes the highest score and uses that score to make the penalty (higher similarity score means lower penalty).

Making the abbrieviation also adds a penalty.

### Reasoning why UOM with digits usually have a higher similarity score
A higher similarity score is given to UOM with digits since it is harder to accidentally add a number to the input. We made it so that user inputted UOM have a higher prefereability to be matched with UOMS in the database that have numbers. This is so M4 is more likely to be matched with M2 and M3 than LM even though the similarity score of M2, M3 and LM compared to M4 would be the same using fuzzy string matching.


## Improvements
The matching algorithm was made based on user inputs and the items database. More examples of the behaviour of user inputs can improve the accuracy of the algorithm. Especially for UOM.

## Conclusion
Made a matching algorithm that gives the best match and provides a reasonable similarity score based on user input.