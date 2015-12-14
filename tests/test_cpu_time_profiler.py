import unittest
import time

from line_profiler import LineProfiler, PROFILE_CPU_TIME, PROFILE_REAL_TIME, \
    BadTimerException

SLEEP_TIME = 0.1


def sleepfn():
    time.sleep(SLEEP_TIME)


def work(profiler_type):
    p = LineProfiler(profiler=profiler_type)
    p.add_function(sleepfn)
    with p:
        sleepfn()
    stats = p.get_stats()
    total_ticks = sum(v[0][2] for k, v in stats.timings.items())
    total_time = total_ticks * stats.unit
    return total_time


class TestLineProfiler(unittest.TestCase):

    def test_cpu_time_does_not_count_sleep(self):
        self.assertLess(work(PROFILE_CPU_TIME), SLEEP_TIME)

    def test_real_time_counts_sleep(self):
        self.assertGreater(work(PROFILE_REAL_TIME), SLEEP_TIME)

    def test_bad_timer_raises_exception(self):
        with self.assertRaises(BadTimerException):
            work(99999)
