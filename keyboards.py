# Layouts ohne Mehrfachbelegung
german_keyboard_rows = [
    '^1234567890ß´',
    'qwertzuiopü+',
    'asdfghjklöä#',
    '<yxcvbnm,.-'
]
american_keyboard_rows = [
    '`1234567890-=',
    'qwertyuiop[]',
    'asdfghjkl;\'\\',
    'zxcvbnm,./'
]
# Arrays, welche eine einzelne Mehrfachbelegung beschreiben
german_keyboard_rows_shift_character = [
    '°!"§$%&/()=?`*\'>;:_',
    '^1234567890ß´+#<,.-'
]
german_keyboard_rows_special_character = [
    '²³{[]}\\@€~|',
    '237890ßqe+<'
]
american_keyboard_rows_shift_character = [
    '~!@#$%^&*()_+{}:"|<>?´',
    '`1234567890-=[];,\\,./\''
]
# Einfügen der einzelnen Arrays in Array, welches alle Mehrfachbelegungen für jedes Layout beschreibt
german_keyboard_rows_changes = [german_keyboard_rows_shift_character, german_keyboard_rows_special_character]
american_keyboard_rows_changes = [american_keyboard_rows_shift_character]
# Vertikale Verschiebung der Tasten
german_keyboard_rows_moving = [-1,0,0,-1]
american_keyboard_rows_moving = [-1,0,0,0]
# keyboards = [[german_keyboard_rows, german_keyboard_rows_changes], [american_keyboard_rows, american_keyboard_rows_changes]]