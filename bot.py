# -*- coding: utf-8 -*-
"""telegram_bot_simple_application.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1vC6o3AeBQOCmhyR_KCVvs_a37T9_wQHU
"""
import telebot
import os
from flask import Flask, request

API_KEY = '5682851395:AAEe7D_j4mCabT2fsQpltiJuFOR75fSml_c'

server = Flask(__name__)

REQUEST_DEFAULT = 'default'
REQUEST_CPF = 'cpf'
REQUEST_ADDRESS = 'address'

request_stage = REQUEST_DEFAULT

WELCOME_MESSAGE = """
  Olá, bem vindo ao lanche 'Comida Boa'.

  Escolha um dos itens abaixo para reservar seu pedido

  /x_salada     X-Salada   R$ 06,00
  /x_tudo       X-Tudo     R$ 12,00
  /misto        Misto      R$ 04,00
"""

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

bot = telebot.TeleBot(API_KEY)


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
        bot.reply_to(message, WELCOME_MESSAGE)
    elif request_stage == REQUEST_CPF:
        request_stage = REQUEST_ADDRESS
        bot.reply_to(message, ASK_FOR_ADDRESS)
    elif request_stage == REQUEST_ADDRESS:
        request_stage = REQUEST_DEFAULT
        bot.reply_to(message, FINISH_LABEL)


# FLASK SERVER

@server.route('/' + API_KEY, methods=['POST'])
def get_message():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode('utf-8'))])
    return '!', 200


@server.route('/')
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://telegram-bot-gsda.herokuapp.com/' + API_KEY)
    return '!', 200


if __name__ == '__main__':
    server.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
