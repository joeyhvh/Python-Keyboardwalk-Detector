import analyser

def isKeyboardWalk(_input: str, keyboard_rows: list, keyboard_rows_changes: list, keyboard_rows_moving: list):

    arr_positions = []
    set_true_indexes = set()
    arr_typeOfKbW = [False, False, False, False]
    set_unknownChars = set()
    arr_strKbW = []

    # Vorbereitung: Wandele den Input in Kleinbuchstaben um
    for arr in keyboard_rows_changes:
        for i, (char1, char2) in enumerate(zip(arr[0], arr[1])):
            _input = _input.replace(char1, char2)

    # Stelle auf dem Keyboard für alle Zeichen bestimmen
    for char in _input:
        arr_positions.append(analyser.getPositionOfChar(char, keyboard_rows, set_unknownChars, keyboard_rows_moving))

    # Durch den Input iterieren
    for i in range(len(arr_positions) - 2):
        analyser.checkInputonKeyBoardWalk(arr_positions[i], arr_positions[i + 1], arr_positions[i + 2], i, set_true_indexes, arr_typeOfKbW)

    # Berechnen wie lang der Keyboard Walk ist und filtern der Teile in welchen ein KbW vorhanden ist
    keyboardwalk_length = len(set_true_indexes)
    arr_true_indexes = sorted(set_true_indexes)
    for i, currIndex in enumerate(arr_true_indexes):
        if i > 0 and currIndex - arr_true_indexes[i - 1] == 1:
            arr_strKbW[-1] += _input[currIndex]
        else:
            arr_strKbW.append(_input[currIndex])
    return keyboardwalk_length, arr_typeOfKbW, set_unknownChars, arr_strKbW