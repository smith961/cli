import inquirer
from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.orm import declarative_base
from termcolor import colored
import pyfiglet

#Create the database engine and session
DATABASE_URL = 'sqlite:///mydatabase.db'
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()  #Create a session instance

#Create the base class for declarative models
Base = declarative_base()

#Define the Artist and Song classes
class Artist(Base):
    __tablename__ = 'artist_table'
    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True, nullable=False)
    genre = Column(String)
    songs = relationship('Song' backref='artist')

class Song(Base):
    __tablename__ = 'songs_table'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    release_date = Column(Text)
    bpm = Column(Integer)
    artist_id = Column(Integer, ForeignKey('artist_table.id'))

#Create the tables if they don't exist
Base.metadata.create_all(engine)

#Function to find or create an artist
def find_or_create_artist(title, genre):
    artist = session.query(Artist).filter(Artist.title == title).first()

    if artist is None:
        artist = Artist(title=title, genre=genre)
        session.add(artist)
        session.commit()
        print(colored(f"Artist '{title}' added with ID {artist.id}", "green"))
    else:
        print(colored(f"Artist '{title}' already exists with ID {artist.id}", "red"))

    return artist

#Function to create an artist
def create_artist():
    title = input(colored('Artist Name: ', "gold"))
    genre = input(colored('Genre: ', "gold"))

    find_or_create_artist(title, genre)
