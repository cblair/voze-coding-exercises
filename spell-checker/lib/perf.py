from functools import wraps
import time

def perf_func(func):
  """Just a quick decorator to time how long a function takes to run.

  Args:
      func (fuction): The function to time, using the decorator protocol.

  Returns:
      function: Wrapped function with timing output, per the decorator protocol.
  """
  @wraps(func)
  def perf_func_wrapper(*args, **kwargs):
    start_time = time.perf_counter()
    result = func(*args, **kwargs)
    end_time = time.perf_counter()
    total_time = end_time - start_time
    print(f'Function {func.__name__}{args} {kwargs} Took {total_time:.4f} seconds')
    return result
  return perf_func_wrapper
