# util/format.py

# Further expanded mapping of special characters to QMK labels
special_char_mapping = {
    '-': 'MINS',
    '&': 'AMPR',
    '*': 'ASTR',
    '[': 'LBRC',
    ']': 'RBRC',
    ',': 'COMM',
    '.': 'DOT',
    '!': 'EXLM',
    '@': 'AT',
    '#': 'HASH',
    '$': 'DLR',
    '%': 'PERC',
    '^': 'CIRC',
    '(': 'LPRN',
    ')': 'RPRN',
    '_': 'UNDS',
    '|': 'PIPE',
    '\\': 'BSLS',
    '/': 'SLSH',
    '+': 'PLUS',
    ';': 'SCLN',  # Semicolon
    ':': 'COLN',  # Colon
    "'": 'QUOT',  # Single Quote
    '"': 'DQUO',  # Double Quote
    '{': 'LCBR',  # Left Curly Brace
    '}': 'RCBR',  # Right Curly Brace
}

def replace_special_chars_in_label(label):
    """Replaces special characters in a label with their mappings."""
    for char, replacement in special_char_mapping.items():
        label = label.replace(char, replacement)
    label = label.replace(' ', '_')  # Also replace spaces with underscores
    return label
