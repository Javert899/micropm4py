import unittest
from micro_tests.test_petri import TestPetri
from micro_tests.test_log import TestLog
from micro_tests.test_conv import TestConv

if __name__ == "__main__":
    t1 = TestPetri()
    t2 = TestLog()
    unittest.main()
