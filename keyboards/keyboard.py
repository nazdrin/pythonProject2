
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup #ReplyKeyboardRemove,
from handlers import answers

button_dict = {'Товари💊':                  {'🔎Товар не відображається на сайті': [answers.no_goods, answers.hours_6], '📥Додати товар на сайт': [answers.add_goods, answers.hours_24],
                                            '🪢Змінити прив"язку товара🪢' : [answers.change_binding, answers.hours_6] },
              'Відображення даних аптек🏥': {'🏥Додати нові аптеки':[answers.add_pharmacies, answers.hours_24],'🔎Аптека не відображається':[answers.show, answers.hours_1],
                                            '📜☎ Змінити графік роботи, номер телефона️':[answers.schedule, answers.hours_24],'🗺Змінити точку на карті':[answers.point_map, answers.hours_24],
                                             '🆕Змінити назву аптеки' : [answers.change_name_store, answers.hours_24],
                                             '🚫Відключити аптеку':[answers.cancel_pharmacy, answers.hours_1],'❌Відключити мережу':[answers.cancel_chain, answers.hours_1] },
               'Договори,рахунки,акти📑': {'📜Договори': [answers.contract, answers.hours_48], '🧾Рахунки': [answers.bills, answers.hours_6],
                                           '📇Акти' : [answers.acts, answers.hours_6],'🏃Зміна контактної особи' :[answers.change_contact, answers.hours_24]},
               'Тех.збій🛠' :             { '📵Особистий кабінет' : [answers.personal, answers.hours_1],'⛔️Замовлення': [answers.orders, answers.hours_1],'⭕️Залишки': [answers.stock, answers.hours_2]},
               'Звіти📈' :                { '🪢Товари без прив"язки' : [answers.no_con, answers.hours_24], '📈Якість' : [answers.quality, answers.hours_24],
                                          '🗺Оточення' : [answers.around, answers.hours_24], '💰Фінансовий' : [answers.finance, answers.hours_24]}}

kb_cl_1 = ReplyKeyboardMarkup(resize_keyboard=True)# главное меню
buttons = []
for key in button_dict:
    buttons.append(key)
kb_cl_1.add(*buttons)

def kb_cl_2 (father_button_list):# второй уровень меню
        kb_cl_2 = ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = []
        for key in father_button_list:
            buttons.append(key)
        buttons.append('Запитати менеджера⁉️')
        buttons.append('До головного меню ⤴️️')
        kb_cl_2.add(*buttons)
        return kb_cl_2

kb_cl_3 = ReplyKeyboardMarkup(resize_keyboard=True)#третий уровень меню пользователя
button1 = KeyboardButton('Додати коментар📝')
button2 = KeyboardButton('До головного меню ⤴️️')
kb_cl_3.add(button1, button2)

kb_cl_4 = ReplyKeyboardMarkup(resize_keyboard=True)
button1 = KeyboardButton('До головного меню ⤴️️')
kb_cl_4.add(button1)

kb_adm_1 = ReplyKeyboardMarkup(resize_keyboard=True)# Главное меню админа
button1 = KeyboardButton('/🆕_chain')
button2 = KeyboardButton('/⚠️_report')
button3 = KeyboardButton('/🔂_status')
button4 = KeyboardButton('/⭕_all_statuses')
kb_adm_1.add(button1, button2, button3, button4)

kb_adm_2 = ReplyKeyboardMarkup(resize_keyboard=True)# менеддеры
button1 = KeyboardButton('tun')
button2 = KeyboardButton('sia')
button3 = KeyboardButton('ivk')
kb_adm_2.add(button1, button2, button3)

kb_iniine = InlineKeyboardMarkup(row_width=2)# инлайн клавиатура
in_button1 = InlineKeyboardButton(text='ДА', callback_data='btn_1')
in_button2 = InlineKeyboardButton(text='НЕТ', callback_data='btn_2')
kb_iniine.add(in_button1, in_button2)




