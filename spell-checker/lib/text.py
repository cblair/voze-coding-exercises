import logging

logger = logging.getLogger(__name__)

class Text:
  """Class for getting text from a file, line by line, in memory efficient ways.
  Uses python iterator protocol to yield text. This allows us to read large files
  and just process each line in memory at a time.
  """
  linecount = 0
  filepath = ""
  file = None

  def __init__(self, filepath: str):
    """Get ready for reading the file.

    Args:
        filepath (str): File with text to read.
    """
    self.filepath = filepath

  def __iter__(self):
    """Using python iterator protocol, the initialization, which opens the file and prepares for reading.

    Returns:
        Text: Return the instance of this class, for further processing.
    """
    self.file = open(self.filepath, 'r')
    return self

  def __next__(self):
    """Using python iterator protocol, retrieve just the next line of the file and return it.

    Raises:
      StopIteration: Raised when done when done and an iteration still attempted.

    Returns:
        dict: Dictionary with the key/values:
          - line_number (int): Line number of the line in the file.
          - line (str): The test from the entire line.
    """
    if self.file and not self.file.closed:
      line = self.file.readline()
      if line:
        self.linecount += 1
        return {"line_number": self.linecount, "line": line}
    self.cleanup()
    raise StopIteration

  def __del__(self):
    """When garbage collected, guarantee the file is closed."""
    logger.debug(f"Closing file: {self.filepath}")
    self.cleanup()

  def cleanup(self):
    """Close the file if it is open."""
    if self.file and not self.file.closed:
      self.file.close()
