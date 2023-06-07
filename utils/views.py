from sqlalchemy import update, delete
from database.models import Session, TodoModel, DetailTodo


class Get:
    @classmethod
    def get_todo_list(self, owner: str) -> str:
        with Session() as session:
            queryset = session.query(TodoModel).filter(TodoModel.owner == owner)
            query = [item for item in queryset]
            result = ""
            for i in range(len(query)):
                result += f"{query[i]}\n"
            return result
            
    
class Detail:
    @classmethod
    def get_detail_point(self, id: int, username: str) -> list:
        with Session() as session:
            queryset = session.query(DetailTodo)
            query = queryset.filter(DetailTodo.id == id).filter(DetailTodo.owner == username)
            result = [item for item in query]
            try:
                return result[0]
            except IndexError:
                return "There is no such unique id in your Todo-list!"
            

class Add:
    def __init__(self, title: str, description: str, deadline: str) -> None:
        self.title = title
        self.description = description
        self.deadline = deadline
    
    def add_point_to_list(self, username):
        point = TodoModel(self.title, self.description, self.deadline, username)
        with Session() as session:
            session.add(point)
            session.commit()
            

class Patch:
    @classmethod
    def update_title(self, id: int, new_title: str) -> None:
        statement = (
            update(TodoModel).where(TodoModel.id == id).values(title = new_title)
        )
        with Session() as session:
            session.execute(statement)
            session.commit()
    
    @classmethod
    def update_description(self, id: int, new_description: str) -> None:
        statement = (
            update(TodoModel).where(TodoModel.id == id).values(description = new_description)
        )
        with Session() as session:
            session.execute(statement)
            session.commit()
     
    @classmethod
    def update_deadline(self, id: int, new_deadline) -> None:
        statement = (
            update(TodoModel).where(TodoModel.id == id).values(deadline = new_deadline)
        )
        with Session() as session:
            session.execute(statement)
            session.commit()
            

class Delete:
    @classmethod
    def delete_point(self, id: int, username):
        statement = (
            delete(TodoModel).where(TodoModel.id == id).where(TodoModel.owner == username)
        )
        with Session() as session:
            session.execute(statement)
            session.commit()