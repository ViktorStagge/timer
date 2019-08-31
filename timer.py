from datetime import datetime


_first_checkpoint_name = 'start'


class Timer:
    _checkpoints = []

    @classmethod
    def __new__(cls, *args, name='timer', output_format=str, print_decimals=3, **kwargs):
        if not hasattr(cls, '_timer') or cls._timer is None:
            cls._timer = super(Timer, cls).__new__(cls)

            cls._name = name
            cls._output_format = output_format
            cls._decimals = print_decimals
            cls._start_checkpoint = Checkpoint(name=_first_checkpoint_name)
            cls._current_checkpoint = cls._start_checkpoint
            cls._end_checkpoint = None
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
        if cls._output_format == str:
            return cls._describe_time_as_string(description=description)
        elif cls._output_format == int:
            return cls._describe_time_as_int(time_since_start=time_since_start)
        else:
            raise NotImplementedError()

    @classmethod
    def _describe_time_as_string(cls, show_checkpoint=True, description=None):
        min_length = 2 + cls._decimals + (cls._decimals > 0)

        name = f'{cls._name}:\t'
        time = f'{cls.duration().total_seconds():{min_length}.{cls._decimals}f}s'

        time_as_string = name + time
        if show_checkpoint and cls._has_checkpoint() and cls._current_checkpoint is not None:
            checkpoint_name = f'\t\t{cls._current_checkpoint.name}: ' if cls._current_checkpoint.name else '\t\t'
            checkpoint_time = f'{cls._current_checkpoint.duration().total_seconds():{min_length}.{cls._decimals}f}s'
            time_as_string += checkpoint_name + checkpoint_time

        if description is not None:
            time_as_string += '\t' + description

        return time_as_string

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
        if cls._has_active_checkpoint():
            cls._current_checkpoint.end_checkpoint()

        checkpoint = Checkpoint(name=name)
        cls._current_checkpoint = checkpoint
        cls._checkpoints.append(checkpoint)
        return checkpoint

    @classmethod
    def duration(cls):
        start_time = cls._checkpoints[0].start
        end_time = datetime.now()
        if cls._end_checkpoint is not None:
            raise
            end_time = cls._end_checkpoint.end or end_time
        return end_time - start_time

    @classmethod
    def set_unit(cls, unit=str):
        pass

    @classmethod
    def end_timer(cls):
        pass

    @classmethod
    def end_checkpoint(cls):
        cls._current_checkpoint.end_checkpoint()
        cls._current_checkpoint = None

    @classmethod
    def _has_checkpoint(cls):
        return len(cls._checkpoints) > 1

    @classmethod
    def _has_active_checkpoint(cls):
        return cls._current_checkpoint is not None

    @classmethod
    def summary(cls):
        max_start_time_length = len(f'{cls.duration().total_seconds():.0f}') + cls._decimals + (cls._decimals > 0)
        longest_checkpoint_name = max((len(c.name) for c in cls._checkpoints))
        longest_duration = max((len(f'{c.duration().total_seconds():.0f}') for c in cls._checkpoints)) + cls._decimals + (cls._decimals > 0)

        _summary = f'{cls._name} summary\n'
        for checkpoint in cls._checkpoints:
            _summary += f'{checkpoint.name + ": " if checkpoint.name is not None else "":{longest_checkpoint_name + 2}}'
            _summary += f'{cls._time_since_start(timestamp=checkpoint.start).total_seconds():{max_start_time_length}.{cls._decimals}f}s    '
            _summary += f'duration={checkpoint.duration().total_seconds():{longest_duration}.{cls._decimals}f}s\n'
        _summary += f'{"end:":{longest_checkpoint_name + 2}}{cls.duration().total_seconds():{max_start_time_length}.{cls._decimals}f}s\n'

        return _summary

    @classmethod
    def restart(cls):
        cls._start_checkpoint = Checkpoint(name=_first_checkpoint_name)
        cls._current_checkpoint = cls._start_checkpoint
        cls._checkpoints = [cls._start_checkpoint]
        return cls._timer


def time_this_method(method=None, name=None):
    def wrapper(method):
        def _time_this_method(*args, **kwargs):
            _name = name or method.__name__
            timer.new_checkpoint(name=_name)
            returned_from_method = method(*args, **kwargs)
            timer.end_checkpoint()
            return returned_from_method
        return _time_this_method

    # decorator call, i.e. `@time_this_method`
    if method is not None:
        return wrapper(method)

    # factory call, i.e.`@time_this_method()`
    return wrapper


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


# @time_everything
# def alot_of_things():
#   pass

timer = Timer()
