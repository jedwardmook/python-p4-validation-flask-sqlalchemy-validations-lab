from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    @validates("name")
    def validates_name(self, key, name):
        if not name:
            raise ValueError("Must have name")
        existing = self.query.filter(Author.name == name).first()
        if existing and existing.id != self.id:
            raise ValueError("Name already taken")
        return name
    
    @validates("phone_number")
    def validates_phone_number(self, key, phone_number):
        if len(phone_number) != 10:
            print(len(phone_number))
            raise ValueError("Phone number must be 10 digits")
        if not phone_number.isdigit():
            raise ValueError("Phone number must only be digits")
        return phone_number

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators
    @validates("title")
    def post_has_title(self, key, title):
        if not title:
            raise ValueError("Post must have title.")
        clickbait_phrase = ["Won't Believe", "Secret", "Top", "Guess"]
        if not any(phrase in title for phrase in clickbait_phrase):
                raise ValueError("Title must have clickbait")
        return title
    
    @validates("content")
    def content_minimum(self, key, content):
        if len(content) < 250:
            raise ValueError("Content must be at least 250 characters")
        return content
    
    @validates("summary")
    def summary_maximum(self, key, summary):
        if len(summary) > 250:
            raise ValueError("Summary must be under 250 characters")
        return summary
    
    @validates("category")
    def is_Fiction_Or_Non_Fiction(self, key, category):
        valid_categories = ["Fiction", "Non-Fiction"]
        if category not in valid_categories:
            raise ValueError("Category must be Fiction or Non-Fiction")
        return category
    

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
