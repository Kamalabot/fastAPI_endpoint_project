from .databaseORM import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.expression import null, text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship

class Post(Base):
    __tablename__ = "social_posts"

    post_id = Column(Integer, primary_key=True,nullable=False)
    title = Column(String,nullable=False)
    content = Column(String, nullable=False)
    is_published = Column(Boolean, default=True, nullable=False)
    time_created = Column(TIMESTAMP(timezone=True),
                          nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey("users.user_id",ondelete="CASCADE"),
                      nullable=False)
    owner = relationship("User")
#When you create the ORM model, the server may be reloading automatically.
#Once the table is created in the database, it has to be dropped manually.
#SQLAlchemy will not drop it for you...
class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, nullable=False)
    user_create_time = Column(TIMESTAMP(timezone=True),nullable=False,
                              server_default=text('now()'))
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    phone = Column(String, nullable=True)

class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(Integer, ForeignKey("users.user_id",ondelete="CASCADE"),primary_key=True)
    post_id = Column(Integer, ForeignKey("social_posts.post_id",ondelete="CASCADE"),primary_key=True)
