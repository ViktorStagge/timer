import unittest

from time import sleep
from datetime import datetime
from datetime import timedelta

from timer import timer
from timer import Timer
from timer import Checkpoint


class TestTimerMethods(unittest.TestCase):

    def test_import(self):
        from timer import timer
        self.assertEqual(type(timer), Timer)

    def test_call_doesnt_crash(self):
        for _ in range(10):
            actual = timer()
            sleep(0.05)
            print(actual)

    def test_restart(self):
        sleep(1)
        timer.restart()
        self.assertTrue(len(timer._checkpoints) == 1)
        self.assertTrue(timer._start_checkpoint == timer._current_checkpoint)
        self.assertTrue(timer._start_checkpoint.duration() < timedelta(milliseconds=500))

    def test_one_checkpoint(self):
        _start_checkpoint_before = timer._start_checkpoint
        _current_checkpoint_before = timer._current_checkpoint
        number_of_checkpoints_before = len(timer._checkpoints)

        print(f'{self.test_one_checkpoint.__name__}\n')
        for _ in range(3):
            print(timer())
            sleep(0.1)

        checkpoint = timer.new_checkpoint(name='checkpoint_0')

        for _ in range(3):
            print(timer())
            sleep(0.1)

        _start_checkpoint_after = timer._start_checkpoint
        _current_checkpoint_after = timer._current_checkpoint
        number_of_checkpoints_after = len(timer._checkpoints)

        self.assertEqual(number_of_checkpoints_before, 1, f'expected 1, received {number_of_checkpoints_before} checkpoints')
        self.assertEqual(number_of_checkpoints_after, 2, f'expected 2, received {number_of_checkpoints_after} checkpoints')
        self.assertTrue(_start_checkpoint_before == _start_checkpoint_after, '_start_checkpoint changed')
        self.assertTrue(_start_checkpoint_before == _current_checkpoint_before, 'mismatch between first checkpoints')
        self.assertTrue(_start_checkpoint_after != _current_checkpoint_after, 'current checkpoint or start checkpoint changed unexpectedly')
        self.assertEqual(type(checkpoint), Checkpoint, '.new_checkpoint() does not return the Checkpoint')

    def test_many_checkpoints(self):
        pass

    def test_string_representation(self):
        pass

    def test_summary(self):
        timer.restart()

        [timer() for _ in range(3)]
        timer.new_checkpoint(name='checkpoint_0')
        for _ in range(3):
            timer()
            sleep(0.1)

        timer.new_checkpoint(name='checkpoint_1')
        for _ in range(3):
            timer()
            sleep(0.1)

        timer.new_checkpoint(name='victory lap')
        for _ in range(10):
            timer()
            sleep(1.3)

        summary = timer.summary()
        print(f'{self.test_summary.__name__}\n')
        print(summary)


if __name__ == '__main__':
    unittest.main()
