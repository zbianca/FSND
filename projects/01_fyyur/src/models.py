#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from app import db

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

venueGenres = db.Table('Venue_Genres',
                       db.Column('genre_id', db.Integer, db.ForeignKey('Genre.id'), nullable=False),
                       db.Column('venue_id', db.Integer, db.ForeignKey('Venue.id'), nullable=False)
                       )

artistGenres = db.Table('Artist_Genres',
                        db.Column('genre_id', db.Integer, db.ForeignKey('Genre.id'), nullable=False),
                        db.Column('artist_id', db.Integer, db.ForeignKey('Artist.id'), nullable=False)
                        )


class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(120))
    status = db.Column(db.String(280))
    genres = db.relationship('Genre', secondary=venueGenres, lazy='subquery', backref='venue')

    def __repr__(self):
        return f'<Venue ID: {self.id}, genres: {self.genres}>'


class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(120))
    status = db.Column(db.String(280))
    genres = db.relationship('Genre', secondary=artistGenres, lazy='subquery', backref='artist')

    def __repr__(self):
        return f'<Artist ID: {self.id}, genres: {self.genres}>'


class Show(db.Model):
    __tablename__ = 'Show'

    id = db.Column(db.Integer, primary_key=True)
    artist = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
    venue = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f'<Show ID: {self.id}, artist: {self.artist}, venue: {self.venue}, date: {self.date}>'


class Genre(db.Model):
    __tablename__ = 'Genre'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f'<Genre name: {self.name}>'
