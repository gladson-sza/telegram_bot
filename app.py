import emoji
from telebot import TeleBot, types
from flask import Flask, request

API_KEY = '5682851395:AAEe7D_j4mCabT2fsQpltiJuFOR75fSml_c'

app = Flask(__name__)

REQUEST_DEFAULT = 'default'
REQUEST_CPF = 'cpf'
REQUEST_ADDRESS = 'address'

request_stage = REQUEST_DEFAULT

WELCOME_MESSAGE = emoji.emojize("""
  Olá, bem vindo ao lanche 'Comida Boa'.
  Escolha um dos itens abaixo para reservar seu pedido
  
  :thumbs_up:
""")

ASK_FOR_CPF = """
  Certo, gostaria de adicionar seu CPF à nota?
  /sim
  /nao
"""

ASK_FOR_ADDRESS = 'Insira seu endereço para que possamos enviar seu pedido, o pagamento será realizado na entrega'

CPF_LABEL = 'Insira seu CPF, somente números'

FINISH_LABEL = """
  Parabéns, seu pedido foi concluído com sucesso, seu pedido estará pronto em alguns minutos, fique de olho no seu dispositivo, o motorista poderá lhe contatar caso não encontre o endereço.

  Tenha uma ótima refeição.
"""

bot = TeleBot(API_KEY)


@bot.message_handler(commands=['x_salada', 'x_tudo', 'misto'])
def ask_for_cpf(message):
    bot.reply_to(message, ASK_FOR_CPF)


@bot.message_handler(commands=['nao'])
def ask_for_address(message):
    global request_stage

    request_stage = REQUEST_ADDRESS
    bot.reply_to(message, ASK_FOR_ADDRESS)


@bot.message_handler(commands=['sim'])
def insert_cpf(message):
    global request_stage

    request_stage = REQUEST_CPF
    bot.reply_to(message, CPF_LABEL)


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    global request_stage

    if request_stage == REQUEST_DEFAULT:
        markup = types.ReplyKeyboardMarkup(row_width=2)
        heart = types.KeyboardButton(emoji.emojize(':red_heart:'))
        markup.add(heart)

        bot.reply_to(message, WELCOME_MESSAGE, reply_markup=markup)
    elif request_stage == REQUEST_CPF:
        request_stage = REQUEST_ADDRESS
        bot.reply_to(message, ASK_FOR_ADDRESS)
    elif request_stage == REQUEST_ADDRESS:
        request_stage = REQUEST_DEFAULT
        bot.reply_to(message, FINISH_LABEL)


# FLASK SERVER

@app.route('/' + API_KEY, methods=['POST'])
def get_message():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode('utf-8'))])
    return 'Bot Online!', 200


@app.route('/')
def set_webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://18.216.97.113.nip.io/' + API_KEY)
    return 'Bot webhook set', 200


# MAIN
if __name__ == '__main__':
    bot.remove_webhook()
    bot.polling()

    # app.run(host='0.0.0.0', port=8000)
