# Einstiegsfunktion der Analyse eines einzelnen Passworts für ein Layout
def isKeyboardWalk(_input: str, keyboard_rows: list, keyboard_rows_changes: list, keyboard_rows_moving: list):

    arr_positions = []
    set_true_indexes = set()
    arr_typeOfKbW = [False, False, False, False]
    set_unknownChars = set()

    # Vorbereitung: Wandele den Input in Kleinbuchstaben um
    for arr in keyboard_rows_changes:
        for i, (char1, char2) in enumerate(zip(arr[0], arr[1])):
            _input = _input.replace(char1, char2)

    # Stelle auf dem Keyboard für alle Zeichen bestimmen
    for char in _input:
        arr_positions.append(getPositionOfChar(char, keyboard_rows, set_unknownChars, keyboard_rows_moving))

    # Durch den Input iterieren
    for i in range(len(arr_positions) - 2):
        checkInputonKeyBoardWalk(arr_positions[i], arr_positions[i + 1], arr_positions[i + 2], i, set_true_indexes, arr_typeOfKbW)

    # Berechnen wie lang der Keyboard Walk ist
    len_KbW = len(set_true_indexes)
    return len_KbW, arr_typeOfKbW, set_unknownChars


# Analyse von 3 aufeinanderfolgende Zeichen
def checkInputonKeyBoardWalk(pos0, pos1, pos2, i: int, set_true_indexes: set, arr_typeOfKbW: list):

    if pos0 is not None and pos1 is not None and pos2 is not None:
        # Überprüfe, ob Key mehrmals gedrückt wird
        if pos0 == pos1 == pos2:
            set_true_indexes |= {i, i + 1, i + 2}
            arr_typeOfKbW[0] = True
            return

        # Überprüfe, ob die Keys auf der selben Keyboard-Row und regelmäßiger Abstand zwischen direkten Nachbarn
        if pos0[0] == pos1[0] == pos2[0] and abs(pos0[1] - pos1[1] == pos1[1] - pos2[1]) == 1:
            set_true_indexes |= {i, i + 1, i + 2}
            arr_typeOfKbW[1] = True
            return

        # KbW auf genau einer Spalte
        if abs(pos0[0] - pos1[0] == pos1[0] - pos2[0]) == 1 and pos1[1] == pos0[1] == pos2[1]:
            set_true_indexes |= {i, i + 1, i + 2}
            arr_typeOfKbW[3] = True
            return

        # Key muss sich neben Key horizontal befinden und dürfen nur in der selben oder benachbarten Zeile liegen
        if (pos1[1] - pos0[1]) in getValuesForVertical(pos0, pos1) and (pos2[1] - pos1[1]) in getValuesForVertical(pos1, pos2):
            set_true_indexes |= {i, i + 1, i + 2}
            arr_typeOfKbW[2] = True
            return
    return


# Position eines Zeichens im Layout bestimmen
def getPositionOfChar(char: str, keyboard_rows: list, set_unknownChars: set, keyboard_rows_moving: list):
    # Finde die Position (Reihe und Spalte) des Buchstabens/Zeichens im Tastaturlayout
    for i, row in enumerate(keyboard_rows):
        if char in row:
            rowIndex = row.index(char)
            # Vorbereitung: Korrektur, dass Keyboardkeys der obersten und untersten Row verschoben sind
            rowIndex = rowIndex + keyboard_rows_moving[i]
            return [i, rowIndex]
    set_unknownChars.add(char)
    return None


# Fallunterscheidung, bei welcher relativen Verschiebung der Tasten es sich um ein KbW handeln kann
def getValuesForVertical(pos0: list, pos1: list):
    if pos0[0] - pos1[0] == 1:
        return 0, 1
    if pos0[0] - pos1[0] == 0:
        return -1, 0, 1
    if pos0[0] - pos1[0] == -1:
        return -1, 0
    return []

