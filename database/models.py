from sqlalchemy.sql import func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import String, Text, Integer, DateTime, Column, create_engine, ForeignKey
from decouple import config

Base = declarative_base()


class TodoModel(Base):
    """ Data writing """
    __tablename__ = "todo_list"
    
    id = Column("id", Integer, primary_key=True)
    owner = Column("owner", Text)
    title = Column("title", String)
    description = Column("description", Text)
    deadline = Column("deadline", String)
    created_at = Column(DateTime(timezone=True), 
                        server_default=func.now())
    
    def __init__(self, title, description, deadline, owner):
        self.title = title
        self.description = description
        self.deadline = deadline
        self.owner = owner
    
    def __repr__(self):
        return f"<b>unique id:</b>  {self.id};    <b>todo:</b>  {self.title}"
    

class DetailTodo(TodoModel):
    def __repr__(self):
        super().__repr__()
        return (f"<b>Unique id:</b>  {self.id}\n<b>Todo:</b>  {self.title}\n<b>Description:</b>  {self.description}\n"
                f"<b>Deadline:</b>  {self.deadline}\n<b>Created_at:</b>  {self.created_at}")
    

engine = create_engine(config("DATABASE_URL"))
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)