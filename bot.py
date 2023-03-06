from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import Message, CallbackQuery

from aiogram_dialog.widgets.input import MessageInput
from aiogram.dispatcher import FSMContext
from aiogram_dialog import Window, Dialog, DialogRegistry, DialogManager, StartMode
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const
from bot_state import Form
from servey_data import Servey

s = Servey()
bs = Form()
s.save_state = bs.name


async def servey_click(c: CallbackQuery, state: FSMContext, dialog_manager: DialogManager):
    if s.save_state == bs.name:
        await dialog_manager.start(Form.name, mode=StartMode.RESET_STACK)
    elif s.save_state != bs.end_servey:
        await dialog_manager.start(s.save_state, mode=StartMode.RESET_STACK)
    else:
        await c.message.answer("Вы уже прошли опрос")


async def main_click(c: CallbackQuery, state: FSMContext, dialog_manager: DialogManager):
    await dialog_manager.start(bs.main, mode=StartMode.RESET_STACK)


async def input_name(message: Message, state: FSMContext, dialog_manager: DialogManager):
    s.answers['name'] = message.text
    await dialog_manager.start(bs.surname, mode=StartMode.RESET_STACK)
    s.save_state = dialog_manager.current_context().state


async def input_surname(message: Message, state: FSMContext, dialog_manager: DialogManager):
    s.answers['surname'] = message.text
    await dialog_manager.start(bs.age, mode=StartMode.RESET_STACK)
    s.save_state = dialog_manager.current_context().state


async def input_age(message: Message, state: FSMContext, dialog_manager: DialogManager):
    if str.isnumeric(message.text):
        s.answers['age'] = int(message.text)
        dialog_manager.current_context().dialog_data.update(age=message.text)
        await dialog_manager.start(bs.state, mode=StartMode.RESET_STACK)
        s.save_state = dialog_manager.current_context().state
    else:
        await message.answer("Ошибка ввода:Введите число ")


async def input_state(message: Message, state: FSMContext, dialog_manager: DialogManager):
    s.answers['state'] = message.text
    await dialog_manager.start(bs.city, mode=StartMode.RESET_STACK)
    s.save_state = dialog_manager.current_context().state


async def input_city(message: Message, state: FSMContext, dialog_manager: DialogManager):
    s.answers['city'] = message.text
    await message.answer(f"Имя: {s.answers['name']}\n"
                         f"Фамилия: {s.answers['surname']}\n"
                         f"Возраст: {s.answers['age']}\n"
                         f"Страна: {s.answers['state']}\n"
                         f"Город: {s.answers['city']}"
                         )
    await dialog_manager.start(bs.end_servey, mode=StartMode.RESET_STACK)
    s.save_state = dialog_manager.current_context().state


main_window = Window(
    Const("Привет"),
    Const("Нажмите на кнопку, чтобы начать опрос"),
    Button(Const("Начать опрос"), id="begin_servey", on_click=servey_click),
    state=bs.main,
)
question_name = Window(
    Const("1.Как вас зовут?"),
    Button(Const("На главный экран"), id="main", on_click=main_click),
    MessageInput(
        func=input_name
    ),
    state=bs.name,
)
question_surname = Window(
    Const("2.Какая ваша фамилия?"),
    Button(Const("На главный экран"), id="main", on_click=main_click),
    MessageInput(
        func=input_surname
    ),
    state=bs.surname,
)
question_age = Window(
    Const("3.Сколько вам лет?"),
    Button(Const("На главный экран"), id="main", on_click=main_click),
    MessageInput(
        func=input_age
    ),
    state=bs.age,
)
question_state = Window(
    Const("4.В какой стране вы проживаете?"),
    Button(Const("На главный экран"), id="main", on_click=main_click),
    MessageInput(
        func=input_state
    ),
    state=bs.state,
)
question_city = Window(
    Const("5.В каком городе вы живете?"),
    Button(Const("На главный экран"), id="main", on_click=main_click),
    MessageInput(
        func=input_city
    ),
    state=bs.city,
)
end_servey = Window(
    Const("Конец опроса"),
    Button(Const("На главный экран"), id="main", on_click=main_click),
    state=bs.end_servey,
)

storage = MemoryStorage()
bot = Bot(token="6138231355:AAGM9k41FIUbRoU4pBvqmGr0qB8nFbHZv2o")
dp = Dispatcher(bot, storage=storage)
registry = DialogRegistry(dp)
dialog = Dialog(
    main_window,
    question_name,
    question_surname,
    question_age,
    question_state,
    question_city,
    end_servey,
)
registry.register(dialog)


@dp.message_handler(commands=["start"])
async def start(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(Form.main, mode=StartMode.RESET_STACK)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
