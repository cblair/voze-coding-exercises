# Make a spell checker!

A program that checks spelling. The input to the program is a dictionary file containing a list of valid words and a file containing the text to be checked.

To run:

```text
python3 spell_checker.py dictionary.txt file-to-check.txt
# Example output:
Line 2 best suggestions: 
        Someone tell me how you spell m̶i̶s̶p̶e̶a̶k̶s̶misspeaks.
All misspelled words and suggestions, in order of probability:
        Ln 2, Col 30: "mispeaks": ['misspeaks']
```

Example run with a sample in this repo:
```text
python3 spell_checker.py ./dictionary.txt samples/sample1.txt
...
```

Supports the following features:

- ✅ The program outputs a list of incorrectly spelled words.
- ✅ For each misspelled word, the program outputs a list of suggested words.
- ✅ The program includes the line and column number of the misspelled word.
- ✅ The program prints the misspelled word along with some surrounding context.
- ✅ The program handles proper nouns (person or place names, for example) correctly.

To test:
```text
./scripts/coverage.sh
```
~
```text
..............
----------------------------------------------------------------------
Ran 14 tests in 6.107s

OK
Name                   Stmts   Miss  Cover   Missing
----------------------------------------------------
lib/spell_checker.py      65      0   100%
lib/text.py               25      0   100%
lib/word.py               20      0   100%
----------------------------------------------------
TOTAL                    110      0   100%
```
