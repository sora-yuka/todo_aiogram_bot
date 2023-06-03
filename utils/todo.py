from database.models import session, ToDoModel

class Get:
    @classmethod
    def get_todo_list(self) -> list:
        result = ""
        queryset = session.query(ToDoModel).all()
        for query in queryset:
            result += f"{query}\n"
        return result


class Add:
    def __init__(self, todo_title, todo_description, todo_deadline):
        self.todo_title = todo_title
        self.todo_description = todo_description
        self.todo_deadline = todo_deadline
    
    def add_point_to_list(self):
        point = ToDoModel(self.todo_title, self.todo_description, self.todo_deadline)
        session.add(point)
        session.commit()