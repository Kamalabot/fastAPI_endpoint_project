from .databaseORM import Base
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.sql.expression import null

class Post(Base):
    __tablename__ = "social_posts"

    post_id = Column(Integer, primary_key=True,nullable=False)
    title = Column(String,nullable=False)
    content = Column(String, nullable=False)
    is_published = Column(Boolean, default=True)

