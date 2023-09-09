import analyser
import analyser_single
import keyboards
import os


# Analyse eines einzelnen Passwortes/Testfunktion
def single():
    # Eingabe
    inputPW: str = input('Enter a password:')
    # Wenn leer/einfach nur Enter Taste verlassen des Moduses
    if inputPW == '':
        mainmenu()
        return
    # Validierung, ob keinen Inhalt
    inputStr = inputPW.lower().replace(' ', '').replace('\n', '')
    if len(inputStr) == 0:
        print('empty input please repeat')
        single()
        return
    length_pw: int = len(inputPW)
    # Aufruf der Analysefunktionen
    result_german = analyser_single.isKeyboardWalk(inputPW, keyboards.german_keyboard_rows, keyboards.german_keyboard_rows_changes, keyboards.german_keyboard_rows_moving)
    result_american = analyser_single.isKeyboardWalk(inputPW, keyboards.american_keyboard_rows, keyboards.american_keyboard_rows_changes, keyboards.american_keyboard_rows_moving)
    # Berechnung und Ausgabe der Übereinstimmung
    print(f'conformity with german layout: {result_german[0] / length_pw * 100}% -> { result_german[3] }')
    print(f'conformity with american layout: {result_american[0] / length_pw * 100}% -> { result_american[3] }')
    # Berechnung und Ausgabe der Art des KbW
    if result_german[1][0] or result_american[1][0]:
        print('PW contains a 3 three time repetition of a character')
    if result_german[1][1] or result_american[1][1]:
        print('PW contains a KbW in one row')
    if result_german[1][2] or result_american[1][2]:
        print('PW contains a complex KbW')
    if result_german[1][3] or result_american[1][3]:
        print('PW contains a KbW in one column')
    # Ausgabe der unbekannten Zeichen im Passwort
    print(f'Unknown characters: { result_german[2].update(result_american[2]) }')
    single()


def pwdict():

    # Eingabe
    filePath: str = input('[ls] Get all text files in current directory\nEnter the Path to the password dictionary:')
    # Wenn leer/einfach nur Enter Taste verlassen des Moduses und ls Funktionalität
    if filePath == '':
        mainmenu()
        return
    # ls Funktion
    elif filePath == 'ls':
        files = [f for f in os.listdir(os.getcwd()) if os.path.isfile(f) and f.endswith('.txt') and not f.startswith('result')]
        for file in files:
            print(file)
        pwdict()
        return
    # Validierung, ob keinen Inhalt
    inputstr = filePath.lower().replace(' ', '').replace('\n', '')
    if len(inputstr) == 0:
        print('empty input please repeat')
        pwdict()
        return

    counter_complete_unknown, counter_complete_german, counter_complete_american, counter_partly_unknown, counter_partly_german, counter_partly_american, counter_false, length_partly, length_partly_true, counter_all, counter_key, counter_row, counter_column, counter_complex, length_pw = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    set_unknownChars = set()

    # Lesen und Analyse der Zeichen
    try:
        with open(filePath, "r", encoding='utf-8') as readfile:
            # Iterierung durch die Zeilen/Passwörter
            line = readfile.readline()
            while line:
                counter_all += 1
                # Vorbereitungen
                line = line.lower().replace(' ', '').replace('\n', '')
                length_pw = len(line)
                result_german = analyser.isKeyboardWalk(line, keyboards.german_keyboard_rows, keyboards.german_keyboard_rows_changes, keyboards.german_keyboard_rows_moving)
                result_american = analyser.isKeyboardWalk(line, keyboards.american_keyboard_rows, keyboards.american_keyboard_rows_changes, keyboards.american_keyboard_rows_moving)
                # Unterscheidung, ob KbW enthalten und welches Layout
                if result_german[0] == result_american[0] > 0:
                    if result_german[0] == length_pw:
                        counter_complete_unknown += 1
                    else:
                        counter_partly_unknown += 1
                        length_partly_true = length_partly_true + result_german[0]
                        length_partly = length_partly + length_pw
                elif result_german[0] > result_american[0]:
                    if result_german[0] == length_pw:
                        counter_complete_german += 1
                    else:
                        counter_partly_german += 1
                        length_partly_true = length_partly_true + result_german[0]
                        length_partly = length_partly + length_pw
                elif result_german[0] < result_american[0]:
                    if result_american[0] == length_pw:
                        counter_complete_american += 1
                    else:
                        counter_partly_american += 1
                        length_partly_true = length_partly_true + result_american[0]
                        length_partly = length_partly + length_pw
                else:
                    counter_false += 1

                # Unterscheidung der Arten des KbW
                if result_german[1][0] or result_american[1][0]:
                    counter_key += 1
                elif result_german[1][1] or result_american[1][1]:
                    counter_row += 1
                elif result_german[1][2] or result_american[1][2]:
                    counter_complex += 1
                elif result_german[1][3] or result_american[1][3]:
                    counter_column += 1

                # Zusammenführen aller unbekannten Zeichen
                set_unknownChars.update(result_german[2])
                set_unknownChars.update(result_american[2])

                line = readfile.readline()
    except Exception as e:
        print(f'Error in IO operation or content processing. Error Message: { e }')
    # Ausgabe unbekannter Zeichen
    print(f'Unknown characters: {set_unknownChars}')

    # Berechnungen
    length_partly_sumOfAmount = counter_partly_unknown + counter_partly_german + counter_partly_american
    sum_true = counter_complete_unknown + counter_complete_german + counter_complete_american + counter_partly_unknown + counter_partly_german + counter_partly_american
    sum_complete = counter_complete_unknown + counter_complete_german + counter_complete_american
    sum_partly = counter_partly_unknown + counter_partly_german + counter_partly_american
    dif_validator = counter_all - (sum_true + counter_false)

    # Name des Resultdatei zusammenführen und Ergebnisse in diese schreiben
    filePath = os.path.basename(filePath)
    filePath = filePath.split('.')[0]
    resultFileName = f'results_{filePath}.txt'

    with open(resultFileName, 'w', encoding='utf-8') as writefile:
        writefile.write(f'Vollständig ein Keyboard Walk unabhängig vom Layout: {sum_complete:,}\n')
        writefile.write(f'Vollständig ein Keyboard Walk und Layout nicht zuordbar: {counter_complete_unknown:,}\n')
        writefile.write(f'Vollständig ein Keyboard Walk mit wahrscheinlich deutschem Tastaturlayout: {counter_complete_german:,}\n')
        writefile.write(f'Vollständig ein Keyboard Walk mit wahrscheinlich amerikanischem Tastaturlayout: {counter_complete_american:,}\n\n')
        writefile.write(f'Teilweise ein Keyboard Walk unabhängig vom Layout: {sum_partly:,}\n')
        writefile.write(f'Teilweise ein Keyboard Walk und Layout nicht zuordbar: {counter_partly_unknown:,}\n')
        writefile.write(f'Teilweise ein Keyboard Walk mit wahrscheinlich deutschem Tastaturlayout: {counter_partly_german:,}\n')
        writefile.write(f'Teilweise ein Keyboard Walk mit wahrscheinlich amerikanischem Tastaturlayout: {counter_partly_american:,}\n\n')
        writefile.write(f'Durchschnittliche Länge des Keyboards Walks der Passwörter, die teilweise ein Keyboard Walk enthalten: { round(length_partly_true / length_partly_sumOfAmount, 2)}\n',)
        writefile.write(f'Durchschnittliche Länge der Passwörter, die teilweise ein Keyboard Walk enthalten: { round(length_partly / length_partly_sumOfAmount, 2)}\n\n')
        writefile.write(f'Summe der Passwörter, welche MINDESTENS teilweise ein Keyboard Walk unabhängig des Layouts beinhalten: {sum_true:,}\n')
        writefile.write(f'Auf beiden Tastaturlayouts kein Keyboard Walk: {counter_false:,}\n\n')
        writefile.write(f'Passwörter beinhalten mehrfach den selben Buchstaben: {counter_key:,}\n')
        writefile.write(f'Passwörter, welche Keyboard Walk auf einer Zeile durchführen: {counter_row:,}\n')
        writefile.write(f'Passwörter, welche Keyboard Walk auf einer Spalte durchführen: {counter_column:,}\n')
        writefile.write(f'Passwörter, welche Keyboard Walk durchführen, aber komplexer als andere differenzierten Arten: {counter_complex:,}\n\n')
        writefile.write(f'Es wurden insgesamt {counter_all:,} Passwörter analysiert\n')
        if dif_validator:
            writefile.write(f'Es gibt ein Fehler in der Verarbeitung. Es wurden  {dif_validator:,} nicht korrekt verarbeitet\n')
        print(f'Analysis ready. Please look for {os.getcwd()}\\{resultFileName} For operating systems other than Windows, you may need to change some/all slahes')
    pwdict()


def mainmenu():
    print('[0] Test/Check password\n[1] Analysis of password dictionary\nPress enter to go back to main menu')
    choice: str = input('Choice:')
    if choice == '0':
        single()
        return
    elif choice == '1':
        pwdict()
        return
    else:
        print('Wrong input. Please try again')
        mainmenu()

mainmenu()