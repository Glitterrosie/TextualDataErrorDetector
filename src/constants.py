# QWERTY neighbor keys for a simplified layout (excluding shift-based symbols)
KEYBOARD_NEIGHBORS = {
    'a': 'qwsz',
    'b': 'vghn',
    'c': 'xdfv',
    'd': 'serfcx',
    'e': 'wsdfr',
    'f': 'drtgvc',
    'g': 'ftyhbv',
    'h': 'gyujnb',
    'i': 'ujko',
    'j': 'huikmn',
    'k': 'jiolm',
    'l': 'kop',
    'm': 'njk',
    'n': 'bhjm',
    'o': 'iklp',
    'p': 'ol',
    'q': 'wa',
    'r': 'edft',
    's': 'awedxz',
    't': 'rfgy',
    'u': 'yhji',
    'v': 'cfgb',
    'w': 'qase',
    'x': 'zsdc',
    'y': 'tghu',
    'z': 'asx',
}

MISSPELLING_PATTERNS = {
    # Double consonant confusion
    'double_consonant': {
        ('mm', 'm'), ('nn', 'n'), ('ll', 'l'), ('ss', 's'), 
        ('tt', 't'), ('pp', 'p'), ('cc', 'c'), ('ff', 'f')
    },
    
    # ie/ei confusion  
    'ie_ei_confusion': {
        ('ie', 'ei'), ('ei', 'ie')
    },
    
    # Silent letter patterns
    'silent_letters': {
        ('ght', 'gt'), ('kn', 'n'), ('wr', 'r'), ('mb', 'm')
    },
    
    # Phonetic substitutions
    'phonetic': {
        ('ph', 'f'), ('c', 'k'), ('s', 'z'), ('x', 'ks')
    }
}

OCR_CHARACTER_CONFUSIONS = {
    # Letters that look similar - common OCR mistakes
    'rn': 'm',
    'cl': 'd',
    'vv': 'w',
    'ii': 'u',
    'll': 'u',
    'nn': 'u',
    'li': 'h',
    'ri': 'n',
    'lf': 'h',
    'ti': 'h',
    'lh': 'b',
    'lli': 'hi',
    'rri': 'ni',
    'lil': 'hi',
    'ni': 'm',
    'rn': 'm',
    
    # Single character confusions - numbers and letters
    '0': 'O',
    'O': '0',
    '1': 'I',
    'I': '1',
    '1': 'l',
    'l': '1',
    '5': 'S',
    'S': '5',
    '6': 'G',
    'G': '6',
    '8': 'B',
    'B': '8',
    '2': 'Z',
    'Z': '2',
    '3': 'E',
    'E': '3',
    '4': 'A',
    'A': '4',
    '7': 'T',
    'T': '7',
    '9': 'g',
    'g': '9',
    
    # Case confusion - uppercase/lowercase
    'C': 'c',
    'c': 'C',
    'K': 'k',
    'k': 'K',
    'P': 'p',
    'p': 'P',
    'S': 's',
    's': 'S',
    'U': 'u',
    'u': 'U',
    'V': 'v',
    'v': 'V',
    'W': 'w',
    'w': 'W',
    'X': 'x',
    'x': 'X',
    'Y': 'y',
    'y': 'Y',
    'Z': 'z',
    'z': 'Z',
    
    # Similar looking letters
    'a': 'o',
    'o': 'a',
    'e': 'c',
    'c': 'e',
    'n': 'h',
    'h': 'n',
    'u': 'n',
    'n': 'u',
    'b': 'd',
    'd': 'b',
    'p': 'q',
    'q': 'p',
    'f': 't',
    't': 'f',
    'i': 'l',
    'l': 'i',
    'r': 'n',
    
    # Broken or partial characters
    'o': 'c',
    'g': 'q',
    'q': 'g',
    'b': 'h'
    'h': 'b',
    'd': 'cl',
    
    # Punctuation and special characters
    '.': '',
    ',': '',
    '|': 'l',
    'l': '|',
    '\\': '/',
    '/': '\\',
    "'": '',
    '"': '',
    '`': '',
    '~': '',
    '_': '-',
    '-': '_',
    ':': '.',
    ';': '.',
    '!': '.',
    'j': '.',
}