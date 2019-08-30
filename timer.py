from datetime import datetime


_first_checkpoint_name = 'start'


class Timer:
    _checkpoints = []

    @classmethod
    def __new__(cls, *args, name='timer', output_format=str, print_decimals=3, **kwargs):
        if not hasattr(cls, '_timer') or cls._timer is None:
            cls._timer = super(Timer, cls).__new__(cls)

            cls._name = name
            cls._format = output_format
            cls._decimals = print_decimals
            cls._start_checkpoint = Checkpoint(name=_first_checkpoint_name)
            cls._current_checkpoint = cls._start_checkpoint
            cls._checkpoints.append(cls._start_checkpoint)
        return cls._timer

    def __call__(self, description=None):
        now = datetime.now()
        time_since_start = self._time_since_start(timestamp=now)
        if self._start_checkpoint != self._current_checkpoint:
            time_since_checkpoint = self._time_since_checkpoint(timestamp=now)
        else:
            time_since_checkpoint = None

        time = self._describe_time(time_since_start=time_since_start,
                                   time_since_checkpoint=time_since_checkpoint,
                                   description=description)
        return time

    @classmethod
    def _describe_time(cls, time_since_start=None, time_since_checkpoint=None, description=None):
        if time_since_start is None:
            time_since_start = cls._time_since_start()

        if cls._format == str:
            return cls._describe_time_as_string(time_since_start=time_since_start,
                                                time_since_checkpoint=time_since_checkpoint,
                                                description=description)
        elif cls._format == int:
            return cls._describe_time_as_int(time_since_start=time_since_start)
        else:
            raise NotImplementedError()

    @classmethod
    def _describe_time_as_string(cls, time_since_start=None, time_since_checkpoint=None, description=None):
        if description is None:
            description = ''

        time_string = f'{cls._name}:\t{time_since_start}'
        if time_since_checkpoint is not None:
            checkpoint_name_string = f'{cls._current_checkpoint.name + ":":<15}\t' if cls._current_checkpoint.name else ''
            time_string += f'.\t\t{checkpoint_name_string}{time_since_checkpoint}\t{description}'
        return time_string

    @classmethod
    def _describe_time_as_int(cls, time_since_start):
        return time_since_start

    @classmethod
    def _time_since_start(cls, timestamp=None):
        if timestamp is None:
            timestamp = datetime.now()

        return timestamp - cls._start_checkpoint.start

    @classmethod
    def _time_since_checkpoint(cls, timestamp=None):
        if timestamp is None:
            timestamp = datetime.now()

        return timestamp - cls._current_checkpoint.start

    @classmethod
    def new_checkpoint(cls, name=None):
        cls._current_checkpoint.end_checkpoint()
        checkpoint = Checkpoint(name=name)
        cls._current_checkpoint = checkpoint
        cls._checkpoints.append(checkpoint)
        return checkpoint

    @classmethod
    def duration(cls):
        start_time = cls._checkpoints[0].start
        end_time = cls._checkpoints[-1].end or datetime.now()
        return end_time - start_time

    @classmethod
    def set_unit(cls, unit=str):
        pass

    @classmethod
    def summary(cls):
        max_start_time_length = len(f'{cls.duration().total_seconds():.0f}') + cls._decimals + (cls._decimals > 0)
        longest_checkpoint_name = max((len(c.name) for c in cls._checkpoints))
        longest_duration = max((len(f'{c.duration().total_seconds():.0f}') for c in cls._checkpoints)) + cls._decimals + (cls._decimals > 0)

        _summary = f'{cls._name} summary\n'
        for checkpoint in cls._checkpoints:
            _summary += f'{checkpoint.name + ": " if checkpoint.name is not None else "":{longest_checkpoint_name + 2}}'
            _summary += f'{cls._time_since_start(timestamp=checkpoint.start).total_seconds():{max_start_time_length}.{cls._decimals}f}s\t'
            _summary += f'duration={checkpoint.duration().total_seconds():{longest_duration}.{cls._decimals}f}s\n'
        _summary += f'{"end:":{longest_checkpoint_name + 2}}{cls.duration().total_seconds():{max_start_time_length}.{cls._decimals}f}s\n'

        return _summary

    @classmethod
    def restart(cls):
        cls._start_checkpoint = Checkpoint(name=_first_checkpoint_name)
        cls._current_checkpoint = cls._start_checkpoint
        cls._checkpoints = [cls._start_checkpoint]
        return cls._timer


class Checkpoint:
    def __init__(self, name=None, start=None):
        self.start = start or datetime.now()
        self.end = None
        self.name = name

    def __eq__(self, other):
        return type(other) == type(self) and \
               other.start == self.start and \
               other.end == self.end and \
               other.name == self.name

    def duration(self):
        if self.end is None:
            return datetime.now() - self.start

        return self.end - self.start

    def end_checkpoint(self):
        if self.end is None:
            self.end = datetime.now()


timer = Timer()
