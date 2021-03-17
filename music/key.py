"""
This modules defines how to represent music keys.
"""
import enum


@enum.unique
class MusicKey(enum.Enum):
    """
    Standard music key representation for all elements of the 5th wheel
    """
    C_MAJOR = "C Major"  # 1d
    G_MAJOR = "G Major"  # 2d
    D_MAJOR = "D Major"  # 3d
    A_MAJOR = "A Major"  # 4d
    E_MAJOR = "E Major"  # 5d
    B_MAJOR = "B Major"  # 6d
    F_SHARP_MAJOR = "F# Major"  # 7d
    D_FLAT_MAJOR = "D♭ Major"  # 8d
    A_FLAT_MAJOR = "A♭ Major"  # 9d
    E_FLAT_MAJOR = "E♭ Major"  # 10d
    B_FLAT_MAJOR = "B♭ Major"  # 11d
    F_MAJOR = "F Major"  # 12d
    A_MINOR = "A Minor"  # 1m
    E_MINOR = "E Minor"  # 2m
    B_MINOR = "B Minor"  # 3m
    G_FLAT_MINOR = "G♭ Minor"  # 4m
    D_FLAT_MINOR = "D♭ Minor"  # 5m
    A_FLAT_MINOR = "A♭ Minor"  # 6m
    E_FLAT_MINOR = "E♭ Minor"  # 7m
    B_FLAT_MINOR = "B♭ Minor"  # 8m
    F_MINOR = "F Minor"  # 9m
    C_MINOR = "C Minor"  # 10 m
    G_MINOR = "G Minor"  # 11m
    D_MINOR = "D Minor"  # 12 m


@enum.unique
class CamelotKey(enum.Enum):
    """
    Camelot music key representation
    """
    B1 = "1B"
    B2 = "2B"
    B3 = "3B"
    B4 = "4B"
    B5 = "5B"
    B6 = "6B"
    B7 = "7B"
    B8 = "8B"
    B9 = "9B"
    B10 = "10B"
    B11 = "11B"
    B12 = "12B"
    A1 = "1A"
    A2 = "2A"
    A3 = "3A"
    A4 = "4A"
    A5 = "5A"
    A6 = "6A"
    A7 = "7A"
    A8 = "8A"
    A9 = "9A"
    A10 = "10A"
    A11 = "11A"
    A12 = "12A"


@enum.unique
class OpenKey(enum.Enum):
    """
    Openkey music key representation
    """
    D1 = "1d"
    D2 = "2d"
    D3 = "3d"
    D4 = "4d"
    D5 = "5d"
    D6 = "6d"
    D7 = "7d"
    D8 = "8d"
    D9 = "9d"
    D10 = "10d"
    D11 = "11d"
    D12 = "12d"
    M1 = "1m"
    M2 = "2m"
    M3 = "3m"
    M4 = "4m"
    M5 = "5m"
    M6 = "6m"
    M7 = "7m"
    M8 = "8m"
    M9 = "9m"
    M10 = "10m"
    M11 = "11m"
    M12 = "12m"


camelotToOpenKey = {
    CamelotKey.B1: OpenKey.D6,
    CamelotKey.B2: OpenKey.D7,
    CamelotKey.B3: OpenKey.D8,
    CamelotKey.B4: OpenKey.D9,
    CamelotKey.B5: OpenKey.D10,
    CamelotKey.B6: OpenKey.D11,
    CamelotKey.B7: OpenKey.D12,
    CamelotKey.B8: OpenKey.D1,
    CamelotKey.B9: OpenKey.D2,
    CamelotKey.B10: OpenKey.D3,
    CamelotKey.B11: OpenKey.D4,
    CamelotKey.B12: OpenKey.D5,
    CamelotKey.A1: OpenKey.M6,
    CamelotKey.A2: OpenKey.M7,
    CamelotKey.A3: OpenKey.M8,
    CamelotKey.A4: OpenKey.M9,
    CamelotKey.A5: OpenKey.M10,
    CamelotKey.A6: OpenKey.M11,
    CamelotKey.A7: OpenKey.M12,
    CamelotKey.A8: OpenKey.M1,
    CamelotKey.A9: OpenKey.M2,
    CamelotKey.A10: OpenKey.M3,
    CamelotKey.A11: OpenKey.M4,
    CamelotKey.A12: OpenKey.M5
}
"""
Generate inverted dict mappings
"""
openKeyToCamelotKey = {value: key for (key, value) in camelotToOpenKey.items()}

musicKeyToOpenKey = {
    MusicKey.C_MAJOR: OpenKey.D1,
    MusicKey.G_MAJOR: OpenKey.D2,
    MusicKey.D_MAJOR: OpenKey.D3,
    MusicKey.A_MAJOR: OpenKey.D4,
    MusicKey.E_MAJOR: OpenKey.D5,
    MusicKey.B_MAJOR: OpenKey.D6,
    MusicKey.F_SHARP_MAJOR: OpenKey.D7,
    MusicKey.D_FLAT_MAJOR: OpenKey.D8,
    MusicKey.A_FLAT_MAJOR: OpenKey.D9,
    MusicKey.E_FLAT_MAJOR: OpenKey.D10,
    MusicKey.B_FLAT_MAJOR: OpenKey.D11,
    MusicKey.F_MAJOR: OpenKey.D12,
    MusicKey.A_MINOR: OpenKey.M1,
    MusicKey.E_MINOR: OpenKey.M2,
    MusicKey.B_MINOR: OpenKey.M3,
    MusicKey.G_FLAT_MINOR: OpenKey.M4,
    MusicKey.D_FLAT_MINOR: OpenKey.M5,
    MusicKey.A_FLAT_MINOR: OpenKey.M6,
    MusicKey.E_FLAT_MINOR: OpenKey.M7,
    MusicKey.B_FLAT_MINOR: OpenKey.M8,
    MusicKey.F_MINOR: OpenKey.M9,
    MusicKey.C_MINOR: OpenKey.M10,
    MusicKey.G_MINOR: OpenKey.M11,
    MusicKey.D_MINOR: OpenKey.M12,
}

musicKeyToCamelotKey = {
    MusicKey.C_MAJOR: openKeyToCamelotKey[OpenKey.D1],
    MusicKey.G_MAJOR: openKeyToCamelotKey[OpenKey.D2],
    MusicKey.D_MAJOR: openKeyToCamelotKey[OpenKey.D3],
    MusicKey.A_MAJOR: openKeyToCamelotKey[OpenKey.D4],
    MusicKey.E_MAJOR: openKeyToCamelotKey[OpenKey.D5],
    MusicKey.B_MAJOR: openKeyToCamelotKey[OpenKey.D6],
    MusicKey.F_SHARP_MAJOR: openKeyToCamelotKey[OpenKey.D7],
    MusicKey.D_FLAT_MAJOR: openKeyToCamelotKey[OpenKey.D8],
    MusicKey.A_FLAT_MAJOR: openKeyToCamelotKey[OpenKey.D9],
    MusicKey.E_FLAT_MAJOR: openKeyToCamelotKey[OpenKey.D10],
    MusicKey.B_FLAT_MAJOR: openKeyToCamelotKey[OpenKey.D11],
    MusicKey.F_MAJOR: openKeyToCamelotKey[OpenKey.D12],
    MusicKey.A_MINOR: openKeyToCamelotKey[OpenKey.M1],
    MusicKey.E_MINOR: openKeyToCamelotKey[OpenKey.M2],
    MusicKey.B_MINOR: openKeyToCamelotKey[OpenKey.M3],
    MusicKey.G_FLAT_MINOR: openKeyToCamelotKey[OpenKey.M4],
    MusicKey.D_FLAT_MINOR: openKeyToCamelotKey[OpenKey.M5],
    MusicKey.A_FLAT_MINOR: openKeyToCamelotKey[OpenKey.M6],
    MusicKey.E_FLAT_MINOR: openKeyToCamelotKey[OpenKey.M7],
    MusicKey.B_FLAT_MINOR: openKeyToCamelotKey[OpenKey.M8],
    MusicKey.F_MINOR: openKeyToCamelotKey[OpenKey.M9],
    MusicKey.C_MINOR: openKeyToCamelotKey[OpenKey.M10],
    MusicKey.G_MINOR: openKeyToCamelotKey[OpenKey.M11],
    MusicKey.D_MINOR: openKeyToCamelotKey[OpenKey.M12],
}

"""
Reverse dictionary to get inverted mapping
"""
openKeyToMusicKey = {value: key for (key, value) in musicKeyToOpenKey.items()}
camelotKeyToMusicKey = {value: key for (key, value) in musicKeyToCamelotKey.items()}
