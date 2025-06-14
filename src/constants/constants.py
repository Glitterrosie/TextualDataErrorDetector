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

OCR_DICT = {
    "0": ["8", "9", "o", "O", "D"],
    "1": ["7", "l", "I"],
    "2": ["z", "Z"],
    "3": ["8", "B"],
    "6": ["b", "G", "C"],
    "8": ["s", "S", "B", "5"],
    "5": ["S"],
    "9": ["g", "q"],
    "o": ["u"],
    "C": ["G"],
    "O": ["D", "o"],
    "R": ["B"],
    "m": ["rn"],
    "li": ["h"],
    " ": [""],
}

OCR_NUMBER_TO_NUMBER_MAPPING = {
    "0": ["8", "9"],
    "1": ["7"],
    "3": ["8"],
    "5": ["8"],
    "7": ["1"],
    "8": ["0", "3", "5"],
    "9": ["0"]
}

OCR_LETTER_TO_NUMBER_MAPPING = {
    "o": ["0"],
    "O": ["0"],
    "D": ["0"],
    "l": ["1"],
    "I": ["1"],
    "z": ["2"],
    "Z": ["2"],
    "B": ["3", "8"],
    "b": ["6"],
    "G": ["6"],
    "C": ["6"],
    "s": ["8"],
    "S": ["8", "5"],
    "g": ["9"],
    "q": ["9"]
}


MEDICAL_SPECIALTY_VALUES = [
    "InternalMedicine",
    "Cardiology",
    "Family/GeneralPractice",
    "Surgery-General",
    "Orthopedics-Reconstructive",
    "Pediatrics",
    "Surgery-Cardiovascular/Thoracic",
    "Pediatrics-Pulmonology",
    "Urology",
    "Emergency/Trauma",
    "Psychiatry",
    "Pulmonology",
    "Pediatrics-Endocrinology",
    "Orthopedics",
    "Hematology/Oncology",
    "Surgery-Neuro",
    "Nephrology",
    "ObstetricsandGynecology",
    "Otolaryngology",
    "Pediatrics-CriticalCare",
    "PhysicalMedicineandRehabilitation",
    "Gastroenterology",
    "Obsterics&Gynecology-GynecologicOnco",
    "Surgery-Plastic",
    "Surgery-Colon&Rectal",
    "Pediatrics-Neurology",
    "Osteopath",
    "Endocrinology",
    "AllergyandImmunology",
    "Surgery-Vascular",
    "Radiology",
    "Anesthesiology-Pediatric",
    "InfectiousDiseases",
    "Surgery-Maxillofacial",
    "Oncology",
    "Neurology",
    "Surgery-Thoracic",
    "Gynecology",
    "Surgeon",
    "Surgery-Pediatric",
    "Psychiatry-Addictive",
    "Surgery-Cardiovascular",
    "Anesthesiology",
    "PhysicianNotFound",
    "Hematology",
    "Podiatry",
    "Proctology",
    "Ophthalmology",
    "Rheumatology",
    "Psychology",
    "Obstetrics",
    "Dentistry",
    "SurgicalSpecialty",
]


def get_misspellings_list():
    with open('/src/constants/misspellings', 'r') as f:
        return f.read().splitlines()