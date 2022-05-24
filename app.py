#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
import os
import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
from models import db, Venue, Artist, Show
import sys
#----------------------------------------------------------------------------#
# App Config.


app = Flask(__name__)
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:learn101.@localhost:5432/fyyur'
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app,db)

    

def format_datetime(value, format='medium'):
  if isinstance(value, str):
        date = dateutil.parser.parse(value)
  else:
        date = value
  return babel.dates.format_datetime(date, format)     
app.jinja_env.filters['datetime'] = format_datetime


# Controllers.


@app.route('/')
def index():
  return render_template('pages/home.html')

# artists

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    body = {}
    return render_template('forms/new_artist.html', form=form, body=body)

'''
posting the artists information when created
'''
@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    form = ArtistForm()
    error = False
    body = {}
    try:
        artist = Artist()
        artist.name = request.form['name']
        artist.city = request.form['city']
        artist.state = request.form['state']
        artist.phone = request.form['phone']
        tmp_genres = request.form.getlist('genres')
        artist.genres = ','.join(tmp_genres)
        artist.website = request.form['website']
        artist.image_link = request.form['image_link']
        artist.facebook_link = request.form['facebook_link']
        artist.seeking_description = request.form['seeking_description']
        db.session.add(artist)
        db.session.commit()
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
        '''
        flash message incase of error when listing the artist or when artist has successfully been enlisted
        '''
        if error:
            flash('An error occurred. Artist ' +
                  request.form['name'] + ' could not be listed.')
        else:
            flash('Artist ' + request.form['name'] +
                  ' was successfully listed!')
        return render_template('pages/home.html')


'''
listing all artists recorded
'''
@app.route('/artists')
def artists():
    return render_template('pages/artists.html',
                           artists=Artist.query.all())


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):

    '''
    geting the artists data through the artists id
    '''
    artist = Artist.query.get(artist_id)

    '''
    artists past shows, upcoming shows , there venues and the time the took place
    '''
    past_shows = list(filter(lambda d: d.start_time <
                             datetime.today(), artist.shows))  
    upcoming_shows = list(filter(lambda d: d.start_time >=
                                 datetime.today(), artist.shows))

    past_shows = list(map(lambda d: d.show_venue(), past_shows))

    upcoming_shows = list(map(lambda d: d.show_venue(), upcoming_shows))
    
    '''
    shows the data of the artists past and upcoming stored
    '''

    data = artist.to_dict()
    print(data)
    data['past_shows'] = past_shows
    data['upcoming_shows'] = upcoming_shows
    data['past_shows_count'] = len(past_shows)
    data['upcoming_shows_count'] = len(upcoming_shows)
    return render_template('pages/show_artist.html', artist=data)



'''
geting artists information allowing the user to edit it 
'''
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()
    artist = Artist.query.get(artist_id)

    return render_template('forms/edit_artist.html', form=form, artist=artist)

'''
posting the edited information of the artists
'''
@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    error = False
    try:
        artist = Artist.query.get(artist_id)
        artist.name = request.form['name']
        artist.city = request.form['city']
        artist.state = request.form['state']
        artist.phone = request.form['phone']
        tmp_genres = request.form.getlist('genres')
        artist.genres = ','.join(tmp_genres)
        artist.website = request.form['website']
        artist.image_link = request.form['image_link']
        artist.facebook_link = request.form['facebook_link']
        artist.seeking_description = request.form['seeking_description']
        db.session.add(artist)
        db.session.commit()
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
        if error:
            return redirect(url_for('server_error'))
        else:
            return redirect(url_for('show_artist', artist_id=artist_id))

'''
allowing the user to search for artists and posting the search results
'''
@app.route('/artists/search', methods=['POST'])
def search_artists():
    search_term = request.form.get('search_term')
    '''
    filtering the search results according to the users requirements
    '''
    search_results = Artist.query.filter(
        Artist.name.ilike('%{}%'.format(search_term))).all()  
    
    '''
    responses to return to the user upon the search filters
    '''
    response = {}
    response['count'] = len(search_results)
    response['data'] = search_results

    return render_template('pages/search_artists.html',
                           results=response,
                           search_term=request.form.get('search_term', ''))

# Venues

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    error = False
    body = {}
    try:
        venue = Venue()
        venue.name = request.form['name']
        venue.city = request.form['city']
        venue.state = request.form['state']
        venue.address = request.form['address']
        venue.phone = request.form['phone']
        tmp_genres = request.form.getlist('genres')
        venue.genres = ','.join(tmp_genres)
        venue.facebook_link = request.form['facebook_link']
        db.session.add(venue)
        db.session.commit()
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
        if error:
            '''
            flash message incase of successfull listing or incase of an error when listing
            '''
            
            flash('An error occured. Venue ' +
                  request.form['name'] + ' Could not be listed')
        else:
            flash('Venue ' + request.form['name'] +
                  ' was successfully listed')
    return render_template('pages/home.html')


@app.route('/venues')
def venues():
    venues = Venue.query.order_by(Venue.state, Venue.city).all()

    data = []
    tmp = {}
    prev_city = None
    prev_state = None
    for venue in venues:
        venue_data = {
            'id': venue.id,
            'name': venue.name,
            'num_upcoming_shows': len(list(filter(lambda d: d.start_time > datetime.today(),
                                                  venue.shows)))
        }
        if venue.city == prev_city and venue.state == prev_state:
            tmp['venues'].append(venue_data)
        else:
            if prev_city is not None:
                data.append(tmp)
            tmp['city'] = venue.city
            tmp['state'] = venue.state
            tmp['venues'] = [venue_data]
        prev_city = venue.city
        prev_state = venue.state

    data.append(tmp)
    return render_template('pages/venues.html', areas=data)

'''
user searches for different venues and the information is posted on the view
'''
@app.route('/venues/search', methods=['POST'])
def search_venues():
    search_term = request.form.get('search_term')
    venues = Venue.query.filter(
        Venue.name.ilike('%{}%'.format(search_term))).all()

    '''
    upon searching the responses should include the data below
    '''
    data = []
    for venue in venues:
        tmp = {}
        tmp['id'] = venue.id
        tmp['name'] = venue.name
        tmp['num_upcoming_shows'] = len(venue.shows)
        data.append(tmp)

    response = {}
    response['count'] = len(data)
    response['data'] = data

    return render_template('pages/search_venues.html',
                           results=response,
                           search_term=request.form.get('search_term', ''))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    '''
    venues with the specific id filled are retrieved with there past shows and upcoming shows and what time they occur
    '''
    venue = Venue.query.get(venue_id)
    past_shows = list(filter(lambda d: d.start_time <
                             datetime.today(), venue.shows))
    upcoming_shows = list(filter(lambda d: d.start_time >=
                                 datetime.today(), venue.shows))

    '''
    shows the previous and upcoming data of the shows stored
    '''
    data = venue.to_dict()
    data['past_shows'] = past_shows
    data['upcoming_shows'] = upcoming_shows
    data['past_shows_count'] = len(past_shows)
    data['upcoming_shows_count'] = len(upcoming_shows)

    return render_template('pages/show_venue.html', venue=data)

'''
retriving the previous data and editing it
'''
@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()
    venue = Venue.query.get(venue_id).to_dict()
    return render_template('forms/edit_venue.html', form=form, venue=venue)

'''
the venues being edited if any changes are required. 
'''
@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    '''
    the data is updated according to the information submitted by the user
    '''
    venue = Venue.query.get(venue_id)

    error = False
    try:
        venue.name = request.form['name']
        venue.city = request.form['city']
        venue.state = request.form['state']
        venue.address = request.form['address']
        venue.phone = request.form['phone']
        tmp_genres = request.form.getlist('genres')
        venue.genres = ','.join(tmp_genres)  
        venue.facebook_link = request.form['facebook_link']
        db.session.add(venue)
        db.session.commit()
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
        '''
        flash messages incase of error or success
        '''
        if error:
            flash('Something went wrong. Venue ' +
                  request.form['name'] + ' could not be updated.')
        else:
            flash('Venue ' + request.form['name'] +
                  ' has successfully been updated!')
    return redirect(url_for('show_venue', venue_id=venue_id))


#  Shows

@app.route('/shows')
def shows():
    '''
    list all shows created
    '''
    shows = Show.query.all()

    data = []
    '''
    the data included is that, that has been entered in the postgres data 
    '''
    for show in shows:
        data.append({
            'venue_id': show.venue.id,
            'venue_name': show.venue.name,
            'artist_id': show.artist.id,
            'artist_name': show.artist.name,
            'artist_image_link': show.artist.image_link,
            'start_time': show.start_time.isoformat()
        })

    return render_template('pages/shows.html', shows=data)


@app.route('/shows/create')
def create_shows():
    '''
    rendering forms to create the show
    '''
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)

 
'''
show the created show created by the user
'''  

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    error = False
    body = {}
    try:
        show = Show()
        show.artist_id = request.form['artist_id']
        show.venue_id = request.form['venue_id']
        show.start_time = request.form['start_time']
        db.session.add(show)
        db.session.commit()
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
        if error:
            flash('Something went wrong. Show could not be listed.')
        else:
            flash('Show has successfully been listed')
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
        Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

# Launch.

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=port, debug=True)
