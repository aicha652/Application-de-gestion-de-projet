# -*- encoding: utf-8 -*-

import os
import time
from datetime import datetime
from os import path

import pdfkit as pdfkit
import sqlalchemy as sql
from flask import current_app as app, make_response
from flask import render_template, redirect, url_for, abort, request, jsonify, flash, send_file
from flask_login import login_required, current_user
from sqlalchemy import func
from sqlalchemy.sql.expression import cast

from app.base.models import User, Contact, Societe, Personne, Administration, Prestation, Ouvrage, Projet, Devis, \
    Article, Chapitre
from app.base.tools import send_email
from app.base.orm_tools import FactoryController
from app.home import blueprint
from .forms import UserForm, EditUserForm, SocieteForm, PersonneForm, AdministrationForm, EditPersonneForm, \
    EditSocieteForm, \
    EditAdministrationForm, PrestationForm, OuvrageForm, EditPrestationForm, EditOuvrageForm, \
    ProjetForm, EditProjetForm, DevisForm, ChapitreForm,EditChapitreForm, ArticleForm, EditArticleForm, SousArticleForm,\
    EditSousArticleForm, EditDevisForm
from .. import db


@blueprint.route('/index')
@login_required
def index():
    if current_user.is_admin:
        return redirect(url_for('home_blueprint.admin_dashboard'))
    else:
        return redirect(url_for('home_blueprint.dashboard'))


@blueprint.route('/administration')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        abort(403)

    return redirect(url_for('home_blueprint.dashboard'))


@blueprint.route('/dashboard')
@login_required
def dashboard():
    count_users = User.query.count()
    count_personnes = Personne.query.count()
    count_societes = Societe.query.count()
    count_administrations = Administration.query.count()
    count_ouvrages = Ouvrage.query.count()
    count_prestations = Prestation.query.count()
    count_projets = Projet.query.count()
    count_devis = Devis.query.count()
    return render_template('dashboard.html', count_users=count_users, count_personnes=count_personnes, count_societes=count_societes,
                           count_administrations=count_administrations, count_ouvrages=count_ouvrages,
                           count_prestations=count_prestations, count_projets=count_projets, count_devis=count_devis,
                           page='dashboard')


@blueprint.route('/users')
@login_required
def list_users():
    if not current_user.is_admin:
        abort(403)

    count_users = User.query.count()

    return render_template('users_list.html', count_users=count_users, page='list_users')


@blueprint.route('/usersData')
@login_required
def users_data():
    if not current_user.is_admin:
        abort(403)

    users = User.query.all()
    user_array = []
    json_array = []
    for user in users:
        user_obj = {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'last_seen': user.last_seen,
            'is_active': user.is_active,
            'is_admin': user.is_admin}

        user_array.append(user_obj)

    return jsonify(user_array)


@blueprint.route('/addUser', methods=['POST', 'GET'])
@login_required
def add_user():
    if not current_user.is_admin:
        abort(403)

    form = UserForm()

    if form.validate_on_submit():
        user = User(email=form.email.data,
                    first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    password=form.password.data)

        is_admin = form.is_admin.data
        if is_admin:
            user.is_admin = True

        is_active = form.is_active.data
        if is_active:
            user.is_active = True
        else:
            # send verification email to activate the account
            user.generate_activation_token()
            url = f'{request.host_url}auth/activateAccount/{user.activation_token}'
            mail_subject = "ERP BET - POC: Activation de compte !"
            mail_content = f"Votre compte d'analayse salariale a été crée avec succès," \
                           f" afin de l'activer veuillez cliquer sur le lien suivant  : {url}"
            mail_content_html = f"Votre compte d'analayse salariale a été crée avec succès," \
                                f" afin de l'activer veuillez cliquer sur le lien suivant   :<br>" \
                                f" <a href='{url}'>Activer votre compte !</a>"
            mail_sender = app.config['MAIL_DEFAULT_SENDER']
            mail_recipts = [user.email]
            try:
                send_email(subject=mail_subject,
                           sender=mail_sender,
                           recipients=mail_recipts,
                           text_body=mail_content,
                           html_body=mail_content_html)
            except Exception as e:
                return render_template('add_user.html', edit=False, form=form, msg=f'Erreur server email {str(e)}')

        FactoryController.createOne(user)

        return redirect(url_for('home_blueprint.list_users'))

    return render_template('add_user.html', edit=False, form=form)


@blueprint.route('/editUser/<int:user_id>', methods=['POST', 'GET'])
@login_required
def edit_user(user_id):
    if not current_user.is_admin:
        abort(403)

    user = User.query.get_or_404(user_id)
    form = EditUserForm(obj=user)

    if form.validate_on_submit():

        email = form.email.data
        if email != user.email:
            usr = User.query.filter_by(email=email).first()
            if usr:
                return render_template('add_user.html',
                                       edit=True, form=form,
                                       msg="Cette adresse email existe déjà dans la base donnée")
        else:
            user.email = email

        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.is_admin = form.is_admin.data
        user.is_active = form.is_active.data
        FactoryController.commit()

        return redirect(url_for('home_blueprint.list_users'))

    return render_template('add_user.html', edit=True, form=form)


@blueprint.route('/deleteUser/<int:user_id>', methods=['POST', 'GET'])
@login_required
def delete_user(user_id):
    if not current_user.is_admin:
        abort(403)

    user = User.query.get_or_404(user_id)
    if current_user.id == user.id:
        jsonify(status='ERROR', message='Impossible de supprimer cet utilisateur')

    FactoryController.deleteOne(user)

    return jsonify(status='OK')


@blueprint.route('/add_client')
@login_required
def add_client():
    return render_template('add_client.html', page='add_client')


@blueprint.route('/add_societe', methods=['POST', 'GET'])
@login_required
def add_societe():
    form = SocieteForm()
    if form.validate_on_submit():
        societe = Societe(
            nom=form.nom.data,
            type=form.type.data,
            domaine=form.domaine.data,
            tel1=form.tel1.data,
            tel2=form.tel2.data,
            fax=form.fax.data,
            email=form.email.data,
            adresse=form.adresse.data)
        db.session.add(societe)
        db.session.commit()



        return redirect(url_for('home_blueprint.list_societes'))

    return render_template('add_societe.html', form=form, page='add_societe')


@blueprint.route('/add_personne', methods=['POST', 'GET'])
@login_required
def add_personne():
    form = PersonneForm()
    if form.validate_on_submit():
        personne = Personne(
            nom=form.nom.data,
            prenom=form.prenom.data,
            profession=form.profession.data,
            tel1=form.tel1.data,
            tel2=form.tel2.data,
            fax=form.fax.data,
            email=form.email.data,
            adresse=form.adresse.data)
        db.session.add(personne)
        db.session.commit()



        return redirect(url_for('home_blueprint.list_personnes'))

    return render_template('add_personne.html', form=form, page='add_personne')


@blueprint.route('/add_administration', methods=['POST', 'GET'])
def add_administration():
    form = AdministrationForm()
    if form.validate_on_submit():
        administration = Administration(
            nom=form.nom.data,
            type=form.type.data,
            domaine=form.domaine.data,
            tel1=form.tel1.data,
            tel2=form.tel2.data,
            fax=form.fax.data,
            email=form.email.data,
            adresse=form.adresse.data)
        db.session.add(administration)
        db.session.commit()



        return redirect(url_for('home_blueprint.list_administrations'))

    return render_template('add_administration.html', form=form, page='add_administration')


@blueprint.route('/clients')
@login_required
def list_clients():
    return render_template('clients_list.html', page='list_clients')


@blueprint.route('/personnes')
@login_required
def list_personnes():


    count_personnes = Personne.query.count()

    return render_template('personnes_list.html', count_personnes=count_personnes, page='list_personnes')


@blueprint.route('/personnesData')
@login_required
def personnes_data():


    personnes = Personne.query.all()
    personne_array = []
    json_array = []
    for personne in personnes:
        personne_obj = {
            'id': personne.id,
            'nom': personne.nom,
            'prenom': personne.prenom,
            'profession': personne.profession,
            'tel1': personne.tel1,
            'tel2': personne.tel2,
            'fax': personne.fax,
            'email': personne.email,
            'adresse': personne.adresse}

        personne_array.append(personne_obj)

    return jsonify(personne_array)


@blueprint.route('/editPersonne/<int:personne_id>', methods=['POST', 'GET'])
@login_required
def edit_personne(personne_id):


    personne = Personne.query.get_or_404(personne_id)
    form = EditPersonneForm(obj=personne)

    if form.validate_on_submit():
        personne.id = form.id.data
        personne.nom = form.nom.data
        personne.prenom = form.prenom.data
        personne.profession = form.profession.data
        personne.tel1 = form.tel1.data
        personne.tel2 = form.tel2.data
        personne.fax = form.fax.data
        personne.email = form.email.data
        personne.adresse = form.adresse.data
        FactoryController.commit()

        return redirect(url_for('home_blueprint.list_personnes'))

    return render_template('add_personne.html', edit=True, form=form)


@blueprint.route('/deletePersonne/<int:personne_id>', methods=['POST', 'GET'])
@login_required
def delete_personne(personne_id):


    personne = Personne.query.get_or_404(personne_id)

    FactoryController.deleteOne(personne)

    return jsonify(status='OK')


@blueprint.route('/societes')
@login_required
def list_societes():


    count_societes = Societe.query.count()

    return render_template('societes_list.html', count_societes=count_societes, page='list_societes')


@blueprint.route('/societesData')
@login_required
def societes_data():


    societes = Societe.query.all()
    societe_array = []
    json_array = []
    for societe in societes:
        societe_obj = {
            'id': societe.id,
            'nom': societe.nom,
            'type': societe.type,
            'domaine': societe.domaine,
            'tel1': societe.tel1,
            'tel2': societe.tel2,
            'fax': societe.fax,
            'email': societe.email,
            'adresse': societe.adresse}

        societe_array.append(societe_obj)

    return jsonify(societe_array)


@blueprint.route('/editSociete/<int:societe_id>', methods=['POST', 'GET'])
@login_required
def edit_societe(societe_id):


    societe = Societe.query.get_or_404(societe_id)
    form = EditSocieteForm(obj=societe)

    if form.validate_on_submit():
        societe.id = form.id.data
        societe.nom = form.nom.data
        societe.type = form.type.data
        societe.domaine = form.domaine.data
        societe.tel1 = form.tel1.data
        societe.tel2 = form.tel2.data
        societe.fax = form.fax.data
        societe.email = form.email.data
        societe.adresse = form.adresse.data
        FactoryController.commit()

        return redirect(url_for('home_blueprint.list_societes'))

    return render_template('add_societe.html', edit=True, form=form)


@blueprint.route('/deleteSociete/<int:societe_id>', methods=['POST', 'GET'])
@login_required
def delete_societe(societe_id):


    societe = Societe.query.get_or_404(societe_id)

    FactoryController.deleteOne(societe)

    return jsonify(status='OK')


@blueprint.route('/administrations')
@login_required
def list_administrations():


    count_administrations = Administration.query.count()

    return render_template('administrations_list.html', count_administrations=count_administrations,
                           page='list_administrations')


@blueprint.route('/administrationsData')
@login_required
def administrations_data():

    administrations = Administration.query.all()
    administration_array = []
    json_array = []
    for administration in administrations:
        administration_obj = {
            'id': administration.id,
            'nom': administration.nom,
            'type': administration.type,
            'domaine': administration.domaine,
            'tel1': administration.tel1,
            'tel2': administration.tel2,
            'fax': administration.fax,
            'email': administration.email,
            'adresse': administration.adresse}

        administration_array.append(administration_obj)

    return jsonify(administration_array)


@blueprint.route('/editAdministration/<int:administration_id>', methods=['POST', 'GET'])
@login_required
def edit_administration(administration_id):


    administration = Administration.query.get_or_404(administration_id)
    form = EditAdministrationForm(obj=administration)

    if form.validate_on_submit():
        administration.id = form.id.data
        administration.nom = form.nom.data
        administration.type = form.type.data
        administration.domaine = form.domaine.data
        administration.tel1 = form.tel1.data
        administration.tel2 = form.tel2.data
        administration.fax = form.fax.data
        administration.email = form.email.data
        administration.adresse = form.adresse.data
        FactoryController.commit()

        return redirect(url_for('home_blueprint.list_administrations'))

    return render_template('add_administration.html', edit=True, form=form)


@blueprint.route('/deleteAdministration/<int:administration_id>', methods=['POST', 'GET'])
@login_required
def delete_administration(administration_id):


    administration = Administration.query.get_or_404(administration_id)

    FactoryController.deleteOne(administration)

    return jsonify(status='OK')


@blueprint.route('/add_prestation', methods=['POST', 'GET'])
@login_required
def add_prestation():
    if not current_user.is_admin:
        abort(403)

    form = PrestationForm()
    if form.validate_on_submit():
        prestation = Prestation(
            type_prestation=form.type_prestation.data,
            code_prestation=form.code_prestation.data)
        db.session.add(prestation)
        db.session.commit()



        return redirect(url_for('home_blueprint.list_prestations'))

    return render_template('add_prestation.html', form=form, page='add_prestation')


@blueprint.route('/add_ouvrage', methods=['POST', 'GET'])
@login_required
def add_ouvrage():
    if not current_user.is_admin:
        abort(403)

    form = OuvrageForm()
    if form.validate_on_submit():
        ouvrage = Ouvrage(
            type_ouvrage=form.type_ouvrage.data,
            code_ouvrage=form.code_ouvrage.data)
        db.session.add(ouvrage)
        db.session.commit()



        return redirect(url_for('home_blueprint.list_ouvrages'))

    return render_template('add_ouvrage.html', form=form, page='add_ouvrage')


@blueprint.route('/list')
@login_required
def list():
    return render_template('list.html', page='list')


@blueprint.route('/prestations')
@login_required
def list_prestations():
    if not current_user.is_admin:
        abort(403)

    count_prestations = Prestation.query.count()

    return render_template('prestations_list.html', count_prestations=count_prestations, page='list_prestations')


@blueprint.route('/prestationsData')
@login_required
def prestations_data():
    if not current_user.is_admin:
        abort(403)

    prestations = Prestation.query.all()
    prestation_array = []
    json_array = []
    for prestation in prestations:
        prestation_obj = {
            'id_prestation': prestation.id,
            'type_prestation': prestation.type_prestation,
            'code_prestation': prestation.code_prestation}

        prestation_array.append(prestation_obj)

    return jsonify(prestation_array)


@blueprint.route('/editPrestation/<int:prestation_id>', methods=['POST', 'GET'])
@login_required
def edit_prestation(prestation_id):
    if not current_user.is_admin:
        abort(403)

    prestation = Prestation.query.get_or_404(prestation_id)
    form = EditPrestationForm(obj=prestation)

    if form.validate_on_submit():
        prestation.type_prestation = form.type_prestation.data
        prestation.code_prestation = form.code_prestation.data
        FactoryController.commit()

        return redirect(url_for('home_blueprint.list_prestations'))

    return render_template('add_prestation.html', edit=True, form=form)


@blueprint.route('/deletePrestation/<int:prestation_id>', methods=['POST', 'GET'])
@login_required
def delete_prestation(prestation_id):
    if not current_user.is_admin:
        abort(403)

    prestation = Prestation.query.get_or_404(prestation_id)

    FactoryController.deleteOne(prestation)

    return jsonify(status='OK')


@blueprint.route('/ouvrages')
@login_required
def list_ouvrages():
    if not current_user.is_admin:
        abort(403)

    count_ouvrages = Ouvrage.query.count()

    return render_template('ouvrages_list.html', count_ouvrages=count_ouvrages, page='list_ouvrages')


@blueprint.route('/ouvragesData')
@login_required
def ouvrages_data():
    if not current_user.is_admin:
        abort(403)

    ouvrages = Ouvrage.query.all()
    ouvrage_array = []
    json_array = []
    for ouvrage in ouvrages:
        ouvrage_obj = {
            'id_ouvrage': ouvrage.id,
            'type_ouvrage': ouvrage.type_ouvrage,
            'code_ouvrage': ouvrage.code_ouvrage}

        ouvrage_array.append(ouvrage_obj)

    return jsonify(ouvrage_array)


@blueprint.route('/editOuvrage/<int:ouvrage_id>', methods=['POST', 'GET'])
@login_required
def edit_ouvrage(ouvrage_id):
    if not current_user.is_admin:
        abort(403)

    ouvrage = Ouvrage.query.get_or_404(ouvrage_id)
    form = EditOuvrageForm(obj=ouvrage)

    if form.validate_on_submit():
        ouvrage.type_ouvrage = form.type_ouvrage.data
        ouvrage.code_ouvrage = form.code_ouvrage.data
        FactoryController.commit()

        return redirect(url_for('home_blueprint.list_ouvrages'))

    return render_template('add_ouvrage.html', edit=True, form=form)


@blueprint.route('/deleteOuvrage/<int:ouvrage_id>', methods=['POST', 'GET'])
@login_required
def delete_ouvrage(ouvrage_id):
    if not current_user.is_admin:
        abort(403)

    ouvrage = Ouvrage.query.get_or_404(ouvrage_id)

    FactoryController.deleteOne(ouvrage)

    return jsonify(status='OK')


@blueprint.route('/add_projet', methods=['POST', 'GET'])
@login_required
def add_projet():
    form = ProjetForm()

    if form.validate_on_submit():
        date_obj = datetime.strptime(form.date.data, '%m/%d/%Y')

        projet = Projet(
            titre=form.titre.data,
            prestation=form.prestation.data,
            ouvrage=form.ouvrage.data,
            client_id=form.client_id.data,
            date=date_obj,
            agent=form.agent.data)

        FactoryController.createOne(projet)



        return redirect(url_for('home_blueprint.list_projets'))

    return render_template('add_projet.html', form=form, page='add_projet')


@blueprint.route('/get-contacts/<genre>')
@login_required
def get_contacts(genre):

    contacts = Contact.query.filter_by(genre=genre).all()
    contact_array = []
    for contact in contacts:
        contact_obj = {
            'id': contact.id,
            'nom': contact.get_name}
        contact_array.append(contact_obj)
    return jsonify(contact_array)


@blueprint.route('projets')
@login_required
def list_projets():
    count_projets = Projet.query.count()

    return render_template('projets_list.html', count_projets=count_projets, page='list_projets')


@blueprint.route('/projetsData')
@login_required
def projets_data():

    projets = Projet.query.all()
    projet_array = []
    json_array = []
    for projet in projets:
        projet_obj = {
            'id': projet.id,
            'state': projet.state,
            'fsn': projet.fsn,
            'titre': projet.titre,
            'prestation': projet.prestation.type_prestation,
            'ouvrage': projet.ouvrage.type_ouvrage,
            'client': projet.client.get_name,
            'date': projet.date,
            'agent': projet.agent.get_name}

        projet_array.append(projet_obj)

    return jsonify(projet_array)


@blueprint.route('/editProjet/<int:projet_id>', methods=['POST', 'GET'])
@login_required
def edit_projet(projet_id):


    projet = Projet.query.get_or_404(projet_id)
    form = EditProjetForm(obj=projet)

    if form.validate_on_submit():
        date_obj = datetime.strptime(form.date.data, '%m/%d/%Y')


        projet.titre = form.titre.data
        projet.prestation = form.prestation.data
        projet.ouvrage = form.ouvrage.data
        projet.date = date_obj
        projet.agent = form.agent.data
        FactoryController.commit()

        return redirect(url_for('home_blueprint.list_projets'))

    date_obj = projet.date
    date_string = date_obj.strftime('%m/%d/%Y')
    form.date.data = date_string

    return render_template('add_projet.html', edit=True, form=form)


@blueprint.route('/deleteProjet/<int:projet_id>', methods=['POST', 'GET'])
@login_required
def delete_projet(projet_id):
    if not current_user.is_admin:
        abort(403)

    projet = Projet.query.get_or_404(projet_id)

    FactoryController.deleteOne(projet)

    return jsonify(status='OK')


@blueprint.route('/Projet/<int:projet_id>')
@login_required
def page_projet_details(projet_id):
    projet = Projet.query.get_or_404(projet_id)

    return render_template('page_projet.html', projet=projet)


@blueprint.route('/Projet/<int:projet_id>/devis')
@login_required
def page_projet_devis(projet_id):
    projet = Projet.query.get_or_404(projet_id)

    return render_template('page_projet_devis.html', new_version=True, projet=projet)


@blueprint.route('/Projet/<int:projet_id>/devis/nouveau', methods=["GET", "POST"])
@login_required
def add_devis(projet_id):
    projet = Projet.query.get_or_404(projet_id)

    devis = Devis(projet=projet)
    FactoryController.createOne(devis)

    return redirect(url_for("home_blueprint.edit_devis", devis_id=devis.id))


@blueprint.route('/Devis/<int:devis_id>/edit', methods=["GET", "POST"])
@login_required
def edit_devis(devis_id):
    devis = Devis.query.get_or_404(devis_id)
    projet = Projet.query.get_or_404(devis.projet_id)
    form = DevisForm(obj=devis)
    last_devis = Devis.query.filter_by(projet_id=projet.id).filter(Devis.status != 'brouillon').filter(Devis.numero.contains('A')).order_by(Devis.id.desc()).first()

    #last_status = last_devis.status
    #fsn = projet.fsn.split("/")
    #number_fsn = fsn[0]
    #number_fsn = 0

    if form.validate_on_submit():
        devis.info = form.info.data
        devis.status = "Envoyé au client"
        if last_devis:
            lettre ="A"
            last_numero = last_devis.numero
            _numero = last_numero.split("/")
            number_fsn = _numero[2]
            #lettre_fsn = _numero[3]
            #number = ord(lettre_fsn[0])
            #number += 1
            #lettre_fsn = chr(number)
            new_number_fsn = int(number_fsn) + 1
            devis.numero = projet.fsn + '/' + str(new_number_fsn).zfill(3) + '/' + lettre
        else:
            lettre = "A"
            new_number_fsn = "1"
            devis.numero = projet.fsn + '/' + new_number_fsn .zfill(3) + '/' + lettre
        #if last_newdevis:
            #_numero = last_numero.split("/")
            #number_fsn = _numero[0]
            #lettre_fsn = "A"
            #number = ord(lettre_fsn[0])
            #number += 1
            #lettre_fsn = chr(number)
            #devis.numero = projet.fsn + '/' + number_fsn + '/' + lettre_fsn

        FactoryController.commit()
        return redirect(url_for('home_blueprint.page_projet_devis', projet=devis.projet, projet_id=devis.projet_id))
    return render_template('add_devis.html', form=form, edit=True, projet=projet, devis=devis)




@blueprint.route('/deleteDevis/<int:devis_id>', methods=['POST', 'GET'])
@login_required
def delete_devis(devis_id):


    devis = Devis.query.get_or_404(devis_id)
    projet = Projet.query.get_or_404(devis.projet_id)


    FactoryController.deleteOne(devis)

    return redirect(url_for("home_blueprint.page_projet_devis", projet=projet, projet_id=projet.id))


@blueprint.route('/Devis/<int:devis_id>/chapitre/nouveau', methods=["GET", "POST"])
@login_required
def devis_add_chapitre(devis_id):
    devis = Devis.query.get_or_404(devis_id)
    form = ChapitreForm()

    if form.validate_on_submit():
        chapitre = Chapitre(titre=form.titre.data)
        devis.chapitres.append(chapitre)
        FactoryController.commit()

        return redirect(url_for("home_blueprint.edit_devis", devis_id=devis.id))

    return render_template('devis_add_chapitre.html', devis=devis, projet=devis.projet, form=form)




@blueprint.route('/editChapitre/<int:chapitre_id>', methods=['POST', 'GET'])
@login_required
def edit_chapitre(chapitre_id):


    chapitre = Chapitre.query.get_or_404(chapitre_id)
    devis = Devis.query.get_or_404(chapitre.devis_id)
    form = EditChapitreForm(obj=chapitre)

    if form.validate_on_submit():
        chapitre.id = form.id.data
        chapitre.titre = form.titre.data
        FactoryController.commit()

        return redirect(url_for("home_blueprint.edit_devis", devis_id=devis.id))

    return render_template('devis_add_chapitre.html', devis=devis, projet=devis.projet, edit=True, form=form)



@blueprint.route('/deleteChapitre/<int:chapitre_id>', methods=['POST', 'GET'])
@login_required
def delete_chapitre(chapitre_id):

    chapitre = Chapitre.query.get_or_404(chapitre_id)
    devis = Devis.query.get_or_404(chapitre.devis_id)

    FactoryController.deleteOne(chapitre)

    return redirect(url_for("home_blueprint.edit_devis", devis_id=devis.id))

@blueprint.route('/Devis/<int:devis_id>/chapitre/<int:chapitre_id>/article/nouveau', methods=["GET", "POST"])
@blueprint.route('/Devis/<int:devis_id>/article/nouveau', methods=["GET", "POST"])
@login_required
def devis_add_article(devis_id, chapitre_id=None):
    devis = Devis.query.get_or_404(devis_id)
    form = ArticleForm()
    chapitre = None
    if chapitre_id:
        chapitre = Chapitre.query.get_or_404(chapitre_id)

    if form.validate_on_submit():
        article = Article(titre=form.titre.data,
                          info=form.info.data,
                          quantite=form.quantite.data,
                          prix_unitaire=form.prix_unitaire.data,
                          chapitre_id=chapitre_id)

        if chapitre_id:
            chapitre.articles.append(article)
        else:
            devis.articles.append(article)

        devis.recalculate_montant()
        FactoryController.createOne(article)

        return redirect(url_for("home_blueprint.edit_devis", devis_id=devis.id))

    return render_template('devis_add_article.html', projet=devis.projet, devis=devis, chapitre=chapitre,
                           form=form)


@blueprint.route('/editArticle/<int:article_id>', methods=['POST', 'GET'])
@login_required
def edit_article(article_id):


    article = Article.query.get_or_404(article_id)
    devis = Devis.query.get_or_404(article.devis_id)
    form = EditArticleForm(obj=article)

    if form.validate_on_submit():
        article.id = form.id.data
        article.titre = form.titre.data
        article.info = form.info.data
        article.quantite = form.quantite.data
        article.prix_unitaire = form.prix_unitaire.data
        FactoryController.commit()

        return redirect(url_for("home_blueprint.edit_devis", devis_id=devis.id))

    return render_template('devis_add_article.html', devis=devis, projet=devis.projet, edit=True, form=form)



@blueprint.route('/deleteArticle/<int:article_id>', methods=['POST', 'GET'])
@login_required
def delete_article(article_id):


    article = Article.query.get_or_404(article_id)
    devis = Devis.query.get_or_404(article.devis_id)

    FactoryController.deleteOne(article)

    return redirect(url_for("home_blueprint.edit_devis", devis_id=devis.id))

@blueprint.route('/editChapArticle/<int:devis_id>/<int:article_id>', methods=['POST', 'GET'])
@login_required
def edit_chap_article(devis_id, article_id):


    article = Article.query.get_or_404(article_id)
    devis = Devis.query.get_or_404(devis_id)
    form = EditArticleForm(obj=article)

    if form.validate_on_submit():
        article.id = form.id.data
        article.titre = form.titre.data
        article.info = form.info.data
        article.quantite = form.quantite.data
        article.prix_unitaire = form.prix_unitaire.data
        FactoryController.commit()

        return redirect(url_for("home_blueprint.edit_devis", devis_id=devis.id))

    return render_template('devis_add_article.html', devis=devis, projet=devis.projet, edit=True, form=form)


@blueprint.route('/deleteChapArticle/<int:devis_id>/<int:article_id>', methods=['POST', 'GET'])
@login_required
def delete_chap_article(devis_id, article_id):


    article = Article.query.get_or_404(article_id)
    devis = Devis.query.get_or_404(devis_id)

    FactoryController.deleteOne(article)

    return redirect(url_for("home_blueprint.edit_devis", devis_id=devis.id))



@blueprint.route('/Devis/<int:devis_id>/article/<int:parent_article_id>/sous-article/nouveau', methods=["GET", "POST"])
@login_required
def devis_add_sous_article(devis_id, parent_article_id):
    devis = Devis.query.get_or_404(devis_id)
    parent_article = Article.query.get_or_404(parent_article_id)

    form = SousArticleForm()

    if form.validate_on_submit():
        article = Article(titre=form.titre.data,
                          info=form.info.data,
                          quantite=form.quantite.data,
                          prix_unitaire=form.prix_unitaire.data,
                          parent_article_id=parent_article_id)

        devis.recalculate_montant()
        FactoryController.createOne(article)

        return redirect(url_for("home_blueprint.edit_devis", devis_id=devis.id))

    return render_template('devis_add_sous_article.html', devis=devis, parent_article=parent_article,
                           projet=devis.projet, form=form)


@blueprint.route('/editSousArticle/<int:devis_id>/sousarticle/<int:sous_article_id>', methods=['POST', 'GET'])
@login_required
def edit_sous_article(devis_id, sous_article_id):

    sous_article = Article.query.get_or_404(sous_article_id)
    devis = Devis.query.get_or_404(devis_id)
    parent_article = Article.query.get_or_404(sous_article.parent_article_id)
    form = EditSousArticleForm(obj=sous_article)

    if form.validate_on_submit():
        sous_article.titre = form.titre.data
        sous_article.info = form.info.data
        sous_article.quantite = form.quantite.data
        sous_article.prix_unitaire = form.prix_unitaire.data
        FactoryController.commit()

        return redirect(url_for("home_blueprint.edit_devis",  devis_id=devis.id))

    return render_template('devis_add_sous_article.html',  projet=devis.projet, devis=devis, parent_article=parent_article,
                           edit=True, form=form)



@blueprint.route('/editChapSousArticle/<int:devis_id>/sousarticle/<int:sous_article_id>', methods=['POST', 'GET'])
@login_required
def edit_chap_sous_article(devis_id, sous_article_id):


    sous_article = Article.query.get_or_404(sous_article_id)
    devis = Devis.query.get_or_404(devis_id)
    parent_article = Article.query.get_or_404(sous_article.parent_article_id)
    form = EditSousArticleForm(obj=sous_article)

    if form.validate_on_submit():
        sous_article.titre = form.titre.data
        sous_article.info = form.info.data
        sous_article.quantite = form.quantite.data
        sous_article.prix_unitaire = form.prix_unitaire.data
        FactoryController.commit()

        return redirect(url_for("home_blueprint.edit_devis",  devis_id=devis.id))

    return render_template('devis_add_sous_article.html',  projet=devis.projet, devis=devis, parent_article=parent_article,
                           edit=True, form=form)



@blueprint.route('/deleteSousArticle/<int:devis_id>/<int:sous_article_id>', methods=['POST', 'GET'])
@login_required
def delete_sous_article(devis_id, sous_article_id):


    sous_article = Article.query.get_or_404(sous_article_id)
    devis = Devis.query.get_or_404(devis_id)

    FactoryController.deleteOne(sous_article)

    return redirect(url_for("home_blueprint.edit_devis", devis_id=devis.id))




@blueprint.route('/deleteSousArticle/<int:devis_id>/<int:sous_article_id>', methods=['POST', 'GET'])
@login_required
def delete_chap_sous_article(devis_id, sous_article_id):


    sous_article = Article.query.get_or_404(sous_article_id)
    devis = Devis.query.get_or_404(devis_id)

    FactoryController.deleteOne(sous_article)

    return redirect(url_for("home_blueprint.edit_devis", devis_id=devis.id))




@blueprint.route('/devis')
@login_required
def list_devis():


    somme = 0

    devis = Devis.query.all()

    for devi in devis:
        if devi.status == "Envoyé au client":
            somme = somme + 1




    return render_template('devis_list.html', count_devis=somme , page='list_devis')




@blueprint.route('/devisData')
@login_required
def devis_data():


    devis = Devis.query.all()
    devi_array = []
    json_array = []
    for devi in devis:
        if devi.status == "Envoyé au client":
            devi_obj = {
                'id': devi.id,
                'numero': devi.numero,
                'status': devi.status,
                'info': devi.info,
                'projet': devi.projet.id,
                'montant_ht': devi.montant_ht}

            devi_array.append(devi_obj)

    return jsonify(devi_array)





@blueprint.route('/editDevis/<int:devis_id>', methods=["GET", "POST"])
@login_required
def modifier_devis(devis_id):


    devi = Devis.query.get_or_404(devis_id)
    projet = Projet.query.get_or_404(devi.projet_id)
    form = EditDevisForm(obj=devi)

    if form.validate_on_submit():
        devi.chapitres = form.chapitres.data
        devi.articles = form.articles.data
        devi.montant_ht = form.montant_ht.data
        FactoryController.commit()

        return redirect(url_for('home_blueprint.list_devis'))

    return render_template('devis.html', projet=projet, devis=devi, edit=True, form=form)



@blueprint.route('/addnewVersionDevis/<int:devis_id>', methods=["GET", "POST"])
@login_required
def add_new_version_devis(devis_id):

    devis = Devis.query.get_or_404(devis_id)
    clone_devis = Devis(projet=devis.projet)


    numero_devis = devis.numero

    _numero = numero_devis.split("/")
    fsn = devis.projet.fsn

    number_fsn = _numero[2]
    lettre_fsn = _numero[3]
    number = ord(lettre_fsn[0])
    number += 1
    lettre_fsn = chr(number)



    clone_devis.status ="Brouillon"
    clone_devis.info = devis.info
    clone_devis.numero= fsn + '/' + number_fsn + '/' + lettre_fsn
    clone_devis.montant_ht = devis.montant_ht

    for chapitre in devis.chapitres:
        clone_chapitre = Chapitre(titre=chapitre.titre)
        clone_devis.chapitres.append(clone_chapitre)
        for article in chapitre.articles:
            clone_article = Article(titre=article.titre,
                                    info=article.info,
                                    quantite=article.quantite,
                                    prix_unitaire=article.prix_unitaire)
            clone_chapitre.articles.append(clone_article)
            for sous_article in article.sous_articles:
                clone_sous_article = Article(titre=sous_article.titre,
                                             info=sous_article.info,
                                             quantite=sous_article.quantite,
                                             prix_unitaire=sous_article.prix_unitaire)
                clone_article.sous_articles.append(clone_sous_article)

    for article in devis.articles:
        clone_article = Article(titre=article.titre,
                                info=article.info,
                                quantite=article.quantite,
                                prix_unitaire=article.prix_unitaire)
        clone_devis.articles.append(clone_article)
        for sous_article in article.sous_articles:
            clone_sous_article = Article(titre=sous_article.titre,
                                    info=sous_article.info,
                                    quantite=sous_article.quantite,
                                    prix_unitaire=sous_article.prix_unitaire)
            clone_article.sous_articles.append(clone_sous_article)

    FactoryController.createOne(clone_devis)

    return redirect(url_for("home_blueprint.edit_new_devis", devis_id=clone_devis.id))






@blueprint.route('/newDevis/<int:devis_id>/edit', methods=["GET", "POST"])
@login_required
def edit_new_devis(devis_id):
    devis = Devis.query.get_or_404(devis_id)
    projet = Projet.query.get_or_404(devis.projet_id)
    form = DevisForm(obj=devis)
    last_devis = Devis.query.filter_by(projet_id=projet.id).filter(Devis.status == 'brouillon').order_by(Devis.id.desc()).first()

    #last_status = last_devis.status
    #fsn = projet.fsn.split("/")
    #number_fsn = fsn[0]
    #number_fsn = 0

    if form.validate_on_submit():
        devis.info = form.info.data
        devis.status = "Envoyé au client"
        devis.numero = last_devis.numero
        #if last_newdevis:
            #_numero = last_numero.split("/")
            #number_fsn = _numero[0]
            #lettre_fsn = "A"
            #number = ord(lettre_fsn[0])
            #number += 1
            #lettre_fsn = chr(number)
            #devis.numero = projet.fsn + '/' + number_fsn + '/' + lettre_fsn

        FactoryController.commit()
        return redirect(url_for('home_blueprint.page_projet_devis', projet=devis.projet, projet_id=devis.projet_id))
    return render_template('add_new_version_devis.html', form=form,  projet=projet, devis=devis)




@blueprint.route('/delete_new_versionDevis/<int:devis_id>', methods=['POST', 'GET'])
@login_required
def delete_new_version_devis(devis_id):


    devis = Devis.query.get_or_404(devis_id)
    projet = Projet.query.get_or_404(devis.projet_id)


    FactoryController.deleteOne(devis)

    return redirect(url_for("home_blueprint.page_projet_devis", projet=projet, projet_id=projet.id))



@blueprint.route('/new_version_Devis/<int:devis_id>/chapitre/nouveau', methods=["GET", "POST"])
@login_required
def new_version_devis_add_chapitre(devis_id):
    devis = Devis.query.get_or_404(devis_id)
    form = ChapitreForm()

    if form.validate_on_submit():
        chapitre = Chapitre(titre=form.titre.data)
        devis.chapitres.append(chapitre)
        FactoryController.commit()

        return redirect(url_for("home_blueprint.edit_new_devis", devis_id=devis.id))

    return render_template('new_version_devis_add_chapitre.html', devis=devis, projet=devis.projet, form=form)



@blueprint.route('/edit_new_version_Chapitre/<int:chapitre_id>', methods=['POST', 'GET'])
@login_required
def edit_new_version_chapitre(chapitre_id):


    chapitre = Chapitre.query.get_or_404(chapitre_id)
    devis = Devis.query.get_or_404(chapitre.devis_id)
    form = EditChapitreForm(obj=chapitre)

    if form.validate_on_submit():
        chapitre.id = form.id.data
        chapitre.titre = form.titre.data
        FactoryController.commit()

        return redirect(url_for("home_blueprint.edit_new_devis", devis_id=devis.id))

    return render_template('new_version_devis_add_chapitre.html', devis=devis, projet=devis.projet, edit=True, form=form)




@blueprint.route('/delete_new_version_Chapitre/<int:chapitre_id>', methods=['POST', 'GET'])
@login_required
def delete_new_version_chapitre(chapitre_id):


    chapitre = Chapitre.query.get_or_404(chapitre_id)
    devis = Devis.query.get_or_404(chapitre.devis_id)

    FactoryController.deleteOne(chapitre)

    return redirect(url_for("home_blueprint.edit_new_devis", devis_id=devis.id))



@blueprint.route('/new_version_Devis/<int:devis_id>/chapitre/<int:chapitre_id>/article/nouveau', methods=["GET", "POST"])
@blueprint.route('/new_version_Devis/<int:devis_id>/article/nouveau', methods=["GET", "POST"])
@login_required
def new_version_devis_add_article(devis_id, chapitre_id=None):
    devis = Devis.query.get_or_404(devis_id)
    form = ArticleForm()
    chapitre = None
    if chapitre_id:
        chapitre = Chapitre.query.get_or_404(chapitre_id)

    if form.validate_on_submit():
        article = Article(titre=form.titre.data,
                          info=form.info.data,
                          quantite=form.quantite.data,
                          prix_unitaire=form.prix_unitaire.data,
                          chapitre_id=chapitre_id)

        if chapitre_id:
            chapitre.articles.append(article)
        else:
            devis.articles.append(article)

        devis.recalculate_montant()
        FactoryController.createOne(article)

        return redirect(url_for("home_blueprint.edit_new_devis", devis_id=devis.id))

    return render_template('new_version_devis_add_article.html', projet=devis.projet, devis=devis, chapitre=chapitre,
                           form=form)


@blueprint.route('/edit_new_version_Article/<int:article_id>', methods=['POST', 'GET'])
@login_required
def edit_new_version_article(article_id):


    article = Article.query.get_or_404(article_id)
    devis = Devis.query.get_or_404(article.devis_id)
    form = EditArticleForm(obj=article)

    if form.validate_on_submit():
        article.id = form.id.data
        article.titre = form.titre.data
        article.info = form.info.data
        article.quantite = form.quantite.data
        article.prix_unitaire = form.prix_unitaire.data
        FactoryController.commit()

        return redirect(url_for("home_blueprint.edit_new_devis", devis_id=devis.id))

    return render_template('new_version_devis_add_article.html', devis=devis, projet=devis.projet, edit=True, form=form)




@blueprint.route('/delete_new_version_Article/<int:article_id>', methods=['POST', 'GET'])
@login_required
def delete_new_version_article(article_id):

    article = Article.query.get_or_404(article_id)
    devis = Devis.query.get_or_404(article.devis_id)

    FactoryController.deleteOne(article)

    return redirect(url_for("home_blueprint.edit_new_devis", devis_id=devis.id))



@blueprint.route('/editnewversionChapArticle/<int:devis_id>/<int:article_id>', methods=['POST', 'GET'])
@login_required
def edit_new_version_chap_article(devis_id, article_id):


    article = Article.query.get_or_404(article_id)
    devis = Devis.query.get_or_404(devis_id)
    form = EditArticleForm(obj=article)

    if form.validate_on_submit():
        article.id = form.id.data
        article.titre = form.titre.data
        article.info = form.info.data
        article.quantite = form.quantite.data
        article.prix_unitaire = form.prix_unitaire.data
        FactoryController.commit()

        return redirect(url_for("home_blueprint.edit_new_devis", devis_id=devis.id))

    return render_template('new_version_devis_add_article.html', devis=devis, projet=devis.projet, edit=True, form=form)




@blueprint.route('/deletenewversionChapArticle/<int:devis_id>/<int:article_id>', methods=['POST', 'GET'])
@login_required
def delete_new_version_chap_article(devis_id, article_id):


    article = Article.query.get_or_404(article_id)
    devis = Devis.query.get_or_404(devis_id)

    FactoryController.deleteOne(article)

    return redirect(url_for("home_blueprint.edit_new_devis", devis_id=devis.id))



@blueprint.route('/new_version_Devis/<int:devis_id>/article/<int:parent_article_id>/sous-article/nouveau', methods=["GET", "POST"])
@login_required
def new_version_devis_add_sous_article(devis_id, parent_article_id):
    devis = Devis.query.get_or_404(devis_id)
    parent_article = Article.query.get_or_404(parent_article_id)

    form = SousArticleForm()

    if form.validate_on_submit():
        article = Article(titre=form.titre.data,
                          info=form.info.data,
                          quantite=form.quantite.data,
                          prix_unitaire=form.prix_unitaire.data,
                          parent_article_id=parent_article_id)

        devis.recalculate_montant()
        FactoryController.createOne(article)

        return redirect(url_for("home_blueprint.edit_new_devis", devis_id=devis.id))

    return render_template('new_version_devis_add_sous_article.html', devis=devis, parent_article=parent_article,
                           projet=devis.projet, form=form)




@blueprint.route('/edit_new_version_SousArticle/<int:devis_id>/sousarticle/<int:sous_article_id>', methods=['POST', 'GET'])
@login_required
def edit_new_version_sous_article(devis_id, sous_article_id):

    sous_article = Article.query.get_or_404(sous_article_id)
    devis = Devis.query.get_or_404(devis_id)
    parent_article = Article.query.get_or_404(sous_article.parent_article_id)
    form = EditSousArticleForm(obj=sous_article)

    if form.validate_on_submit():
        sous_article.titre = form.titre.data
        sous_article.info = form.info.data
        sous_article.quantite = form.quantite.data
        sous_article.prix_unitaire = form.prix_unitaire.data
        FactoryController.commit()

        return redirect(url_for("home_blueprint.edit_new_devis",  devis_id=devis.id))

    return render_template('new_version_devis_add_sous_article.html',  projet=devis.projet, devis=devis, parent_article=parent_article,
                           edit=True, form=form)




@blueprint.route('/edit_new_version_ChapSousArticle/<int:devis_id>/sousarticle/<int:sous_article_id>', methods=['POST', 'GET'])
@login_required
def edit_new_version_chap_sous_article(devis_id, sous_article_id):

    sous_article = Article.query.get_or_404(sous_article_id)
    devis = Devis.query.get_or_404(devis_id)
    parent_article = Article.query.get_or_404(sous_article.parent_article_id)
    form = EditSousArticleForm(obj=sous_article)

    if form.validate_on_submit():
        sous_article.titre = form.titre.data
        sous_article.info = form.info.data
        sous_article.quantite = form.quantite.data
        sous_article.prix_unitaire = form.prix_unitaire.data
        FactoryController.commit()

        return redirect(url_for("home_blueprint.edit_new_devis",  devis_id=devis.id))

    return render_template('new_version_devis_add_sous_article.html',  projet=devis.projet, devis=devis, parent_article=parent_article,
                           edit=True, form=form)



@blueprint.route('/delete_new_version_SousArticle/<int:devis_id>/<int:sous_article_id>', methods=['POST', 'GET'])
@login_required
def delete_new_version_sous_article(devis_id, sous_article_id):

    sous_article = Article.query.get_or_404(sous_article_id)
    devis = Devis.query.get_or_404(devis_id)

    FactoryController.deleteOne(sous_article)

    return redirect(url_for("home_blueprint.edit_new_devis", devis_id=devis.id))




@blueprint.route('/delete_new_version_SousArticle/<int:devis_id>/<int:sous_article_id>', methods=['POST', 'GET'])
@login_required
def delete_new_version_chap_sous_article(devis_id, sous_article_id):

    sous_article = Article.query.get_or_404(sous_article_id)
    devis = Devis.query.get_or_404(devis_id)

    FactoryController.deleteOne(sous_article)

    return redirect(url_for("home_blueprint.edit_new_devis", devis_id=devis.id))


@blueprint.route('/get_pdf/<devis_id>/<projet_id>', methods=['POST', 'GET'])
@login_required
def get_pdf(devis_id, projet_id):
    projet = Projet.query.get_or_404(projet_id)
    devis = Devis.query.get_or_404(devis_id)
    form = DevisForm()
    rendered = render_template("invoice.html", devis=devis, projet=projet, form=form)

    config = pdfkit.configuration(wkhtmltopdf='C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')


    pdf = pdfkit.from_string(rendered, False, configuration=config)

    response = make_response(pdf)
    response.headers['content-Type'] = 'application/pdf'
    response.headers['content-Disposition'] = 'attachement; filename=Devis.pdf'
    return response



# @blueprint.route('/add_unite', methods=['POST', 'GET'])
# @login_required
# def add_unite():
#     form = UniteForm()
#     if form.validate_on_submit():
#         unite = Unite(
#               unite=form.unite.data)
#         db.session.add(unite)
#         db.session.commit()
#
#         flash("l'ajout a bient été enregistré !")
#
#         return redirect(url_for('home_blueprint.add_unite'))
#
#     return render_template('add_unite.html', form=form, page='add_unite')
#
# @blueprint.route('unites')
# @login_required
# def list_unites():
#     if not current_user.is_admin:
#         abort(403)
#
#     count_unites = Unite.query.count()
#
#     return render_template('unites_list.html', count_unites=count_unites, page='list_unites')
#
# @blueprint.route('/unitesData')
# @login_required
# def unites_data():
#     if not current_user.is_admin:
#         abort(403)
#
#
#     unites = Unite.query.all()
#     unite_array = []
#     json_array = []
#     for unite in unites:
#         unite_obj = {
#             'id ': unite.id,
#             'unite': unite.unite}
#
#         unite_array.append(unite_obj)
#
#     return jsonify(unite_array)


# @blueprint.route('/add_devis', methods=['POST', 'GET'])
# @login_required
# def add_devis():
#     form = DevisForm(request.form)
#     formset = ArticleForm(request.form)
#     if form.validate_on_submit():
#         devis = Devis(
#             projet=form.projet.data
#         )
#     if formset.validate_on_submit():
#         total = 0
#         for form in formset:
#             article = request.form.get('article')
#             unite = request.form.get('unite')
#             quantite = request.form.get('quantite')
#             prix_unitaire = request.form.get('prix_unitaire')
#             if article and unite and quantite and prix_unitaire:
#                 prix_total = float(quantite) * float(prix_unitaire)
#                 total += float(prix_total)
#                 article = Article(
#                     project=devis,
#                     article=formset.article.data,
#                     unit=formset.unite.data,
#                     quantite=formset.quantite.data,
#                     prix_unitaire=formset.prix_unitaire.data
#                 )
#                 db.session.add(article)
#                 db.session.commit()
#
#         devis.montant_ht = total
#
#         db.session.add(devis)
#         db.session.commit()
#
#         flash("l'ajout a bient été enregistré !")
#
#         return redirect(url_for('home_blueprint.add_devis'))
#
#     return render_template('add_devis.html', formset=formset, form=form, page='add_devis')