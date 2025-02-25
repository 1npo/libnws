from typing import Callable
from functools import wraps
from rich.progress import Progress, SpinnerColumn, TimeElapsedColumn


def display_spinner(message: str = None) -> Callable:
	"""A decorator for displaying a spinner with Rich

	See the below for more information on why we're using functools.wraps() here:

	https://stackoverflow.com/questions/5929107/decorators-with-parameters
	https://realpython.com/primer-on-python-decorators/#decorators-with-arguments

	:param message: The message to display beside the spinner
	"""

	def decorator(func: Callable):
		@wraps(func)
		def wrapper(*args, **kwargs):
			progress = Progress(SpinnerColumn(spinner_name='dots'),
								TimeElapsedColumn(),
								message,
								transient=True)
			with progress:
				task = progress.add_task('message', total=1)
				while not progress.finished:
					func_return_value = func(*args, **kwargs)
					progress.update(task, advance=1)
				return func_return_value
		return wrapper
	return decorator
