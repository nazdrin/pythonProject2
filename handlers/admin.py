from aiogram import types, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from create_bot import bot, id_admin
from data_base import sqlite_db
from keyboards import kb_adm_1, kb_adm_2, kb_iniine

storage = MemoryStorage()

class state_admin(StatesGroup):# состояния админа
    input_code = State()
    input_name = State()
    input_manager = State()
    callback = State()
    change_status = State()
    callback_all = State()

async def new_chain (message: types.Message): # ввод  новой сети
    if message.chat.id == id_admin:
        await state_admin.next()
        await bot.send_message(id_admin, 'Укажите номер сети')

async def input_code_chain (message: types.Message, state: FSMContext): #  обработка ввода кода сети
    if message.chat.id == id_admin:
        try:
            code_chain = int(message.text)
            try:
                name_chain = sqlite_db.sql_check_code(str(code_chain))
                await bot.send_message(id_admin, 'Данная сеть:" ' + str(name_chain[0]) + '" уже присутствует в базе!')
                await state.finish()
            except:
                await bot.send_message(id_admin, "Теперь введите наименование сети")
                async with state.proxy() as data:
                    data['code_chain'] = message.text
                    await state_admin.next()
        except:
            await bot.send_message(id_admin, "Введите цифровое значение")

async def input_name_chain (message: types.Message, state: FSMContext):# обработка ввода наименования сети
    async with state.proxy() as data:
        data['name_chain'] = message.text
        await bot.send_message(id_admin, 'Укажите менеджера, воспользовавшись кнопками', reply_markup=kb_adm_2)
        await state_admin.next()

async def input_manager (message: types.Message, state: FSMContext):# обработка ввода менеджера
    admin_data = await state.get_data()
    code_chain = admin_data['code_chain']
    name_chain = admin_data['name_chain']
    async with state.proxy() as data:
        data['manager'] = message.text
    await state_admin.next()
    await bot.send_message(id_admin, 'Вы желаете сохранить сеть: №' + code_chain + '_' + name_chain + '. Менеджер: ' + message.text + '? \nДля сохранения нажмите "Да", '
     'если данные некорректны, нажмите "Нет" и произведите повторный ввод. ', reply_markup=kb_iniine)

async def callback_step (callback : types.CallbackQuery, state: FSMContext): # обаботка заданий от inline клавиатуры
    action = callback.data.split('_')[1]
    if action == '1':
        admin_data = await state.get_data()
        code_chain = admin_data['code_chain']
        name_chain = admin_data['name_chain']
        manager = admin_data['manager']
        sqlite_db.sql_insert_new_chain(code_chain, name_chain, manager)
        await bot.send_message(id_admin, 'Сеть сохранена!', reply_markup=kb_adm_1)
        await state.finish()
    if action == '2':
        await bot.send_message(id_admin, 'Можете повторить процедуру ввода', reply_markup=kb_adm_1)
        await state.finish()

async def report (message: types.Message):
    await report_1()
async def report_1 ():# отправка  отчёта по необработанным обращениям
    try:
        report = sqlite_db.sql_report()
        text = ''
        for t in report:
            text = text + '\n' + str(t)
        await bot.send_message(id_admin, str(text), reply_markup=kb_adm_1)
    except:
        await bot.send_message(id_admin, 'Необработанные сообщения отсутствуют', reply_markup=kb_adm_1)

async def input_number_request (message: types.Message): # запрос на ввод номера обращения для изменения статуса
    await bot.send_message(id_admin, 'Введите номер сообщения')
    await state_admin.change_status.set()

async def change_status (message, state: FSMContext): # обработка номера сообщения и изменения статуса
    try:
        number_request = int(message.text)
        request = sqlite_db.sql_change_status_request(number_request)
        if request == []:
            await bot.send_message(id_admin, 'Обращения с таким номером не существует, поробуйте снова', reply_markup=kb_adm_1)
            await state.finish()
        else:
            await bot.send_message(id_admin, 'Статус изменён', reply_markup=kb_adm_1)
            await state.finish()
    except:
        await bot.send_message(id_admin, 'Введите цифровое значение')

async def change_all_status (message: types.Message): # изменение всех статусов необработанных сообщений
    await state_admin.callback_all.set()
    await bot.send_message(id_admin, 'Вы дейтвительно хотите изменить статус всех обращений на "Ответ предоставлен"', reply_markup=kb_iniine)

async def call_all (callback : types.CallbackQuery, state: FSMContext): # подтверждендие изменения всех статусов, обработка заданий клавиатуры
    action = callback.data.split('_')[1]
    if action == '1':
        sqlite_db.sql_change_status_all()
        await bot.send_message(id_admin, 'Изменено!', reply_markup=kb_adm_1)
        await state.finish()
    if action == '2':
        await bot.send_message(id_admin, 'Можете повторить процедуру ввода', reply_markup=kb_adm_1)
        await state.finish()

def register_handler_admin (dp : Dispatcher):# регистрация хендлеров
    dp.register_message_handler(new_chain, commands='🆕_chain', state=None)
    dp.register_message_handler(input_code_chain, content_types=['text'], state=state_admin.input_code)
    dp.register_message_handler(input_name_chain, state=state_admin.input_name)
    dp.register_message_handler(input_manager, state=state_admin.input_manager)
    dp.register_callback_query_handler(callback_step, Text(startswith='btn'), state=state_admin.callback)
    dp.register_message_handler(report, commands='⚠️_report', state=None)
    dp.register_message_handler(input_number_request, commands='🔂_status', state=None)
    dp.register_message_handler(change_status, state=state_admin.change_status)
    dp.register_message_handler(change_all_status, commands='⭕_all_statuses', state=None)
    dp.register_callback_query_handler(call_all, Text(startswith='btn'), state=state_admin.callback_all)




