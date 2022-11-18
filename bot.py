import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import datetime

now = datetime.datetime.now()

API_TOKEN = ''

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class UserState(StatesGroup):
    Get_contact = State()
    Get_name = State()
    Get_topic = State()


@dp.message_handler(commands=['start', 'ariza'], state='*')
async def send_welcome(message: types.Message):
    await message.reply(
        f"Assalomu aleykum {message.from_user.username}! 👋\n"
        f"Botga muammoingiz haqida yozishingiz mumkin 📁\n"
        f"Botga nomeringizni quyidagi formatda qilib kiriting : +9989XXXXXXXX. \n"
        f"Biz shu nomer orqali sizga qayta aloqaga chiqamiz 📞", )
    await UserState.Get_contact.set()


@dp.message_handler(state=UserState.Get_contact)
async def get_contact(message: types.Message, state=FSMContext):
    contact = message.text
    if len(contact) == 13 and contact.startswith("+") and (contact.lstrip('+')).isdigit():
        await bot.send_message(message.from_user.id, 'Kontaktingiz qabul qilindi. 📲\n'
                                                     'Endi esa ism familiyangizni quyidagi formatda yuboring:\n'
                                                     'Abdullayev Abdulla',
                               reply_markup=InlineKeyboardMarkup(row_width=1).insert(
                                   InlineKeyboardButton('🔙 ortga', callback_data='get_contact_back')))
        await state.update_data(contact=contact)
        await UserState.next()
    else:
        await bot.send_message(message.from_user.id, 'Kontakt notogri formatda kiritildi! ❌\n'
                                                     'Iltimos kontaktingizni qayta tekshirib kiriting 🔄\n'
                                                     'Eslatib otamiz kontakt quyidagi formatda bolishi lozim:\n'
                                                     '+9989XXXXXXXX')


@dp.message_handler(state=UserState.Get_name)
async def get_name(message: types.Message, state=FSMContext):
    name = message.text
    if ' ' in name:
        await state.update_data(name=name)
        await bot.send_message(message.from_user.id, 'Ism familiyangiz saqlandi. ✅\n'
                                                     'Muammoingiz haqaida yozing.',
                               reply_markup=InlineKeyboardMarkup(row_width=1).insert(
                                   InlineKeyboardButton('🔙 ortga', callback_data='get_name_back'))
                               )
        await UserState.next()
    else:
        await bot.send_message(message.from_user.id, 'Ism familiya notogri formatda kiritildi. ❌\n'
                                                     'Iltimos ism familiyangizni qayta tekshirib kiriting. 🔄\n'
                                                     'Eslatib otamiz ism familiya quyidagi formatda bolishi lozim:\n'
                                                     'Abdullaeyev Abdulla')


@dp.message_handler(state=UserState.Get_topic)
async def get_name(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['topic'] = message.text
        await bot.send_message(
            -1001520916889,
            f'🕔 Vaqti: {now.strftime("%d-%m-%Y %H:%M")}\n'
            f'👨 Ism familiya: {data["name"]}\n'
            f'📞 Kontakt: {data["contact"]}\n'
            f'📁 Ariza: {data["topic"]}'
        )
        await bot.send_message(message.from_user.id, 'Arizangiz qabul qilindi. ✅ \n'
                                                     'Tez orada sizga aloqaga chiqamiz. 🧑‍💻\n'
                                                     'Yangi ariza qoldirish uchun /ariza tugmasini bosing.')
    await state.finish()


@dp.callback_query_handler(text='get_contact_back', state=UserState.Get_name)
async def get_contact_back(call: types.CallbackQuery):
    await call.message.delete()
    await bot.send_message(call.from_user.id,
                           'Botga nomeringizni quyidagi formatda qilib kiriting : +9989XXXXXXXX. \n'
                           'Biz shu nomer orqali sizga qayta aloqaga chiqamiz 📞 ')
    await UserState.Get_contact.set()


@dp.callback_query_handler(text='get_name_back', state=UserState.Get_topic)
async def get_contact_back(call: types.CallbackQuery):
    await call.message.delete()
    await bot.send_message(call.from_user.id,
                           'Ism familiyangizni quyidagi formatda yuboring:\n'
                           'Abdullayev Abdulla')
    await UserState.Get_name.set()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)













