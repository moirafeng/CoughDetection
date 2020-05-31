# FluSense Label Definition

u_labels = [
    'cough', 'speech', 'snore', 'dog-bark', 'drill',
    'vacuum', 'baby-cry', 'chopping',  'door', 'hazard-alarm',
    'water-running', 'knock', 'microwave', 'shaver', 'toothbrush',
    'blender', 'dishwasher', 'doorbell', 'flush', 'hair-dryer',
    'laugh',  'typing', 'hammer', 'car-horn',  'phone-ring',
    'engine', 'saw', 'cat-meow', 'alarm-clock', 'cooking'
]

f_labels = ['cough',
            'speech',
            'snore',
            'silence',
            'sniffle',
            'sneeze',
            'gasp',
            'breathe',
            'throat-clearing',
            'hiccup',
            'vomit',
            'burp',
            'wheeze',
            'etc'
            ]

count = dict.fromkeys(u_labels, 0)
conf_mat = dict.fromkeys(f_labels, count)

