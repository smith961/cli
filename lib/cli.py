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
    songs = relationship('Song' ,backref='artist')

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

#Function to find or create a song
def find_or_create_song(title, artist_name, release_date, bpm):
    artist = session.query(Artist).filter(Artist.title == artist_name).first()

    if artist is None:
        print(colored(f"Artist '{artist_name}' not found. Song not created", "red"))
        return
    song = session.query(Song).filter(Song.title == title, Song.artist_id == artist.id).first()

    if song is None:
        song = Song(
            title= title,
            artist_id = artist.id,
            release_date=release_date,
            bmp = bpm
        )
        session.add(song)
        session.commit()
        print(colored(f"Song '{title}' added with ID {song.id}", "green" ))

    else:
        print(colored(f"Song '{title}' already exists with ID {song.id}", "red"))

    #Function to create a song
    def create_song():
        artists = session.query(Artist).all()
        artist_choices = {artist.title: artist for artist in artists}

        title = input(colored('Song Title: ', 'gold'))
        artist_name = input(colored('Select Artist or enter "new" to create a new artist: ', "gold"))

        if artist_name.lower() == "new":
            #Create a new artist
            new_artist_name = input(colored('New Artist Name: ', "gold"))
            new_artist_genre = input(colored('Genre: ', "gold"))

            if not new_artist_name:
                print(colored("Artist Name cannot be empty.", "red"))
                return
            
            find_or_create_artist(new_artist_name, new_artist_genre)
            artist_name = new_artist_name
        elif artist_name not in artist_choices:
            print(colored("Invalid Artist Name.", "red"))
            return
        release_date = input(colored ('Release Date: ', "gold"))
        bpm = input(colored('BPM (optional): ', "gold"))

        if not title:
            print(colored("Song Title cannot be empty.", "red"))
            return 
        
        if not release_date:
            print(colored("Release Date cannot be empty.", "red"))
        
        if not bpm:
            bpm = None
        elif not bpm.isdigit() or len(bpm) == 0:
            print(colored("Invalid BPM input. BPM set to None.", "red"))
            bpm = None
        else:
            bpm= int(bpm)
        
        find_or_create_song(title, artist_name, release_date, bpm)

    
