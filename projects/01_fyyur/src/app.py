#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, jsonify, flash, redirect, url_for
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from forms import *
from models import *
from extensions import db

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

def create_app(config):
    _app = Flask(__name__)
    _app.config.from_pyfile(config)
    moment.init_app(_app)
    csrf.init_app(_app)
    return _app


moment = Moment()
csrf = CSRFProtect()
app = create_app('config.py')
migrate = Migrate(app, db)
db.init_app(app)

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

@app.route('/venues', methods=['GET'])
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


@app.route('/venues/<int:venue_id>', methods=['GET'])
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
    form = VenueForm(meta={'csrf': False})
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    form = VenueForm(meta={'csrf': False})
    status = None
    try:
        if form.validate_on_submit():

            if form.seeking_talent.data == True and form.seeking_description:
                status = form.seeking_description.data

            venue = Venue(name=form.name.data, city=form.city.data,
                          state=form.state.data, address=form.address.data,
                          phone=form.phone.data, image_link=form.image_link.data,
                          facebook_link=form.facebook_link.data,
                          website_link=form.website_link.data, status=status)

            for genre in form.genres.data:
                entry = Genre.query.get(genre)
                venue.genres.append(entry)

            db.session.add(venue)
            db.session.commit()


            flash('Venue ' + form.name.data + ' was successfully listed!')
        else:
            errorMessage = "Please correct the following information: "
            for error in form.errors:
                errorMessage += error + " "
            flash(errorMessage)
    except:
        Raise
        db.session.rollback()
        flash('An error occurred. Venue ' + form.name.data + ' could not be listed.')
    finally:
        db.session.close()
    return render_template('pages/home.html')


@app.route('/venues/<int:venue_id>', methods=['DELETE'])
@csrf.exempt
def delete_venue(venue_id):
    success = False
    try:
        shows = Show.query.filter_by(venue=venue_id).delete()
        venue = Venue.query.get(venue_id)
        venue.genres.clear()
        db.session.delete(venue)
        db.session.commit()
        success = True
        flash('The venue was successfully deleted!')
    except:
        db.session.rollback()
        flash('An error occurred. The venue could not be deleted.')
        success = False
    finally:
        db.session.close()

    return jsonify({'success': success})


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
    form = ArtistForm(meta={'csrf': False})
    statusBool = False
    query = Artist.query.get_or_404(artist_id)

    if query.status:
        statusBool = True
    form.name.data = query.name
    form.genres.default = query.genres
    form.city.data = query.city
    form.state.data = query.state
    form.phone.data = query.phone
    form.website_link.data = query.website_link
    form.facebook_link.data = query.facebook_link
    form.seeking_venue.data = statusBool
    form.seeking_description.data = query.status
    form.image_link.data = query.image_link

    artist = {
        "id": artist_id,
        "name": query.name
    }

    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    form = ArtistForm(meta={'csrf': False})
    status = None
    try:
        if form.validate_on_submit():

            if form.seeking_venue.data == True and form.seeking_description:
                status = form.seeking_description.data

            artist = Artist.query.get_or_404(artist_id)
            artist.name = form.name.data
            artist.city = form.city.data
            artist.state = form.state.data
            artist.phone = form.phone.data
            artist.image_link = form.image_link.data
            artist.facebook_link = form.facebook_link.data
            artist.website_link = form.website_link.data
            artist.status = status

            for genre in form.genres.data:
                entry = Genre.query.get(genre)
                artist.genres.append(entry)

            db.session.add(artist)
            db.session.commit()

            flash('Artist ' + form.name.data + ' was successfully updated!')
        else:
            errorMessage = "Please correct the following information: "
            for error in form.errors:
                errorMessage += error + " "
            flash(errorMessage)
    except:
        db.session.rollback()
        flash('An error occurred. Artist ' + form.name.data + ' could not be updated.')
    finally:
        db.session.close()
    return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm(meta={'csrf': False})

    statusBool = False
    query = Venue.query.get_or_404(venue_id)
    if query.status:
        statusBool = True

    form.name.data = query.name
    form.genres.default = query.genres
    form.address.data = query.address
    form.city.data = query.city
    form.state.data = query.state
    form.phone.data = query.phone
    form.website_link.data = query.website_link
    form.facebook_link.data = query.facebook_link
    form.seeking_talent.data = statusBool
    form.seeking_description.data = query.status
    form.image_link.data = query.image_link

    venue = {
        "id": venue_id,
        "name": query.name
    }

    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    form = VenueForm(meta={'csrf': False})
    status = None
    try:
        if form.validate_on_submit():

            if form.seeking_talent.data == True and form.seeking_description:
                status = form.seeking_description.data

            venue = Venue.query.get_or_404(venue_id)
            venue.name=form.name.data
            venue.city=form.city.data
            venue.state=form.state.data
            venue.address=form.address.data
            venue.phone=form.phone.data
            venue.image_link=form.image_link.data
            venue.facebook_link=form.facebook_link.data
            venue.website_link=form.website_link.data
            venue.status=status

            for genre in form.genres.data:
                entry = Genre.query.get(genre)
                venue.genres.append(entry)

            db.session.add(venue)
            db.session.commit()

            flash('Venue ' + form.name.data + ' was successfully updated!')
        else:
            errorMessage = "Please correct the following information: "
            for error in form.errors:
                errorMessage += error + " "
            flash(errorMessage)
    except:
        db.session.rollback()
        flash('An error occurred. Venue ' + form.name.data + ' could not be updated.')
    finally:
        db.session.close()
    return redirect(url_for('show_venue', venue_id=venue_id))


#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm(meta={'csrf': False})
    return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    form = ArtistForm(meta={'csrf': False})
    status = None
    try:
        if form.validate_on_submit():

            if form.seeking_venue.data == True and form.seeking_description:
                status = form.seeking_description.data

            artist = Artist(name=form.name.data, city=form.city.data,
                        state=form.state.data, phone=form.phone.data,
                        image_link=form.image_link.data,
                        facebook_link=form.facebook_link.data,
                        website_link=form.website_link.data, status=status)

            for genre in form.genres.data:
                entry = Genre.query.get(genre)
                artist.genres.append(entry)

            db.session.add(artist)
            db.session.commit()

            flash('Artist ' + form.name.data + ' was successfully listed!')
        else:
            errorMessage = "Please correct the following information: "
            for error in form.errors:
                errorMessage += error + " "
            flash(errorMessage)
    except:
        db.session.rollback()
        flash('An error occurred. Artist ' + form.name.data + ' could not be listed.')
    finally:
        db.session.close()
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
  form = ShowForm(meta={'csrf': False})
  return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    form = ShowForm(meta={'csrf': False})
    try:
        if form.validate_on_submit():
            artist_id=int(form.artist_id.data)
            venue_id=int(form.venue_id.data)
            show = Show(artist=artist_id, venue=venue_id, date=form.start_time.data)

            db.session.add(show)
            db.session.commit()

            flash('Show was successfully listed!')
        else:
            errorMessage = "Please correct the following information: "
            for error in form.errors:
                errorMessage += error + " "
            flash(errorMessage)
    except:
        db.session.rollback()
        flash('An error occurred. Show could not be listed.')
    finally:
        db.session.close()
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
