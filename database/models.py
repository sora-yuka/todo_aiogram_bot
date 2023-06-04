from sqlalchemy import String, Text, Integer, DateTime, Column, create_engine, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.orm import sessionmaker
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
        return f"unique id: {self.id};  title: {self.title}"
    

class DetailTodo(TodoModel):
    def __repr__(self):
        super().__repr__()
        return (f"Title: {self.title}\nDescription: {self.description}\n"
                f"Deadline: {self.deadline}\nCreated_at: {self.created_at}")
    

engine = create_engine(config("DATABASE_URL"))
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()


# queryset = session.query(TodoModel).filter(TodoModel.owner == "yukl_sora")
# result = [item for item in queryset]
# for i in range(len(result)):
#     print(result[i])