import unittest
from lib.spell_checker import SpellChecker

class TestSpellChecker(unittest.TestCase):
  def test_spell_checker_attributes(self):
    spell_checker = SpellChecker("dictionary.txt")
    self.assertEqual("abacus" in spell_checker.dictionary, True)

  def test_links(self):
    spell_checker = SpellChecker("dictionary.txt")
    self.assertEqual(spell_checker._SpellChecker__sanitize("http://www.google.com"), "")
    self.assertEqual(spell_checker._SpellChecker__sanitize("https://www.google.com"), "")

  def test_word_relationship_scores(self):
    spell_checker = SpellChecker("dictionary.txt")
    self.assertEqual(spell_checker._SpellChecker__get_two_words_relation_score("test", "tester"), 0.8)
    self.assertEqual(spell_checker._SpellChecker__get_two_words_relation_score("test", "test"), 1.0)
    self.assertEqual(spell_checker._SpellChecker__get_two_words_relation_score("OPPOSITES", "NQ"), 0.0)

  def test_suggested_words(self):
    spell_checker = SpellChecker("dictionary.txt")
    
    (suggested_word, other_suggested_words) = spell_checker._SpellChecker__suggest_word("abacsu")
    self.assertEqual(suggested_word, "abacus")
    self.assertEqual(other_suggested_words, [])
    
    (suggested_word, other_suggested_words) = spell_checker._SpellChecker__suggest_word("kot")
    self.assertEqual(suggested_word, "knot")
    self.assertTrue(len(other_suggested_words) > 0, True)

  def test_check_test(self):
    spell_checker = SpellChecker("dictionary.txt")
    try:
      spell_checker.check_text(1, "This is a test of the emergency misspelling system. Nothing in this text is misspelled, including the work 'misspelled'.")
      spell_checker.check_text(2, "It would be really embarrassing if there were any misspellings in this test.")
      spell_checker.check_text(2, "Someone tell me how you spell mispeaks.")
    except Exception as e:
      self.fail(f"Spell checking failed: {e}")