#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#


def create_app(config):
    _app = Flask(__name__)
    _app.config.from_pyfile(config)
    moment.init_app(_app)
    return _app


moment = Moment()
app = create_app('config.py')
db = SQLAlchemy(app)
migrate = Migrate(app, db)


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
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(120))
    status = db.Column(db.String(120))
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
    status = db.Column(db.String(120))
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


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/')
def index():
    return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
    data = []
    areas = Venue.query.distinct(Venue.city, Venue.state).all()

    for area in areas:
        venues_query = Venue.query.filter_by(city=area.city).filter_by(state=area.state)

        _venues = []
        for venue in venues_query:
            _venues.append({
              "id": venue.id,
              "name": venue.name
            })

        data.append({
          "city": area.city,
          "state": area.state,
          "venues": _venues
        })
    return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['GET'])
def search_venues():
    query = request.args.get('search_term')
    matches = Venue.query.filter(Venue.name.ilike('%' + query + '%')).all()
    data = []

    for match in matches:
        data.append({
          "id": match.id,
          "name": match.name
        })

    response = {
      "count": len(matches),
      "data": data
      }

    return render_template('pages/search_venues.html', results=response, search_term=request.args.get('search_term'))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    venue = Venue.query.get_or_404(venue_id)

    named_genres = []
    for genre in venue.genres:
        named_genres.append(genre.name)

    venue_shows = db.session.query(Show, Artist).filter_by(venue=venue_id).join(Artist).all()
    _past_shows = []
    _upcoming_shows = []

    for (show, artist) in venue_shows:
        item = {
            "artist_id": artist.id,
            "artist_name": artist.name,
            "artist_image_link": artist.image_link,
            "start_time": show.date.strftime("%m/%d/%Y, %H:%M:%S")
        }

        if show.date < datetime.now():
            _past_shows.append(item)
        else:
            _upcoming_shows.append(item)

    data = {
        "id": venue.id,
        "name": venue.name,
        "genres": named_genres,
        "city": venue.city,
        "state": venue.state,
        "phone": venue.phone,
        "website": venue.website_link,
        "facebook_link": venue.facebook_link,
        "status": venue.status,
        "image_link": venue.image_link,
        "past_shows": _past_shows,
        "past_shows_count": len(_past_shows),
        "upcoming_shows": _upcoming_shows,
        "upcoming_shows_count": len(_upcoming_shows),
    }

    return render_template('pages/show_venue.html', venue=data)


#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  # on successful db insert, flash success
  flash('Venue ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None


#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
    data = []
    _artists = Artist.query.all()

    for artist in _artists:
        data.append({
          "id": artist.id,
          "name": artist.name
        })
    return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['GET'])
def search_artists():
    query = request.args.get('search_term')
    matches = Artist.query.filter(Artist.name.ilike('%' + query + '%')).all()
    data = []

    for match in matches:
        data.append({
            "id": match.id,
            "name": match.name
        })

    response = {
        "count": len(matches),
        "data": data
    }

    return render_template('pages/search_artists.html', results=response, search_term=request.args.get('search_term'))


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    artist = Artist.query.get_or_404(artist_id)

    named_genres = []
    for genre in artist.genres:
        named_genres.append(genre.name)

    artist_shows = db.session.query(Show, Venue).filter_by(artist=artist_id).join(Venue).all()
    _past_shows = []
    _upcoming_shows = []

    for (show, venue) in artist_shows:
        item = {
            "venue_id": venue.id,
            "venue_name": venue.name,
            "venue_image_link": venue.image_link,
            "start_time": show.date.strftime("%m/%d/%Y, %H:%M:%S")
        }

        if show.date < datetime.now():
            _past_shows.append(item)
        else:
            _upcoming_shows.append(item)

    data = {
        "id": artist.id,
        "name": artist.name,
        "genres": named_genres,
        "city": artist.city,
        "state": artist.state,
        "phone": artist.phone,
        "website": artist.website_link,
        "facebook_link": artist.facebook_link,
        "status": artist.status,
        "image_link": artist.image_link,
        "past_shows": _past_shows,
        "past_shows_count": len(_past_shows),
        "upcoming_shows": _upcoming_shows,
        "upcoming_shows_count": len(_upcoming_shows),
    }

    return render_template('pages/show_artist.html', artist=data)


#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist={
    "id": 4,
    "name": "Guns N Petals",
    "genres": ["Rock n Roll"],
    "city": "San Francisco",
    "state": "CA",
    "phone": "326-123-5000",
    "website": "https://www.gunsnpetalsband.com",
    "facebook_link": "https://www.facebook.com/GunsNPetals",
    "seeking_venue": True,
    "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
    "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
  }
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue={
    "id": 1,
    "name": "The Musical Hop",
    "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    "address": "1015 Folsom Street",
    "city": "San Francisco",
    "state": "CA",
    "phone": "123-123-1234",
    "website": "https://www.themusicalhop.com",
    "facebook_link": "https://www.facebook.com/TheMusicalHop",
    "seeking_talent": True,
    "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
  }
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  # on successful db insert, flash success
  flash('Artist ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    shows = db.session.query(Show, Artist, Venue).join(Artist).join(Venue).all()
    data = []

    for (show, artist, venue) in shows:
        item = {
              "venue_id": venue.id,
              "venue_name": venue.name,
              "artist_id": artist.id,
              "artist_name": artist.name,
              "artist_image_link": artist.image_link,
              "start_time": show.date.strftime("%m/%d/%Y, %H:%M:%S")
        }
        data.append(item)

    return render_template('pages/shows.html', shows=data)


@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead

  # on successful db insert, flash success
  flash('Show was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
