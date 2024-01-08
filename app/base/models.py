# -*- encoding: utf-8 -*-
import enum
from lib2to3.pytree import Base
from multiprocessing.connection import Client
from tokenize import String

from flask_admin.contrib.sqla.fields import QuerySelectField
from flask_login import UserMixin
from app import db, login_manager


import datetime
from app.base.tools import hash_pass
import secrets


from sqlalchemy import ForeignKey, Column, Integer, insert
from sqlalchemy.orm import relationship
from sqlalchemy.sql.elements import Null
from sqlalchemy.sql.functions import now


@login_manager.user_loader
def user_loader(id):
    return User.query.filter_by(id=id).first()


# @login_manager.request_loader
# def request_loader(request):
#     username = request.form.get('username')
#     user = User.query.filter_by(username=username).first()
#     return user if user else None


############## MIXINS ##############################################

class TimestampMixin(object):
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

############## Models ##############################################


class User(db.Model, UserMixin, TimestampMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    first_name = db.Column(db.String(60), index=True, unique=True)
    last_name = db.Column(db.String(60), index=True, unique=True)
    password = db.Column(db.String(128))
    password_reset_token = db.Column(db.String(128))
    password_reset_expires = db.Column(db.DateTime)
    activation_token = db.Column(db.String(128))

    is_admin = db.Column(db.Boolean, default=False)

    last_seen = db.Column(db.DateTime, server_default=db.func.now())
    is_active = db.Column(db.Boolean, default=False)

    projets = db.relationship("Projet", back_populates="agent")

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            if property == 'password':
                value = hash_pass(value)  # hash the password

            setattr(self, property, value)

    def __repr__(self):
        return f"<User {self.id} - {self.email}>"

    def change_password(self, newPassword):
        self.password = hash_pass(newPassword)

    def generate_forgot_token(self):
        token = secrets.token_urlsafe(16)
        token_exp_minutes = 10
        self.password_reset_token = token
        self.password_reset_expires = datetime.datetime.now(
        ) + datetime.timedelta(minutes=token_exp_minutes)

    def generate_activation_token(self):
        token = secrets.token_urlsafe(16)
        self.activation_token = token

    @property
    def get_name(self):
        return f"{self.first_name} {self.last_name}"







class Contact(db.Model):
    __tablename__ = 'contacts'
    id = db.Column(Integer, primary_key=True)
    tel1 = db.Column(db.String(60), index=True, unique=True)
    tel2 = db.Column(db.String(60), index=True, unique=True)
    fax = db.Column(db.String(60), index=True, unique=True)
    email = db.Column(db.String(60), index=True, unique=True)
    adresse = db.Column(db.String(128), index=True)
    is_client = db.Column(db.Boolean, default=False)
    genre = db.Column(db.String(50), nullable=True)

    client_projets = db.relationship("Projet", back_populates="client")

    __mapper_args__ = {
        'polymorphic_identity': 'contacts',
        'polymorphic_on': genre
    }


class Societe(Contact):
    __tablename__ = 'societes'
    id = db.Column(db.Integer, db.ForeignKey('contacts.id'), primary_key=True)
    nom = db.Column(db.String(60), index=True, unique=True)
    type = db.Column(db.String(60), index=True)
    domaine = db.Column(db.String(60), index=True)

    __mapper_args__ = {
        'polymorphic_identity': 'societes',
    }

    @property
    def get_name(self):
        return f"{self.nom}"


class Personne(Contact):
    __tablename__ = 'personnes'
    id = db.Column(db.Integer, db.ForeignKey('contacts.id'), primary_key=True)
    nom = db.Column(db.String(128), index=True)
    prenom = db.Column(db.String(128), index=True)
    profession = db.Column(db.String(128), index=True)

    __mapper_args__ = {
        'polymorphic_identity': 'personnes',
    }

    @property
    def get_name(self):
        return f"{self.nom} {self.prenom}"


class Administration(Contact):
    __tablename__ = 'administrations'
    id = db.Column(db.Integer, db.ForeignKey('contacts.id'), primary_key=True)
    nom = db.Column(db.String(60), index=True, unique=True)
    type = db.Column(db.String(60), index=True)
    domaine = db.Column(db.String(60), index=True)

    __mapper_args__ = {
        'polymorphic_identity': 'administrations',
    }

    @property
    def get_name(self):
        return f"{self.nom}"


class Prestation(db.Model):
    __tablename__ = 'prestations'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type_prestation = db.Column(db.String(60), index=True, unique=True)
    code_prestation = db.Column(db.String(60), index=True, unique=True)
    projets = db.relationship("Projet", back_populates="prestation")


class Ouvrage(db.Model):
    __tablename__ = 'ouvrages'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type_ouvrage = db.Column(db.String(60), index=True, unique=True)
    code_ouvrage = db.Column(db.String(60), index=True, unique=True)
    projets = db.relationship("Projet", back_populates="ouvrage")


class Projet(db.Model, TimestampMixin):
    __tablename__ = 'projets'

    id = db.Column(db.Integer, primary_key=True)

    titre = db.Column(db.String(60), index=True)
    fsn = db.Column(db.String(8), unique=True, default="000/21")
    date = db.Column(db.Date)
    state = db.Column(db.String(24))

    prestation_id = db.Column(db.Integer, db.ForeignKey('prestations.id'))
    prestation = db.relationship("Prestation", back_populates="projets")

    ouvrage_id = db.Column(db.Integer, db.ForeignKey('ouvrages.id'))
    ouvrage = db.relationship("Ouvrage", back_populates="projets")

    client_id = db.Column(Integer, db.ForeignKey('contacts.id'))
    client = db.relationship("Contact", back_populates="client_projets")

    agent_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    agent = db.relationship("User", back_populates="projets")

    list_devis = db.relationship("Devis", back_populates="projet")

    def __init__(self,   **kwargs):
        now = datetime.datetime.now()
        year = now.strftime("%y")
        new_fsn = ""
        last_projet = Projet.query.order_by(Projet.id.desc()).first()
        if last_projet:
            last_fsn = last_projet.fsn
            _fsn = last_fsn.split("/")
            number_fsn = _fsn[0]
            year_fsn = _fsn[1]
            if year == year_fsn:
                new_number_fsn = int(number_fsn) + 1
                new_fsn = str(new_number_fsn).zfill(3) + "/" + year
            elif year_fsn < year:
                new_number_fsn = "1"
                new_fsn = new_number_fsn .zfill(3) + "/" + year
        else:
            new_number_fsn = "1"
            new_fsn = new_number_fsn .zfill(3) + "/" + year

        self.fsn = new_fsn
        self.state = "Fiche de suivi"

        super().__init__(**kwargs)


class Devis(db.Model, TimestampMixin):
    __tablename__ = 'devis'

    id = db.Column(db.Integer, primary_key=True)

    status = db.Column(db.String(20), default="Brouillon")
    numero = db.Column(db.String(20))

    projet_id = db.Column(db.Integer, db.ForeignKey("projets.id"))
    projet = db.relationship("Projet", back_populates="list_devis")

    info = db.Column(db.String(255))
    montant_ht = db.Column(db.Float, default=0)

    chapitres = db.relationship("Chapitre", cascade="all, delete")
    articles = db.relationship("Article", cascade="all, delete")

    def __init__(self, projet):

        self.projet = projet
        self.numero = f"{self.projet.fsn}/Draft"

    def recalculate_montant(self):
        montant_ht = 0
        for chapitre in self.chapitres:
            for chapitre_article in chapitre.articles:
                montant_ht = float(montant_ht) + float(chapitre_article.prix_total)

        for article in self.articles:
            montant_ht = float(montant_ht) + float(article.prix_total)

        self.montant_ht = montant_ht


class Article(db.Model, TimestampMixin):
    __tablename__ = 'articles'

    id = db.Column(db.Integer, primary_key=True)
    devis_id = db.Column(db.Integer, db.ForeignKey('devis.id', ondelete="cascade"))

    titre = db.Column(db.String(128), index=True)
    info = db.Column(db.String(255))
    quantite = db.Column(db.Integer)
    prix_unitaire = db.Column(db.Float)
    prix_total = db.Column(db.Float)

    parent_article_id = db.Column(db.Integer, db.ForeignKey('articles.id', ondelete="cascade"))
    sous_articles = db.relationship("Article", cascade="all, delete")

    chapitre_id = db.Column(db.Integer, db.ForeignKey('chapitres.id', ondelete="cascade"))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.quantite and self.prix_unitaire:
            self.prix_total = self.quantite * self.prix_unitaire


class Chapitre(db.Model, TimestampMixin):
    __tablename__ = 'chapitres'

    id = db.Column(db.Integer, primary_key=True)
    devis_id = db.Column(db.Integer, db.ForeignKey("devis.id", ondelete="cascade"))

    titre = db.Column(db.String(128))

    articles = db.relationship("Article", cascade="all, delete")


class DefaultArticle(db.Model):
    __tablename__ = 'default_articles'

    id = db.Column(db.Integer, primary_key=True)

    titre = db.Column(db.String(128), index=True)
    description = db.Column(db.String(255))

    prix_unitaire = db.Column(db.Float, default=0)

    parent_article_id = db.Column(db.Integer, db.ForeignKey('default_articles.id', ondelete="cascade"))
    sous_article = db.relationship("DefaultArticle", cascade="all, delete")

    chapitre_id = db.Column(db.Integer, db.ForeignKey('default_chapitres.id', ondelete="cascade"))


class DefaultChapitre(db.Model):
    __tablename__ = 'default_chapitres'

    id = db.Column(db.Integer, primary_key=True)

    titre = db.Column(db.String(128), index=True)

    articles = db.relationship("DefaultArticle", cascade="all, delete")