class Word:
  """Class to represent a word in a text, with some necessary accounting to make it easier to
     grep and restore. For use for things like spell checking.
  """
  __word = ""
  # Indicators to things like spell checking for special cases.
  is_all_caps = False

  def __init__(self, word):
    self.__word = word
    self.is_all_caps = word.isupper()

  def __eq__(self, other):
    """Comparison operator override, for comparing two words in text and dictionary.

    Args:
        other (Word): Other word to compare with.

    Returns:
        boolean: Two words equal?
    """
    return str(self.__word).lower() == str(other).lower()
  
  def __str__(self):
    """Override for string conversion str().

    Returns:
        str: String representation of the Word.
    """
    return self.__word

  def __len__(self):
    """Override for length representation via len().

    Returns:
        int: Length
    """
    return len(self.__word)

  def __hash__(self):
    """Override for ordering for functionality for things like set's.

    Returns:
        int: Hashable value.
    """
    return hash(self.__word)

  def __getitem__(self, index):
    """Support indexing internal word stream by index.

    Args:
        index (Word): Character at index to retrieve.

    Returns:
        Word: Retrieved single character.
    """
    return self.__word[index].lower()

  def replace(self, old, new, count=-1):
    """Wrapper for string replace(), but for Word. Do str like operations on our internal str representation.

    Args:
        old (str): Old string to replace.
        new (str): New string to replace with.
        count (int): How many occurrences to replace. When not set, will replace all.

    Returns:
        str: New str representation of the Word, with replacements.
    """
    return self.__word.replace(old, new, count)

  def lower(self):
    """Wrapper for string lower(), but for Word."""
    return self.__word.lower()
