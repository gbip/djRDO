"""
Test module for musical keys enumeration
"""

import unittest
import music.key as key


class TestKeyMethods(unittest.TestCase):

    def test_declaration(self):
        """
        Test if all enum variants are well declared
        """
        for i in range(1, 12):
            camelot_name_a = "A" + str(i)
            camelot_name_b = "B" + str(i)
            openkey_name_m = "M" + str(i)
            openkey_name_d = "D" + str(i)
            self.assertTrue(openkey_name_m in key.OpenKey.__members__)
            self.assertTrue(openkey_name_d in key.OpenKey.__members__)
            self.assertTrue(camelot_name_a in key.CamelotKey.__members__)
            self.assertTrue(camelot_name_b in key.CamelotKey.__members__)

    def test_key_mappings(self):
        """
        Test if the double-conversion of a key returns the original key
        """
        for i in range(1, 12):
            camelot_name_a = key.CamelotKey["A" + str(i)]
            camelot_name_b = key.CamelotKey["B" + str(i)]
            openkey_name_m = key.OpenKey["M" + str(i)]
            openkey_name_d = key.OpenKey["D" + str(i)]

            self.assertTrue(key.openKeyToCamelotKey[key.camelotToOpenKey[camelot_name_a]] == camelot_name_a)
            self.assertTrue(key.musicKeyToCamelotKey[key.camelotKeyToMusicKey[camelot_name_a]] == camelot_name_a)

            self.assertTrue(key.openKeyToCamelotKey[key.camelotToOpenKey[camelot_name_b]] == camelot_name_b)
            self.assertTrue(key.musicKeyToCamelotKey[key.camelotKeyToMusicKey[camelot_name_b]] == camelot_name_b)

            self.assertTrue(key.musicKeyToOpenKey[key.openKeyToMusicKey[openkey_name_d]] == openkey_name_d)
            self.assertTrue(key.camelotToOpenKey[key.openKeyToCamelotKey[openkey_name_d]] == openkey_name_d)
            
            self.assertTrue(key.musicKeyToOpenKey[key.openKeyToMusicKey[openkey_name_m]] == openkey_name_m)
            self.assertTrue(key.camelotToOpenKey[key.openKeyToCamelotKey[openkey_name_m]] == openkey_name_m)
