import hashlib
from collections import OrderedDict

VOWS = 'aeiuo'
CONS = 'bcdfghjklmnpqrstvwxyz'

WEIGHTED_VOWS = OrderedDict((
    ('a', [0.2239197319415553, 0.06573868644196577, 0.9342613135580342]),
    ('e', [0.29760466361903815, 0.1512788851649321, 0.848721114835068]),
    ('i', [0.17146024588632428, 0.04313092429322406, 0.9568690757067759]),
    ('o', [0.22231910414668477, 0.3112887515534209, 0.6887112484465792]),
    ('u', [0.08469625440639753, 0.027024820378837362, 0.9729751796211626])
))
WEIGHTED_CONS = OrderedDict((
    ('b', [0.02709687084511526, 0.7811315456970378, 0.21886845430296223]),
    ('c', [0.02952379168929421, 0.5088523754935677, 0.4911476245064323]),
    ('d', [0.08755641280125841, 0.6463371475757933, 0.3536628524242067]),
    ('f', [0.028478867436939382, 0.6771236504379711, 0.32287634956202893]),
    ('g', [0.03934008726428344, 0.5890269151138716, 0.4109730848861284]),
    ('h', [0.09794947660156177, 0.9303114272715993, 0.06968857272840068]),
    ('j', [0.0043182711934233444, 1.0, 0.0]),
    ('k', [0.021048294975749518, 0.7382585751978892, 0.2617414248021108]),
    ('l', [0.06424598790284826, 0.537254626046577, 0.4627453739534229]),
    ('m', [0.03789442145278178, 0.8225142705429443, 0.17748572945705562]),
    ('n', [0.12017377951723751, 0.24210526315789474, 0.7578947368421053]),
    ('p', [0.02122432164191682, 0.5518553758325404, 0.44814462416745954]),
    ('q', [0.0006928709200202243, 1.0, 0.0]),
    ('r', [0.07264657965206645, 0.6154915155061439, 0.38450848449385605]),
    ('s', [0.0927473268290856, 0.5261508461592033, 0.47384915384079673]),
    ('t', [0.15473493005748956, 0.3699522691112963, 0.6300477308887037]),
    ('v', [0.01076758862193592, 0.9919156414762742, 0.008084358523725835]),
    ('w', [0.04926124978932979, 0.7309051144010767, 0.2690948855989233]),
    ('x', [0.0018763693563790941, 0.30673316708229426, 0.6932668329177057]),
    ('y', [0.037725885283047135, 0.5816549912434326, 0.41834500875656744]),
    ('z', [0.0006966161682365499, 0.6666666666666666, 0.3333333333333333])
))


def namify(string):
    name = ''

    hx = hashlib.sha256(string.encode('utf-8')).hexdigest()

    length = (int(hx[0], 16) % 6) + 4
    con = int(hx[2], 16) <= 8

    for i, c in enumerate(hx[3::3]):
        c = hx[i*2:i*2 + 3]
        num = int(c[:2], 16)

        if i == length: name += ' '

        r = num/255
        letter = None
        s = 0.0
        weighted = WEIGHTED_CONS if con else WEIGHTED_VOWS
        for key, weight in weighted.items():
            s += weight[0]
            if r < s:
                letter = key
                break
        if not letter: letter = key

        #letter = CONSONANTS[num % (len(CONSONANTS) - 1)] if con else VOWELS[num % (len(VOWELS) - 1)]
        name += letter.upper() if i == 0 or i == length else letter

        weighted = WEIGHTED_CONS if letter in CONS else WEIGHTED_VOWS
        con = False if int(c[2], 16)/16 > weighted[letter][2] else True

    return name


if __name__ == '__main__':
    print(namify('hello world'))