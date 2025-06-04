KEYBOARD_NEIGHBORS = {
    'a': 'qwsxz',
    'b': 'vghn',
    'c': 'xdfv',
    'd': 'wersfxcv',
    'e': '23wrsdf',
    'f': 'ertdgcv',
    'g': 'rtyfhvb',
    'h': 'tyugjbn',
    'i': '78uojkl',
    'j': 'uihknm',
    'k': 'uiojlm',
    'l': 'iopk',
    'm': 'njk',
    'n': 'bhjm',
    'o': '89ipkl',
    'p': '90ol',
    'q': '1was',
    'r': '34etdfg',
    's': 'qweadzx',
    't': '45ryfgh',
    'u': '67yihjk',
    'v': 'cfgb',
    'w': '12qeasd',
    'x': 'zsdc',
    'y': '56tughj',
    'z': 'asx',
    '0': '9p',
    '1': '2qw',
    '2': '13we',
    '3': '24er',
    '4': '35rt',
    '5': '46ty',
    '6': '57yu',
    '7': '68ui',
    '8': '79io',
    '9': '80op',
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
