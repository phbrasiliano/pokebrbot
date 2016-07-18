import time
import random
import telepot
import pickle
import schedule
import PokeFight
import _thread

"""
PokeBot versão beta
Bot criado com o propósito de aprender programação.
possui alguns comandos simples e uma batalha.
"""
pokelist = pickle.load(open("pokelist2.p", "rb"))
battledic = {}
battledic[0] = PokeFight.Battle(0)


def handle(msg):
    global battledic
    msg_id = msg['message_id']
    content_type, chat_type, chat_id = telepot.glance(msg)
    nome_usuario = msg['from']['first_name']
    user_id = msg['from']['id']
    bot_name = str.lower(bot.getMe()['username'])

    # Este if impede o bot de responder mensagens que tenham sido enviadas antes de sua ativação
    if timestamp >= msg['date']:
        return

    if content_type == 'text':
        mensagem = str.lower(msg['text'])
        print('%s: "%s"' % (nome_usuario, mensagem))
        if mensagem == '/shutdown0709':
            global off_switch
            off_switch = 0

        if mensagem == '/ajuda':
            bot.sendMessage(chat_id, 'Olá, eu sou o PokebrBOT, o Bot de batalhas pokemon! \n'
                                     'Meus principais comandos são:'
                                     '\n /pokedex retorna um Pokemon aleatório, e uma breve descrição (em inglês).'
                                     '\n /batalhar inicia uma batalha pokemon! (apenas em grupos)'
                                     '\n /ranking exibe o rank global da atual temporada de batalhas pokemon.'
                                     '\n /meurank exibe estatísticas do seu próprio desempenho.'
                                     '\n /faq mostra perguntas mais frequentes sobre o funcionamento do BOT'
                                     '(apenas em privado).'
                                     '\n outros comandos serão adicionados posteriormente :)')

        elif mensagem[0] != '/' and any(i in mensagem for i in ('RameloBOT', 'ramelobot', 'RAMELOBOT', 'RameloBot',
                                                                'Blitzcrank', 'bot do ramelo', 'ramelo bot')):
            bot.sendMessage(chat_id, "Oi %s, me chamou? Digite /ajuda para saber meus comandos." % nome_usuario,
                            reply_to_message_id=msg_id)

        elif mensagem == '/pokedex' or mensagem == '/pokedex@%s' % bot_name:
            responder_poke = pokemon(random.randrange(251))
            bot.sendSticker(chat_id, responder_poke[0], reply_to_message_id=msg_id)
            bot.sendMessage(chat_id, responder_poke[1], )
        elif mensagem == '/ranking' or mensagem == '/ranking@%s' % bot_name:
            bot.sendMessage(chat_id, 'Ranking da segunda temporada de batalhas Pokemon:\n%s' % PokeFight.rank())
        elif mensagem == '/resetdoudaralho0709':
            PokeFight.restart()
        elif mensagem == '/meurank' or mensagem == '/ranking@%s' % bot_name:
            try:
                bot.sendMessage(chat_id, 'Sua posição no rank da segunda temporada de batalhas Pokemon:\n%s'
                                % PokeFight.myrank(user_id))
            except IndexError:
                bot.sendMessage(chat_id, 'Você ainda não está classificado no rank das batalhas.')
        elif mensagem == '/batalhar' or mensagem == '/batalhar@%s' % bot_name:
            if chat_type == 'group':
                try:
                    if chat_id not in battledic:
                        battledic[chat_id] = PokeFight.Battle(chat_id)
                    battle = battledic[chat_id]
                    for i in battledic:
                        if user_id in battledic[i].p1 or user_id in battledic[i].p2:
                            bot.sendMessage(user_id, 'Você já está registrado para uma batalha, '
                                                     'aguarde enquanto a anterior não termina.')
                            return
                    if battle.pcount == 2:
                        bot.sendMessage(user_id, 'No momento, %s está batalhando contra %s.\n'
                                                 'Aguarde enquanto a batalha não acaba.' % (
                                                  battle.p1[0], battle.p2[0]))
                        return
                    if battle.pcount == 0:
                        bot.sendMessage(user_id, 'Você se cadastrou para batalha, aguarde um oponente.')
                        battle.timer += 1
                        _thread.start_new_thread(timeout, (chat_id,))
                        battle.team1 = PokeFight.genteam()
                        bot.sendMessage(chat_id,
                                        'Desafio lançado! digite /batalhar para aceitar o desafio de %s' % nome_usuario)

                        battle.pcount += 1
                        battle.p1 = (nome_usuario, user_id)
                    elif battle.pcount == 1:
                        bot.sendMessage(user_id, 'Você aceitou o desafio!')
                        battle.p2 = (nome_usuario, user_id)
                        battle.team2 = PokeFight.genteam()
                        bot.sendMessage(battle.p2[1], 'Esta batalha é uma melhor de 3. Escolha seu primeiro pokemon:',
                                        reply_markup=PokeFight.poke_keyboard3(battle.team2))
                        bot.sendMessage(battle.p1[1], 'Esta batalha é uma melhor de 3. Escolha seu primeiro pokemon:',
                                        reply_markup=PokeFight.poke_keyboard3(battle.team1))
                        bot.sendMessage(chat_id, 'Desafio aceito! %s e %s agora estão batalhando.' % (
                            battle.p1[0], nome_usuario))
                        battle.pcount += 1
                        battle.timer -= 1

                except telepot.exception.TelegramError:
                    bot.sendMessage(chat_id, 'Você ainda não possui registro, envie o comando /start para mim em um'
                                             'chat particular (@%s <-- clique aqui) para cadastrar-se' % bot_name)
                    return
        elif mensagem == '/start' or mensagem == '/start@%s' % bot_name:
            if chat_type == 'group':
                bot.sendMessage(chat_id, 'Para se cadastrar para as batalhas, envie o comando diretamente para mim em'
                                         ' um chat particular! Clique em @%s e envie /start' % bot_name),
            if chat_type == 'private':
                bot.sendMessage(chat_id, 'Você agora está cadastrado para as batalhas pokemon, as batalhas funcionam '
                                         'somente em grupos em que o bot esteja adicionado.\nDigite /ajuda para '
                                         'conhecer os comandos do bot, ou /faq para as perguntas mais frequentes.')
        if chat_type == 'private':
            if mensagem == '/faq' or mensagem == '/faq@%s' % bot_name:
                bot.sendMessage(user_id, '<strong>O que é o @PokebrBot?</strong>\n'
                                         'Esse bot foi criado como um projeto pessoal, com o objetivo de estudar '
                                         'programação. Quis fazer uma aplicação que fosse complexa o suficiente para '
                                         'representar um desafio para mim, e que fosse divertido de alguma forma. O bot'
                                         ' foi desenvolvido inteiramente em Python, utilizando a '
                                         '<a href="https://pokeapi.co/">PokeAPI</a>, e o '
                                         '<a href="https://github.com/nickoala/telepot">Telepot</a>.'
                                         '\n\n<strong>Como são definidas as batalhas?</strong>\n'
                                         'Os times são gerados aleatoriamente, sem modificadores, as batalhas em si'
                                         ' levam em conta a soma dos status base de cada Pokemon que são somados a um'
                                         ' modificador semi-aleatório baseado nas suas fraquezas e resistências. '
                                         'Basicamente pokemons mais fortes ganham de mais fracos na maior parte das'
                                         ' vezes, mas ainda há um valor aleatório nos combates.'
                                         '\n\n<strong>Por que a pokedex está em inglês?</strong>\n'
                                         'A database do bot foi criada utilizando a '
                                         '<a href="https://pokeapi.co/">PokeAPI</a>, que está em inglês. Traduzir tudo '
                                         'levaria tempo demais\n\n<strong>Por que o bot só tem 251 Pokemons?</strong>\n'
                                         'Basicamente por três motivos: Primeiro, há uma limitação pois não encontrei '
                                         'stickers para pokemons até a última geração. Segundo, preferi um numero mais '
                                         'limitado de opções para os jogadores, e por fim, por questão de gosto mesmo'
                                         '\n\n<strong>Encontrei um Erro / Bug, ou tenho uma sugestão!</strong>\n'
                                         'Qualquer erro (mesmo que de gramática) que encontrar pode enviar direto para '
                                         'mim @phellpss, também aceito sugestões e reclamações para futuras alterações'
                                         ' no bot. Lembrando que é apenas um projeto pessoal, sem grandes pretenções ;)'
                                , disable_web_page_preview=True, parse_mode='HTML')


# função que retorna um sticker e os dados do pokemon relacionado
def pokemon(n):
    sticker = pokelist[n]['sticker']
    if len(pokelist[n]['types']) == 1:
        texto = "You've got %s! The %s Pokémon, its type is %s and his pokédex number is %s" % (
            pokelist[n]['name'], pokelist[n]['species'], pokelist[n]['types'][0], pokelist[n]['national_id'])
    else:
        texto = "You've got %s! The %s Pokémon, its types are %s and %s, and his national pokédex number is %s" % (
            pokelist[n]['name'], pokelist[n]['species'], pokelist[n]['types'][0], pokelist[n]['types'][1],
            pokelist[n]['national_id'])
    return sticker, texto


def pokebat(chat_id):
    battle = battledic[chat_id]
    poke1 = battle.battlechoicep1
    poke2 = battle.battlechoicep2
    p1score = battle.p1score
    p2score = battle.p2score
    if poke1 == -1 or poke2 == -1:
        return
    elif p1score != 2 and p2score != 2:
        result = PokeFight.type_fight(poke1, poke2)
        battle.team1.remove(poke1)
        battle.team2.remove(poke2)
        battle.battlechoicep1 = -1
        battle.battlechoicep2 = -1
        if result == 'win1':
            battle.p1score += 1
            bot.sendSticker(battle.p1[1], pokelist[poke2]['sticker'])
            bot.sendMessage(battle.p1[1],
                            'Seu oponente escolheu %s, e agora eles estão batalhando!' % pokelist[poke2]['name'])
            bot.sendSticker(battle.p2[1], pokelist[poke1]['sticker'])
            bot.sendMessage(battle.p2[1],
                            'Seu oponente escolheu %s, e agora eles estão batalhando!' % pokelist[poke1]['name'])
            time.sleep(4)
            bot.sendMessage(battle.p1[1],
                            'Seu %s venceu a batalha contra %s' % (pokelist[poke1]['name'], pokelist[poke2]['name']))
            bot.sendMessage(battle.p2[1],
                            'Seu %s perdeu a batalha contra %s' % (pokelist[poke2]['name'], pokelist[poke1]['name']))
        if result == 'win2':
            battle.p2score += 1
            bot.sendSticker(battle.p2[1], pokelist[poke1]['sticker'])
            bot.sendMessage(battle.p2[1],
                            'Seu oponente escolheu %s, e agora eles estão batalhando!' % pokelist[poke1]['name'])
            bot.sendSticker(battle.p1[1], pokelist[poke2]['sticker'])
            bot.sendMessage(battle.p1[1],
                            'Seu oponente escolheu %s, e agora eles estão batalhando!' % pokelist[poke2]['name'])
            time.sleep(4)
            bot.sendMessage(battle.p2[1],
                            'Seu %s venceu a batalha contra %s' % (pokelist[poke2]['name'], pokelist[poke1]['name']))
            bot.sendMessage(battle.p1[1],
                            'Seu %s perdeu a batalha contra %s' % (pokelist[poke1]['name'], pokelist[poke2]['name']))
    if battle.p1score == 2 or battle.p2score == 2:
        if battle.p1[1] not in PokeFight.ranking['season2']:
            PokeFight.ranking['season2'][battle.p1[1]] = {}
            PokeFight.ranking['season2'][battle.p1[1]]['nome'] = battle.p1[0]
            PokeFight.ranking['season2'][battle.p1[1]]['vitorias'] = 0
            PokeFight.ranking['season2'][battle.p1[1]]['derrotas'] = 0
            PokeFight.ranking['season2'][battle.p1[1]]['ELO'] = 50
        if battle.p2[1] not in PokeFight.ranking['season2']:
            PokeFight.ranking['season2'][battle.p2[1]] = {}
            PokeFight.ranking['season2'][battle.p2[1]]['nome'] = battle.p2[0]
            PokeFight.ranking['season2'][battle.p2[1]]['vitorias'] = 0
            PokeFight.ranking['season2'][battle.p2[1]]['derrotas'] = 0
            PokeFight.ranking['season2'][battle.p2[1]]['ELO'] = 50
        if battle.p1score == 2:
            bot.sendMessage(battle.p1[1], 'Parabéns! você venceu a batalha :)')
            bot.sendMessage(battle.p2[1], 'Você perdeu esta batalha, mais sorte na próxima.')
            bot.sendMessage(battle.mainchat,
                            'A batalha terminou! %s venceu.\nDigite /batalhar para ser o próximo.' % battle.p1[0])
            if battle.p1[1] in PokeFight.ranking['season2']:
                PokeFight.ranking['season2'][battle.p1[1]]['vitorias'] += 1
                PokeFight.ranking['season2'][battle.p1[1]]['ELO'] += 1
                PokeFight.ranking['season2'][battle.p2[1]]['derrotas'] += 1
                PokeFight.ranking['season2'][battle.p2[1]]['ELO'] -= 1
        elif battle.p2score == 2:
            bot.sendMessage(battle.p2[1], 'Parabéns! você venceu a batalha :)')
            bot.sendMessage(battle.p1[1], 'Você perdeu esta batalha, mais sorte na próxima.')
            bot.sendMessage(battle.mainchat,
                            'A batalha terminou! %s venceu.\nDigite /batalhar para ser o próximo.' % battle.p2[0])
            if battle.p2[1] in PokeFight.ranking['season2']:
                PokeFight.ranking['season2'][battle.p2[1]]['vitorias'] += 1
                PokeFight.ranking['season2'][battle.p2[1]]['ELO'] += 1
                PokeFight.ranking['season2'][battle.p1[1]]['derrotas'] += 1
                PokeFight.ranking['season2'][battle.p1[1]]['ELO'] -= 1
        battle.reset()
        PokeFight.save()
        return

    bot.sendMessage(battle.p1[1], '%s %s x %s %s\nEscolha seu próximo pokemon:' %
                    (battle.p1[0], battle.p1score, battle.p2score, battle.p2[0]),
                    reply_markup=PokeFight.poke_keyboard3(battle.team1))
    bot.sendMessage(battle.p2[1], '%s %s x %s %s\nEscolha seu próximo pokemon:' %
                    (battle.p1[0], battle.p1score, battle.p2score, battle.p2[0]),
                    reply_markup=PokeFight.poke_keyboard3(battle.team2))


def callback_query(msg):
    query_id, from_id, data = telepot.glance(msg, flavor='callback_query')
    idata = int(data)
    iduser = int(from_id)
    for i in battledic:
        if iduser in battledic[i].p1 or iduser in battledic[i].p2:
            battle = battledic[i]

            try:
                if battle.battlechoicep1 == -1 and battle.p1[1] == from_id:
                    if idata not in battle.team1:
                        bot.sendMessage(from_id,
                                        'Este pokemon não está disponível pra você no momento...'
                                        ' está tentando trapacear? ;)')
                    else:
                        bot.sendSticker(from_id, pokelist[idata]['sticker'])
                        bot.sendMessage(from_id, 'Você escolheu %s!' % pokelist[idata]['name'])
                        battle.battlechoicep1 = idata
                        pokebat(battle.mainchat)
                elif battle.battlechoicep1 != -1 and battle.p1[1] == from_id:
                    bot.sendMessage(from_id, 'Aguardando oponente')
                elif battle.battlechoicep2 == -1 and battle.p2[1] == from_id:
                    if idata not in battle.team2:
                        bot.sendMessage(from_id,
                                        'Este pokemon não está disponível pra você no momento... '
                                        'está tentando trapacear? ;)')
                    else:
                        bot.sendMessage(from_id, 'Você escolheu %s!' % pokelist[idata]['name'])
                        bot.sendSticker(from_id, pokelist[idata]['sticker'])
                        battle.battlechoicep2 = idata
                        pokebat(battle.mainchat)
                elif battle.battlechoicep2 != -1 and battle.p2[1] == from_id:
                    bot.sendMessage(from_id, 'Aguardando oponente')
                else:
                    bot.sendMessage(from_id, 'Você não está inscrito para esta batalha,'
                                             ' por favor aguarde enquanto não termina')
            except IndexError:
                pass
        else:
            pass


def timeout(idbattle):
    time.sleep(90)
    battle = battledic[idbattle]
    if battledic[idbattle].timer == 1:
        print('batalha foi interrompida por timeout')
        bot.sendMessage(idbattle, 'Ninguém aceitou o desafio, por favor tente novamente')
        battle.reset()
    else:
        return


timestamp = int(time.time())
token = '' #insert token here
bot = telepot.Bot(token)
bot.message_loop({'chat': handle,
                  'callback_query': callback_query})
print('I am listening ...')
off_switch = 1

while off_switch == 1:
    schedule.run_pending()
    time.sleep(10)

print('morto por causas naturais')
