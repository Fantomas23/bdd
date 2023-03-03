from flask import render_template, flash, redirect, url_for, make_response, send_file, request
from appstagesn.forms import NewEntrForm, NewContactForm, NewEleveForm, NewPromoForm, NewNiveauForm, NewStageForm1, \
    NewStageForm2, NewPeriodeForm, NewAnneeScolaireForm, SearchEntrForm, SearchContactForm, SearchEleveForm, RegistrationForm, \
    LoginForm, OldStageForm, NewStageForm3, NewStageForm4, NewClasseForm1, EleveToClasseForm
from appstagesn.models import Entreprise, Contact, Eleve, Classe, Professeur, Promotion, Niveau, Stage, Date, \
    AnneeScolaire, User
from flask_login import current_user, login_user, logout_user, login_required
from datetime import datetime

from appstagesn import app, db
from werkzeug.utils import secure_filename

# import pandas as pd
import pdfkit
import requests
import csv
import os



@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Login ou mot de passe invalide !')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))



@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', title='Home')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Félicitations, vous êtes enregistré(e) !')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)



@app.route('/entreprise/')
@login_required
def home_entr():
    entreprises = Entreprise.query.order_by(Entreprise.name).all()
    return render_template('home_entreprise.html', title='Home Entreprise', entreprises=entreprises)


@app.route('/newentr/', methods=['GET', 'POST'])
@login_required
def new_entr():
    form = NewEntrForm()
    if form.validate_on_submit():
        oldentr = Entreprise.query.filter_by(name=form.name.data).first()
        if oldentr:
            flash(f'{form.name.data.capitalize()} est déjà présent dans votre base de données !')
            return redirect(url_for('newentr'))
        entreprise = Entreprise(name=form.name.data.capitalize(), adresse1=form.adresse1.data,
                                adresse2=form.adresse2.data, CP=form.CP.data, ville=form.ville.data.upper(),
                                active=form.active.data, phonenumber=form.phonenumber.data,
                                mail=form.mail.data)
        db.session.add(entreprise)
        db.session.commit()
        flash(f'Entreprise :  {form.name.data.capitalize()} ajoutée !')
        return redirect(url_for('home_entr'))
    return render_template('newentreprise.html', title='Nouvelle entreprise', form=form)



@app.route('/delentreprise<entreprise_id>/<confirm>', methods=['GET', 'POST'])
@login_required
def delentreprise(entreprise_id, confirm):
    if confirm == '0':
        print("confirmation effacement")
        entreprise = Entreprise.query.get(entreprise_id)
        return render_template('conf_del_entreprise.html', title='Confirmation effacement entreprise', \
                               entreprise=entreprise)
    else:
        delentreprise = Entreprise.query.get(entreprise_id)
        db.session.delete(delentreprise)
        db.session.commit()
        flash(f'Entreprise supprimée !')
        return redirect(url_for('home_entr'))



@app.route('/updatentreprise/<entreprise_id>', methods=['GET', 'POST'])
@login_required
def updatentreprise(entreprise_id):
    oldentreprise = Entreprise.query.get(entreprise_id)
    form = NewEntrForm(obj=oldentreprise, name=oldentreprise.name)

    if form.validate_on_submit():
        oldentreprise.name = form.name.data.capitalize()
        oldentreprise.adresse1 = form.adresse1.data
        oldentreprise.adresse2 = form.adresse2.data
        oldentreprise.CP = form.CP.data
        oldentreprise.ville = form.ville.data.upper()
        oldentreprise.active = form.active.data
        oldentreprise.phonenumber = form.phonenumber.data
        oldentreprise.mail = form.mail.data
        db.session.add(oldentreprise)
        db.session.commit()
        flash(f'Entreprise {form.name.data.capitalize()} modifié !')
        return redirect(url_for('home_entr'))
    return render_template('updatentreprise.html', title='Modification contact', form=form, entreprise_id=entreprise_id)



@app.route('/entreprise/<entreprise_id>')
@login_required
def details_entr(entreprise_id):
    entreprise = Entreprise.query.get(entreprise_id)
    return render_template('details_entreprise.html', title='Details Entreprise', entreprise=entreprise)



@app.route('/entreprise/search/', methods=['GET', 'POST'])
@login_required
def search_entreprise():
    # entreprises = Entreprise.query.order_by(Entreprise.name).all()
    form = SearchEntrForm()
    if form.validate_on_submit():
        if form.name.data and form.CP.data and form.ville.data and form.active.data:
            entreprises = Entreprise.query.filter_by(name=form.name.data.capitalize(), CP=form.CP.data,
                                                     ville=form.ville.data.upper(), active=form.active.data)
        elif form.name.data and form.CP.data and form.ville.data and not form.active.data:
            entreprises = Entreprise.query.filter_by(name=form.name.data.capitalize(), CP=form.CP.data,
                                                     ville=form.ville.data.upper())

        elif form.name.data and form.CP.data and not form.ville.data and form.active.data:
            entreprises = Entreprise.query.filter_by(name=form.name.data.capitalize(), CP=form.CP.data,
                                                     active=form.active.data)
        elif form.name.data and form.CP.data and not form.ville.data and form.active.data:
            entreprises = Entreprise.query.filter_by(name=form.name.data.capitalize(), CP=form.CP.data)

        elif form.name.data and not form.CP.data and form.ville.data and form.active.data:
            entreprises = Entreprise.query.filter_by(name=form.name.data.capitalize(), ville=form.ville.data.upper(),
                                                     active=form.active.data)
        elif form.name.data and not form.CP.data and form.ville.data and not form.active.data:
            entreprises = Entreprise.query.filter_by(name=form.name.data.capitalize(), ville=form.ville.data.upper())

        elif not form.name.data and form.CP.data and form.ville.data and form.active.data:
            entreprises = Entreprise.query.filter_by(CP=form.CP.data, ville=form.ville.data.upper(),
                                                     active=form.active.data)
        elif not form.name.data and form.CP.data and form.ville.data and not form.active.data:
            entreprises = Entreprise.query.filter_by(CP=form.CP.data, ville=form.ville.data.upper())

        elif form.name.data and not form.CP.data and not form.ville.data and form.active.data:
            entreprises = Entreprise.query.filter_by(name=form.name.data.capitalize(), active=form.active.data)
        elif form.name.data and not form.CP.data and not form.ville.data and form.active.data:
            entreprises = Entreprise.query.filter_by(name=form.name.data.capitalize())

        elif not form.name.data and form.CP.data and not form.ville.data and form.active.data:
            entreprises = Entreprise.query.filter_by(CP=form.CP.data, active=form.active.data)
        elif not form.name.data and form.CP.data and not form.ville.data and not form.active.data:
            entreprises = Entreprise.query.filter_by(CP=form.CP.data)

        elif not form.name.data and not form.CP.data and form.ville.data and form.active.data:
            entreprises = Entreprise.query.filter_by(ville=form.ville.data.upper(), active=form.active.data)
        elif not form.name.data and not form.CP.data and form.ville.data and not form.active.data:
            entreprises = Entreprise.query.filter_by(ville=form.ville.data.upper())

        else:
            flash(f'Aucune entreprise ne correspond aux critères recherchés !')
            return redirect(url_for('home_entr'))
        return render_template('resultSearchEntr.html', title='Résultat recherche entreprise', entreprises=entreprises)
    return render_template('searchEntreprise.html', title='Search Entreprise', form=form)



@app.route('/contact/')
@login_required
def home_contacts():
    contacts = Contact.query.order_by(Contact.name).all()
    return render_template('home_contact.html', title='Home Contact', contacts=contacts)



@app.route('/newcontact/', methods=['GET', 'POST'])
@login_required
def new_contact():
    list_entreprises = [(e.id, e.name) for e in Entreprise.query.order_by(Entreprise.name).all()]
    form = NewContactForm()
    form.entreprise_id.choices = list_entreprises
    if form.validate_on_submit():
        oldcontact = Contact.query.filter_by(name=form.name.data).first()
        if oldcontact:
            flash(
                f'{form.name.data.upper()} {form.firstname.data.capitalize()} est déjà présent dans votre base de données !')
            return redirect(url_for('newentr'))
        contact = Contact(name=form.name.data.upper(), firstname=form.firstname.data.capitalize(),
                          fonction=form.fonction.data, active=form.active.data, phonenumber1=form.phonenumber1.data,
                          phonenumber2=form.phonenumber2.data, mail=form.mail.data,
                          entreprise_id=form.entreprise_id.data)
        print(form.entreprise_id.data)
        db.session.add(contact)
        db.session.commit()
        flash(f'Contact :  {form.name.data.capitalize()} ajoutée !')
        return redirect(url_for('home_contacts'))
    return render_template('newcontact.html', title='Nouveau contact', form=form)


@app.route('/delcontact<contact_id>/<confirm>', methods=['GET', 'POST'])
@login_required
def delcontact(contact_id, confirm):
    print(f"confirm = {confirm}")
    if confirm == '0':
        print("confirmation effacement")
        delcontact = Contact.query.get(contact_id)
        return render_template('conf_del_contact.html', title='Confirmation effacement contact', contact=delcontact)
    else:
        delcontact = Contact.query.get(contact_id)
        db.session.delete(delcontact)
        db.session.commit()
        flash(f'Contact supprimée !')
        return redirect(url_for('home_contacts'))


@app.route('/updatecontact/<contact_id>', methods=['GET', 'POST'])
@login_required
def updatecontact(contact_id):
    list_entreprises = [(e.id, e.name) for e in Entreprise.query.order_by(Entreprise.name).all()]
    oldcontact = Contact.query.get(contact_id)
    form = NewContactForm(obj=oldcontact, name=oldcontact.name)
    form.entreprise_id.choices = list_entreprises
    if form.validate_on_submit():
        # if form.annuler.data:
        #     return redirect(url_for('home_contacts'))
        # else:
        oldcontact.name = form.name.data.upper()
        oldcontact.firstname = form.firstname.data.capitalize()
        oldcontact.fonction = form.fonction.data
        oldcontact.active = form.active.data
        oldcontact.phonenumber1 = form.phonenumber1.data
        oldcontact.phonenumber2 = form.phonenumber2.data
        oldcontact.mail = form.mail.data
        oldcontact.entreprise_id = form.entreprise_id.data
        db.session.add(oldcontact)
        db.session.commit()
        flash(f'Contact {form.name.data.upper()} {form.firstname.data.capitalize()} modifié !')
        return redirect(url_for('home_contacts'))
    return render_template('updatecontact.html', title='Modification contact', form=form, contact_id=contact_id)


@app.route('/contact/<contact_id>')
@login_required
def details_contact(contact_id):
    contact = Contact.query.get(contact_id)
    return render_template('details_contact.html', title='Details contact', contact=contact)



@app.route('/contacts/<entreprise_id>')
@login_required
def entr_contacts(entreprise_id):
    contacts = Contact.query.filter_by(entreprise_id=entreprise_id)
    entreprise = Entreprise.query.get(entreprise_id)
    return render_template('home_contact.html', title='Entreprise', contacts=contacts, entreprise=entreprise)



@app.route('/contact/search/', methods=['GET', 'POST'])
@login_required
def search_contact():
    # entreprises = Entreprise.query.order_by(Entreprise.name).all()
    form = SearchContactForm()
    if form.validate_on_submit():
        if form.name.data and form.firstname.data and form.phonenumber1.data and form.phonenumber2.data and form.mail.data and form.active.data:
            contacts = Contact.query.filter_by(name=form.name.data.upper(), firstname=form.firstname.data.capitalize(),
                                               phonenumber1=form.phonenumber1.data, phonenumber2=form.phonenumber2.data,
                                               mail=form.mail.data, active=form.active.data)
        elif form.name.data and form.firstname.data and form.phonenumber1.data and form.phonenumber2.data and form.mail.data and not form.active.data:
            contacts = Contact.query.filter_by(name=form.name.data.upper(), firstname=form.firstname.data.capitalize(),
                                               phonenumber1=form.phonenumber1.data, phonenumber2=form.phonenumber2.data,
                                               mail=form.mail.data)
        elif form.name.data and form.firstname.data and form.phonenumber1.data and form.phonenumber2.data and not form.mail.data and form.active.data:
            contacts = Contact.query.filter_by(name=form.name.data.upper(), firstname=form.firstname.data.capitalize(),
                                               phonenumber1=form.phonenumber1.data, phonenumber2=form.phonenumber2.data,
                                               active=form.active.data)
        elif form.name.data and form.firstname.data and form.phonenumber1.data and form.phonenumber2.data and not form.mail.data and not form.active.data:
            contacts = Contact.query.filter_by(name=form.name.data.upper(), firstname=form.firstname.data.capitalize(),
                                               phonenumber1=form.phonenumber1.data, phonenumber2=form.phonenumber2.data)
        elif form.name.data and form.firstname.data and form.phonenumber1.data and not form.phonenumber2.data and form.mail.data and form.active.data:
            contacts = Contact.query.filter_by(name=form.name.data.upper(), firstname=form.firstname.data.capitalize(),
                                               phonenumber1=form.phonenumber1.data, mail=form.mail.data,
                                               active=form.active.data)
        elif form.name.data and form.firstname.data and form.phonenumber1.data and not form.phonenumber2.data and form.mail.data and not form.active.data:
            contacts = Contact.query.filter_by(name=form.name.data.upper(), firstname=form.firstname.data.capitalize(),
                                               phonenumber1=form.phonenumber1.data, mail=form.mail.data)
        elif form.name.data and form.firstname.data and form.phonenumber1.data and not form.phonenumber2.data and not form.mail.data and form.active.data:
            contacts = Contact.query.filter_by(name=form.name.data.upper(), firstname=form.firstname.data.capitalize(),
                                               phonenumber1=form.phonenumber1.data, active=form.active.data)
        elif form.name.data and form.firstname.data and form.phonenumber1.data and not form.phonenumber2.data and not form.mail.data and not form.active.data:
            contacts = Contact.query.filter_by(name=form.name.data.upper(), firstname=form.firstname.data.capitalize(),
                                               phonenumber1=form.phonenumber1.data)
        elif form.name.data and form.firstname.data and not form.phonenumber1.data and form.phonenumber2.data and form.mail.data and form.active.data:
            contacts = Contact.query.filter_by(name=form.name.data.upper(), firstname=form.firstname.data.capitalize(),
                                               phonenumber2=form.phonenumber2.data, mail=form.mail.data,
                                               active=form.active.data)
        elif form.name.data and form.firstname.data and not form.phonenumber1.data and form.phonenumber2.data and form.mail.data and not form.active.data:
            contacts = Contact.query.filter_by(name=form.name.data.upper(), firstname=form.firstname.data.capitalize(),
                                               phonenumber2=form.phonenumber2.data, mail=form.mail.data)
        elif form.name.data and form.firstname.data and not form.phonenumber1.data and form.phonenumber2.data and not form.mail.data and form.active.data:
            contacts = Contact.query.filter_by(name=form.name.data.upper(), firstname=form.firstname.data.capitalize(),
                                               phonenumber2=form.phonenumber2.data, active=form.active.data)
        elif form.name.data and form.firstname.data and not form.phonenumber1.data and form.phonenumber2.data and not form.mail.data and not form.active.data:
            contacts = Contact.query.filter_by(name=form.name.data.upper(), firstname=form.firstname.data.capitalize(),
                                               phonenumber2=form.phonenumber2.data)
        elif form.name.data and form.firstname.data and not form.phonenumber1.data and not form.phonenumber2.data and form.mail.data and form.active.data:
            contacts = Contact.query.filter_by(name=form.name.data.upper(), firstname=form.firstname.data.capitalize(),
                                               mail=form.mail.data, active=form.active.data)
        elif form.name.data and form.firstname.data and not form.phonenumber1.data and not form.phonenumber2.data and form.mail.data and not form.active.data:
            contacts = Contact.query.filter_by(name=form.name.data.upper(), firstname=form.firstname.data.capitalize(),
                                               mail=form.mail.data)
        elif form.name.data and form.firstname.data and not form.phonenumber1.data and not form.phonenumber2.data and not form.mail.data and form.active.data:
            contacts = Contact.query.filter_by(name=form.name.data.upper(), firstname=form.firstname.data.capitalize(),
                                               active=form.active.data)
        elif form.name.data and form.firstname.data and not form.phonenumber1.data and not form.phonenumber2.data and not form.mail.data and not form.active.data:
            contacts = Contact.query.filter_by(name=form.name.data.upper(), firstname=form.firstname.data.capitalize())
        elif form.name.data and not form.firstname.data and form.phonenumber1.data and form.phonenumber2.data and form.mail.data and form.active.data:
            contacts = Contact.query.filter_by(name=form.name.data.upper(), phonenumber1=form.phonenumber1.data,
                                               phonenumber2=form.phonenumber2.data, mail=form.mail.data,
                                               active=form.active.data)
        elif form.name.data and not form.firstname.data and form.phonenumber1.data and form.phonenumber2.data and form.mail.data and not form.active.data:
            contacts = Contact.query.filter_by(name=form.name.data.upper(), phonenumber1=form.phonenumber1.data,
                                               phonenumber2=form.phonenumber2.data, mail=form.mail.data)
        elif form.name.data and not form.firstname.data and form.phonenumber1.data and form.phonenumber2.data and not form.mail.data and form.active.data:
            contacts = Contact.query.filter_by(name=form.name.data.upper(), phonenumber1=form.phonenumber1.data,
                                               phonenumber2=form.phonenumber2.data, active=form.active.data)
        elif form.name.data and not form.firstname.data and form.phonenumber1.data and form.phonenumber2.data and not form.mail.data and not form.active.data:
            contacts = Contact.query.filter_by(name=form.name.data.upper(), phonenumber1=form.phonenumber1.data,
                                               phonenumber2=form.phonenumber2.data)
        elif form.name.data and not form.firstname.data and form.phonenumber1.data and not form.phonenumber2.data and form.mail.data and form.active.data:
            contacts = Contact.query.filter_by(name=form.name.data.upper(), phonenumber1=form.phonenumber1.data,
                                               mail=form.mail.data, active=form.active.data)
        elif form.name.data and not form.firstname.data and form.phonenumber1.data and not form.phonenumber2.data and form.mail.data and not form.active.data:
            contacts = Contact.query.filter_by(name=form.name.data.upper(), phonenumber1=form.phonenumber1.data,
                                               mail=form.mail.data)
        elif form.name.data and not form.firstname.data and form.phonenumber1.data and not form.phonenumber2.data and not form.mail.data and form.active.data:
            contacts = Contact.query.filter_by(name=form.name.data.upper(), phonenumber1=form.phonenumber1.data,
                                               active=form.active.data)
        elif form.name.data and not form.firstname.data and form.phonenumber1.data and not form.phonenumber2.data and not form.mail.data and not form.active.data:
            contacts = Contact.query.filter_by(name=form.name.data.upper(), phonenumber1=form.phonenumber1.data)
        elif form.name.data and not form.firstname.data and not form.phonenumber1.data and form.phonenumber2.data and form.mail.data and form.active.data:
            contacts = Contact.query.filter_by(name=form.name.data.upper(), phonenumber2=form.phonenumber2.data,
                                               mail=form.mail.data, active=form.active.data)
        elif form.name.data and not form.firstname.data and not form.phonenumber1.data and form.phonenumber2.data and form.mail.data and not form.active.data:
            contacts = Contact.query.filter_by(name=form.name.data.upper(), phonenumber2=form.phonenumber2.data,
                                               mail=form.mail.data)
        elif form.name.data and not form.firstname.data and not form.phonenumber1.data and form.phonenumber2.data and not form.mail.data and form.active.data:
            contacts = Contact.query.filter_by(name=form.name.data.upper(), phonenumber2=form.phonenumber2.data,
                                               active=form.active.data)
        elif form.name.data and not form.firstname.data and not form.phonenumber1.data and form.phonenumber2.data and not form.mail.data and not form.active.data:
            contacts = Contact.query.filter_by(name=form.name.data.upper(), phonenumber2=form.phonenumber2.data)
        elif form.name.data and not form.firstname.data and not form.phonenumber1.data and not form.phonenumber2.data and form.mail.data and form.active.data:
            contacts = Contact.query.filter_by(name=form.name.data.upper(), mail=form.mail.data,
                                               active=form.active.data)
        elif form.name.data and not form.firstname.data and not form.phonenumber1.data and not form.phonenumber2.data and form.mail.data and not form.active.data:
            contacts = Contact.query.filter_by(name=form.name.data.upper(), mail=form.mail.data)
        elif form.name.data and not form.firstname.data and not form.phonenumber1.data and not form.phonenumber2.data and not form.mail.data and form.active.data:
            contacts = Contact.query.filter_by(name=form.name.data.upper(), active=form.active.data)
        elif form.name.data and not form.firstname.data and not form.phonenumber1.data and not form.phonenumber2.data and not form.mail.data and not form.active.data:
            contacts = Contact.query.filter_by(name=form.name.data.upper())
        elif not form.name.data and form.firstname.data and form.phonenumber1.data and form.phonenumber2.data and form.mail.data and form.active.data:
            contacts = Contact.query.filter_by(firstname=form.firstname.data.capitalize(),
                                               phonenumber1=form.phonenumber1.data, phonenumber2=form.phonenumber2.data,
                                               mail=form.mail.data, active=form.active.data)
        elif not form.name.data and form.firstname.data and form.phonenumber1.data and form.phonenumber2.data and form.mail.data and not form.active.data:
            contacts = Contact.query.filter_by(firstname=form.firstname.data.capitalize(),
                                               phonenumber1=form.phonenumber1.data, phonenumber2=form.phonenumber2.data,
                                               mail=form.mail.data)
        elif not form.name.data and form.firstname.data and form.phonenumber1.data and form.phonenumber2.data and not form.mail.data and form.active.data:
            contacts = Contact.query.filter_by(firstname=form.firstname.data.capitalize(),
                                               phonenumber1=form.phonenumber1.data, phonenumber2=form.phonenumber2.data,
                                               active=form.active.data)
        elif not form.name.data and form.firstname.data and form.phonenumber1.data and form.phonenumber2.data and not form.mail.data and not form.active.data:
            contacts = Contact.query.filter_by(firstname=form.firstname.data.capitalize(),
                                               phonenumber1=form.phonenumber1.data, phonenumber2=form.phonenumber2.data)
        elif not form.name.data and form.firstname.data and form.phonenumber1.data and not form.phonenumber2.data and form.mail.data and form.active.data:
            contacts = Contact.query.filter_by(firstname=form.firstname.data.capitalize(),
                                               phonenumber1=form.phonenumber1.data, mail=form.mail.data,
                                               active=form.active.data)
        elif not form.name.data and form.firstname.data and form.phonenumber1.data and not form.phonenumber2.data and form.mail.data and not form.active.data:
            contacts = Contact.query.filter_by(firstname=form.firstname.data.capitalize(),
                                               phonenumber1=form.phonenumber1.data, mail=form.mail.data)
        elif not form.name.data and form.firstname.data and form.phonenumber1.data and not form.phonenumber2.data and not form.mail.data and form.active.data:
            contacts = Contact.query.filter_by(firstname=form.firstname.data.capitalize(),
                                               phonenumber1=form.phonenumber1.data, active=form.active.data)
        elif not form.name.data and form.firstname.data and form.phonenumber1.data and not form.phonenumber2.data and not form.mail.data and not form.active.data:
            contacts = Contact.query.filter_by(firstname=form.firstname.data.capitalize(),
                                               phonenumber1=form.phonenumber1.data)
        elif not form.name.data and form.firstname.data and not form.phonenumber1.data and form.phonenumber2.data and form.mail.data and form.active.data:
            contacts = Contact.query.filter_by(firstname=form.firstname.data.capitalize(),
                                               phonenumber2=form.phonenumber2.data, mail=form.mail.data,
                                               active=form.active.data)
        elif not form.name.data and form.firstname.data and not form.phonenumber1.data and form.phonenumber2.data and form.mail.data and not form.active.data:
            contacts = Contact.query.filter_by(firstname=form.firstname.data.capitalize(),
                                               phonenumber2=form.phonenumber2.data, mail=form.mail.data)
        elif not form.name.data and form.firstname.data and not form.phonenumber1.data and form.phonenumber2.data and not form.mail.data and form.active.data:
            contacts = Contact.query.filter_by(firstname=form.firstname.data.capitalize(),
                                               phonenumber2=form.phonenumber2.data, active=form.active.data)
        elif not form.name.data and form.firstname.data and not form.phonenumber1.data and form.phonenumber2.data and not form.mail.data and not form.active.data:
            contacts = Contact.query.filter_by(firstname=form.firstname.data.capitalize(),
                                               phonenumber2=form.phonenumber2.data)
        elif not form.name.data and form.firstname.data and not form.phonenumber1.data and not form.phonenumber2.data and form.mail.data and form.active.data:
            contacts = Contact.query.filter_by(firstname=form.firstname.data.capitalize(), mail=form.mail.data,
                                               active=form.active.data)
        elif not form.name.data and form.firstname.data and not form.phonenumber1.data and not form.phonenumber2.data and form.mail.data and not form.active.data:
            contacts = Contact.query.filter_by(firstname=form.firstname.data.capitalize(), mail=form.mail.data)
        elif not form.name.data and form.firstname.data and not form.phonenumber1.data and not form.phonenumber2.data and not form.mail.data and form.active.data:
            contacts = Contact.query.filter_by(firstname=form.firstname.data.capitalize(), active=form.active.data)
        elif not form.name.data and form.firstname.data and not form.phonenumber1.data and not form.phonenumber2.data and not form.mail.data and not form.active.data:
            contacts = Contact.query.filter_by(firstname=form.firstname.data.capitalize())
        elif not form.name.data and not form.firstname.data and form.phonenumber1.data and form.phonenumber2.data and form.mail.data and form.active.data:
            contacts = Contact.query.filter_by(phonenumber1=form.phonenumber1.data, phonenumber2=form.phonenumber2.data,
                                               mail=form.mail.data, active=form.active.data)
        elif not form.name.data and not form.firstname.data and form.phonenumber1.data and form.phonenumber2.data and form.mail.data and not form.active.data:
            contacts = Contact.query.filter_by(phonenumber1=form.phonenumber1.data, phonenumber2=form.phonenumber2.data,
                                               mail=form.mail.data)
        elif not form.name.data and not form.firstname.data and form.phonenumber1.data and form.phonenumber2.data and not form.mail.data and form.active.data:
            contacts = Contact.query.filter_by(phonenumber1=form.phonenumber1.data, phonenumber2=form.phonenumber2.data,
                                               active=form.active.data)
        elif not form.name.data and not form.firstname.data and form.phonenumber1.data and form.phonenumber2.data and not form.mail.data and not form.active.data:
            contacts = Contact.query.filter_by(phonenumber1=form.phonenumber1.data, phonenumber2=form.phonenumber2.data)
        elif not form.name.data and not form.firstname.data and form.phonenumber1.data and not form.phonenumber2.data and form.mail.data and form.active.data:
            contacts = Contact.query.filter_by(phonenumber1=form.phonenumber1.data, mail=form.mail.data,
                                               active=form.active.data)
        elif not form.name.data and not form.firstname.data and form.phonenumber1.data and not form.phonenumber2.data and form.mail.data and not form.active.data:
            contacts = Contact.query.filter_by(phonenumber1=form.phonenumber1.data, mail=form.mail.data)
        elif not form.name.data and not form.firstname.data and form.phonenumber1.data and not form.phonenumber2.data and not form.mail.data and form.active.data:
            contacts = Contact.query.filter_by(phonenumber1=form.phonenumber1.data, active=form.active.data)
        elif not form.name.data and not form.firstname.data and form.phonenumber1.data and not form.phonenumber2.data and not form.mail.data and not form.active.data:
            contacts = Contact.query.filter_by(phonenumber1=form.phonenumber1.data)
        elif not form.name.data and not form.firstname.data and not form.phonenumber1.data and form.phonenumber2.data and form.mail.data and form.active.data:
            contacts = Contact.query.filter_by(phonenumber2=form.phonenumber2.data, mail=form.mail.data,
                                               active=form.active.data)
        elif not form.name.data and not form.firstname.data and not form.phonenumber1.data and form.phonenumber2.data and form.mail.data and not form.active.data:
            contacts = Contact.query.filter_by(phonenumber2=form.phonenumber2.data, mail=form.mail.data)
        elif not form.name.data and not form.firstname.data and not form.phonenumber1.data and form.phonenumber2.data and not form.mail.data and form.active.data:
            contacts = Contact.query.filter_by(phonenumber2=form.phonenumber2.data, active=form.active.data)
        elif not form.name.data and not form.firstname.data and not form.phonenumber1.data and form.phonenumber2.data and not form.mail.data and not form.active.data:
            contacts = Contact.query.filter_by(phonenumber2=form.phonenumber2.data)
        elif not form.name.data and not form.firstname.data and not form.phonenumber1.data and not form.phonenumber2.data and form.mail.data and form.active.data:
            contacts = Contact.query.filter_by(mail=form.mail.data, active=form.active.data)
        elif not form.name.data and not form.firstname.data and not form.phonenumber1.data and not form.phonenumber2.data and form.mail.data and not form.active.data:
            contacts = Contact.query.filter_by(mail=form.mail.data)
        elif not form.name.data and not form.firstname.data and not form.phonenumber1.data and not form.phonenumber2.data and not form.mail.data and form.active.data:
            contacts = Contact.query.filter_by(active=form.active.data)
        else:
            flash(f'Aucun contact ne correspond aux critères recherchés !')
            return redirect(url_for('home_contacts'))
        return render_template('resultSearchContact.html', title='Résultat recherche contacts', contacts=contacts)
    return render_template('searchContact.html', title='Search Contact', form=form)


@app.route('/eleve/')
@login_required
def home_eleve():
    eleves = Eleve.query.order_by(Eleve.name).all()
    return render_template('home_eleve.html', title='Home Eleve', eleves=eleves)


@app.route('/neweleve/', methods=['GET', 'POST'])
@login_required
def new_eleve():
    list_promos = [(e.id, e.name) for e in Promotion.query.order_by(Promotion.name).all()]
    form = NewEleveForm()
    form.promotion_id.choices = list_promos
    if form.validate_on_submit():
        oldeleve = Eleve.query.filter_by(name=form.name.data).first()
        if oldeleve:
            flash(f'{form.name.data.upper()} {form.firstname.data.capitalize()} '
                  f'est déjà présent dans votre base de données !')
            return redirect(url_for('home_eleves'))
        eleve = Eleve(name=form.name.data.upper(),
                      firstname=form.firstname.data.capitalize(),
                      promotion_id=form.promotion_id.data,
                      # niveau_id=form.niveau.data,
                      active=form.active.data,
                      phonenumber=form.phonenumber.data,
                      mail1=form.mail1.data,
                      mail2=form.mail2.data)

        db.session.add(eleve)
        db.session.commit()
        flash(f'Elève :  {form.name.data.capitalize()} ajouté !')
        return redirect(url_for('home_eleve'))
    return render_template('neweleve.html', title='Nouvel élève', form=form)


@app.route('/deleleve/<eleve_id>/<confirm>', methods=['GET', 'POST'])
@login_required
def deleleve(eleve_id, confirm):
    if confirm == '0':
        deleleve = Eleve.query.get(eleve_id)
        return render_template('conf_del_eleve.html', title='Confirmation effacement eleve', eleve=deleleve)
    else:
        deleleve = Eleve.query.get(eleve_id)
        db.session.delete(deleleve)
        db.session.commit()
        flash(f'Elève supprimé !')
        return redirect(url_for('home_eleve'))


@app.route('/eleve/<eleve_id>')
@login_required
def details_eleve(eleve_id):
    eleve = Eleve.query.get(eleve_id)
    return render_template('details_eleve.html', title='Details eleve', eleve=eleve)



@app.route('/updateleve/<eleve_id>', methods=['GET', 'POST'])
@login_required
def updateleve(eleve_id):
    oldeleve = Eleve.query.get(eleve_id)
    form = NewEleveForm(obj=oldeleve, name=oldeleve.name)
    list_niveaux = [(e.id, e.name) for e in Niveau.query.all()]
    # form.niveau.choices = list_niveaux
    if form.validate_on_submit():
        if form.annuler.data:
            return redirect(url_for('home_eleves'))
        else:
            oldeleve.name = form.name.data.upper()
            oldeleve.firstname = form.firstname.data.capitalize()
            oldeleve.promotion = form.promotion.data
            # oldeleve.classe = list_classes[form.classe.data-1][1]
            # oldeleve.niveau_id = form.niveau.data
            oldeleve.active = form.active.data
            oldeleve.phonenumber = form.phonenumber.data
            oldeleve.mail1 = form.mail1.data
            oldeleve.mail2 = form.mail2.data
            db.session.add(oldeleve)
            db.session.commit()
            flash(f'Eleve {form.name.data.upper()} {form.firstname.data.capitalize()} modifié !')
            return redirect(url_for('home_eleves'))
    return render_template('updateleve.html', title='Modification eleve', form=form, eleve_id=eleve_id)



@app.route('/eleve/search/', methods=['GET', 'POST'])
@login_required
def search_eleve():
    form = SearchEleveForm()
    if form.validate_on_submit():
        if form.name.data and form.firstname.data and form.phonenumber.data and form.promotion.data and form.mail2.data and form.active.data:
            eleves = Eleve.query.filter_by(name=form.name.data.upper(), firstname=form.firstname.data.capitalize(),
                                               phonenumber=form.phonenumber.data, promotion=form.promotion.data,
                                               mail2=form.mail2.data, active=form.active.data)
        elif form.name.data and form.firstname.data and form.phonenumber.data and form.promotion.data and form.mail2.data and not form.active.data:
            eleves = Eleve.query.filter_by(name=form.name.data.upper(), firstname=form.firstname.data.capitalize(),
                                               phonenumber=form.phonenumber.data, promotion=form.promotion.data,
                                               mail2=form.mail2.data)
        elif form.name.data and form.firstname.data and form.phonenumber.data and form.promotion.data and not form.mail2.data and form.active.data:
            eleves = Eleve.query.filter_by(name=form.name.data.upper(), firstname=form.firstname.data.capitalize(),
                                               phonenumber=form.phonenumber.data, promotion=form.promotion.data,
                                               active=form.active.data)
        elif form.name.data and form.firstname.data and form.phonenumber.data and form.promotion.data and not form.mail2.data and not form.active.data:
            eleves = Eleve.query.filter_by(name=form.name.data.upper(), firstname=form.firstname.data.capitalize(),
                                               phonenumber=form.phonenumber.data, promotion=form.promotion.data)
        elif form.name.data and form.firstname.data and form.phonenumber.data and not form.promotion.data and form.mail2.data and form.active.data:
            eleves = Eleve.query.filter_by(name=form.name.data.upper(), firstname=form.firstname.data.capitalize(),
                                               phonenumber=form.phonenumber.data, mail2=form.mail2.data,
                                               active=form.active.data)
        elif form.name.data and form.firstname.data and form.phonenumber.data and not form.promotion.data and form.mail2.data and not form.active.data:
            eleves = Eleve.query.filter_by(name=form.name.data.upper(), firstname=form.firstname.data.capitalize(),
                                               phonenumber=form.phonenumber.data, mail2=form.mail2.data)
        elif form.name.data and form.firstname.data and form.phonenumber.data and not form.promotion.data and not form.mail2.data and form.active.data:
            eleves = Eleve.query.filter_by(name=form.name.data.upper(), firstname=form.firstname.data.capitalize(),
                                               phonenumber=form.phonenumber.data, active=form.active.data)
        elif form.name.data and form.firstname.data and form.phonenumber.data and not form.promotion.data and not form.mail2.data and not form.active.data:
            eleves = Eleve.query.filter_by(name=form.name.data.upper(), firstname=form.firstname.data.capitalize(),
                                               phonenumber=form.phonenumber.data)
        elif form.name.data and form.firstname.data and not form.phonenumber.data and form.promotion.data and form.mail2.data and form.active.data:
            eleves = Eleve.query.filter_by(name=form.name.data.upper(), firstname=form.firstname.data.capitalize(),
                                               promotion=form.promotion.data, mail2=form.mail2.data,
                                               active=form.active.data)
        elif form.name.data and form.firstname.data and not form.phonenumber.data and form.promotion.data and form.mail2.data and not form.active.data:
            eleves = Eleve.query.filter_by(name=form.name.data.upper(), firstname=form.firstname.data.capitalize(),
                                               promotion=form.promotion.data, mail2=form.mail2.data)
        elif form.name.data and form.firstname.data and not form.phonenumber.data and form.promotion.data and not form.mail2.data and form.active.data:
            eleves = Eleve.query.filter_by(name=form.name.data.upper(), firstname=form.firstname.data.capitalize(),
                                               promotion=form.promotion.data, active=form.active.data)
        elif form.name.data and form.firstname.data and not form.phonenumber.data and form.promotion.data and not form.mail2.data and not form.active.data:
            eleves = Eleve.query.filter_by(name=form.name.data.upper(), firstname=form.firstname.data.capitalize(),
                                               promotion=form.promotion.data)
        elif form.name.data and form.firstname.data and not form.phonenumber.data and not form.promotion.data and form.mail2.data and form.active.data:
            eleves = Eleve.query.filter_by(name=form.name.data.upper(), firstname=form.firstname.data.capitalize(),
                                               mail2=form.mail2.data, active=form.active.data)
        elif form.name.data and form.firstname.data and not form.phonenumber.data and not form.promotion.data and form.mail2.data and not form.active.data:
            eleves = Eleve.query.filter_by(name=form.name.data.upper(), firstname=form.firstname.data.capitalize(),
                                               mail2=form.mail2.data)
        elif form.name.data and form.firstname.data and not form.phonenumber.data and not form.promotion.data and not form.mail2.data and form.active.data:
            eleves = Eleve.query.filter_by(name=form.name.data.upper(), firstname=form.firstname.data.capitalize(),
                                               active=form.active.data)
        elif form.name.data and form.firstname.data and not form.phonenumber.data and not form.promotion.data and not form.mail2.data and not form.active.data:
            eleves = Eleve.query.filter_by(name=form.name.data.upper(), firstname=form.firstname.data.capitalize())
        elif form.name.data and not form.firstname.data and form.phonenumber.data and form.promotion.data and form.mail2.data and form.active.data:
            eleves = Eleve.query.filter_by(name=form.name.data.upper(), phonenumber=form.phonenumber.data,
                                               promotion=form.promotion.data, mail2=form.mail2.data,
                                               active=form.active.data)
        elif form.name.data and not form.firstname.data and form.phonenumber.data and form.promotion.data and form.mail2.data and not form.active.data:
            eleves = Eleve.query.filter_by(name=form.name.data.upper(), phonenumber=form.phonenumber.data,
                                               promotion=form.promotion.data, mail2=form.mail2.data)
        elif form.name.data and not form.firstname.data and form.phonenumber.data and form.promotion.data and not form.mail2.data and form.active.data:
            eleves = Eleve.query.filter_by(name=form.name.data.upper(), phonenumber=form.phonenumber.data,
                                               promotion=form.promotion.data, active=form.active.data)
        elif form.name.data and not form.firstname.data and form.phonenumber.data and form.promotion.data and not form.mail2.data and not form.active.data:
            eleves = Eleve.query.filter_by(name=form.name.data.upper(), phonenumber=form.phonenumber.data,
                                               promotion=form.promotion.data)
        elif form.name.data and not form.firstname.data and form.phonenumber.data and not form.promotion.data and form.mail2.data and form.active.data:
            eleves = Eleve.query.filter_by(name=form.name.data.upper(), phonenumber=form.phonenumber.data,
                                               mail2=form.mail2.data, active=form.active.data)
        elif form.name.data and not form.firstname.data and form.phonenumber.data and not form.promotion.data and form.mail2.data and not form.active.data:
            eleves = Eleve.query.filter_by(name=form.name.data.upper(), phonenumber=form.phonenumber.data,
                                               mail2=form.mail2.data)
        elif form.name.data and not form.firstname.data and form.phonenumber.data and not form.promotion.data and not form.mail2.data and form.active.data:
            eleves = Eleve.query.filter_by(name=form.name.data.upper(), phonenumber=form.phonenumber.data,
                                               active=form.active.data)
        elif form.name.data and not form.firstname.data and form.phonenumber.data and not form.promotion.data and not form.mail2.data and not form.active.data:
            eleves = Eleve.query.filter_by(name=form.name.data.upper(), phonenumber=form.phonenumber.data)
        elif form.name.data and not form.firstname.data and not form.phonenumber.data and form.promotion.data and form.mail2.data and form.active.data:
            eleves = Eleve.query.filter_by(name=form.name.data.upper(), promotion=form.promotion.data,
                                               mail2=form.mail2.data, active=form.active.data)
        elif form.name.data and not form.firstname.data and not form.phonenumber.data and form.promotion.data and form.mail2.data and not form.active.data:
            eleves = Eleve.query.filter_by(name=form.name.data.upper(), promotion=form.promotion.data,
                                               mail2=form.mail2.data)
        elif form.name.data and not form.firstname.data and not form.phonenumber.data and form.promotion.data and not form.mail2.data and form.active.data:
            eleves = Eleve.query.filter_by(name=form.name.data.upper(), promotion=form.promotion.data,
                                               active=form.active.data)
        elif form.name.data and not form.firstname.data and not form.phonenumber.data and form.promotion.data and not form.mail2.data and not form.active.data:
            eleves = Eleve.query.filter_by(name=form.name.data.upper(), promotion=form.promotion.data)
        elif form.name.data and not form.firstname.data and not form.phonenumber.data and not form.promotion.data and form.mail2.data and form.active.data:
            eleves = Eleve.query.filter_by(name=form.name.data.upper(), mail2=form.mail2.data,
                                               active=form.active.data)
        elif form.name.data and not form.firstname.data and not form.phonenumber.data and not form.promotion.data and form.mail2.data and not form.active.data:
            eleves = Eleve.query.filter_by(name=form.name.data.upper(), mail2=form.mail2.data)
        elif form.name.data and not form.firstname.data and not form.phonenumber.data and not form.promotion.data and not form.mail2.data and form.active.data:
            eleves = Eleve.query.filter_by(name=form.name.data.upper(), active=form.active.data)
        elif form.name.data and not form.firstname.data and not form.phonenumber.data and not form.promotion.data and not form.mail2.data and not form.active.data:
            eleves = Eleve.query.filter_by(name=form.name.data.upper())
        elif not form.name.data and form.firstname.data and form.phonenumber.data and form.promotion.data and form.mail2.data and form.active.data:
            eleves = Eleve.query.filter_by(firstname=form.firstname.data.capitalize(),
                                               phonenumber=form.phonenumber.data, promotion=form.promotion.data,
                                               mail2=form.mail2.data, active=form.active.data)
        elif not form.name.data and form.firstname.data and form.phonenumber.data and form.promotion.data and form.mail2.data and not form.active.data:
            eleves = Eleve.query.filter_by(firstname=form.firstname.data.capitalize(),
                                               phonenumber=form.phonenumber.data, promotion=form.promotion.data,
                                               mail2=form.mail2.data)
        elif not form.name.data and form.firstname.data and form.phonenumber.data and form.promotion.data and not form.mail2.data and form.active.data:
            eleves = Eleve.query.filter_by(firstname=form.firstname.data.capitalize(),
                                               phonenumber=form.phonenumber.data, promotion=form.promotion.data,
                                               active=form.active.data)
        elif not form.name.data and form.firstname.data and form.phonenumber.data and form.promotion.data and not form.mail2.data and not form.active.data:
            eleves = Eleve.query.filter_by(firstname=form.firstname.data.capitalize(),
                                               phonenumber=form.phonenumber.data, promotion=form.promotion.data)
        elif not form.name.data and form.firstname.data and form.phonenumber.data and not form.promotion.data and form.mail2.data and form.active.data:
            eleves = Eleve.query.filter_by(firstname=form.firstname.data.capitalize(),
                                               phonenumber=form.phonenumber.data, mail2=form.mail2.data,
                                               active=form.active.data)
        elif not form.name.data and form.firstname.data and form.phonenumber.data and not form.promotion.data and form.mail2.data and not form.active.data:
            eleves = Eleve.query.filter_by(firstname=form.firstname.data.capitalize(),
                                               phonenumber=form.phonenumber.data, mail2=form.mail2.data)
        elif not form.name.data and form.firstname.data and form.phonenumber.data and not form.promotion.data and not form.mail2.data and form.active.data:
            eleves = Eleve.query.filter_by(firstname=form.firstname.data.capitalize(),
                                               phonenumber=form.phonenumber.data, active=form.active.data)
        elif not form.name.data and form.firstname.data and form.phonenumber.data and not form.promotion.data and not form.mail2.data and not form.active.data:
            eleves = Eleve.query.filter_by(firstname=form.firstname.data.capitalize(),
                                               phonenumber=form.phonenumber.data)
        elif not form.name.data and form.firstname.data and not form.phonenumber.data and form.promotion.data and form.mail2.data and form.active.data:
            eleves = Eleve.query.filter_by(firstname=form.firstname.data.capitalize(),
                                               promotion=form.promotion.data, mail2=form.mail2.data,
                                               active=form.active.data)
        elif not form.name.data and form.firstname.data and not form.phonenumber.data and form.promotion.data and form.mail2.data and not form.active.data:
            eleves = Eleve.query.filter_by(firstname=form.firstname.data.capitalize(),
                                               promotion=form.promotion.data, mail2=form.mail2.data)
        elif not form.name.data and form.firstname.data and not form.phonenumber.data and form.promotion.data and not form.mail2.data and form.active.data:
            eleves = Eleve.query.filter_by(firstname=form.firstname.data.capitalize(),
                                               promotion=form.promotion.data, active=form.active.data)
        elif not form.name.data and form.firstname.data and not form.phonenumber.data and form.promotion.data and not form.mail2.data and not form.active.data:
            eleves = Eleve.query.filter_by(firstname=form.firstname.data.capitalize(),
                                               promotion=form.promotion.data)
        elif not form.name.data and form.firstname.data and not form.phonenumber.data and not form.promotion.data and form.mail2.data and form.active.data:
            eleves = Eleve.query.filter_by(firstname=form.firstname.data.capitalize(), mail2=form.mail2.data,
                                               active=form.active.data)
        elif not form.name.data and form.firstname.data and not form.phonenumber.data and not form.promotion.data and form.mail2.data and not form.active.data:
            eleves = Eleve.query.filter_by(firstname=form.firstname.data.capitalize(), mail2=form.mail2.data)
        elif not form.name.data and form.firstname.data and not form.phonenumber.data and not form.promotion.data and not form.mail2.data and form.active.data:
            eleves = Eleve.query.filter_by(firstname=form.firstname.data.capitalize(), active=form.active.data)
        elif not form.name.data and form.firstname.data and not form.phonenumber.data and not form.promotion.data and not form.mail2.data and not form.active.data:
            eleves = Eleve.query.filter_by(firstname=form.firstname.data.capitalize())
        elif not form.name.data and not form.firstname.data and form.phonenumber.data and form.promotion.data and form.mail2.data and form.active.data:
            eleves = Eleve.query.filter_by(phonenumber=form.phonenumber.data, promotion=form.promotion.data,
                                               mail2=form.mail2.data, active=form.active.data)
        elif not form.name.data and not form.firstname.data and form.phonenumber.data and form.promotion.data and form.mail2.data and not form.active.data:
            eleves = Eleve.query.filter_by(phonenumber=form.phonenumber.data, promotion=form.promotion.data,
                                               mail2=form.mail2.data)
        elif not form.name.data and not form.firstname.data and form.phonenumber.data and form.promotion.data and not form.mail2.data and form.active.data:
            eleves = Eleve.query.filter_by(phonenumber=form.phonenumber.data, promotion=form.promotion.data,
                                               active=form.active.data)
        elif not form.name.data and not form.firstname.data and form.phonenumber.data and form.promotion.data and not form.mail2.data and not form.active.data:
            eleves = Eleve.query.filter_by(phonenumber=form.phonenumber.data, promotion=form.promotion.data)
        elif not form.name.data and not form.firstname.data and form.phonenumber.data and not form.promotion.data and form.mail2.data and form.active.data:
            eleves = Eleve.query.filter_by(phonenumber=form.phonenumber.data, mail2=form.mail2.data,
                                               active=form.active.data)
        elif not form.name.data and not form.firstname.data and form.phonenumber.data and not form.promotion.data and form.mail2.data and not form.active.data:
            eleves = Eleve.query.filter_by(phonenumber=form.phonenumber.data, mail2=form.mail2.data)
        elif not form.name.data and not form.firstname.data and form.phonenumber.data and not form.promotion.data and not form.mail2.data and form.active.data:
            eleves = Eleve.query.filter_by(phonenumber=form.phonenumber.data, active=form.active.data)
        elif not form.name.data and not form.firstname.data and form.phonenumber.data and not form.promotion.data and not form.mail2.data and not form.active.data:
            eleves = Eleve.query.filter_by(phonenumber=form.phonenumber.data)
        elif not form.name.data and not form.firstname.data and not form.phonenumber.data and form.promotion.data and form.mail2.data and form.active.data:
            eleves = Eleve.query.filter_by(promotion=form.promotion.data, mail2=form.mail2.data,
                                               active=form.active.data)
        elif not form.name.data and not form.firstname.data and not form.phonenumber.data and form.promotion.data and form.mail2.data and not form.active.data:
            eleves = Eleve.query.filter_by(promotion=form.promotion.data, mail2=form.mail2.data)
        elif not form.name.data and not form.firstname.data and not form.phonenumber.data and form.promotion.data and not form.mail2.data and form.active.data:
            eleves = Eleve.query.filter_by(promotion=form.promotion.data, active=form.active.data)
        elif not form.name.data and not form.firstname.data and not form.phonenumber.data and form.promotion.data and not form.mail2.data and not form.active.data:
            eleves = Eleve.query.filter_by(promotion=form.promotion.data)
        elif not form.name.data and not form.firstname.data and not form.phonenumber.data and not form.promotion.data and form.mail2.data and form.active.data:
            eleves = Eleve.query.filter_by(mail2=form.mail2.data, active=form.active.data)
        elif not form.name.data and not form.firstname.data and not form.phonenumber.data and not form.promotion.data and form.mail2.data and not form.active.data:
            eleves = Eleve.query.filter_by(mail2=form.mail2.data)
        elif not form.name.data and not form.firstname.data and not form.phonenumber.data and not form.promotion.data and not form.mail2.data and form.active.data:
            eleves = Eleve.query.filter_by(active=form.active.data)
        else:
            flash(f'Aucun élève ne correspond aux critères recherchés !')
            return redirect(url_for('home_eleve'))
        return render_template('resultSearchEleve.html', title='Résultat recherche élève', eleves=eleves)
    return render_template('searchEleve.html', title='Search Eleve', form=form)


@app.route('/classe/<classe>')
@login_required
def details_classe(classe):
    eleves = Eleve.query.filter_by(classe_id=classe).order_by(Eleve.name)
    classe = Classe.query.get(classe)
    profs = Professeur.query.filter(Professeur.ces_classes.any(id=classe.id)).all()
    return render_template('details_classe.html', title='Details classe', classe=classe, eleves=eleves, profs=profs)


@app.route('/promotion/')
@login_required
def home_promo():
    promotions = Promotion.query.order_by(Promotion.name).all()
    return render_template('home_promotion.html', title='Home Promotion', promotions=promotions)


@app.route('/newpromo/', methods=['GET', 'POST'])
@login_required
def new_promo():
    form = NewPromoForm()
    if form.validate_on_submit():
        oldpromo = Promotion.query.filter_by(name=form.name.data).first()
        if oldpromo:
            flash(f'{form.name.data.upper()} '
                  f'est déjà présente dans votre base de données !')
            return redirect(url_for('home_promo'))
        promo = Promotion(name=form.name.data.upper(),
                          annee_deb=form.annee_deb.data,
                          annee_fin=form.annee_fin.data)
        db.session.add(promo)
        db.session.commit()
        flash(f'Promotion :  {form.name.data.capitalize()} ajouté !')
        return redirect(url_for('home_promo'))
    return render_template('newpromo.html', title='Nouvelle promotion', form=form)


@app.route('/delpromo/<promo_id>/<confirm>', methods=['GET', 'POST'])
@login_required
def delpromo(promo_id, confirm):
    if confirm == '0':
        delpromo = Promotion.query.get(promo_id)
        return render_template('conf_del_promo.html', title='Confirmation effacement promotion', promo=delpromo)
    else:
        delpromo = Promotion.query.get(promo_id)
        db.session.delete(delpromo)
        db.session.commit()
        flash(f'Promotion supprimée !')
        return redirect(url_for('home_promo'))


@app.route('/updatepromo/<promo_id>', methods=['GET', 'POST'])
@login_required
def update_promo(promo_id):
    oldpromo = Promotion.query.get(promo_id)
    form = NewPromoForm(obj=oldpromo, name=oldpromo.name)
    if form.validate_on_submit():
        oldpromo.name = form.name.data.upper()
        oldpromo.annee_deb = form.annee_deb.data
        oldpromo.annee_fin = form.annee_fin.data
        db.session.add(oldpromo)
        db.session.commit()
        flash(f'Promotion {form.name.data.upper()}  modifiée !')
        return redirect(url_for('home_promo'))
    return render_template('updatepromo.html', title='Modification promo', form=form, promo_id=promo_id)


@app.route('/niveau/')
@login_required
def home_niveau():
    niveaux = Niveau.query.order_by(Niveau.name).all()
    return render_template('home_niveau.html', title='Home Niveau', niveaux=niveaux)


@app.route('/newniveau/', methods=['GET', 'POST'])
@login_required
def new_niveau():
    form = NewNiveauForm()
    if form.validate_on_submit():
        oldniveau = Niveau.query.filter_by(name=form.name.data).first()
        if oldniveau:
            flash(f'{form.name.data.upper()} '
                  f'est déjà présent dans votre base de données !')
            return redirect(url_for('home_niveau'))
        niveau = Niveau(name=form.name.data.upper())
        db.session.add(niveau)
        db.session.commit()
        flash(f'Niveau :  {form.name.data.capitalize()} ajouté !')
        return redirect(url_for('home_niveau'))
    return render_template('newNiveau.html', title='Nouveau niveau', form=form)


@app.route('/updateNiveau/<niveau_id>', methods=['GET', 'POST'])
@login_required
def updateNiveau(niveau_id):
    oldNiveau = Niveau.query.get(niveau_id)
    form = NewNiveauForm(obj=oldNiveau, name=oldNiveau.name)
    if form.validate_on_submit():
        oldNiveau.name = form.name.data.upper()
        db.session.add(oldNiveau)
        db.session.commit()
        flash(f'Contact {form.name.data.upper()} modifié !')
        return redirect(url_for('home_niveau'))
    return render_template('updateNiveau.html', title='Modification niveau', form=form, niveau_id=niveau_id)


@app.route('/delNiveau<niveau_id>/<confirm>', methods=['GET', 'POST'])
@login_required
def delNiveau(niveau_id, confirm):
    print(f"confirm = {confirm}")
    if confirm == '0':
        print("confirmation effacement")
        delNiveau = Niveau.query.get(niveau_id)
        return render_template('conf_del_niveau.html', title='Confirmation effacement niveau', niveau=delNiveau)
    else:
        delNiveau = Niveau.query.get(niveau_id)
        db.session.delete(delNiveau)
        db.session.commit()
        flash(f'Niveau supprimé !')
        return redirect(url_for('home_niveau'))


@app.route('/classe/')
@login_required
def home_classe():
    classes = Classe.query.order_by(Classe.name).all()

    # return render_template('home_niveau.html', title='Home Niveau', niveaux=niveaux)
    return render_template('home_classe.html', title='Home Stage', classes=classes)


@app.route('/newclasse1/', methods=['GET', 'POST'])
@login_required
def new_classe1():
    list_promotions = [(e.id, e.name) for e in Promotion.query.order_by(Promotion.name.desc()).all()]
    list_niveaux = [(e.id, e.name) for e in Niveau.query.all()]
    list_annees_scolaires = [(e.id, e.name) for e in AnneeScolaire.query.order_by(AnneeScolaire.id.desc()).all()]
    list_groupes = [(1, "1"), (2, "2")]

    form = NewClasseForm1()
    form.promotion.choices = list_promotions
    form.niveau.choices = list_niveaux
    form.annee_scolaire.choices = list_annees_scolaires
    form.groupe.choices = list_groupes

    if form.validate_on_submit():
        # promotion = Promotion.query.get(form.promotion.data).id
        niveau = Niveau.query.get(form.niveau.data).name
        annee_scolaire = AnneeScolaire.query.get(form.annee_scolaire.data).name
        groupe = form.groupe.data
        propo_nom = niveau + str(groupe) + "_" + annee_scolaire
        oldclasse = Classe.query.filter_by(name=propo_nom).first()
        if oldclasse:
            flash(f'La classe {oldclasse.name} '
                  f'est déjà présent dans votre base de données !')
            return redirect(url_for('home_classe'))
        classe = Classe(name=propo_nom, promotion_id=form.promotion.data, niveau_id=form.niveau.data,
                        annee_scolaire_id=form.annee_scolaire.data)
        db.session.add(classe)
        db.session.commit()
        flash(f'Classe :  {propo_nom} ajoutée !')

        return redirect(url_for('new_classe2', classe_id=classe.id))
    return render_template('newClasse.html', title='Nouvelle classe', form=form)


@app.route('/newclasse2/<classe_id>', methods=['GET', 'POST'])
@login_required
def new_classe2(classe_id):
    form = EleveToClasseForm()
    new_classe = Classe.query.get(classe_id)
    list_eleves = [(e.id, e.name+" "+e.firstname) for e in Eleve.query.filter_by(promotion_id=new_classe.promotion_id).order_by(Eleve.name).all()]
    form.eleves_id.choices = list_eleves
    if form.validate_on_submit():
        print(form.eleves_id.data)
        data = form.eleves_id.data
        for eleve_id in data:
            eleve=Eleve.query.get(eleve_id)
            print(eleve)
            new_classe.classe.append(eleve)
        db.session.commit()

        return render_template('newClasse4.html', title='Nouvelle classe', data=data)
    return render_template('newClasse3.html', title='Nouvelle classe', form=form)
    # return render_template('newClasse3.html', title='Nouvelle classe', form=form, propo_nom=propo_nom)


@app.route('/delclasse/<classe_id>/<confirm>', methods=['GET', 'POST'])
@login_required
def delclasse(classe_id, confirm):
    if confirm == '0':
        delclasse = Classe.query.get(classe_id)
        return render_template('conf_del_classe.html', title='Confirmation effacement classe', classe=delclasse)
    else:
        delclasse = Classe.query.get(classe_id)
        db.session.delete(delclasse)
        db.session.commit()
        flash(f'Classe supprimée !')
        return redirect(url_for('home_classe'))


@app.route('/updateClasse/<classe_id>', methods=['GET', 'POST'])
@login_required
def updateClasse(classe_id):
    oldClasse = Classe.query.get(classe_id)
    form = NewClasseForm1(obj=oldClasse, name=oldClasse.name)

    if form.validate_on_submit():
        name = propo_nom, promotion_id = form.promotion.data, niveau_id = form.niveau.data,
        oldClasse.promotion_id = form.promotion.data
        oldClasse.niveau_id = form.niveau.data
        oldClasse.annee_scolaire_id = form.annee_scolaire.data

        db.session.add(oldClasse)
        db.session.commit()
        flash(f'Classe {form.name.data} modifiée !')
        return redirect(url_for('home_niveau'))
    return render_template('updateNiveau.html', title='Modification niveau', form=form, niveau_id=niveau_id)


@app.route('/stage/')
@login_required
def home_stage():
    # stages = Stage.query.order_by(Stage.niveau_id).all()
    stages = Stage.query.order_by(Stage.niveau_id,Stage.periode_id).all()

    # return render_template('home_niveau.html', title='Home Niveau', niveaux=niveaux)
    return render_template('home_stage.html', title='Home Stage', stages=stages)


@app.route('/newStage1/', methods=['GET', 'POST'])
@login_required
def new_stage1():
    list_annees_scolaires = [(e.id, e.name) for e in AnneeScolaire.query.all()]
    form = NewStageForm1()
    form.annee_scolaire.choices = list_annees_scolaires
    if form.validate_on_submit():
        print(form.annee_scolaire.data)
        annee_scolaire = AnneeScolaire.query.get(form.annee_scolaire.data).name
        print(annee_scolaire)
        # periodes = Date.query.filter_by(annee_scolaire=annee_scolaire).all()
        # print(periodes)
        return redirect(url_for('new_stage2', annee_scolaire=annee_scolaire))
    return render_template('newStage.html', title='Nouveau stage', form=form)


@app.route('/newstage2/<annee_scolaire>', methods=['GET', 'POST'])
@login_required
def new_stage2(annee_scolaire):
    print(annee_scolaire)
    list_periodes = [(e.id, e.date_deb1) for e in Date.query.filter_by(annee_scolaire=annee_scolaire).all()]
    print(list_periodes)
    list_nom_eleves = [(e.id, e.name) for e in Eleve.query.all()]
    list_prenom_eleves = [(e.id, e.firstname) for e in Eleve.query.all()]
    list_niveaux = [(e.id, e.name) for e in Niveau.query.all()]
    list_entreprises = [(e.id, e.name) for e in Entreprise.query.all()]
    list_contacts = [(e.id, e.name) for e in Contact.query.all()]
    # list_periodes = [(e.id, e.annee_scolaire) for e in Date.query.all()]

    # print(list_eleves)
    form = NewStageForm2()
    form.nom_eleve.choices = list_nom_eleves
    # form.prenom_eleve.choices = list_prenom_eleves
    form.niveau.choices = list_niveaux
    form.entreprise.choices = list_entreprises
    form.contact.choices = list_contacts
    form.periode.choices = list_periodes

    if form.validate_on_submit():
        # TODO à préciser car multifacteurs
        oldstage = Stage.query.filter_by(eleve_id=form.nom_eleve.data).first()

        if oldstage:
            flash(f'{form.eleve_id.data} '
                  f'est déjà présent dans votre base de données !')
            return redirect(url_for('home_stage'))
        print("donnée Période")
        print(form.periode.data)
        stage = Stage(eleve_id=form.nom_eleve.data,
                      niveau_id=form.niveau.data,
                      entreprise_id=form.entreprise.data,
                      contact_id=form.contact.data,
                      periode_id=form.periode.data)
        db.session.add(stage)
        db.session.commit()
        flash(f'Stage ajouté !')
        return redirect(url_for('home_stage'))
    return render_template('newStage.html', title='Nouveau stage', form=form)


#######################################################################################################################
######################################################################################################################
@app.route('/newStage3/', methods=['GET', 'POST'])
@login_required
def new_stage3():
    list_annees_scolaires = [(e.id, e.name) for e in AnneeScolaire.query.all()]
    list_promotions = [(e.id, e.name) for e in Promotion.query.all()]
    list_niveaux = [(e.id, e.name) for e in Niveau.query.all()]

    form = NewStageForm3()
    form.annee_scolaire.choices = list_annees_scolaires
    form.promotion.choices = list_promotions
    form.niveau.choices = list_niveaux

    if form.validate_on_submit():
        annee_scolaire = AnneeScolaire.query.get(form.annee_scolaire.data).name
        promotion = Promotion.query.get(form.promotion.data).id
        niveau = Niveau.query.get(form.niveau.data).id

        return redirect(url_for('new_stage4', annee_scolaire=annee_scolaire, promotion=promotion, niveau=niveau))
    return render_template('newStage.html', title='Nouveau stage', form=form)


@app.route('/newstage4/<annee_scolaire>/<promotion>/<niveau>', methods=['GET', 'POST'])
@login_required
def new_stage4(annee_scolaire, promotion):
    print(annee_scolaire)
    print(promotion)
    list_periodes = [(e.id, e.date_deb1) for e in Date.query.filter_by(annee_scolaire=annee_scolaire).all()]
    list_nom_eleves = [(e.id, e.name) for e in Eleve.query.filter_by(promotion_id=promotion).all()]
    list_prenom_eleves = [(e.id, e.firstname) for e in Eleve.query.all()]
    list_entreprises = [(e.id, e.name) for e in Entreprise.query.all()]
    list_contacts = [(e.id, e.name) for e in Contact.query.all()]
    # list_periodes = [(e.id, e.annee_scolaire) for e in Date.query.all()]

    # print(list_eleves)
    form = NewStageForm4()
    form.nom_eleve.choices = list_nom_eleves
    # form.prenom_eleve.choices = list_prenom_eleves
    form.niveau.choices = list_niveaux
    form.entreprise.choices = list_entreprises
    form.contact.choices = list_contacts
    form.periode.choices = list_periodes

    if form.validate_on_submit():
        # TODO à préciser car multifacteurs
        oldstage = Stage.query.filter_by(eleve_id=form.nom_eleve.data).first()

        if oldstage:
            flash(f'{form.eleve_id.data} '
                  f'est déjà présent dans votre base de données !')
            return redirect(url_for('home_stage'))
        print("donnée Période")
        print(form.periode.data)
        stage = Stage(eleve_id=form.nom_eleve.data,
                      niveau_id=form.niveau.data,
                      entreprise_id=form.entreprise.data,
                      contact_id=form.contact.data,
                      periode_id=form.periode.data)
        db.session.add(stage)
        db.session.commit()
        flash(f'Stage ajouté !')
        return redirect(url_for('home_stage'))
    return render_template('newStage.html', title='Nouveau stage', form=form)
#######################################################################################################################
#######################################################################################################################
@app.route('/eleve/<annee_scolaire>')
@login_required
def eleve(annee_scolaire):

    eleves=Eleve.query.filter_by()



#######################################################################################################################
#######################################################################################################################


@app.route('/updateStage/<stage_id>', methods=['GET', 'POST'])
@login_required
def updateStage(stage_id):
    oldStage = Stage.query.get(stage_id)
    print(f"info oldstage : {oldStage}")
    print(oldStage.periode.date_deb1)
    print(type(oldStage.periode.date_deb1))
    print(oldStage.periode.date_deb1.strftime('%d-%m-%Y'))

    # form = OldStageForm(obj=oldStage, id=stage_id, nom_eleve=oldStage.eleve.name, niveau=oldStage.niveau.name)
    form = OldStageForm(obj=oldStage, id=stage_id, nom_eleve=oldStage.eleve.name, date_deb1=oldStage.periode.date_deb1.strftime('%d-%m-%Y'), date_fin2=oldStage.periode.date_fin2.strftime('%d-%m-%Y'))

    # list_nom_eleves = [(e.id, e.name) for e in Eleve.query.all()]
    # list_niveaux = [(e.id, e.name) for e in Niveau.query.all()]
    # list_entreprises = [(e.id, e.name) for e in Entreprise.query.all()]
    # list_contacts = [(e.id, e.name) for e in Contact.query.all()]
    # # list_periodes = [(e.id, e.date_deb1) for e in Date.query.filter_by(annee_scolaire=annee_scolaire).all()]
    #
    # # form.nom_eleve.choices = list_nom_eleves
    # print(oldStage.eleve.name)
    # # form.nom_eleve.choices = oldStage.eleve.name
    #
    # form.nom_eleve.default = oldStage.eleve.name
    # # form.prenom_eleve.choices = list_prenom_eleves
    # form.niveau.choices = list_niveaux
    # form.entreprise.choices = list_entreprises
    # form.contact.choices = list_contacts
    # # form.periode.choices = list_periodes

    if form.validate_on_submit():
        oldStage.eleve_id = form.nom_eleve.data
        oldStage.niveau_id = form.niveau.data
        oldStage.entreprise_id = form.entreprise.data
        oldStage.contact_id = form.contact.data
        oldStage.periode_id = form.periode.data
        db.session.add(oldStage)
        db.session.commit()
        flash(f'Stage modifié !')
        return redirect(url_for('home_stage'))
    return render_template('updateStage.html', title='Modification stage', form=form, stage_id=stage_id)


@app.route('/delStage<stage_id>/<confirm>', methods=['GET', 'POST'])
@login_required
def delStage(stage_id, confirm):
    print(f"confirm = {confirm}")
    if confirm == '0':
        print("confirmation effacement")
        delStage = Stage.query.get(stage_id)
        return render_template('conf_del_stage.html', title='Confirmation effacement stage', stage=delStage)
    else:
        delStage = Stage.query.get(stage_id)
        db.session.delete(delStage)
        db.session.commit()
        flash(f'Stage supprimé !')
        return redirect(url_for('home_stage'))


@app.route('/periode/')
@login_required
def home_periode():
    periodes = Date.query.order_by(Date.date_deb1).all()
    return render_template('home_periode.html', title='Home période', periodes=periodes)


@app.route('/newPeriode/', methods=['GET', 'POST'])
@login_required
def new_periode():
    form = NewPeriodeForm()
    if form.validate_on_submit():
        oldPeriode = Date.query.filter_by(annee_scolaire=form.annee_scolaire.data,
                                          date_deb1=form.date_deb1.data).first()
        if oldPeriode:
            flash('Cette période est déjà présente dans votre base de données !')
            return redirect(url_for('home_periode'))
        periode = Date(annee_scolaire=form.annee_scolaire.data,
                       date_deb1=form.date_deb1.data,
                       date_fin1=form.date_fin1.data,
                       date_deb2=form.date_deb2.data,
                       date_fin2=form.date_fin2.data)
        db.session.add(periode)
        db.session.commit()
        flash(f'Période de stage ajoutée !')
        return redirect(url_for('home_periode'))
    return render_template('newPeriode.html', title='Nouvelle période', form=form)

    return render_template('newPeriode.html', title='Nouvelle periode')


@app.route('/updatePeriode/<date_id>', methods=['GET', 'POST'])
@login_required
def updatePeriode(date_id):
    oldPeriode = Date.query.get(date_id)
    form = NewPeriodeForm(obj=oldPeriode, id=oldPeriode.id)
    if form.validate_on_submit():
        oldPeriode.annee_scolaire = form.annee_scolaire.data
        oldPeriode.date_deb1 = form.date_deb1.data
        oldPeriode.date_fin1 = form.date_fin1.data
        oldPeriode.date_deb2 = form.date_deb2.data
        oldPeriode.date_fin2 = form.date_fin2.data

        db.session.add(oldPeriode)
        db.session.commit()
        flash(f'Période modifiée !')
        return redirect(url_for('home_periode'))
    return render_template('updatePeriode.html', title='Modification periode', form=form, date_id=date_id)


@app.route('/delPeriode<date_id>/<confirm>', methods=['GET', 'POST'])
@login_required
def delPeriode(date_id, confirm):
    print(f"confirm = {confirm}")
    if confirm == '0':
        print("confirmation effacement")
        delPeriode = Date.query.get(date_id)
        return render_template('conf_del_periode.html', title='Confirmation effacement periode', periode=delPeriode)
    else:
        delPeriode = Date.query.get(date_id)
        db.session.delete(delPeriode)
        db.session.commit()
        flash(f'Période supprimée !')
        return redirect(url_for('home_periode'))


@app.route('/anneescolaire/')
@login_required
def home_anneeScolaire():
    anneeScolaires = AnneeScolaire.query.order_by(AnneeScolaire.name).all()
    return render_template('home_anneeScolaire.html', title='Home AnneeScolaire', anneeScolaires=anneeScolaires)


@app.route('/newAnneeScolaire/', methods=['GET', 'POST'])
@login_required
def new_anneeScolaire():
    form = NewAnneeScolaireForm()
    if form.validate_on_submit():
        oldAnneeScolaire = AnneeScolaire.query.filter_by(name=form.name.data).first()
        if oldAnneeScolaire:
            flash(f'{form.name.data.upper()} '
                  f'est déjà présente dans votre base de données !')
            return redirect(url_for('home_anneeScolaire'))
        anneeScolaire = AnneeScolaire(name=form.name.data.upper())
        db.session.add(anneeScolaire)
        db.session.commit()
        flash(f'Année scolaire :  {form.name.data} ajouté !')
        return redirect(url_for('home_anneeScolaire'))
    return render_template('newAnneeScolaire.html', title='Nouvelle année scolaire', form=form)


@app.route('/updateAnneeScolaire/<anneeScolaire_id>', methods=['GET', 'POST'])
@login_required
def updateAnneeScolaire(anneeScolaire_id):
    oldAnneeScolaire = AnneeScolaire.query.get(anneeScolaire_id)
    form = NewAnneeScolaireForm(obj=oldAnneeScolaire, name=oldAnneeScolaire.name)
    if form.validate_on_submit():
        oldAnneeScolaire.name = form.name.data.upper()
        db.session.add(oldAnneeScolaire)
        db.session.commit()
        flash(f'Année Scolaire {form.name.data.upper()} modifiée !')
        return redirect(url_for('home_anneeScolaire'))
    return render_template('updateAnneeScolaire.html', title='Modification année scolaire', form=form,
                           anneeScolaire_id=anneeScolaire_id)


@app.route('/delAnneeScolaire<anneeScolaire_id>/<confirm>', methods=['GET', 'POST'])
@login_required
def delAnneeScolaire(anneeScolaire_id, confirm):
    print(f"confirm = {confirm}")
    if confirm == '0':
        print("confirmation effacement")
        delAnneeScolaire = AnneeScolaire.query.get(anneeScolaire_id)
        return render_template('conf_del_anneeScolaire.html', title='Confirmation effacement année scolaire',
                               anneeScolaire=delAnneeScolaire)
    else:
        delAnneeScolaire = AnneeScolaire.query.get(anneeScolaire_id)
        db.session.delete(delAnneeScolaire)
        db.session.commit()
        flash(f'Année scolaire supprimée !')
        return redirect(url_for('home_anneeScolaire'))


########################################################################################################################
########################################################################################################################
# Différentes fonctions testées pour enrichir l'application
########################################################################################################################
########################################################################################################################

# cette fonction permet de charger un fichier précis (exemple eleves.csv) sur le poste de l'utilisateur
# de la page lorsque celui-ci clique sur le mot download page test.html
@app.route('/test/download')
def download_File():
    PATH = 'eleves.csv'
    return send_file(PATH, as_attachment=True)


@app.route('/upload')
def upload_file1():
    return render_template('test.html')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('Pas de fichier')
            print("Pas de fichier")
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            flash('No selected file')
            print("Pas de fichier2")

            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print("fichier au format autorisé")

            # return redirect(url_for('download_file', name=filename))
            return 'file uploaded successfully'

        return 'fichier au format non autorisé'


# fonction permettant de peupler la base de données avec les différentes années, promotions et niveaux
# à partir du fichiers csv annee.csv, promo.csv et niveaux.csv présent dans le répertoire appstagesn

@app.route('/peupler_bdd/APN/')
def add_apn_via_csv():
    with open('appstagesn\\annee.csv', 'r') as f:  # Read lines separately
        reader = csv.reader(f, delimiter=';')
        for i, line in enumerate(reader):
            annee_scolaire = AnneeScolaire(name=line[0].upper())
            db.session.add(annee_scolaire)
            db.session.commit()

    with open('appstagesn\promo.csv', 'r') as f:  # Read lines separately
        reader = csv.reader(f, delimiter=';')
        for i, line in enumerate(reader):
            promo = Promotion(name=line[0].upper(),
                              annee_deb=line[1],
                              annee_fin=line[2])
            db.session.add(promo)
            db.session.commit()

    with open('appstagesn\\niveaux.csv', 'r') as f:  # Read lines separately
        reader = csv.reader(f, delimiter=';')
        for i, line in enumerate(reader):
            niveau = Niveau(name=line[0].upper())
            db.session.add(niveau)
            db.session.commit()

    return render_template('index.html', title='Home')


@app.route('/peupler_bdd/eleves/')
def add_eleve_via_csv():
    with open('appstagesn\eleves.csv', 'r') as f:  # Read lines separately
        reader = csv.reader(f, delimiter=';')
        for i, line in enumerate(reader):
            eleve = Eleve(name=line[0].upper(),
                          firstname=line[1].capitalize(),
                          phonenumber=line[2],
                          mail1=line[3],
                          mail2=line[4],
                          active=int(line[5]),
                          promotion_id=line[6])
            db.session.add(eleve)
            db.session.commit()
    eleves = Eleve.query.order_by(Eleve.name).all()
    return render_template('home_eleve.html', title='Home Eleve', eleves=eleves)


@app.route('/peupler_bdd/entreprises/')
def add_entr_via_csv():
    with open('appstagesn\entreprises.csv', 'r') as f:  # Read lines separately
        reader = csv.reader(f, delimiter=';')
        for i, line in enumerate(reader):
            entreprise = Entreprise(name=line[0].capitalize(),
                                    adresse1=line[1],
                                    adresse2=line[2],
                                    CP=line[3],
                                    ville=line[4].upper(),
                                    active=int(line[5]),
                                    phonenumber=line[6],
                                    mail=line[7])
            db.session.add(entreprise)
            db.session.commit()
    entreprises = Entreprise.query.order_by(Entreprise.name).all()
    return render_template('home_entreprise.html', title='Home Entreprise', entreprises=entreprises)


@app.route('/peupler_bdd/contacts/')
def add_contact_via_csv():
    with open('appstagesn\contacts.csv', 'r') as f:  # Read lines separately
        reader = csv.reader(f, delimiter=';')
        for i, line in enumerate(reader):
            contact = Contact(name=line[0].upper(),
                              firstname=line[1].capitalize(),
                              fonction=line[2],
                              active=int(line[3]),
                              phonenumber1=line[4],
                              phonenumber2=line[5],
                              mail=line[6],
                              entreprise_id=line[7])
            db.session.add(contact)
            db.session.commit()
    contacts = Contact.query.order_by(Contact.name).all()
    return render_template('home_contact.html', title='Home Contact', contacts=contacts)

# TODO modifier afin de prendre en compte le type time en entrée via le fichier periodes.csv
# @app.route('/peupler_bdd/periodes/')
# def add_periode_via_csv():
#     with open('appstagesn\periodes.csv', 'r') as f:  # Read lines separately
#         reader = csv.reader(f, delimiter=';')
#         for i, line in enumerate(reader):
#             periode = Date(annee_scolaire=line[0],
#                           date_deb1=line[1],
#                           date_fin1=line[2],
#                           date_deb2=line[3],
#                           date_fin2=line[4])
#             db.session.add(periode)
#             db.session.commit()
#     periodes = Date.query.order_by(Date.annee_scolaire).all()
#     return render_template('home_periode.html', title='Home Période', periodes=periodes)


@app.route('/peupler_bdd/all/')
def add_all_via_csv():
    add_apn_via_csv()
    add_eleve_via_csv()
    add_entr_via_csv()
    add_contact_via_csv()
    add_periode_via_csv()
    return render_template('index.html', title='Home')


# fonction permettant de récupérer via une API la liste des villes correspondant à un code postal CP
# entrée --> string : CP
# sortie --> liste : list_commune
def recup_ville2(CP):
    url = 'https://apicarto.ign.fr/api/codes-postaux/communes/' + CP
    res = requests.get(url)
    json = res.json()
    list_commune = []
    for key in range(len(json)):
        list_commune.append(json[key]['nomCommune'])
    print(list_commune)

    return list_commune


@app.route('/codepostal/<CP>')
def recup_ville(CP):
    url = 'https://apicarto.ign.fr/api/codes-postaux/communes/' + CP
    res = requests.get(url)
    json = res.json()
    list_commune = []
    for key in range(len(json)):
        list_commune.append(json[key]['nomCommune'])
    print(list_commune)

    return render_template('test_API.html', title='villes', liste=list_commune)


# fonction permettant de
# entrée -->
# sortie -->

@app.route('/pdf/<name>/<location>')
def pdf_template(name, location):
    path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

    rendered = render_template('pdf_template.html', name=name, location=location)
    pdf = pdfkit.from_string(rendered, False, configuration=config)

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=output.pdf'

    return response
    # pdfkit.from_file('/templates/pdf_template.html', 'demo.pdf', configuration=config)
    # pdfkit.from_url("http://google.com", "out.pdf", configuration=config)
    # pdfkit.from_string('Hello World 17:01', 'demo.pdf', configuration=config)
    # return render_template('pdf_template.html')