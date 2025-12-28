import random

STICKERS = {
    'common': ['☃️', '🎄', '🎆'],
    'rare': ['🍪', '☕️ '],
    'epic': ['🎇'],
    'legendary': ['❄️']
}

def get_sticker():
    roll = random.random()
    if roll < 0.70:
        return random.choice(STICKERS['common'])
    elif roll < 0.90:
        return random.choice(STICKERS['rare']) 
    elif roll < 0.97:
        return random.choice(STICKERS['epic'])
    else:
        return random.choice(STICKERS['legendary'])