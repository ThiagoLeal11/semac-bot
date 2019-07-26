import random

from pytgbot import Bot
from semac_back import SemacBackend
from semac_front import SemacFrontend
from nlp import analyze_text
from variables import ALLOWED_IDS, BOT_TOKEN

# Some const
PRIVATE_COMMANDS = ['deploy', 'roolback', 'view']

def get_default_fallback():
    return random.choice(['Lamento, mas não compreendi.',
                          'Desculpe, mas eu não consigo. 😐',
                          'Infelizmente, não captei o que deseja. 😔',
                          'Não consegui entender, desculpe.',
                          'Isso não me diz nada.',
                          'Puxa, não foi dessa fez, mas continue tentando. Tchau!'])


def get_authorization_fallback():
    return random.choice(['Você não está autorizado para fazer isso...',
                          'Desculpe, isso é apenas para os adultos.',
                          'Sorry, não posso deixar que você faça isso.',
                          'Queria muito poder te ajudar, mas não posso.',
                          'Eu não estou autorizado a fazer isso pra você 😔',
                          'Me falaram que só a staff pode fazer esse tipo de coisa, e eu tenho que respeitar eles.',])


def get_welcome_fallback():
    return random.choice(['Olá!',
                          'Oi!',
                          'Saudações!',
                          'Opa!',
                          'Tudo bem?',
                          'Olá! É muito bom ter você por aqui. 😁',])


def get_online_fallback():
    return random.choice(['Está tudo ótimo!',
                          'Estou online e pronto pra qualquer coisa.',
                          'Tudo sim!',
                          'Melhor impossível!',
                          'Deixa eu verificar... sistemas funcionando normalmente, tudo em seu devido lugar... é, eu'
                          'estou bem sim. Obrigado por perguntar!',
                          'Estou sim! Obrigado por perguntar.',
                          'Olá. Tudo bem. Obrigada por perguntar.',
                          'Tudo as mil maravilhas, o que posso fazer por você?',
                          'Melhor impossível!',])


def get_doing_fallback(action, name):
    return random.choice([f'É pra já!\nFazendo o {action} do {name} agora mesmo.',
                          f'Iniciando o {action} do {name} nesse instante.',
                          f'Deixa comigo! Começando o {action} do {name}...',
                          f'Tudo bem, fazendo o {action} do {name} agorinha!'
                          f'{name} é comigo mesmo, fazendo o {action} agora',
                          f'Mal posso esperar para isso, começando o {action} do {name}.',
                          f'Já era hora, vou fazer {action} do {name} com muito amor.\nEu te aviso se alguma coisa der errado',
                          f'Vou fazer o {action} do {name} com muito cuidado.'])


def get_bad_word_correction():
    return random.choice(['Que coisa feia, você não deveria falar isso.',
                          'Acho que vou ter que lavar sua boca com sabão.',
                          'Sua mão não te ensinou modos, não?',
                          'Não vou nem falar nada.',
                          'Quem está falando? É a Dercy?',
                          'Puxa vida 😔\nSe você quiser reportar algo, me envie um comentário.'])


def was_made_by_staff(context):
    return context['message']['from']['id'] in ALLOWED_IDS


def get_text(context):
    return context['message']['text'] if 'text' in context['message'] else None


def get_user_id(context):
    return context['message']['from']['id']


def process_input(context):
    text = get_text(context)
    context = analyze_text(text, context)
    print(context)

    if not context['intent'] in PRIVATE_COMMANDS:
        process_regular_command(context)
    elif was_made_by_staff(context):
        process_private_command(context)
    else:
        bot.send_message(get_user_id(context), get_authorization_fallback())


def process_regular_command(context):
    user_id = get_user_id(context)

    if context['intent'] == 'hi':
        bot.send_message(user_id, get_welcome_fallback())
    elif context['intent'] == 'ruok':
        bot.send_message(user_id, get_online_fallback())
    elif context['intent'] == 'badword':
        bot.send_message(user_id, get_bad_word_correction())
    elif context['intent'] == 'exit':
        bot.send_message(user_id, get_authorization_fallback())
    else:
        bot.send_message(user_id, get_default_fallback())


def process_private_command(context):
    user_id = get_user_id(context)

    if context['intent'] == 'deploy' and 'type' in context['parameters']:

        if context['parameters']['type'] == 'frontend':
            bot.send_message(user_id, get_doing_fallback('deploy', 'frontend'))
            SemacFrontend(bot, user_id).deploy()
        elif context['parameters']['type'] == 'backend':
            bot.send_message(user_id, get_doing_fallback('deploy', 'backend'))
            SemacBackend(bot, user_id).deploy()

    elif context['intent'] == 'roolback' and 'type' in context['parameters']:
        if context['parameters']['type'] == 'frontend':
            bot.send_message(user_id, get_doing_fallback('roolback', 'frontend'))
            SemacFrontend(bot, user_id).revert()
        elif context['parameters']['type'] == 'backend':
            bot.send_message(user_id, get_doing_fallback('roolback', 'backend'))
            SemacBackend(bot, user_id).revert()

    elif context['intent'] == 'view' and 'type' in context['parameters']:
        if context['parameters']['type'] == 'frontend':
            SemacFrontend(bot, user_id).show_actual_version()
        elif context['parameters']['type'] == 'backend':
            SemacBackend(bot, user_id).show_actual_version()

    else:
        bot.send_message(user_id, get_default_fallback())


# Setup bot
bot = Bot(BOT_TOKEN)

# Sending a message when bot is on
bot.send_message(ALLOWED_IDS[0], "Estou online de novo!")

# Get last message sended
last_update_id = 0
while True:
    for update in bot.get_updates(limit=100, offset=last_update_id+1):
        last_update_id = update.update_id
        process_input(update.to_array())
