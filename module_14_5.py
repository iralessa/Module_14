from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.utils import executor
from crud_functions import *

api = "______________________________"
bot = Bot(token=api)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Клавиатуры
kb_calc = InlineKeyboardMarkup().add(InlineKeyboardButton(text="Рассчитать", callback_data='calories'))
kb_calc1 = InlineKeyboardMarkup().add(InlineKeyboardButton(text="Формула расчёта", callback_data='formulas'))
kb_reg = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(text='Регистрация'))

start_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Выберете необходимое:')],
        [
            KeyboardButton(text='Мужчина'),
            KeyboardButton(text='Женщина'),
            KeyboardButton(text='Перейти к покупкам')
        ]
    ],
    resize_keyboard=True
)

inline_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Продукт 1", callback_data='product_buying')],
        [InlineKeyboardButton(text="Продукт 2", callback_data='product_buying')],
        [InlineKeyboardButton(text="Продукт 3", callback_data='product_buying')],
        [InlineKeyboardButton(text="Продукт 4", callback_data='product_buying')],
        [InlineKeyboardButton(text="Назад", callback_data="back_to_catalog")]
    ]
)

class UserState(StatesGroup):
    gender = State()
    btt = State()
    age = State()
    growth = State()
    weight = State()
    buy = State()

class RegistrationState(StatesGroup):
    reg = State()
    username = State()
    email = State()
    age = State()
    balance = State()
    main = State()

@dp.message_handler()
async def start(message):
    await message.answer(f"Привет, {message.from_user.username}! Я бот, помогающий следить за здоровьем. "
                         f"Пожалуйста, пройдите регистрацию!",
                         reply_markup=kb_reg)
    await RegistrationState.reg.set()

@dp.message_handler(text='Регистрация', state=RegistrationState.reg)
async def sign_up(message):
    await message.reply("Введите имя пользователя (только латинские буквы):")
    await RegistrationState.username.set()

@dp.message_handler(state=RegistrationState.username)
async def set_username(message, state):
    username = message.text
    if is_included(username):
        await message.reply(f"Пользователь '{username}' уже зарегистрирован. Попробуйте еще раз!")
        return
    else:
        await message.reply(f"Регистрация пользователя '{username}' начата.")

    await state.update_data(username=username)
    await message.reply("Введите ваш email:")
    await RegistrationState.email.set()

@dp.message_handler(state=RegistrationState.email)
async def set_email(message, state):
    email = message.text
    await state.update_data(email=email)
    await message.reply("Введите ваш возраст:")
    await RegistrationState.age.set()

@dp.message_handler(state=RegistrationState.age)
async def set_age(message, state):
    age = message.text
    if not age.isdigit():
        await message.reply("Пожалуйста, введите корректный возраст.")
        return
    age = int(age)
    user_data = await state.get_data()
    username = user_data.get('username')
    email = user_data.get('email')
    add_user(username, email, age)
    await message.answer("Регистрация успешно завершена.")
    await message.answer("Укажите ваш пол, и мы подберем для вас витамины.",
                         reply_markup=start_menu)
    await UserState.gender.set()

@dp.message_handler(state=UserState.gender)
async def set_gender(message: types.Message, state: FSMContext):
    gender = message.text.lower()
    if gender not in ["мужчина", "женщина"]:
        await message.answer("Пожалуйста, выберите 'Мужчина' или 'Женщина'.")
        return
    await state.update_data(gender=gender)
    await message.answer("Пока я подбираю витамины, можете рассчитать свою норму калорий:",
                         reply_markup=kb_calc)
    await UserState.btt.set()

@dp.callback_query_handler(text='calories', state=UserState.btt)
async def restart_calculation(call):
    await UserState.age.set()
    await call.message.answer("Введите ваш возраст.")
    await call.answer()

@dp.message_handler(state=UserState.age)
async def set_age1(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Пожалуйста, введите возраст числом.")
        return
    await state.update_data(age=int(message.text))
    await message.answer(f"Принято! Ваш возраст: {message.text}")
    await message.answer('Введите ваш рост.')
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_growth(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Пожалуйста, введите рост числом.")
        return
    await state.update_data(growth=int(message.text))
    await message.answer(f"Принято! Ваш рост: {message.text}")
    await message.answer('Введите ваш вес.')
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def set_weight(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Пожалуйста, введите вес числом.")
        return
    await state.update_data(weight=int(message.text))
    await message.answer(f"Принято! Ваш вес: {message.text}")
    data = await state.get_data()
    age = float(data['age'])
    growth = float(data['growth'])
    weight = float(data['weight'])
    gender = data['gender']
    if gender == 'мужчина':
        calories = 10 * weight + 6.25 * growth - 5 * age + 5
    else:
        calories = 10 * weight + 6.25 * growth - 5 * age - 161

    await message.answer(f"Ваша норма калорий: {calories} ккал в день.")
    await message.answer("Посмотеть формулу рассчета:", reply_markup=kb_calc1)
    await UserState.btt.set()

@dp.callback_query_handler(text='formulas', state=UserState.btt)
async def show_formulas(call, state):
    data = await state.get_data()
    gender = data.get('gender')

    # Формулы расчета калорий
    if gender == 'мужчина':
        formula = ("Формула для мужчин: 10 * вес (кг) + 6.25 * рост (см) - 5 * возраст (лет) + 5 \n"
                   "Теперь можете перейти к покупкам")
    else:
        formula = ("Формула для женщин: 10 * вес (кг) + 6.25 * рост (см) - 5 * возраст (лет) - 161 \n"
                   "Теперь можете перейти к покупкам")

    await call.message.answer(formula)
    await call.answer()
    await UserState.buy.set()
   # await UserState.btt.set()  # `UserState.btt` для дальнейшего использования кнопок

@dp.message_handler(state=UserState.buy)
async def get_buying_list(message, state):
    data = await state.get_data()
    gender = data.get('gender')

    if gender == 'мужчина':
        for i in range(1, 5):
            # Подготовка данных для мужских витаминов
            name = f"Product{i}"
            description = f"Описание {i}"
            price = i * 100
            img = f"Files/{i}.jpg"
            with open(img, "rb") as img1:
            # Отправка сообщения с изображением и текстом
                await message.answer_photo(
                    photo=img1,
                    caption=f"Название: {name} | Описание: {description} | Цена: {price}"
                    )
        await message.answer("Выберите продукт для покупки:", reply_markup=inline_menu)
        await state.finish()
    else:
        for i in range(1, 5):
            # Подготовка данных для товара
            name = f"Product{i}"
            description = f"Описание {i}"
            price = i * 100
            img = f"Files/{i + 10}.jpg"
            with open(img, "rb") as img1:
                 # Отправка сообщения с изображением и текстом
                await message.answer_photo(
                    photo=img1,
                    caption=f"Название: {name} | Описание: {description} | Цена: {price}"
                    )
        await message.answer("Выберите продукт для покупки:", reply_markup=inline_menu)
        await state.finish()

@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer("Вы успешно приобрели продукт!")
    await call.answer()

@dp.callback_query_handler(text="back_to_catalog")
async def back(call):
    await call.message.answer("Вы вернулись вначало", reply_markup=start_menu)
    #await call.message.answer("Что вас интересует?", reply_markup=kb_calc)
    await call.answer()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)