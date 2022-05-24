from flask_wtf import FlaskForm
from wtforms import EmailField, StringField, RadioField, TelField, SelectMultipleField
from wtforms.validators import DataRequired, Email
from grc.utils.form_custom_validators import StrictRequiredIf, validateNationalInsuranceNumber, validatePostcode, validateDateOfTransiton, Integer


class NameForm(FlaskForm):
    title = StringField(
        validators=[DataRequired(message='Enter your title')]
    )

    first_name = StringField(
        validators=[DataRequired(message='Enter your first name(s)')]
    )

    last_name = StringField(
        validators=[DataRequired(message='Enter your last name')]
    )


class AffirmedGenderForm(FlaskForm):
    affirmedGender = RadioField(
        choices=[
            ('MALE', 'Male'),
            ('FEMALE', 'Female')
        ],
        validators=[DataRequired(message='Select your affirmed gender')]
    )


class TransitionDateForm(FlaskForm):
    transition_date_month = StringField(
        validators=[
            DataRequired(message='Enter a month'),
            Integer(min=1, max=12, message='Enter a month as a number between 1 and 12')
        ]
    )

    transition_date_year = StringField(
        validators=[
            DataRequired(message='Enter a year'),
            Integer(min=1000, message='Enter a year as a 4-digit number, like 2000'),
            validateDateOfTransiton
        ]
    )


class PreviousNamesCheck(FlaskForm):
    previousNameCheck = RadioField(
        choices=[
            ('Yes', 'Yes'),
            ('No', 'No')
        ],
        validators=[DataRequired(message='Select if you have ever changed your name to reflect your gender')]
    )


class AddressForm(FlaskForm):
    address_line_one = StringField(
        validators=[DataRequired(message='Enter your address')]
    )

    address_line_two = StringField()  # This field is optional, so has no validators

    town = StringField(
        validators=[DataRequired(message='Enter your town or city')]
    )

    postcode = StringField(
        validators=[DataRequired(message='Enter your postcode'), validatePostcode]
    )


class ContactPreferencesForm(FlaskForm):
    contact_options = SelectMultipleField(
        choices=[
            ('EMAIL', 'Email'),
            ('PHONE', 'Phone call'),
            ('POST', 'Post')
        ],
        validators=[DataRequired(message='Select how would you like to be contacted')]
    )

    email = EmailField(
        validators=[StrictRequiredIf('contact_options', 'EMAIL', message='Enter your email address',
                                     validators=[Email('Enter a valid email address')])]
    )

    phone = TelField(
        validators=[StrictRequiredIf('contact_options', 'PHONE', message='Enter your phone number')]
    )


class ContactDatesForm(FlaskForm):
    contactDatesCheck = RadioField(
        choices=[
            ('Yes', 'Yes'),
            ('No', 'No')
        ],
        validators=[DataRequired(message="Select if you don't want us to contact you at any point in the next 6 months")]
    )

    dates = StringField(
        validators=[StrictRequiredIf('contactDatesCheck', 'Yes', message="Enter the dates you don't want us to contact you by post")]
    )


class HmrcForm(FlaskForm):
    tell_hmrc = RadioField(
        choices=[
            ('Yes', 'Yes'),
            ('No', 'No')
        ],
        validators=[DataRequired(message='Select if you would like us to tell HMRC after you receive a Gender Recognition Certificate')]
    )

    national_insurance_number = StringField(
        validators=[StrictRequiredIf('tell_hmrc', 'Yes', message='Enter your National Insurance number'), validateNationalInsuranceNumber]
    )


class CheckYourAnswers(FlaskForm):
    # There are no fields on the CheckYourAnswers form
    # But, to avoid a compiler error, we need to write 'pass' here
    pass
