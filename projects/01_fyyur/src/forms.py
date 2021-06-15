from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField, BooleanField
from wtforms.validators import DataRequired, Length, Optional, URL


class ShowForm(FlaskForm):
    artist_id = StringField(
        'artist_id'
    )
    venue_id = StringField(
        'venue_id'
    )
    start_time = DateTimeField(
        'start_time',
        validators=[DataRequired()],
        default=datetime.today()
    )


class VenueForm(FlaskForm):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired(), Length(max=120)]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=[
            ('AL', 'AL'),
            ('AK', 'AK'),
            ('AZ', 'AZ'),
            ('AR', 'AR'),
            ('CA', 'CA'),
            ('CO', 'CO'),
            ('CT', 'CT'),
            ('DE', 'DE'),
            ('DC', 'DC'),
            ('FL', 'FL'),
            ('GA', 'GA'),
            ('HI', 'HI'),
            ('ID', 'ID'),
            ('IL', 'IL'),
            ('IN', 'IN'),
            ('IA', 'IA'),
            ('KS', 'KS'),
            ('KY', 'KY'),
            ('LA', 'LA'),
            ('ME', 'ME'),
            ('MT', 'MT'),
            ('NE', 'NE'),
            ('NV', 'NV'),
            ('NH', 'NH'),
            ('NJ', 'NJ'),
            ('NM', 'NM'),
            ('NY', 'NY'),
            ('NC', 'NC'),
            ('ND', 'ND'),
            ('OH', 'OH'),
            ('OK', 'OK'),
            ('OR', 'OR'),
            ('MD', 'MD'),
            ('MA', 'MA'),
            ('MI', 'MI'),
            ('MN', 'MN'),
            ('MS', 'MS'),
            ('MO', 'MO'),
            ('PA', 'PA'),
            ('RI', 'RI'),
            ('SC', 'SC'),
            ('SD', 'SD'),
            ('TN', 'TN'),
            ('TX', 'TX'),
            ('UT', 'UT'),
            ('VT', 'VT'),
            ('VA', 'VA'),
            ('WA', 'WA'),
            ('WV', 'WV'),
            ('WI', 'WI'),
            ('WY', 'WY'),
        ]
    )
    address = StringField(
        'address', validators=[DataRequired(), Length(max=120)]
    )
    phone = StringField(
        'phone', validators=[Length(max=120), Optional(strip_whitespace=True)]
    )
    image_link = StringField(
        'image_link', validators=[Length(max=500), Optional(strip_whitespace=True)]
    )
    genres = SelectMultipleField(
        'genres', validators=[Optional()],
        choices=[
            ('9', 'Alternative'),
            ('10', 'Blues'),
            ('4', 'Classical'),
            ('11', 'Country'),
            ('12', 'Electronic'),
            ('5', 'Folk'),
            ('13', 'Funk'),
            ('8', 'Hip-Hop'),
            ('14', 'Heavy Metal'),
            ('15', 'Instrumental'),
            ('1', 'Jazz'),
            ('16', 'Musical Theatre'),
            ('17', 'Pop'),
            ('18', 'Punk'),
            ('7', 'R&B'),
            ('2', 'Reggae'),
            ('6', 'Rock n Roll'),
            ('19', 'Soul'),
            ('20', 'Other'),
        ]
    )
    facebook_link = StringField(
        'facebook_link', validators=[URL(), Length(max=120), Optional(strip_whitespace=True)]
    )
    website_link = StringField(
        'website_link', validators=[URL(), Length(max=120), Optional(strip_whitespace=True)]
    )

    seeking_talent = BooleanField('seeking_talent')

    seeking_description = StringField(
        'seeking_description', validators=[Length(max=280), Optional(strip_whitespace=True)]
    )


class ArtistForm(FlaskForm):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired(), Length(max=120)]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=[
            ('AL', 'AL'),
            ('AK', 'AK'),
            ('AZ', 'AZ'),
            ('AR', 'AR'),
            ('CA', 'CA'),
            ('CO', 'CO'),
            ('CT', 'CT'),
            ('DE', 'DE'),
            ('DC', 'DC'),
            ('FL', 'FL'),
            ('GA', 'GA'),
            ('HI', 'HI'),
            ('ID', 'ID'),
            ('IL', 'IL'),
            ('IN', 'IN'),
            ('IA', 'IA'),
            ('KS', 'KS'),
            ('KY', 'KY'),
            ('LA', 'LA'),
            ('ME', 'ME'),
            ('MT', 'MT'),
            ('NE', 'NE'),
            ('NV', 'NV'),
            ('NH', 'NH'),
            ('NJ', 'NJ'),
            ('NM', 'NM'),
            ('NY', 'NY'),
            ('NC', 'NC'),
            ('ND', 'ND'),
            ('OH', 'OH'),
            ('OK', 'OK'),
            ('OR', 'OR'),
            ('MD', 'MD'),
            ('MA', 'MA'),
            ('MI', 'MI'),
            ('MN', 'MN'),
            ('MS', 'MS'),
            ('MO', 'MO'),
            ('PA', 'PA'),
            ('RI', 'RI'),
            ('SC', 'SC'),
            ('SD', 'SD'),
            ('TN', 'TN'),
            ('TX', 'TX'),
            ('UT', 'UT'),
            ('VT', 'VT'),
            ('VA', 'VA'),
            ('WA', 'WA'),
            ('WV', 'WV'),
            ('WI', 'WI'),
            ('WY', 'WY'),
        ]
    )
    phone = StringField(
        'phone', validators=[Length(max=120)]
    )
    image_link = StringField(
        'image_link', validators=[Length(max=500)]
    )
    genres = SelectMultipleField(
        'genres', validators=[DataRequired()],
        choices=[
            ('9', 'Alternative'),
            ('10', 'Blues'),
            ('4', 'Classical'),
            ('11', 'Country'),
            ('12', 'Electronic'),
            ('5', 'Folk'),
            ('13', 'Funk'),
            ('8', 'Hip-Hop'),
            ('14', 'Heavy Metal'),
            ('15', 'Instrumental'),
            ('1', 'Jazz'),
            ('16', 'Musical Theatre'),
            ('17', 'Pop'),
            ('18', 'Punk'),
            ('7', 'R&B'),
            ('2', 'Reggae'),
            ('6', 'Rock n Roll'),
            ('19', 'Soul'),
            ('20', 'Other'),
        ]
     )
    facebook_link = StringField(
        'facebook_link', validators=[URL(), Length(max=120), Optional(strip_whitespace=True)]
     )

    website_link = StringField(
        'website_link', validators=[URL(), Length(max=120), Optional(strip_whitespace=True)]
     )

    seeking_venue = BooleanField('seeking_venue')

    seeking_description = StringField(
            'seeking_description', validators=[Length(max=280)]
     )

