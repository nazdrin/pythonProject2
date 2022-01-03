from aiogram import types, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from create_bot import bot, id_admin
from handlers import answers
from data_base import sqlite_db
from keyboards import kb_cl_1, kb_cl_3, kb_cl_4, button_dict, keyboard, kb_adm_1

storage = MemoryStorage()

class state_user(StatesGroup): # состояния клиента
    Q_0 = State()
    Q_1 = State()
    Q_2 = State()
    Q_3 = State()
    Q_4 = State()
    Q_5 = State()
    Q_6 = State()

async def handle_start(message: types.Message, state: FSMContext):# обработка команді start
    if message.chat.id == id_admin:
        await bot.send_message(id_admin, 'Привет! ', reply_markup=kb_adm_1)# если пользователь является админом бот отсылает уведомление и включает клавиатуру в группе поддержки
    else:
        try: # проверка на  зарегестрированного пользователя
            id_user = message.chat.id
            chain = sqlite_db.sql_select(id_user)
            await state_user.Q_2.set()
            async with state.proxy() as data:
                data['code_chain'] = chain[0]
                data['name_chain'] = chain[1]
            await bot.send_message(message.chat.id, 'Вітаємо, ' + str(
                message.from_user.first_name) + '! Ви є представником мережі "' + str(chain[1])
                                   + answers.welcome_reg, reply_markup=kb_cl_1)
        except: # если пользователь незарегистрирован, отправляется на регистрацию
            await state_user.Q_1.set()
            await bot.send_message(message.chat.id,
                                   'Вітаємо, ' + str(message.from_user.first_name) + answers.welcome_noreg)

async def registration(message: types.Message, state: FSMContext): # метод регистрации пользователя
    try:
        code_chain = str(message.text)
        id_user = message.from_user.id
        first_name = message.from_user.first_name
        name_chain = sqlite_db.sql_select_name(code_chain, id_user, first_name)# данные пользователя записываются в БД
        await state_user.next()
        async with state.proxy() as data:
            data['code_chain'] = code_chain
            data['name_chain'] = name_chain # сохранение переменных в состояние пользователя
        await bot.send_message(message.chat.id,
                               'Ви є представником мережі "' + str(name_chain) + answers.welcome_reg,
                               reply_markup=kb_cl_1) # после регистрации вызывается главное меню
    except:
        await bot.send_message(message.from_user.id, 'Будь ласка, введіть корректний код!⌨️')

async def first_menu(message: types.Message, state: FSMContext): # обработка команд от кнопок главного меню
    father_button_list = button_dict.get(message.text)
    if father_button_list == None:
        await bot.send_message(message.from_user.id,
                               'Оберіть, будь ласка, розділ🗂, користуючись кнопками нижче 👇')# проверка на произвольный ввод
    else:
        async with state.proxy() as data:
            data['father_button_list'] = father_button_list # запись словаря в  переменную состояния
        kb_cl_2 = keyboard.kb_cl_2(father_button_list)
        await bot.send_message(message.from_user.id, answers.answer_selection, reply_markup=kb_cl_2) # вызывается клавиатура второго уровня
        await state_user.next()

async def second_menu(message: types.Message, state: FSMContext): # обработка команд второго уровня меню
    users_data = await state.get_data()
    father_button_list = users_data['father_button_list']# достаётся список кнопок из переменной состояния
    list_button = father_button_list.get(message.text)
    if list_button == None:
        if message.text == 'До головного меню ⤴️️':
            await state_user.Q_2.set()
            await bot.send_message(message.from_user.id, answers.type_selection, reply_markup=kb_cl_1)
        elif message.text == 'Запитати менеджера⁉️':
            async with state.proxy() as data: # запись переменных состояния
                data['time_request'] = answers.hours_48
                data['main_question'] = message.text
            await state_user.next()
            await bot.send_message(message.from_user.id, answers.warning_before, reply_markup=kb_cl_3)
        else:
            await bot.send_message(message.from_user.id,
                                   answers.type_selection)
    else:
        question = list_button[0]
        async with state.proxy() as data:
            data['time_request'] = list_button[1]
            data['main_question'] = message.text
        await state_user.next()
        await bot.send_message(message.from_user.id, question, reply_markup=kb_cl_3)

async def last_menu(message: types.Message):# Обработка команд финального меню
    if message.text == 'Додати коментар📝':
        await state_user.next()
        await bot.send_message(message.from_user.id, 'Будь ласка, додайте коментар 🖌', reply_markup=kb_cl_4)
    elif message.text == 'До головного меню ⤴️️':
        await state_user.Q_2.set()
        await bot.send_message(message.from_user.id, answers.type_selection, reply_markup=kb_cl_1)
    else:
        await bot.send_message(message.from_user.id, 'Для того щоб зробити наступний крок, користуючись кнопками нижче 👇')

async def start_dialog(message: types.Message, state: FSMContext): # обработка первого сообщения пользователя
    if message.text == 'До головного меню ⤴️️':
        await bot.send_message(message.from_user.id, answers.type_selection,
                               reply_markup=kb_cl_1)
        await state_user.Q_2.set()
    else:
        number_request = sqlite_db.number_json()
        users_data = await state.get_data()
        name_chain = users_data['name_chain']
        code_chain = users_data['code_chain']
        main_question = users_data['main_question']
        time_request = users_data['time_request']
        time_message = message.date
        id_user = message.from_user.id
        async with state.proxy() as data:
            data['number_request'] = number_request
        status = 'Отправлено'
        text_request = message.text
        await bot.send_message(id_admin, 'Звернення N ' + str(number_request) + ', від мережі: ' + name_chain
                               + ' (' + code_chain + '),\n' + main_question + ' (' +
                               time_request + ')')
        id_m = await bot.forward_message(id_admin, message.chat.id, message.message_id)
        id_message = id_m.message_id
        sqlite_db.sql_insert_message(number_request, id_user, id_message, text_request, status, code_chain, name_chain, time_message)
        await bot.send_message(message.from_user.id,
                               'Дякуємо за звернення. Воно надійшло менеджеру. Очікуйте, будь ласка, відповідь ⏳ протягом ' +
                               time_request)
        await state_user.next()

async def question(message, state: FSMContext): # обработка последующих сообщений пользователя и ответ на них админа
    if message.text == 'До головного меню ⤴️️':
        await bot.send_message(message.from_user.id, answers.type_selection,
                               reply_markup=kb_cl_1)
        await state_user.Q_2.set()
    else:
        users_data = await state.get_data()
        number_request = users_data['number_request']
        name_chain = users_data['name_chain']
        code_chain = users_data['code_chain']
        time_message = message.date
        id_user = message.from_user.id
        async with state.proxy() as data:
            data['number_request'] = number_request
        status = 'Отправлено'
        text_request = message.text
        id_m = await bot.forward_message(id_admin, message.chat.id, message.message_id)
        id_message = id_m.message_id
        sqlite_db.sql_insert_message(number_request, id_user, id_message, text_request, status, code_chain, name_chain,
                                     time_message)

async def defolt(message, state: FSMContext): # обработка всех прочих текстовых наборов пользователей и админа
    if message.chat.id == id_admin:
        try:
            if message.reply_to_message.forward_from.id:
                await bot.forward_message(message.reply_to_message.forward_from.id, id_admin, message.message_id)
                await bot.send_message(id_admin, 'Ответ отправлен')
                sqlite_db.sql_change_status_message(message.reply_to_message.message_id)
            else:
                await bot.send_message(id_admin, 'Нужно ответить на сообщение')
        except:
            await bot.send_message(id_admin, 'Некорректный ввод')
    else:
        id_user = message.chat.id
        try:
            await state_user.Q_2.set()
            chain = sqlite_db.sql_select(id_user)

            async with state.proxy() as data:
                data['code_chain'] = chain[0]
                data['name_chain'] = chain[1]
            await bot.send_message(message.from_user.id, answers.type_selection, reply_markup=kb_cl_1)
        except:
            await state_user.Q_1.set()
            await bot.send_message(message.chat.id,
                                   'Вітаємо, ' + str(message.from_user.first_name) + answers.welcome_noreg)

def register_handler_client (dp : Dispatcher):# регистрация хендлеров
    dp.register_message_handler(handle_start, commands='start', state=None)
    dp.register_message_handler(registration, state=state_user.Q_1)
    dp.register_message_handler(first_menu, state=state_user.Q_2)
    dp.register_message_handler(second_menu, state=state_user.Q_3)
    dp.register_message_handler(last_menu, state=state_user.Q_4)
    dp.register_message_handler(start_dialog, state=state_user.Q_5, content_types=['text', 'photo', 'document', 'video'])
    dp.register_message_handler(question, state=state_user.Q_6, content_types=['text', 'photo', 'document', 'video'])
    dp.register_message_handler(defolt, content_types=['text', 'photo', 'document', 'video'])