import sqlite3

def enable_FKE(cur):
    cur.execute("PRAGMA foreign_keys = ON")

def create_DB(DB_name):
    with sqlite3.connect(DB_name) as con:
        cur = con.cursor()
        enable_FKE(cur)

        # Table: genres
        cur.execute('''
            CREATE TABLE IF NOT EXISTS genres (
                GENRESID INTEGER PRIMARY KEY AUTOINCREMENT,
                NAME TEXT NOT NULL UNIQUE
            )
        ''')

        # Table: artists
        cur.execute('''
            CREATE TABLE IF NOT EXISTS artists (
                ARTISTSID INTEGER PRIMARY KEY AUTOINCREMENT,
                NAME TEXT NOT NULL UNIQUE
            )
        ''')

        # Table: albums
        cur.execute('''
            CREATE TABLE IF NOT EXISTS albums (
                ALBUMID INTEGER PRIMARY KEY AUTOINCREMENT,
                NAME TEXT NOT NULL,
                ARTISTID INTEGER NOT NULL,
                UNIQUE(NAME, ARTISTID),
                FOREIGN KEY (ARTISTID) REFERENCES artists(ARTISTSID) ON DELETE CASCADE
            )
        ''')

        # Table: tracks
        cur.execute('''
            CREATE TABLE IF NOT EXISTS tracks (
                TRACKID INTEGER PRIMARY KEY AUTOINCREMENT,
                NAME TEXT NOT NULL,
                ALBUMID INTEGER NOT NULL,
                GENREID INTEGER,
                TRACKNR INTEGER CHECK(TRACKNR > 0),
                FOREIGN KEY (ALBUMID) REFERENCES albums(ALBUMID) ON DELETE CASCADE,
                FOREIGN KEY (GENREID) REFERENCES genres(GENRESID)
            )
        ''')



create_DB("MUZYCY.db")


def add_genre(DB_name, genre):
    with sqlite3.connect(DB_name) as con:
        cur = con.cursor()
        enable_FKE(cur)
        try:
            cur.execute('''INSERT INTO  genres (NAME) VALUES (?)''', (genre,))
        except sqlite3.IntegrityError:
            print("ERROR GENRE ", genre, " ALREADY EXISTS")

def add_artist(DB_name, artist):
    with sqlite3.connect(DB_name) as con:
        cur = con.cursor()
        enable_FKE(cur)

        try:
            cur.execute('''INSERT INTO  artists (NAME) VALUES (?)''', (artist,))
        except sqlite3.IntegrityError:
            print("ERROR ARTIST ", artist, " ALREADY EXISTS")

def add_album(DB_name, album_name, artist_name):
    with sqlite3.connect(DB_name) as con:
        cur = con.cursor()
        enable_FKE(cur)

        cur.execute("SELECT ARTISTSID FROM artists WHERE Name = ?", (artist_name,))
        row = cur.fetchone()

        if row is None:
            print(f"ERROR: Artist '{artist_name}' does not exist!")
            return

        artist_id = row[0]

        try:
            cur.execute("INSERT INTO albums (NAME, ARTISTID) VALUES (?, ?)", (album_name, artist_id))
        except sqlite3.IntegrityError:
            print(f"ERROR: Album '{album_name}' by '{artist_name}' already exists.")



add_genre("MUZYCY.db","Rock")
add_genre("MUZYCY.db","Rege")
add_genre("MUZYCY.db","Pop")
add_artist("MUZYCY.db","The Beatles")
add_artist("MUZYCY.db","LinkinPark")
add_artist("MUZYCY.db","Kamil Bednarek")
add_album("MUZYCY.db","Revolver","The Beatles")
add_album("MUZYCY.db","First","LinkinPark")
add_album("MUZYCY.db","The End", "LinkinPark")

def show_genres(DB_name):
    print("Genres: ")
    with sqlite3.connect(DB_name) as con:
        cur = con.cursor()
        enable_FKE(cur)
        for row in cur.execute("SELECT * FROM genres"):
            print(row)

def show_artist(DB_name):
    print("Artists: ")
    with sqlite3.connect(DB_name) as con:
        cur = con.cursor()
        enable_FKE(cur)
        for row in cur.execute("SELECT * FROM artists"):
            print(row)

def show_album(DB_name):
    print("ALbums: ")
    with sqlite3.connect(DB_name) as con:
        cur = con.cursor()
        enable_FKE(cur)
        for row in cur.execute("SELECT * FROM albums"):
            print(row)


show_album("MUZYCY.db")
show_genres("MUZYCY.db")
show_artist("MUZYCY.db")