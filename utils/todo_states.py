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
    """ Patch state declaration """
    id = State()

    
class TitlePatchState(StatesGroup):
    """ Title state for patch """
    title = State()
    

class DescriptionPatchState(StatesGroup):
    """ Description state for patch """
    description = State()
    
    
class DeadlinePatchState(StatesGroup):
    """ Deadline state for patch """
    deadline = State()