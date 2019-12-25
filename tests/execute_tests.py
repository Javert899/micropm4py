import unittest
from tests.test_petri import TestPetri
from tests.test_log import TestLog
from tests.test_conv import TestConv

if __name__ == "__main__":
    t1 = TestPetri()
    t2 = TestLog()
    unittest.main()
