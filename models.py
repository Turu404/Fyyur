# ---- Models for Artists , Venues and Shows --- #

# -- Imports
from  flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:learn101.@localhost:5432/fyyur'
db = SQLAlchemy(app)

# --- Models --- #

# --- venue model ---

class Venue(db.Model):
    '''
    naming the table
    '''
    __tablename__ = 'venues'

    '''
    attributes columns to the venues table
    '''
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String(120))
    website = db.Column(db.String(120))
    
    '''
    relationship between the different tables
    '''
    artists = db.relationship('Artist', secondary='shows')
    shows = db.relationship('Show', backref=('venues'))


    '''
    creating a dictionary list that will store the venues table attributes
    '''

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'city': self.city,
            'state': self.state,
            'address': self.address,
            'phone': self.phone,
            'genres': self.genres,
            'image_link': self.image_link,
            'facebook_link': self.facebook_link,
            'website': self.website,
            
        }

    '''
    information to show at the view
    ''' 
    def __repr__(self):
        return f'<Venue {self.id} {self.name}>'

# --- artist model ---

class Artist(db.Model):
    __tablename__ = 'artists'  

    '''
    attributes columns of the artists table
    '''
   
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String(120))
    website = db.Column(db.String(120))
    
    '''
    relationship between the artists table and other tables
    '''
    venues = db.relationship('Venue', secondary='shows')
    shows = db.relationship('Show', backref=('artists'))


    '''
    creating a dictionary list that will store the artists table attributes
    ''' 

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'city': self.city,
            'state': self.state,
            'phone': self.phone,
            'genres': self.genres,
            'image_link': self.image_link,
            'facebook_link': self.facebook_link,
            'website': self.website,
            
        }
    
    '''
    information to show at the view
    ''' 
    def __repr__(self):
        return f'<Artist {self.id} {self.name}>'


# --- Show model --

class Show(db.Model):
    __tablename__ = 'shows'

    '''
    attributes columns of the shows table linked with foreign keys to the other tables
    '''

    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey(
        'artists.id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey(
        'venues.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)

    venue = db.relationship('Venue')
    artist = db.relationship('Artist')


    '''
    creating a function that returns the table attributes
    '''
    def show_artist(self):
        return {
            'artist_id': self.artist_id,
            'artist_name': self.artist.name,
            'artist_image_link': self.artist.image_link,

# --- converting datetime to string ----
            'start_time': self.start_time.strftime('%Y-%m-%d %H:%M:%S')
        }




    def show_venue(self):
        return {
            'venue_id': self.venue_id,
            'venue_name': self.venue.name,
            'venue_image_link': self.venue.image_link,
            'start_time': self.start_time.strftime('%Y-%m-%d %H:%M:%S')
        }



db.create_all()
