from sqlalchemy import String, Text, Integer, DateTime, Column, create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.orm import sessionmaker
from decouple import config

Base = declarative_base()


class User(Base):
    """ User database """
    __tablename__ = "users"
    
    id = Column("id", Integer, primary_key=True)
    


class TodoModel(Base):
    """ Data writing """
    __tablename__ = "in_process"
    
    id = Column("id", Integer, primary_key=True)
    title = Column("title", String)
    description = Column("description", Text)
    deadline = Column("deadline", String)
    created_at = Column(DateTime(timezone=True), 
                        server_default=func.now())
    
    def __init__(self, title, description, deadline):
        self.title = title
        self.description = description
        self.deadline = deadline
    
    def __repr__(self):
        return f"{self.id}. {self.title}"
    

class DetailTodo(TodoModel):
    def __repr__(self):
        super().__repr__()
        return (f"Title: {self.title}\nDescription: {self.description}\n"
                f"Deadline: {self.deadline}\nCreated_at: {self.created_at}")
    

engine = create_engine(config("DATABASE_URL"))
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

