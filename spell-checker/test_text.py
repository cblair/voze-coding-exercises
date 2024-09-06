import unittest
from lib.text import Text

class TestText(unittest.TestCase):
  def test_initialization(self):
    text = Text("test/text.txt")
    self.assertEqual(text.filepath, "test/text.txt")
    self.assertEqual(text.linecount, 0)
    self.assertEqual(text.file, None)
    del text

  def test_iteration(self):
    text = Text("test/text.txt")
    for line_data in text:
      (line_number, line) = line_data.values()
      self.assertNotEqual(line_number, 0)
      self.assertNotEqual(line, "")
    self.assertEqual(text.linecount, 7)
    text.cleanup()
    self.assertEqual(text.file.closed, True)
    del text

  def test_iteration_not_forever(self):
    text = Text("test/text.txt")
    for line_data in text:
      (line_number, line) = line_data.values()
      self.assertNotEqual(line_number, 0)
      self.assertNotEqual(line, "")
    def try_getting_iteration_beyond_end():
      next(text)
    self.assertRaises(StopIteration, try_getting_iteration_beyond_end)

if __name__ == '__main__':
  unittest.main()
