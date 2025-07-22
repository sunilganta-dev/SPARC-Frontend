from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, TextAreaField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, Optional, Email

class UserProfileForm(FlaskForm):
    # Basic Information
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[DataRequired(), Length(min=10, max=15)])
    age = IntegerField('Age', validators=[DataRequired(), NumberRange(min=18, max=120)])
    gender = SelectField('Gender', choices=[('male', 'Male'), ('female', 'Female')])
    height = IntegerField('Height (cm)', validators=[DataRequired(), NumberRange(min=120, max=220)])
    
    # Location
    city = StringField('City', validators=[DataRequired(), Length(max=100)])
    state = StringField('State/Province', validators=[Optional(), Length(max=100)])
    country = StringField('Country', validators=[DataRequired(), Length(max=100)])
    
    # Religious Background
    religious_level = SelectField('Religious Level', choices=[
        ('secular', 'Secular/Hiloni'),
        ('traditional', 'Traditional/Masorti'),
        ('modern_orthodox', 'Modern Orthodox/Dati'),
        ('yeshivish', 'Yeshivish'),
        ('hassidic', 'Hassidic/Hasidi'),
        ('other', 'Other')
    ])
    
    kosher_level = SelectField('Kosher Level', choices=[
        ('strict', 'Strictly Kosher'),
        ('kosher_out', 'Kosher at home, Not Strict Outside'),
        ('vegetarian', 'Vegetarian'),
        ('not_strict', 'Not Strict on Kosher')
    ])
    
    shabbat_observance = SelectField('Shabbat Observance', choices=[
        ('strict', 'Strictly Observant'),
        ('partial', 'Partially Observant'),
        ('not_observant', 'Not Observant')
    ])
    
    # Cultural Background
    background = StringField('Cultural Background', 
                           validators=[Optional(), Length(max=200)],
                           description='e.g., Ashkenazi, Sephardi, etc.')
    
    languages = StringField('Languages Spoken', validators=[Optional(), Length(max=200)])
    
    # Education & Career
    education = SelectField('Highest Education', choices=[
        ('high_school', 'High School'),
        ('associates', 'Associate\'s Degree'),
        ('bachelors', 'Bachelor\'s Degree'),
        ('masters', 'Master\'s Degree'),
        ('doctorate', 'Doctorate/PhD'),
        ('rabbinical', 'Rabbinical Studies'),
        ('other', 'Other')
    ])
    
    occupation = StringField('Occupation', validators=[Optional(), Length(max=100)])
    
    # Family Plans
    wants_children = SelectField('Wants Children', choices=[
        ('yes', 'Yes'),
        ('no', 'No'),
        ('undecided', 'Undecided')
    ])
    
    # Additional Information
    hobbies = TextAreaField('Hobbies & Interests', validators=[Optional(), Length(max=500)])
    additional_info = TextAreaField('Additional Information', validators=[Optional(), Length(max=1000)])
    
    # Preferences for Match
    age_range_min = IntegerField('Minimum Age Preference', 
                                validators=[Optional(), NumberRange(min=18, max=120)])
    age_range_max = IntegerField('Maximum Age Preference', 
                                validators=[Optional(), NumberRange(min=18, max=120)])
    
    height_preference_min = IntegerField('Minimum Height Preference (cm)', 
                                       validators=[Optional(), NumberRange(min=120, max=220)])
    height_preference_max = IntegerField('Maximum Height Preference (cm)', 
                                       validators=[Optional(), NumberRange(min=120, max=220)])
    
    religious_preference = SelectField('Religious Level Preference', choices=[
        ('secular', 'Secular/Hiloni'),
        ('traditional', 'Traditional/Masorti'),
        ('modern_orthodox', 'Modern Orthodox/Dati'),
        ('yeshivish', 'Yeshivish'),
        ('hassidic', 'Hassidic/Hasidi'),
        ('any', 'Any'),
        ('other', 'Other')
    ])
    
    location_preference = StringField('Location Preference', validators=[Optional(), Length(max=200)])
    
    submit = SubmitField('Save Profile') 