import re
import logging
from difflib import SequenceMatcher
from lib.perf import perf_func
from lib.word import Word

logger = logging.getLogger(__name__)

class SpellChecker:
  """Class for doing spell checking. Gives context of text with suggestions in context. 
     Also can list all other suggestions for unfound words.

  Returns:
      _type_: _description_
  """
  
  def __init__(self, dictionary_filepath):
    """Initialize the SpellChecker with a dictionary file. Format of dictionary file is one word per line.

    Args:
        dictionary_filepath (str): File path to the dictionary file.
    """
    self.dictionary = set()
    
    with open(dictionary_filepath, 'r') as dictionary_file:
      for raw_word in dictionary_file:
        word = self.__sanitize(raw_word)
        # Single letter word like 'a' are not useful for spell checking.
        if len(word) > 1:
          logger.debug(f"Adding word: '{word}'")            
          self.dictionary.add(word)

  def __sanitize(self, raw_word):
    """Remove anything about the word we want to compare, like whitespace, punctuation, etc.

    Args:
        raw_word (str): Raw string from input.

    Returns:
        Word: Sanitized resulty. If empty (via str()), then ignore further processing.
    """
    #Ignore links.        
    if raw_word.startswith("http://") or raw_word.startswith("https://"):
      return Word("")
    
    # Basic cleanup.
    word = raw_word.strip()
    
    # Remove leading and tailing punctuation.
    matches = re.findall(r"[\w']+|[.,!?;]", word)
    word = matches[0] if matches else word
    
    return Word(word)

  def __get_two_words_relation_score(self, word1, word2):
    """Give a ratio score to how similar two words are. 0.0 is not at all realated,
       0.8 is considered close, and 1.0 is a perfect match.
    """
    return SequenceMatcher(None, word1, word2).ratio()

  def __suggest_word(self, word):
    """Take a word that is most likely misspelled, and suggest words that are in the dictionary.
    
    We accomplish making suggestions 4 diffrent ways:
    * Adds: Add a letter in every position in the word.
    * Deletes: Delete a letter in every position in the word.
    * Edits: Replace a letter in every position in the word.
    * Swaps: Swap two letters in every position in the word.
    All of these possible sessions are then filtered by what's actually in the dictionary.

    Args:
        word (Word): Word that is not in the dictionary for which we need suggestions.

    Returns:
        tuple: Tuple of:
          str: Suggested word.
          list: Other suggested words, in order of probability scores.
    """
    adds = [word[:i] + c + word[i:] for i in range(len(word)) for c in 'abcdefghijklmnopqrstuvwxyz']
    adds = [x for x in adds if x in self.dictionary]
    deletes = [word.replace(word[i], "", 1) for i in range(len(word))]
    deletes = [x for x in deletes if x in self.dictionary]
    edits = [word[:i] + c + word[i+1:] for i in range(len(word)) for c in 'abcdefghijklmnopqrstuvwxyz']
    edits = [x for x in edits if x in self.dictionary]
    swaps = [word[:i] + word[i+1] + word[i] + word[i+2:] for i in range(len(word) - 1)]
    swaps = [x for x in swaps if x in self.dictionary]
    
    suggested_words = set(adds + deletes + edits + swaps)
    suggested_words = set((x, self.__get_two_words_relation_score(word, x)) for x in suggested_words)
    sorted_suggested_words = sorted(suggested_words, key=lambda x: x[1], reverse=True)
    suggested_word_entry = sorted_suggested_words[0] if sorted_suggested_words else ("", 0)
    suggested_word = suggested_word_entry[0]
    other_suggested_words = [x[0] for x in sorted_suggested_words[1:]]
    
    return (suggested_word, other_suggested_words)

  def check_text(self, line_number, text):
    """Checks a line for misspelled words, and suggests corrections.
    
    Simple print out any suggestions; if all words are correct, nothing is printed.
    Misspelled words are striked through and highlighted in red, and suggestions 
    are highlighted in green.
    
    Example:
    "Line 7 best suggestions:
    Kubernetes: almost de f̶a̶c̶t̶o̶fact status
    All misspelled words and suggestions, in order of probability:
        facto: ['fact', 'facts']
    "

    Args:
        line_number (int): Where in the file the text is.
        text (_type_): What to process for misspellings. Preffered to be for each line.
    """
    misspell_found = False
    suggestion_made = False
    originals_and_suggestions = []
    suggested_text = text
    column_number = 0

    for raw_word in text.split():
      word = self.__sanitize(raw_word)

      # Single letter word like 'a' are not useful for spell checking. Neither are abbreviations.
      # Process the rest.
      if len(word) > 1 and not word.is_all_caps and word.lower() not in self.dictionary:
        misspell_found = True
        (suggested_word, other_suggested_words) = self.__suggest_word(word)
        if suggested_word:
          suggestion_made = True
          originals_and_suggestions.append((word, [suggested_word] + other_suggested_words, column_number))
          misspelled_formatted_word = ''.join([u'{}\u0336'.format(c) for c in str(word)])
          misspelled_formatted_word = "\033[91m{}\033[00m".format(misspelled_formatted_word)
          suggested_word_formatted = "\033[92m{}\033[00m".format(suggested_word)
          suggested_text = suggested_text.replace(str(word),
            misspelled_formatted_word + 
            suggested_word_formatted,
          )
      column_number += len(raw_word) + 1
              
    if misspell_found and suggestion_made:
      print(f"Line {line_number} best suggestions: \n\t{suggested_text}")
      print("All misspelled words and suggestions, in order of probability:")
      for (original, suggestions, column_number) in originals_and_suggestions:
        print(f"\tLn {line_number}, Col {column_number}: \"{original}\": {suggestions}")
      print("\n")
