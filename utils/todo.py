from database.models import session, TodoModel, DetailTodo

class Get:
    @classmethod
    def get_todo_list(self) -> list:
        result = ""
        queryset = session.query(TodoModel).all()
        for query in queryset:
            result += f"{query}\n"
        return result
    
    
class Detail:
    @classmethod
    def get_detail_point(self, id) -> list:
        queryset = session.query(DetailTodo).filter(DetailTodo.id == id)
        result = [item for item in queryset]
        return result[0]


class Add:
    def __init__(self, todo_title, todo_description, todo_deadline) -> None:
        self.todo_title = todo_title
        self.todo_description = todo_description
        self.todo_deadline = todo_deadline
    
    def add_point_to_list(self):
        point = TodoModel(self.todo_title, self.todo_description, self.todo_deadline)
        session.add(point)
        session.commit()