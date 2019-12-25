import unittest
import inspect
import os
import sys

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    parent_dir = os.path.dirname(current_dir)
    sys.path.insert(0, parent_dir)
    from micro_tests.test_petri import TestPetri
    from micro_tests.test_log import TestLog
    from micro_tests.test_conv import TestConv
    t1 = TestPetri()
    t2 = TestLog()
    t3 = TestConv()
    unittest.main()
