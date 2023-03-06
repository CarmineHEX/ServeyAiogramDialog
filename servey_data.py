from aiogram.dispatcher.filters.state import StatesGroup, State


class Servey():
    def __init__(self):
        self.answers = {}
        self.save_state = State()
