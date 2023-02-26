from appstagesn import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class Entreprise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=False)
    adresse1 = db.Column(db.String(64), index=True, unique=False)
    adresse2 = db.Column(db.String(64), index=True, unique=False)
    CP = db.Column(db.String(5), index=True, unique=False)
    ville = db.Column(db.String(20), index=True, unique=False)
    active = db.Column(db.Boolean, index=True, unique=False)
    phonenumber = db.Column(db.String(10), index=True, unique=False)
    mail = db.Column(db.String(64), index=True, unique=False)
    contact = db.relationship("Contact", backref="entreprise", lazy="dynamic")
    stage = db.relationship("Stage", backref="entreprise", lazy="dynamic")

    # rendezVous = db.relationship('RendezVous', backref='contact', lazy='dynamic')

    def __repr__(self):
        # return '<Entreprise {}>'.format(self.name)
        return f'{self.name}'


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=False)
    firstname = db.Column(db.String(64), index=True, unique=False)
    fonction = db.Column(db.String(40), index=True, unique=False)
    active = db.Column(db.Boolean, index=True, unique=False)
    phonenumber1 = db.Column(db.String(10), index=True, unique=False)
    phonenumber2 = db.Column(db.String(10), index=True, unique=False)
    mail = db.Column(db.String(64),index=True, unique=False)
    entreprise_id = db.Column(db.Integer, db.ForeignKey("entreprise.id"))
    stage = db.relationship("Stage", backref="contact", lazy="dynamic")

    # rendezVous = db.relationship('RendezVous', backref='contact', lazy='dynamic')

    def __repr__(self):
        # return '<Contact {}>'.format(self.name)
        return f'{self.name}'


eleve_classe = db.Table('eleve_classe', db.Column('classe_id', db.Integer, db.ForeignKey('classe.id')),
     db.Column('eleve_id', db.Integer, db.ForeignKey('eleve.id')))


class Eleve(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=False)
    firstname = db.Column(db.String(64), index=True, unique=False)
    phonenumber = db.Column(db.String(10), index=True, unique=False)
    mail1 = db.Column(db.String(64),index=True, unique=False)
    mail2 = db.Column(db.String(64),index=True, unique=False)
    active = db.Column(db.Boolean, index=True, unique=False)
    stage = db.relationship("Stage", backref="eleve", lazy="dynamic")
    promotion_id = db.Column(db.Integer, db.ForeignKey("promotion.id"))
    les_classes = db.relationship('Classe', secondary=eleve_classe, backref='classe')

    def __repr__(self):
        return f'<Eleve {self.name}>'


class Classe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=False)
    promotion_id = db.Column(db.Integer, db.ForeignKey("promotion.id"))
    niveau_id = db.Column(db.Integer, db.ForeignKey("niveau.id"))
    annee_scolaire_id = db.Column(db.Integer, db.ForeignKey("annee_scolaire.id"))

    def __repr__(self):
        return f'<Classe {self.name}>'


class Groupe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=False)
    # TODO modifier le modèle de la Groupe en ajoutant une relation one to many de classe vers eleves
    # promotion_id = db.Column(db.Integer, db.ForeignKey("promotion.id"))
    # niveau_id = db.Column(db.Integer, db.ForeignKey("niveau.id"))
    # annee_scolaire_id = db.Column(db.Integer, db.ForeignKey("annee_scolaire.id"))

    def __repr__(self):
        return f'<Groupe {self.name}>'


prof_classe = db.Table('prof_classes', db.Column('classe_id', db.Integer, db.ForeignKey('classe.id')),
     db.Column('prof_id', db.Integer, db.ForeignKey('professeur.id')))


class Professeur(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    firstname = db.Column(db.String(64))
    ces_classes = db.relationship('Classe', secondary=prof_classe, backref='classes')


class Promotion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=False)
    annee_deb = db.Column(db.Integer)
    annee_fin = db.Column(db.Integer)
    eleve = db.relationship("Eleve", backref="promotion", lazy="dynamic")

    def __repr__(self):
        return f'<Promotion {self.name}>'


class AnneeScolaire(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=False)

    def __repr__(self):
        return f'<Année Scolaire {self.name}>'


class Niveau(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=False)
    stage = db.relationship("Stage", backref="niveau", lazy="dynamic")

    def __repr__(self):
        return f'{self.name}'


class Stage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    eleve_id = db.Column(db.Integer, db.ForeignKey("eleve.id"))
    niveau_id = db.Column(db.Integer, db.ForeignKey("niveau.id"))
    entreprise_id = db.Column(db.Integer, db.ForeignKey("entreprise.id"))
    contact_id = db.Column(db.Integer, db.ForeignKey("contact.id"))
    periode_id = db.Column(db.Integer, db.ForeignKey("date.id"))

    def __repr__(self):
        return f'<Stage {self.id}>'


class Date(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    annee_scolaire = db.Column(db.String(64), index=True, unique=False)
    date_deb1 = db.Column(db.DateTime)
    date_fin1 = db.Column(db.DateTime)
    date_deb2 = db.Column(db.DateTime)
    date_fin2 = db.Column(db.DateTime)
    stage = db.relationship("Stage", backref="periode", lazy="dynamic")

    def __repr__(self):
        return f'{self.annee_scolaire}'

####################################################################################
#   model pour l'authentification des utilisateurs
####################################################################################


class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
