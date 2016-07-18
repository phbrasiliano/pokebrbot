import pickle
import random
from telepot.namedtuple import InlineKeyboardButton, InlineKeyboardMarkup
from collections import OrderedDict

print('poke fun starting')
ranking = pickle.load(open("ranking.p", "rb"))
pokelist = pickle.load(open("pokelist2.p", "rb"))
typedict = pickle.load(open('typedict1.p', 'rb'))
battledic = {}


class Battle:
    def __init__(self, mainchat):
        self.mainchat = mainchat
        print('Instance of battle started on chat %s' % self.mainchat)
        self.pcount = 0
        self.team1 = []
        self.team2 = []
        self.p1 = ()
        self.p2 = ()
        self.p1score = 0
        self.p2score = 0
        self.battlechoicep1 = -1
        self.battlechoicep2 = -1
        self.timer = 0

    def reset(self):
        self.pcount = 0
        self.team1 = []
        self.team2 = []
        self.p1 = ()
        self.p2 = ()
        self.p1score = 0
        self.p2score = 0
        self.battlechoicep1 = -1
        self.battlechoicep2 = -1
        self.timer = 0


def type_fight(n1, n2):
    poke1 = pokelist[n1]
    poke2 = pokelist[n2]
    poke1_atk = 8
    poke2_atk = 8
    if len(poke1['types']) == 1:
        for t in poke2['types']:
            if poke1['types'][0] in typedict[t]['wkn']:
                poke1_atk += 2
            if poke1['types'][0] in typedict[t]['res']:
                poke1_atk -= 2
            if poke1['types'][0] in typedict[t]['imu']:
                poke1_atk -= 6
    else:
        poke1_tmp1 = 8
        poke1_tmp2 = 8
        for t in poke2['types']:
            if poke1['types'][0] in typedict[t]['wkn']:
                poke1_tmp1 += 2
            if poke1['types'][0] in typedict[t]['res']:
                poke1_tmp1 -= 2
            if poke1['types'][0] in typedict[t]['imu']:
                poke1_tmp2 -= 6
            if poke1['types'][1] in typedict[t]['wkn']:
                poke1_tmp2 += 2
            if poke1['types'][1] in typedict[t]['res']:
                poke1_tmp2 -= 2
            if poke1['types'][1] in typedict[t]['imu']:
                poke1_tmp1 -= 6
        if poke1_tmp1 > poke1_tmp2:
            poke1_atk = poke1_tmp1
        else:
            poke1_atk = poke1_tmp2

    if len(poke2['types']) == 1:
        for t in poke1['types']:
            if poke2['types'][0] in typedict[t]['wkn']:
                poke2_atk += 2
            if poke2['types'][0] in typedict[t]['res']:
                poke2_atk -= 2
            if poke2['types'][0] in typedict[t]['imu']:
                poke2_atk -= 6
    else:
        poke2_tmp1 = 8
        poke2_tmp2 = 8
        for t in poke1['types']:
            if poke2['types'][0] in typedict[t]['wkn']:
                poke2_tmp1 += 2
            if poke2['types'][0] in typedict[t]['res']:
                poke2_tmp1 -= 2
            if poke2['types'][0] in typedict[t]['imu']:
                poke2_tmp1 -= 6
            if poke2['types'][1] in typedict[t]['wkn']:
                poke2_tmp2 += 2
            if poke2['types'][1] in typedict[t]['res']:
                poke2_tmp2 -= 2
            if poke2['types'][1] in typedict[t]['imu']:
                poke2_tmp2 -= 6
        if poke2_tmp1 > poke2_tmp2:
            poke2_atk = poke2_tmp1
        else:
            poke2_atk = poke2_tmp2
    poke1_final = poke1['power']
    poke2_final = poke2['power']
    for x in range(poke1_atk):
        poke1_final += random.randrange(120)
    for x in range(poke2_atk):
        poke2_final += random.randrange(120)
    print(poke1['name'], 'poder ', poke1['power'], 'mod ', poke1_atk,  poke1_final, 'vs',
          poke2['name'], 'poder ', poke2['power'], 'mod ', poke2_atk,  poke2_final)
    if poke1_final > poke2_final:
        # print('%s ganhou a batalha contra %s' % (poke1['name'], poke2['name']))
        return 'win1'
    else:
        # print('%s ganhou a batalha contra %s' % (poke2['name'], poke1['name']))
        return 'win2'


def poke_keyboard2(team):
    randpoke = team
    randpokelist = []
    randpokelist2 = []
    for i in randpoke:
        randpokelist.append((pokelist[i]['name'], i))
    for i in randpokelist:
        randpokelist2.append([InlineKeyboardButton(text=i[0], callback_data=str(i[1]))])
    finalmarkup = InlineKeyboardMarkup(inline_keyboard=randpokelist2)
    return finalmarkup


def poke_keyboard3(team):
    if len(team) == 6:
        randpokelist = [
            [InlineKeyboardButton(text=pokelist[team[0]]['name'], callback_data=str(team[0])),
             InlineKeyboardButton(text=pokelist[team[1]]['name'], callback_data=str(team[1]))],
            [InlineKeyboardButton(text=pokelist[team[2]]['name'], callback_data=str(team[2])),
             InlineKeyboardButton(text=pokelist[team[3]]['name'], callback_data=str(team[3]))],
            [InlineKeyboardButton(text=pokelist[team[4]]['name'], callback_data=str(team[4])),
             InlineKeyboardButton(text=pokelist[team[5]]['name'], callback_data=str(team[5]))]
                                ]
    elif len(team) == 5:
        randpokelist = [
            [InlineKeyboardButton(text=pokelist[team[0]]['name'], callback_data=str(team[0])),
             InlineKeyboardButton(text=pokelist[team[1]]['name'], callback_data=str(team[1]))],
            [InlineKeyboardButton(text=pokelist[team[2]]['name'], callback_data=str(team[2])),
             InlineKeyboardButton(text=pokelist[team[3]]['name'], callback_data=str(team[3]))],
            [InlineKeyboardButton(text=pokelist[team[4]]['name'], callback_data=str(team[4]))]
                                ]
    elif len(team) == 4:
        randpokelist = [
            [InlineKeyboardButton(text=pokelist[team[0]]['name'], callback_data=str(team[0])),
             InlineKeyboardButton(text=pokelist[team[1]]['name'], callback_data=str(team[1]))],
            [InlineKeyboardButton(text=pokelist[team[2]]['name'], callback_data=str(team[2])),
             InlineKeyboardButton(text=pokelist[team[3]]['name'], callback_data=str(team[3]))],
                                ]
    elif len(team) == 3:
        randpokelist = [
            [InlineKeyboardButton(text=pokelist[team[0]]['name'], callback_data=str(team[0])),
             InlineKeyboardButton(text=pokelist[team[1]]['name'], callback_data=str(team[1]))],
            [InlineKeyboardButton(text=pokelist[team[2]]['name'], callback_data=str(team[2]))],
                                ]
    elif len(team) == 2:
        randpokelist = [
            [InlineKeyboardButton(text=pokelist[team[0]]['name'], callback_data=str(team[0])),
             InlineKeyboardButton(text=pokelist[team[1]]['name'], callback_data=str(team[1]))],
            ]

    finalmarkup = InlineKeyboardMarkup(inline_keyboard=randpokelist)
    return finalmarkup


def genteam():
    team = random.sample(range(251), 6)
    return team


def poke_percent(poke1, poke2):
    poke1s = 0
    poke2s = 0
    for n in range(1000):
        result = type_fight(poke1, poke2)
        if result == 'win1':
            poke1s += 1
        else:
            poke2s += 1
    print('%s ganhou %s vezes e %s ganhou %s vezes de um total de 1000 partidas' % (pokelist[poke1]['name'], poke1s,
                                                                                    pokelist[poke2]['name'], poke2s))


# print(typedict1)
def save():
    print('saved ranking')
    pickle.dump(ranking, open("ranking.p", "wb"))


def rank():
    tempdict = OrderedDict(sorted(ranking['season2'].items(),
                                  key=lambda kv: kv[1]['ELO'], reverse=True))
    finaltext = ''
    rank_pos = 1
    for i in tempdict:
        p = tempdict[i]['vitorias'] + tempdict[i]['derrotas']
        finaltext += '%s. %s: %s pontos (P:%s)\n' % (rank_pos, tempdict[i]['nome'], tempdict[i]['ELO'], p)
        rank_pos += 1
    print('rank exibido')
    return finaltext


def myrank(playerid):
    tempdict = OrderedDict(sorted(ranking['season2'].items(),
                                  key=lambda kv: kv[1]['ELO'], reverse=True))
    rank_pos = 1
    for i in tempdict:
        if i == playerid:
            p = tempdict[i]['vitorias'] + tempdict[i]['derrotas']
            finaltext = 'Você é o %s° no ranking de batalhas com %s pontos.\n' \
                        'Foram %s vitórias e %s derrotas em um total de %s partidas.' \
                        % (rank_pos, tempdict[i]['ELO'], tempdict[i]['vitorias'], tempdict[i]['derrotas'], p)
            print('rank pessoal exibido')
            return finaltext
        else:
            rank_pos += 1


def restart():
    ranking['season2'] = {}
    pickle.dump(ranking, open("ranking.p", "wb"))
    print(ranking)

