import unittest
from lib.word import Word

class TestWord(unittest.TestCase):
  def test_word_attributes(self):
    word = Word("test")
    self.assertEqual(str(word), "test")
    self.assertEqual(len(word), 4)
    self.assertEqual(word.is_all_caps, False)
    
    word = Word("TESTER")
    self.assertEqual(str(word), "TESTER")
    self.assertEqual(len(word), 6)
    self.assertEqual(word.is_all_caps, True)
    
  def test_equality(self):
    word = Word("test")
    other_word = Word("test")
    self.assertEqual(word, other_word)
    
    word = Word("test")
    other_word = Word("tester")
    self.assertNotEqual(word, other_word)

  def test_hash(self):
    word = Word("test")
    self.assertEqual(hash(word), hash("test"))

  def test_indexing(self):
    word = Word("test")
    self.assertEqual(word[0], "t")
    self.assertEqual(word[1], "e")
    self.assertEqual(word[2], "s")
    self.assertEqual(word[3], "t")
    def try_getting_index_beyond_end():
      word[4]
    self.assertRaises(IndexError, try_getting_index_beyond_end)

  def test_replace(self):
    word = Word("test")
    self.assertEqual(word.replace("t", "T", 1), "Test")
    self.assertEqual(word.replace("e", "E"), "tEst")
    self.assertEqual(word.replace("s", "S"), "teSt")
    self.assertEqual(word.replace("t", "T"), "TesT")

  def test_lower(self):
    word = Word("TEST")
    self.assertEqual(word.lower(), "test")