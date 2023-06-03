from sqlalchemy import String, Text, Integer, DateTime, Column, create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.orm import sessionmaker
from decouple import config

Base = declarative_base()


class ToDoModel(Base):
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
    

engine = create_engine(config("DATABASE_URL"))
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

# session.add(ToDoModel("Make a todo bot", 
#                       "Make a telegram bot, based on python class, and which is follow the SOLID princple", 
#                       "05.06.23"))
# session.commit()

# queryset = session.query(ToDoModel).all()
# for item in queryset:
#     print(item)

# queryset = session.query(ToDoModel).filter(ToDoModel.id == "3")
# print([item for item in queryset])