from aiogram import executor, Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import KeyboardButton,ReplyKeyboardMarkup,InlineKeyboardButton,InlineKeyboardMarkup
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup,State
from aiogram.dispatcher import FSMContext
from Razer_DataBase import Data_base
import Razer_keyboards as kb
from Razer_Logic import Start_Logic
from Translate import _
import time
import os
import os.path
import json
import time
import random
from pyotp import *


with open('Config.json') as f:
    Config = json.load(f)
Storage=MemoryStorage()
db=Data_base()
bot=Bot(token=Config["Telegram_token"])
dp= Dispatcher(bot,storage=Storage)
Selected_order=1
lang="en"
adm_lang=Config["Language"]


class States(StatesGroup):
    wait_user_main = State()
    wait_admin=State()
    wait_get_username=State()
    wait_take_username=State()
    Users_main_menu=State()
    wait_user_count=State()
    wait_user_language=State()
    wait_user_settings=State()
    wait_user_produkt=State()
    wait_user_account=State()
    wait_user_email=State()
    wait_user_Pass=State()
    wait_user_FA=State()
    wait_user_format=State()

    # Админы


@dp.callback_query_handler(Text(equals="Main_menu"),state='*')
async def Adminmenu(callback:types.CallbackQuery):
    if callback.from_user.id==int(Config["Admin_ID"]):
        try:
            await callback.message.edit_text(text=_("<b>Главное меню</b>",adm_lang),parse_mode="HTML", reply_markup=kb.Kb_admin_main(adm_lang))
            await States.wait_admin.set()
        except:
            await callback.message.edit_text(text=_("<b>Уже открыто</b>",adm_lang),parse_mode="HTML", reply_markup=kb.Kb_admin_main(adm_lang))
            await States.wait_admin.set()


@dp.message_handler(commands=["start"],state='*')
async def Client(message:types.Message):
    if message.from_user.id == int(Config["Admin_ID"]):
        await message.answer(text=_("<b>Здравствуйте 🤝,панель для админов открыта.</b>",adm_lang),parse_mode="HTML", reply_markup=kb.Kb_admin_main(adm_lang))
        await States.wait_admin.set()
    else:
        global lang
        lang=db.Get_language(message.from_user.username)
        if lang==True:
            print(1)
            lang=db.Set_new_user(message.from_user.id, message.from_user.username)
            await message.answer(text=_("<b>Выберите подходящий язык!</b>",lang),parse_mode="HTML",reply_markup=kb.Kb_language(lang))
            await States.wait_user_language.set()
        else:
            print(2)
            await message.answer(text=_("<b>Выберите действие!</b>", lang), parse_mode="HTML", reply_markup=kb.Kb_user_main(lang))
            await States.wait_user_main.set()


@dp.callback_query_handler(state=States.wait_admin)
async def Get_access(callback:types.CallbackQuery):
    if callback.data=="get_acc":
        await callback.message.edit_text(text=_("<b>Кому выдать 1 месяц подписки?Введите <u>@Username</u></b>",adm_lang),parse_mode="HTML",reply_markup=kb.Kb_main(adm_lang))
        await States.wait_get_username.set()
    if callback.data=="take_acc":
        await callback.message.edit_text(text=_("<b>У кого забрать подписку?Введите @<u>Username</u></b>",adm_lang),parse_mode="HTML",reply_markup=kb.Kb_main(adm_lang))
        await States.wait_take_username.set()
    if callback.data=="Count":
        Count_users=db.get_count_users()
        await callback.message.edit_text(text=Count_users,reply_markup=kb.Kb_main(adm_lang))
        await States.wait_admin.set()
    if callback.data=="list":
        List_users=db.get_list_users()
        await callback.message.edit_text(text=List_users,reply_markup=kb.Kb_main(adm_lang))


@dp.message_handler(state=States.wait_take_username)
async def Take_subcribe(message:types.Message):
        check=db.Take_subscribe(message.text)
        if check:
            await message.answer(text=_("<b>Подписка у данного пользователя была удалена</b>",adm_lang),parse_mode="HTML",reply_markup=kb.Kb_admin_main(adm_lang))
            await States.wait_admin.set()
        else:
            await message.answer(text=_("<b>Произошла ошибка при удалении подписки</b>",adm_lang),parse_mode="HTML")


@dp.message_handler(state=States.wait_get_username)
async def Get_subcribe(message:types.Message):
        check= db.Set_time_subscribe(message.text, int(str(time.time()).split(".")[0]) + 2678400)
        if check:
            await message.answer(text=_("<b>Выдача 1 месяца подписки произошла успешно</b>",adm_lang), parse_mode="HTML", reply_markup=kb.Kb_admin_main(adm_lang))
            await States.wait_admin.set()
        else:
            await message.answer(text=_("<b>Произошла ошибка,пользователь не написал /start боту!</b>",adm_lang), parse_mode="HTML")



            #Юзеры



@dp.callback_query_handler(Text(equals="Main"),state='*')
async def Call_main(callback:types.CallbackQuery):
    global lang
    lang = db.Get_language(callback.from_user.username)
    await callback.message.edit_text(text=_("<b>Главное меню</b>",lang),parse_mode="HTML",reply_markup=kb.Kb_user_main(lang))
    await States.wait_user_main.set()



@dp.callback_query_handler(state=States.wait_user_main)
async def User_main(callback:types.CallbackQuery):
    if callback.data=="Settings":
        await callback.message.edit_text(text=_("<b>Настройки</b>",lang),parse_mode="HTML",reply_markup=kb.Kb_settings(lang))
        await States.wait_user_settings.set()
    elif callback.data=="Purchase":
        await callback.message.edit_text(text=_("<b>Выберите продукт!</b>",lang),parse_mode="HTML",reply_markup=kb.Kb_purchare(lang))
        await States.wait_user_produkt.set()


@dp.callback_query_handler(state=States.wait_user_settings)
async def Settings(callback:types.CallbackQuery):
    if callback.data=="Format":
        await callback.message.edit_text(text=_("<b>Укажите формат в котором вы хотите входить в Razer аккаунт.\n1)Одним сообщением (Email Password 2FA).\n2)Тремя сообщениями.</b>",lang),parse_mode="HTML",reply_markup=kb.Kb_format(lang))
        await States.wait_user_format.set()
    if callback.data=="Language":
        await callback.message.edit_text(text=_("<b>Укажите язык интерфейса..</b>",lang),parse_mode="HTML",reply_markup=kb.Kb_language(lang))
        await States.wait_user_language.set()


@dp.callback_query_handler(state=States.wait_user_language)
async def Select_language(callback:types.CallbackQuery):
    global lang
    if callback.data=="en":
        db.Set_user_language(callback.from_user.username,"en")
        lang="en"
    elif callback.data=="ru":
        db.Set_user_language(callback.from_user.username,"ru")
        lang="ru"
    await callback.message.edit_text(text=_("<b>Выберите действие!</b>",lang),parse_mode="HTML",reply_markup=kb.Kb_user_main(lang))
    await States.wait_user_main.set()


@dp.callback_query_handler(state=States.wait_user_format)
async def Set_format(callback:types.CallbackQuery):
    if callback.data=="one":
        db.Set_format(callback.from_user.username,1)
    elif callback.data=="three":
        db.Set_format(callback.from_user.username, 2)
    await callback.message.edit_text(text=_("<b>Главное меню!</b>",lang),parse_mode="HTML",reply_markup=kb.Kb_user_main(lang))
    await States.wait_user_main.set()


@dp.callback_query_handler(state=States.wait_user_produkt)
async def Set_produkt(callback:types.CallbackQuery):
    if db.check_subscribe(callback.from_user.username, int(str(time.time()).split(".")[0])):
        dir_path = os.path.dirname(os.path.realpath(__file__))  # путь к текущей директории
        for filename in os.listdir(dir_path):  # перебираем все файлы в этой директории
            if filename.endswith(".txt"):  # если файл имеет расширение .txt
                os.remove(os.path.join(dir_path, filename))  # удаляем его
        global Product
        Product=callback.data
        await callback.message.edit_text(text=_("<b>Напишите количество продукта.</b>",lang),parse_mode="HTML",reply_markup=kb.Kb_main_call(lang))
        await States.wait_user_count.set()
    else:
        await callback.message.edit_text(text=_("<b>🔐 Вы не имеете доступ в бота.\nДля покупки Напишите - @foureason</b>",lang), parse_mode="HTML",reply_markup=kb.Kb_main_call(lang))


@dp.message_handler(state=States.wait_user_count)
async def Set_produkt(message: types.Message):
    global Count
    try:
        Count=int(message.text)
    except:
        await message.answer(text=_("<b>Это не число!</b>",lang),parse_mode="HTML",reply_markup=kb.Kb_main_call(lang))
    if db.Get_format(message.from_user.username)==1:
        await message.answer(text=_("<b>Напишите свой Razer аккаунт (Email Password 2FA).</b>",lang),parse_mode="HTML",reply_markup=kb.Kb_main_call(lang))
        await States.wait_user_account.set()
    else:
        await message.answer(text=_("<b>Напишите свой емайл от Razer аккаунта.</b>",lang),parse_mode="HTML",reply_markup=kb.Kb_main_call(lang))
        await States.wait_user_email.set()


@dp.message_handler(state=States.wait_user_account)
async def Set_account(message:types.Message):
    global account
    account=message.text
    await message.answer(text=_("<b>✅ Процесс запустился..</b>",lang),parse_mode="HTML")
    words=account.split(" ")
    Login=words[0]
    Password=words[1]
    FA=words[2]
    result = Start_Logic(Login, Password, FA, int(Count), Product)
    print(f"Принял {result}")
    if result[0] == True:
        if result[1] == 1:
            os.rename(f'BuyUC.txt', f'{result[1]} Pin [{Product}UC].txt')
            file_name = f'{result[1]} Pin [{Product}UC].txt'
            file = open(file_name, mode='r+')
            await bot.send_document(message.chat.id, (file_name, file.read()))
        if result[1] > 1:
            os.rename(f'BuyUC.txt', f'{result[1]} Pins [{Product}UC].txt')
            file_name = f'{result[1]} Pins [{Product}UC].txt'
            file = open(file_name, mode='r+')
            await bot.send_document(message.chat.id, (file_name, file.read()))
        await bot.send_message(chat_id=Config[["Admin_ID"]], text=f"@{message.from_user.username} {_('<b>Купил {Count} кодов</b>', lang)}", parse_mode="HTML")
    else:
        await message.answer(text=_(f"{result}", lang), parse_mode="HTML")


@dp.message_handler(state=States.wait_user_email)
async def Set_email(message:types.Message):
    global Login
    Login=message.text
    await message.answer(text=_("<b>Напишите свой пароль от Razer аккаунта.</b>",lang),parse_mode="HTML",reply_markup=kb.Kb_main_call(lang))
    await States.wait_user_Pass.set()


@dp.message_handler(state=States.wait_user_Pass)
async def Set_email(message:types.Message):
    global Password
    Password=message.text
    await message.answer(text=_("<b>Напишите свой 2FA от Razer аккаунта.</b>",lang),parse_mode="HTML",reply_markup=kb.Kb_main_call(lang))
    await States.wait_user_FA.set()


@dp.message_handler(state=States.wait_user_FA)
async def Set_email(message:types.Message):
    FA=message.text
    await message.answer(text=_("<b>✅ Процесс запустился..</b>", lang), parse_mode="HTML")
    result = Start_Logic(Login, Password, FA, int(Count), Product)
    print(f"Принял {result}")
    if result[0] == True:
        if result[1] == 1:
            os.rename(f'BuyUC.txt', f'{result[1]} Pin [{Product}UC].txt')
            file_name = f'{result[1]} Pin [{Product}UC].txt'
            file = open(file_name, mode='r+')
            await bot.send_document(message.chat.id, (file_name, file.read()))
        if result[1] > 1:
            os.rename(f'BuyUC.txt', f'{result[1]} Pins [{Product}UC].txt')
            file_name = f'{result[1]} Pins [{Product}UC].txt'
            file = open(file_name, mode='r+')
            await bot.send_document(message.chat.id, (file_name, file.read()))
        await bot.send_message(chat_id=Config[["Admin_ID"]], text=f"@{message.from_user.username} {_('<b>Купил {Count} кодов</b>', lang)}", parse_mode="HTML")
    else:
        await message.answer(text=_(f"{result}", lang), parse_mode="HTML")






executor.start_polling(dp, skip_updates=True)