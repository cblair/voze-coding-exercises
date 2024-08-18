import argparse
from lib.text import Text
from lib.spell_checker import SpellChecker
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(filename='/tmp/spell_checker.log', level=logging.INFO)

# CLI arguments
parser = argparse.ArgumentParser(
  prog="SpellChecker",
  description='Spell check a text file',
  epilog='Voze 2024 All Rights Reserved'
)
parser.add_argument(
  'dictionary_filepath',
  type=str,
  help='The path to the dictionary file to use for spelling'
)
parser.add_argument(
  'text_filepath',
  type=str,
  help='The path to the text file to spell check'
),
args = parser.parse_args()

# Main
textfile = Text(args.text_filepath)
spell_checker = SpellChecker(args.dictionary_filepath)
for line_data in textfile:
  (line_number, line) = line_data.values()
  spell_checker.check_text(line_number, line)
del textfile