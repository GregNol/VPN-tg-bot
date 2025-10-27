import datetime
from vless_api import *
import json
import logging
import sqlite3 as sl
from aiogram.methods.delete_message import DeleteMessage
from aiogram import types, Bot, Dispatcher, html, F
# from aiogram.utils import executor
# from aiogram.dispatcher.filters.state import StatesGroup, State
# from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, LabeledPrice
# from aiogram.dispatcher.filters import Text
from keyboard import *
# from aiogram.utils.media_group import MediaGroupBuilder
import asyncio
# from aiogram import F
from aiogram.filters.command import Command
# from aiogram.filters.command import CommandStart
# from aiogram.types import FSInputFile, URLInputFile, BufferedInputFile
from aiogram.types import FSInputFile, URLInputFile, BufferedInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.deep_linking import create_start_link, decode_payload
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types.message import ContentType
from aiogram.exceptions import TelegramAPIError
ADMIN_ID = 817866082
TOKEN_BOT = "8309478056:AAFYSnKH-h12cWDqYru-tyLiKX11qBooO7E" # prod
# TOKEN_BOT = '7808410175:AAHbmlDlJcYDQ40C-RWlNamQio-Wdk2g95s' # dev
month_1 = LabeledPrice(amount=9900, label='Доступ на 1 месяц')
month_3 = LabeledPrice(amount=26900, label='Доступ на 3 месяца')
month_6 = LabeledPrice(amount=44900, label='Доступ на 5 месяцев')
month_12 = LabeledPrice(amount=59900, label='Доступ на 12 месяцев')
bonuses = {
    1: 20,
    3: 54,
    6: 90,
    12: 120
}
provider_token = '390540012:LIVE:74860'
start_message = 'Добро пожаловать!\n\nЗдесь вы сможете подключиться к самым быстрым VLESS серверам🚀\n\nНастройка занимает менее двух минут!\n\nНажимай, чтобы подключиться⬇️'
info_message = '🚀 Высокоскоростные серверы\nPrynet использует высокопроизводительные и скоростные серверы в Европе для обеспечения стабильного и быстрого подключения.\n\n🔐 Безопасность\nPrynet использует VLESS протокол передачи данных, что гарантирует вашу конфиденциальность и безопасность соединения.'
readme_message = 'Инструкция находится в разработке.'
class Form(StatesGroup):
    contact = State()
# FSM для рассылки
class BroadcastState(StatesGroup):
    waiting_for_text = State()

bot = Bot(token=TOKEN_BOT, default=DefaultBotProperties(
        parse_mode=ParseMode.HTML
        # тут ещё много других интересных настроек
    ))
# bot.delete_webhook()
dp = Dispatcher(bot=bot)
logging.basicConfig(level=logging.INFO)
import sqlite3 as sl
con = sl.connect('users.db')
cur = con.cursor()


@dp.message(Command("start"))
async def start_process(message: types.Message,state: FSMContext,bot: Bot,command: Command = None):
    cur.execute(f'''select * from users where tgid = {message.from_user.id}''')
    x = cur.fetchone()
    if not x:
        reference = 817866082
        if command.args:
            args = command.args
            try:
                reference = decode_payload(args)
                cur.execute(
                    f"""SELECT cnt_friend FROM users WHERE tgid='{reference}'""")
                x = cur.fetchone()[0]
                cur.execute(
                    f"""UPDATE users SET cnt_friend={x + 1} WHERE tgid='{reference}'""")
                con.commit()
            except Exception as e:
                reference = 0
                print(e)

        cur.execute(
            f"""INSERT INTO users (username, tgid, name, parentid, expiry_time) VALUES ('{message.from_user.username}', '{message.from_user.id}', '{str(message.from_user.first_name)}', '{reference}', '2020-08-09 23:12:38.322444')""")
        con.commit()
    await bot.send_message(chat_id=message.from_user.id, text=start_message, reply_markup=start_keyboard)


@dp.callback_query(F.data == 'buy')
async def buy_keypoard(message: types.CallbackQuery,state: FSMContext,bot: Bot,command: Command = None):
    await bot.send_message(chat_id=message.from_user.id, text='Выберите вариант подписки.', reply_markup=buy)


@dp.callback_query(F.data == 'main')
async def profil(message: types.CallbackQuery,state: FSMContext,bot: Bot,command: Command = None):
    text = f'ID: {message.from_user.id}\nПодробную информацию про использование сервиса можете найти в Инструкции'

    await bot.send_message(chat_id=message.from_user.id, text=text, reply_markup=main_keyboard)


@dp.callback_query(F.data == 'ref')
async def referal(message: types.CallbackQuery,state: FSMContext,bot: Bot,command: Command = None):

    cur.execute(
        f'''SELECT * FROM users where tgid="{message.from_user.id}"''')
    user = cur.fetchone()
    print(user)
    link = await create_start_link(bot, str(message.from_user.id), encode=True)
    ref_message = f'👤Кабинет Партнера\n\nБаланс: {user[4]}\nПриглашено друзей: {user[9]}\nРеферальная ссылка: {link}\n\nРеферальная программа позволяет Вам приглашать других людей в Prynet. Любой человек, который перейдет по вашей ссылке, будет закреплен за Вами.\n\nПолучайте 20% от суммы платежей приглашенных людей. Заработанные деньги можно потратить на приобретение подписки.'
    await bot.send_message(chat_id=message.from_user.id, text=ref_message, reply_markup=return_keyboard)


@dp.callback_query(F.data == 'info')
async def get_info(message: types.CallbackQuery,state: FSMContext,bot: Bot,command: Command = None):
    await bot.send_message(chat_id=message.from_user.id, text=info_message, reply_markup=return_keyboard)

@dp.callback_query(F.data == 'readme')
async def get_info(message: types.CallbackQuery,state: FSMContext,bot: Bot,command: Command = None):
    await bot.send_message(chat_id=message.from_user.id, text=readme_message, reply_markup=return_keyboard)


@dp.callback_query(F.data == 'sub')
async def subscription(message: types.CallbackQuery,state: FSMContext,bot: Bot,command: Command = None):
    cur.execute(f"""SELECT * FROM users WHERE tgid='{message.from_user.id}'""")
    x = cur.fetchone()
    expiry_time = datetime.strptime(x[7].split('.')[0], '%Y-%m-%d %H:%M:%S')
    if expiry_time > datetime.now():
        connect_link = await get_connection_string(main_inbound_id=5, user_email=str(message.from_user.id))
        print(connect_link)
        text = f'Подписка действует до: {expiry_time}\nСсылка для подключения: <code>{connect_link}</code>\n\nПодробнее про подключение можете узнать в инструкции⬇️'
        await bot.send_message(chat_id=message.from_user.id, text=text, reply_markup=readme)
    else:
        await bot.send_message(chat_id=message.from_user.id, text='Выберите вариант подписки.', reply_markup=buy)

@dp.callback_query(F.data == 'trial')
async def buy_keypoard(message: types.CallbackQuery,state: FSMContext,bot: Bot,command: Command = None):
    cur.execute(f"""SELECT * FROM users WHERE tgid='{message.from_user.id}'""")
    x = cur.fetchone()
    if x[6] == 0:
        await add_client(str(message.from_user.id), 10)
        connect_link = await get_connection_string(main_inbound_id=5, user_email=str(message.from_user.id))
        expiry_time = datetime.now() + timedelta(days=10)
        cur.execute(f"""UPDATE users SET trial=1, expiry_time='{expiry_time}', start_time='{datetime.now()}' WHERE tgid='{message.from_user.id}'""")
        con.commit()
        text = f'Поздравляем с активацией пробной подписки!\n\nПодписка действует до: {expiry_time}\nВаша ссылка для активации: <code>{connect_link}</code>\n\nПодробнее про подключение можете узнать в инструкции⬇️'
        await bot.send_message(chat_id=message.from_user.id, text=text, reply_markup=readme)
    else:
        await bot.send_message(chat_id=message.from_user.id, text='Вы уже воспользовались пробной подпиской')


@dp.callback_query('1month' == F.data)
async def buy_1(message: types.CallbackQuery,state: FSMContext,bot: Bot,command: Command = None):
    provider_data = {"receipt": {
            "customer": {
                "email": "example@example.com"
            },
            "items": [
                {
                    "description": "Доступ к сервису на 1 месяц",
                    "quantity": 1.000,
                    "amount": {
                        "value": "99.00",
                        "currency": "RUB"
                    },
                    "vat_code": 1,
                    "payment_mode": "full_payment",
                    "payment_subject": "commodity",
                    "measure": "piece"
                },
            ]
        }}
    await bot.send_invoice(chat_id=message.from_user.id, provider_token=provider_token, provider_data=json.dumps(provider_data), title='Подписка на 1 месяц',
                           description='Укажите email для получения чека', payload='1', currency='RUB',
                           prices=[month_1], need_email=True, send_email_to_provider=True)


@dp.callback_query('3month' == F.data)
async def buy_3(message: types.CallbackQuery,state: FSMContext,bot: Bot,command: Command = None):
    provider_data = {"receipt": {
        "customer": {
            "email": "example@example.com"
        },
        "items": [
            {
                "description": "Доступ к сервису на 3 месяца",
                "quantity": 1.000,
                "amount": {
                    "value": "269.00",
                    "currency": "RUB"
                },
                "vat_code": 1,
                "payment_mode": "full_payment",
                "payment_subject": "commodity",
                "measure": "piece"
            },
        ]
    }}
    await bot.send_invoice(chat_id=message.from_user.id, provider_token=provider_token,
                           provider_data=json.dumps(provider_data), title='Подписка на 3 месяца',
                           description='Укажите email для получения чека', payload='3', currency='RUB',
                           prices=[month_3], need_email=True, send_email_to_provider=True)

@dp.callback_query('6month' == F.data)
async def buy_keypoard(message: types.CallbackQuery,state: FSMContext,bot: Bot,command: Command = None):
    provider_data = {"receipt": {
        "customer": {
            "email": "matvey.titov.2017@mail.ru"
        },
        "items": [
            {
                "description": "Доступ к сервису на 6 месяцев",
                "quantity": 1.000,
                "amount": {
                    "value": "449.00",
                    "currency": "RUB"
                },
                "vat_code": 1,
                "payment_mode": "full_payment",
                "payment_subject": "commodity",
                "measure": "piece"
            },
        ]
    }}
    await bot.send_invoice(chat_id=message.from_user.id, provider_token=provider_token,
                           provider_data=json.dumps(provider_data), title='Подписка на 6 месяцев',
                           description='Укажите email для получения чека', payload='6', currency='RUB',
                           prices=[month_6], need_email=True, send_email_to_provider=True)

@dp.callback_query('12month' == F.data)
async def buy_keypoard(message: types.CallbackQuery,state: FSMContext,bot: Bot,command: Command = None):
    provider_data = {"receipt": {
        "customer": {
            "email": "example@example.com"
        },
        "items": [
            {
                "description": "Доступ к сервису на 12 месяцев",
                "quantity": 1.000,
                "amount": {
                    "value": "599.00",
                    "currency": "RUB"
                },
                "vat_code": 1,
                "payment_mode": "full_payment",
                "payment_subject": "commodity",
                "measure": "piece"
            },
        ]
    }}
    await bot.send_invoice(chat_id=message.from_user.id, provider_token=provider_token,
                           provider_data=json.dumps(provider_data), title='Подписка на 12 месяцев',
                           description='Укажите email для получения чека', payload='12', currency='RUB',
                           prices=[month_12], need_email=True, send_email_to_provider=True)


@dp.callback_query(F.data == 'promo')
async def buy_keypoard(message: types.CallbackQuery, state: FSMContext, bot: Bot, command: Command = None):
        await bot.send_message(chat_id=message.from_user.id, text='Функционал находится в разработке')


@dp.pre_checkout_query()
async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)


@dp.message(F.successful_payment)
async def successful_payment(message: types.Message, bot: Bot):
    # print("SUCCESSFUL PAYMENT:")
    # payment_info = message.successful_payment
    # for k, v in payment_info.items():
    #     print(f"{k} = {v}")
    await bot(DeleteMessage(chat_id=message.from_user.id, message_id=message.message_id))
    await bot.send_message(message.chat.id,
                           f"Платеж на сумму {message.successful_payment.total_amount // 100} {message.successful_payment.currency} прошел успешно!")
    monhts = int(message.successful_payment.invoice_payload)
    await update_client(str(message.chat.id), monhts)
    expiry_time = await get_expiry_time(str(message.from_user.id))
    connect_link = await get_connection_string(main_inbound_id=5, user_email=str(message.from_user.id))
    cur.execute(
        f"""UPDATE users SET expiry_time='{expiry_time}', start_time='{datetime.now()}' WHERE tgid='{message.from_user.id}'""")
    con.commit()
    text = f'Поздравляем с активацией подписки!\n\nПодписка действует до: {expiry_time}\nВаша ссылка для активации: <code>{connect_link}</code>\n\nПодробнее про подключение можете узнать в инструкции⬇️'
    await bot.send_message(chat_id=message.chat.id, text=text, reply_markup=readme)
    cur.execute(
        f'''SELECT * FROM users where tgid="{message.from_user.id}"''')
    user = cur.fetchone()
    if user[2] == 0:
        pass
    else:
        delta = bonuses[monhts]
        cur.execute(
            f"""SELECT balance FROM users WHERE tgid='{user[2]}'""")
        x = cur.fetchone()[0]
        cur.execute(
            f"""UPDATE users SET balance={x + delta} WHERE tgid='{user[2]}'""")
        con.commit()
        await bot.send_message(chat_id=int(user[2]), text=f'Вам начисленно {delta} баллов за покупку пользователя {message.from_user.id}.')


@dp.message(Command("broadcast"))
async def cmd_broadcast(message: types.Message, state: FSMContext):
    if message.from_user.id == ADMIN_ID:
        await message.answer("Введите текст рассылки:")
        await state.set_state(BroadcastState.waiting_for_text)
    else:
        await message.answer("У вас нет прав на рассылку.")


@dp.message(BroadcastState.waiting_for_text)
async def process_broadcast_text(message: types.Message, state: FSMContext, bot: Bot):
    text = message.text
    await state.clear()
    count = 0
    cur.execute('SELECT tgid FROM users')
    user_ids = cur.fetchall()
    user_ids = [u[0] for u in user_ids]
    for user_id in user_ids:
        try:
            await bot.send_message(user_id, text)
            count += 1
            await asyncio.sleep(0.1)
        except Exception as e:
            print(f"Не удалось отправить сообщение {user_id}: {e}")
    await message.answer(f"Рассылка завершена! Отправлено {count} пользователям.")


async def main():
    await dp.start_polling(bot)



if __name__ == '__main__':
    # asyncio.run(start())
    asyncio.run(main())
    # asyncio.run(add_client('xxxx'))