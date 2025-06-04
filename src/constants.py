# QWERTY neighbor keys for a simplified layout (excluding shift-based symbols)
KEYBOARD_NEIGHBORS = {
    'a': 'qwsz',
    'b': 'vghn',
    'c': 'xdfv',
    'd': 'serfcx',
    'e': 'wsdfr4',
    'f': 'drtgvc',
    'g': 'ftyhbv',
    'h': 'gyujnb',
    'i': 'ujko89',
    'j': 'huikmn',
    'k': 'jiolm',
    'l': 'kop',
    'm': 'njk',
    'n': 'bhjm',
    'o': 'iklp90',
    'p': 'ol0',
    'q': 'wa12',
    'r': 'edft45',
    's': 'awedxz',
    't': 'rfgy56',
    'u': 'yhji78',
    'v': 'cfgb',
    'w': 'qase23',
    'x': 'zsdc',
    'y': 'tghu67',
    'z': 'asx',
    '0': '9op', # TODO: add more neighbors for numbers
    '1': 'wq2',
    '2': 'qwe3',
    '3': 'we24',
    '4': 'er35',
    '5': 'rt46',
    '6': 'ty57',
    '7': 'uy68',
    '8': 'iu79',
    '9': 'io80',
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
    'b': 'h',
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
