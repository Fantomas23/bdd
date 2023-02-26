from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, TimeField, SelectField, BooleanField, PasswordField, SelectMultipleField
from wtforms.validators import DataRequired, Length, Regexp, ValidationError, EqualTo, Email
from datetime import datetime, date
from appstagesn.models import User, Eleve


class NewEntrForm(FlaskForm):
    name = StringField('Nom*', validators=[DataRequired()])
    adresse1 = StringField('Adresse1*', validators=[DataRequired(), Length(min=1, max=40)])
    adresse2 = StringField('Adresse2')
    CP = StringField('Code Postal*',  validators=[DataRequired(), Length(min=1, max=5)])
    ville = StringField('Ville*', validators=[DataRequired(), Length(min=1, max=40)])
    active = BooleanField('En activité', default=True)
    phonenumber = StringField('Numéro de téléphone*', validators=[DataRequired(), Length(min=10, max=10), Regexp(regex="(0[0-9]{9})", message="Format 0XXXXXXXXX")])
    mail = StringField('Adresse Mail')
    submit = SubmitField('Valider')
   # annuler = SubmitField('Annuler')


class SearchEntrForm(FlaskForm):
    name = StringField('Nom')
    CP = StringField('Code Postal')
    ville = StringField('Ville')
    active = BooleanField('En activité', default=True)
    submit = SubmitField('Rechercher')


class NewContactForm(FlaskForm):
    name = StringField('Nom', validators=[DataRequired()])
    firstname = StringField('Prénom')
    # firstname = StringField('Prénom', validators=[DataRequired(), Length(min=1, max=40)])
    fonction = StringField('Fonction')
    # fonction = StringField('Fonction', validators=[Length(min=1, max=40)])
    active = BooleanField('En activité', default=True)
    phonenumber1 = StringField('Téléphone fixe')
    # phonenumber1 = StringField('Téléphone fixe', validators=[Length(min=0, max=10), Regexp(regex="(0[0-9]{9})", message="Format 0XXXXXXXXX")])
    phonenumber2 = StringField('Téléphone portable')
    #phonenumber2 = StringField('Téléphone portable', validators=[Length(min=10, max=10), Regexp(regex="(0[0-9]{9})", message="Format 0XXXXXXXXX")])
    mail = StringField('Adresse Mail')
    entreprise_id = SelectField(u'Entreprise', coerce=int)
    submit = SubmitField('Valider')
    # annuler = SubmitField('Annuler')


class SearchContactForm(FlaskForm):
    name = StringField('Nom')
    firstname = StringField('Prénom')
    active = BooleanField('En activité', default=True)
    phonenumber1 = StringField('Téléphone fixe')
    phonenumber2 = StringField('Téléphone portable')
    mail = StringField('Adresse Mail')
    submit = SubmitField('Valider')


class NewEleveForm(FlaskForm):
    name = StringField('Nom', validators=[DataRequired()])
    firstname = StringField('Prénom', validators=[DataRequired(), Length(min=1, max=40)])
    promotion_id = SelectField(u'Promotion', coerce=int)
    active = BooleanField('En activité', default=True)
    phonenumber = StringField('Téléphone portable', validators=[Length(min=10, max=10), Regexp(regex="(0[0-9]{9})", message="Format 0XXXXXXXXX")])
    mail1 = StringField('Adresse Mail Lycée')
    mail2 = StringField('Adresse Mail perso')
    submit = SubmitField('Valider')


class SearchEleveForm(FlaskForm):
    name = StringField('Nom')
    firstname = StringField('Prénom')
    phonenumber = StringField('Téléphone portable')
    mail2 = StringField('Adresse Mail perso')
    promotion = StringField('Promotion')
    active = BooleanField('En activité', default=True)
    submit = SubmitField('Valider')


class NewPromoForm(FlaskForm):
    name = StringField('Nom', validators=[DataRequired()])
    annee_deb = StringField('Année de début', validators=[DataRequired(), Length(min=4, max=4)])
    annee_fin = StringField('Année de fin', validators=[Length(min=4, max=4)])
    submit = SubmitField('Valider')


class NewNiveauForm(FlaskForm):
    name = StringField('Nom', validators=[DataRequired()])
    submit = SubmitField('Valider')


class NewClasseForm1(FlaskForm):
    promotion = SelectField(u'Promotion', coerce=int)
    niveau = SelectField(u'Niveau', coerce=int)
    annee_scolaire = SelectField(u'Année Scolaire', coerce=int)
    groupe = SelectField(u'Groupe', coerce=int)
    submit = SubmitField('Valider')


class NewClasseForm2(FlaskForm):
    name = StringField('Nom', validators=[DataRequired()])
    submit = SubmitField('Valider')


class EleveToClasseForm(FlaskForm):
    multiselect = SelectMultipleField("Elèves de la promo", coerce=int)
    submit = SubmitField('Valider')

    def __init__(self, *args, **kwargs):
        super(EleveToClasseForm, self).__init__(*args, **kwargs)
        self.multiselect.choices = [(e.id, e.name+" "+e.firstname) for e in (Eleve.query.all())]


class NewStageForm1(FlaskForm):
    annee_scolaire = SelectField(u'Année Scolaire', coerce=int)
    submit = SubmitField('Valider')


class NewStageForm2(FlaskForm):
    nom_eleve = SelectField(u'Nom Eleve', coerce=int)
    # prenom_eleve = SelectField(u'Prénom Eleve', coerce=int)
    niveau = SelectField(u'Niveau', coerce=int)
    entreprise = SelectField(u'Entreprise', coerce=int)
    contact = SelectField(u'Contact', coerce=int)
    periode = SelectField(u'Periode', coerce=int)

    submit = SubmitField('Valider')


#######################################################################################################################
#######################################################################################################################
class NewStageForm3(FlaskForm):
    annee_scolaire = SelectField(u'Année Scolaire', coerce=int)
    promotion = SelectField(u'Promotion', coerce=int)
    niveau = SelectField(u'Niveau', coerce=int)

    submit = SubmitField('Valider')


class NewStageForm4(FlaskForm):
    nom_eleve = SelectField(u'Nom Eleve', coerce=int)
    # prenom_eleve = SelectField(u'Prénom Eleve', coerce=int)
    entreprise = SelectField(u'Entreprise', coerce=int)
    contact = SelectField(u'Contact', coerce=int)
    periode = SelectField(u'Periode', coerce=int)

    submit = SubmitField('Valider')
########################################################################################################################
#######################################################################################################################


class OldStageForm(FlaskForm):
    nom_eleve = StringField(u'Nom Eleve')
    # prenom_eleve = SelectField(u'Prénom Eleve', coerce=int)
    niveau = StringField(u'Niveau')
    entreprise = StringField(u'Entreprise')
    contact = StringField(u'Contact')
    periode = StringField(u'Periode')
    date_deb1 = StringField(u'Date de début')
    date_fin2 = StringField(u'Date de fin')
    submit = SubmitField('Valider')


class NewPeriodeForm(FlaskForm):
    annee_scolaire = StringField('Année scolaire', validators=[DataRequired(), Length(min=9, max=9)])
    date_deb1 = DateField('Date début 1', format='%Y-%m-%d')
    date_fin1 = DateField('Date fin 1', format='%Y-%m-%d')
    date_deb2 = DateField('Date début 2', format='%Y-%m-%d')
    date_fin2 = DateField('Date fin 2', format='%Y-%m-%d')

    submit = SubmitField('Valider')


class NewAnneeScolaireForm(FlaskForm):
    name = StringField('Nom', validators=[DataRequired()])
    submit = SubmitField('Valider')


class RegistrationForm(FlaskForm):
    username = StringField('Login', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    password2 = PasswordField('Répéter le mot de passe', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Enregistrer')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
         raise ValidationError('Please use a different email address.')


class LoginForm(FlaskForm):
    username = StringField('Login', validators=[DataRequired()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    remember_me = BooleanField('Se souvenir de moi')
    submit = SubmitField('Connexion')
