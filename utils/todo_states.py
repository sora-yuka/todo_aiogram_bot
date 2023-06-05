from aiogram.dispatcher.filters.state import StatesGroup, State


class ToDoStatesGroup(StatesGroup):
    """ Todo state declaration """
    title = State()
    description = State()
    deadline = State()
    

class DetailViewStatesGroup(StatesGroup):
    """ Detail state declaration for point """
    id = State()

    
class PatchStateGroup(StatesGroup):
    id = State()

    
class TitlePatchState(StatesGroup):
    title = State()
    

class DescriptionPatchState(StatesGroup):
    description = State()
    
    
class DeadlinePatchState(StatesGroup):
    deadline = State()