import asyncio 
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from  utils import *
from aiogram.enums import ParseMode
import os
from aiogram.enums.content_type import ContentType
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from main import *
from aiogram.methods.ban_chat_member import BanChatMember
from aiogram import F
from aiogram.methods.get_chat_administrators import GetChatAdministrators
import json
from aiogram import Bot, Dispatcher, types
from aiogram.types.message import ContentType
from time import sleep
#как в любом уважающем паттерне  архитектуры как PIDOR добавляем Диспетчера
dp = Dispatcher()

ChatsWithBunt = {}

#добавляем донаты, чтобы лавэха мутилась
COOCKIE = types.LabeledPrice(label='Печенька овсяная', amount=3400)
COFFE  = types.LabeledPrice(label = "Кофе зернёное", amount = 10**4)

PaymentToken = GetBotToken("PaymentToken")

chats = []

# Получить информацию о члене чата
async def CheckAdminModer(ChatId, UserId):
    chat_member = await bot.get_chat_member(ChatId, UserId)

    # Проверить, является ли отправитель администратором
    if chat_member.status in ['administrator', 'creator']:
        return True
    else:
        return False


#создаём мидловую тварь, чтобы на колбэк хэндлеры отвечал как автомат
#dp.callback_query.middleware(CallbackAnswerMiddleware())

#добавляем обработчиков для событий
#сздаём класс для команды start и передаём в dp.message() 
@dp.message(Command("start"))
#заметь, мы добавляем аннотацию что message - это не какой-то чепуч, а объект классса types.Message
async def BotsStart(msg: types.Message):
    global chats
    await msg.reply(f"День добрый. Я - Метрокоп. Добавьте меня в группу для того чтобы я следил за участниками группы",
                     parse_mode=ParseMode.HTML)

    
    

@dp.message(Command("ban"))
async def BanHammer(msg:types.Message):
    chat_id = msg.chat.id
    user_id = msg.from_user.id
    HammerTester = msg.text.split(" ")[1]

    await msg.chat.ban (chat_id, user_id)
    await bot.send_message(chat_id, f"{HammerTester} отведал Молотка бана")

@dp.message(lambda message: "бля" in message.text.lower() or "пизд" in message.text.lower() or "ху" in message.text.lower())
async def BlyadskiyHandler(msg: types.Message):
    await msg.reply("без мата!")
    

@dp.message(lambda message: "монолит" in message.text.lower())
async def MonolitHandler(msg: types.Message):
    await msg.reply("Благодарим тебя за то, что раскрыл слугам твоим козни врагов наших. Озари сиянием своим души тех, кто отдал жизнь во исполнение воли твоей. В бой, защитники Монолита! В бой! Отомстим за павших братьев наших. Да будет благословенно их вечное единение с Монолитом! Смерть… Лютая смерть тем, кто отвергает его священную силу.")

#команды чтоб пользователям жизнь малиной не казалась 
@dp.message(Command("CutAxe"))
async def MurderAxeHandler(msg: types.Message):
    UserId = msg.text.split(" ")[1]
    await msg.reply(f"@{UserId} получил по тыкве топором от американского психопата")


@dp.message(Command("Shoot"))
async def MurderAxeHandler(msg: types.Message):
    UserId = msg.text.split(" ")[1]
    await msg.reply(f"@{UserId} получил по тыкве пулей 9×39 мм из ВСС Винторез")


@dp.message(Command("Acid"))
async def MurderAcidHandler(msg: types.Message):
    UserId = msg.text.split(" ")[1]
    await msg.reply(f"@{UserId} получил по тыкве H2SO4")



#призыв админа. Не рекомендует к использованию
@dp.message(Command("SpawnAdmins"))
async def SpawnAdminHandler(msg: types.Message):
    AdminsList =  await bot.get_chat_administrators(msg.chat.id)
    k = ""
    for i in AdminsList:
        k += f"@{i}"

    report = msg.text.split(" ")[1]

    msg.send_message(msg.chat.id, k + "   " + k)


@dp.message()
async def some_message_handler(msg: types.Message):
    global chats
    if not msg.chat.id in chats:
        chats.append(msg.chat.id)

@dp.message(Command("ThanksToBot"))
async def choose_your_dinner(msg:types.Message):
    await msg.answer("""Спасибо, что пользуетесь моим ботом Метрокоп 🤍
Здесь вы можете увидеть его <a href="https://pornhub.com">исходники👨‍💻</a>
Если вам понравился мой бот, вы можете добавить его в свой чат! 💬""",
                     parse_mode='HTML')
    

#а в этом хэнделере мы инфу о чате намучиваем
@dp.message(Command("Info"))
async def InfoHandler(msg:types.Message):
    ChatId = msg.chat.id
    NumOfMembers = await bot.get_chat_members_count(ChatId)
    ListOfModers = "<ol>"
    DataOfMember = await bot.get_chat_administrators(ChatId)
    for i in DataOfMember:
        ListOfModers += f"<li>{i}</li>"

    ListOfModers += "</ol>"
    ChatTitle = msg.chat.title
    ChatAbout = msg.chat.bio
    ChatAbout2 = msg.chat.description



#вы не подпишите мою петицию? 
#                           Чувак
@dp.message(Command("BanPetiion"))
async def PetionHandler(msg:types.Message):
    UserId = msg.text.split(" ")[1]
    if not UserId in ChatsWithBunt:
        ChatsWithBunt[UserId] = 1
        print(ChatsWithBunt)
    else:
        ChatsWithBunt[UserId] += 1
        if ChatsWithBunt[UserId]  > (await bot.get_chat_members_count(msg.chat.id) ) // 2:
            await msg.chat.ban(msg.chat.id, UserId)
            await bot.reply(msg.chat.id, "После подпсания петиции забанили" + F"@{UserId}")


@dp.message(Command("BuyCookie"))
async def buy(message: types.Message):

    if PaymentToken.split(':')[1] == 'TEST':
        await bot.answer(message.chat.id, "Тестовый платеж!!!")

    await bot.send_invoice(message.chat.id,
                           title="Подписка на бота",
                           description="Активация подписки на бота на 1 месяц",
                           provider_token=PaymentToken,
                           currency="rub",
                           photo_url="https://i.ytimg.com/vi/9C-lnHnkTEI/sddefault.jpg",
                           photo_width=416,
                           photo_height=234,
                           photo_size=416,
                           is_flexible=False,
                           prices=[COOCKIE],
                           start_parameter="one-month-subscription",
                           payload="test-invoice-payload")
    

@dp.message(Command("BuyCoffee"))
async def buy(message: types.Message):

    if PaymentToken.split(':')[1] == 'TEST':
        await bot.answer(message.chat.id, "Тестовый платеж!!!")

    await bot.send_invoice(message.chat.id,
                           title="Подписка на бота",
                           description="Активация подписки на бота на 1 месяц",
                           provider_token=PaymentToken,
                           currency="rub",
                           photo_url="https://i.ytimg.com/vi/9C-lnHnkTEI/sddefault.jpg",
                           photo_width=416,
                           photo_height=234,
                           photo_size=416,
                           is_flexible=False,
                           prices=[COFFE],
                           start_parameter="one-month-subscription",
                           payload="test-invoice-payload")
    

# pre checkout  (must be answered in 10 seconds)
@dp.pre_checkout_query_handler(lambda query: True)
async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)


# successful payment
@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: types.Message):
    payment_info = message.successful_payment.to_python()
    for k, v in payment_info.items():
        print(f"{k} = {v}")

    await bot.send_message(message.chat.id,
                           f"Платеж на сумму {message.successful_payment.total_amount // 100} {message.successful_payment.currency} прошел успешно!!!")