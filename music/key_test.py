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

    def test_key_representation(self):
        """
        Test if keys have a well behaved string representation
        """
        def test(t, val):
            """
            :param t: test fixture
            :param val: an array of [Key.MusicKey, str, str, str]
            """
            key_str = val[0].value
            camelot_str = key.musicKeyToCamelotKey[val[0]].value
            openkey_str = key.musicKeyToOpenKey[val[0]].value
            t.assertTrue(key_str == val[1])
            t.assertTrue(camelot_str == val[2])
            t.assertTrue(openkey_str == val[3])

        d_maj = [key.MusicKey.D_MAJOR, "D Major", "10B", "3d"]
        d_min = [key.MusicKey.D_MINOR, "D Minor", "7A", "12m"]
        c_min = [key.MusicKey.C_MINOR, "C Minor", "5A", "10m"]
        e_flat_maj = [key.MusicKey.E_FLAT_MAJOR, "E♭ Major", "5B", "10d"]
        b_maj = [key.MusicKey.B_MAJOR, "B Major", "1B", "6d"]
        a_flat_min = [key.MusicKey.A_FLAT_MINOR, "A♭ Minor", "1A", "6m"]
        f_sharp_maj = [key.MusicKey.F_SHARP_MAJOR, "F# Major", "2B", "7d"]
        notes = [d_maj, d_min, c_min, e_flat_maj, b_maj, a_flat_min, f_sharp_maj]
        for note in notes:
            test(self, note)
