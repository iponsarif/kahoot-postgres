import unittest

from ..utils.crypt import encrypt, decrypt

class TestCryptMethods(unittest.TestCase):

    def testEncrypt(self):
        self.assertEqual(encrypt("a"), "c")

    def testDecrypt(self):
        self.assertEqual(decrypt("c"), "a")

if __name__ == "__main__":
    unittest.main()