"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

DEFAULT_URL = "https://www.freeiconspng.com/uploads/icon-user-blue-symbol-people-person-generic--public-domain--21.png"

def connect_db(app):

    db.app = app 
    db.init_app(app)

#models go below:
class User(db.Model):
    """User model including id[PK], first_name, last_name,
    image_url"""
    __tablename__ = 'users'
    id = db.Column(db.Integer,
                    primary_key = True,
                    autoincrement = True)
    first_name = db.Column(db.String(50),
                    nullable = False,
                    unique = True)
    last_name = db.Column(db.String(50),
                    nullable = False,
                    unique = True)
    image_url = db.Column(db.string(100),
                    nullable = False,
                    default = DEFAULT_URL)
    
    @classmethod
    def full_name(self):
        """Return user's full name"""
        return f'{self.first_name} {self.last_name}'


    
    #primary key means unique and not null in SQL for id