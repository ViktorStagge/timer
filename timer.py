from datetime import datetime


class Timer():
	_timer = None
	_name = None
	_start_time = None
	_current_checkpoint = 
	_checkpoints = []
 

	def __new__(cls, *args, name='timer', output_format=str, **kwargs):
		if cls._timer is not None:
			cls._timer = super(Timer, cls).__new__(cls, *args, **kwargs)
		cls._name = name
		cls._format = output_format
		cls._start_checkpoint = Checkpoint()
		cls._current_checkpoint = cls._start_checkpoint
		cls._checkpoints.append(cls._start_checkpoint)
		return cls._timer


	def __call__(self, name=None):
		now = datetime.now() 
		time_since_start = self._time_since_start(timestamp=now)
		if self._start_time != self._current_checkpoint.start:
			time_since_checkpoint = self._time_since_checkpoint(timestamp=now)
		else:
			time_since_checkpoint = None

		time = _describe_time(time_since_start=time_since_start, 
							  time_since_checkpoint=time_since_checkpoint)
		return time


	def _describe_time(cls, time_since_start=None, time_since_checkpoint=None):
		if time_since_start is None:
			time_since_start = _time_since_start()

		if cls._format == str:
			return _describe_time_as_string(time_since_start=time_since_start, time_since_checkpoint=time_since_checkpoint)
		elif cls._format == int:
			return _describe_time_as_int(time_since_start=time_since_start)
		else:
			raise NotImplementedError()


	def _describe_time_as_string(cls, time_since_start=None, time_since_checkpoint=None):
		time_string = f'{cls._name}:\t{time_since_start}'
		if time_since_checkpoint is not None:
			checkpoint_name_string = f'{cls._current_checkpoint.name:15}:' if cls._current_checkpoint.name else ''  
			time_string += f'.\t\t{checkpoint_name_string}{time_since_checkpoint}'
		return time_string


	def _describe_time_as_int(cls, time_since_start):
		return time_since_start


	def _time_since_start(cls, timestamp=None):
		if timestamp is None:
			timestamp = datetime.now()

		return now - cls._start_checkpoint.start


	def _time_since_checkpoint(timestamp=None):
		if timestamp is None:
			timestamp = datetime.now()

		return timestamp - cls._current_checkpoint.start


	def new_checkpoint(cls, name=None):
		checkpoint = Checkpoint(name=name)
		cls._current_checkpoint = checkpoint
		cls._checkpoints.append(checkpoint)
		return checkpoint


	def set_unit(cls, type=str):
		pass


	def summary(cls):
		_summary = f'{name}\n'
		for checkpoint in cls._checkpoints:
			_summary += f'{cls._time_since_start(timestamp=checkpoint.start)}\t'
			_summary += f'{checkpoint.name + ": " if checkpoint.name is not None else ""}'
			_summary += f'{checkpoint.duration()}\n'
		_summary = f'end: {_time_since_start()}'
		return _summary

	def restart(cls):
		cls._start_checkpoint = Checkpoint()
		cls._current_checkpoint = cls._start_checkpoint
		cls._checkpoints.append(cls._start_checkpoint)
		return self._timer


class Checkpoint
	start = None
	end = None
	name = None


	def __init__(self, name=name, start=None):
		self.start = start or datetime.now()
		self.name = name

	def duration(self):
		if self.end is None:
			return datetime.now() - self.start

		return self.end - self.start


timer = Timer()
