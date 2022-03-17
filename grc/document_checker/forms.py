from flask_wtf import FlaskForm
from wtforms import EmailField, StringField, SubmitField, RadioField, TelField
from wtforms.validators import DataRequired, Email
from grc.utils.form_custom_validators import StrictRequiredIf
from grc.utils.from_widgets import MultiCheckboxField

class PreviousNamesCheck(FlaskForm):
    check = RadioField('check', choices=[('Yes'),('No')], validators=[DataRequired(message='Select if you have ever changed your name')])
    submit = SubmitField('Save and continue')

class MarriageCivilPartnershipForm(FlaskForm):
    check = RadioField('check', choices=[('Married'),('Civil partnership'),("Neither")], validators=[DataRequired(message='Select if you are currently married or in a civil partnership')])
    submit = SubmitField('Save and continue')

class StayTogetherForm(FlaskForm):
    check = RadioField('check', choices=[('Yes'),('No')], validators=[DataRequired(message='Select if you you plan to remain married after receiving your Gender Recognition Certificate')])
    submit = SubmitField('Save and continue')

class PartnerAgreesForm(FlaskForm):
    check = RadioField('check', choices=[('Yes'),('No')], validators=[DataRequired(message='Select if you can provide a declaration of consent from your spouse')])
    submit = SubmitField('Save and continue')

class PartnerDiedForm(FlaskForm):
    check = RadioField('check', choices=[('Yes'),('No')], validators=[DataRequired(message='Select if you were previously married or in a civil partnership, but your spouse or partner has died')])
    submit = SubmitField('Save and continue')

class EndedCheckForm(FlaskForm):
    check = RadioField('check', choices=[('Yes'),('No')], validators=[DataRequired(message='Select if you have ever been married or in a civil partnership that has now ended')])
    submit = SubmitField('Save and continue')

class InterimCheckForm(FlaskForm):
    submit = SubmitField('Save and continue')

class OverseasApprovedCheckForm(FlaskForm):
    check = RadioField('check', choices=[('Yes'),('No')], validators=[DataRequired(message='Select if you have official documentation')])
    submit = SubmitField('Continue')