import unittest
from mTwit.Error import (
    MTwitError,
    VerifyError,
    TaskbarError
)


class TestError(unittest.TestCase):

    def test_mtwit_error(self):
        self.assertEqual("john", str(MTwitError("john")))

    def test_verify_error(self):
        self.assertEqual("john", str(VerifyError("john")))

    def test_taskbar_error(self):
        self.assertEqual("john", str(TaskbarError("john")))


if __name__ == "__main__":
    unittest.main()
