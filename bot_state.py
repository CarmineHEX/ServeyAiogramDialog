from aiogram.dispatcher.filters.state import StatesGroup, State

class Form(StatesGroup):
    main = State()
    name = State()
    surname = State()
    age = State()
    state = State()
    city = State()
    end_servey = State()