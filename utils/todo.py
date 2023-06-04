from database.models import session, TodoModel, DetailTodo

class Get:
    @classmethod
    def get_todo_list(self, owner) -> list:
        queryset = session.query(TodoModel).filter(TodoModel.owner == owner)
        query = [item for item in queryset]
        if query != []:
            result = ""
            for i in range(len(query)):
                result += f"{query[i]}\n"
            return result
        else:
            return "Nothing here."
    
    
class Detail:
    @classmethod
    def get_detail_point(self, id, username) -> list:
        queryset = session.query(DetailTodo)
        query = queryset.filter(DetailTodo.id == id) and queryset.filter(DetailTodo.owner == username)
        result = [item for item in query]
        return result[0]


class Add:
    def __init__(self, todo_title, todo_description, todo_deadline) -> None:
        self.todo_title = todo_title
        self.todo_description = todo_description
        self.todo_deadline = todo_deadline
    
    def add_point_to_list(self, username):
        point = TodoModel(self.todo_title, self.todo_description, self.todo_deadline, username)
        session.add(point)
        session.commit()