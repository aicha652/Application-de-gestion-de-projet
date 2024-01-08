from flask_admin.contrib.sqla.fields import QuerySelectField
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, DateField, SelectField,\
    DecimalField, HiddenField, IntegerField, FieldList, FormField, TextAreaField
from wtforms import ValidationError, validators
from wtforms.validators import Email, DataRequired, EqualTo, Optional

from app.base.models import User, Societe, Personne, Administration, Prestation, Ouvrage,\
    Contact, Projet, Article, Chapitre, Devis


class UserForm(FlaskForm):
    first_name = StringField("Prénom",
                             validators=[DataRequired()])
    last_name = StringField("Nom",
                            validators=[DataRequired()])

    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Mot de passe',
                             id='pwd_create',
                             validators=[DataRequired(),
                                         EqualTo('confirm_password',
                                                 message='Le mot de passe de confirmation est incorrect'),
                                         validators.Length(min=8,
                                                           message='Mot de passe doit '
                                                                   'contenir au moins 8 caractère !')])
    confirm_password = PasswordField('Confirm Password')
    is_admin = BooleanField('Administrateur', default=False)
    is_active = BooleanField('Activer', default=True)

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Cet email est déjà enregistré !')


class EditUserForm(FlaskForm):
    first_name = StringField("Prénom",
                             validators=[DataRequired()])
    last_name = StringField("Nom",
                            validators=[DataRequired()])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])

    is_admin = BooleanField('Administrateur', default=False)
    is_active = BooleanField('Activer', default=True)


villes_choices = [('Casablanca', 'Casablanca'), ('Rabat', 'Rabat'), ('Tanger', 'Tanger'), ('Agadir', 'Agadir'),
                  ('Ben Guerir', 'Ben Guerir'), ('Dakhla', 'Dakhla'),
                  ('El Jadida', 'El Jadida'), ('Fès', 'Fès'), ('Guelmim', 'Guelmim'), ('Ifrane', 'Ifrane'),
                  ('Khouribga', 'Khouribga'), ('Laayoune', 'Laayoune'),
                  ('Marrakech', 'Marrakech'), ('Nador', 'Nador'), ('Oujda', 'Oujda'), ('Salé', 'Salé'),
                  ('Tétouan', 'Tétouan'),
                  ('Youssoufia', 'Youssoufia'), ('Zagora', 'Zagora ')]


class SocieteForm(FlaskForm):
    nom = StringField("Nom",
                      validators=[DataRequired()])
    type = StringField("Type",
                       validators=[DataRequired()])

    domaine = StringField('Domaine',
                          validators=[DataRequired()])

    tel1 = StringField('Tel1',
                       validators=[DataRequired()])

    tel2 = StringField('Tel2',
                       validators=[DataRequired()])

    fax = StringField('Fax',
                      validators=[DataRequired()])

    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    adresse = StringField('Adresse',
                          validators=[DataRequired()])

    def validate_nom(self, field):
        if Societe.query.filter_by(nom=field.data).first():
            raise ValidationError('Cette société déja existe !')

    def validate_tel1(self, field):
        if Societe.query.filter_by(tel1=field.data).first():
            raise ValidationError('Ce N° de téléphone déja existe !')

    def validate_tel2(self, field):
        if Societe.query.filter_by(tel2=field.data).first():
            raise ValidationError('Ce N° de téléphone déja existe !')

    def validate_fax(self, field):
        if Societe.query.filter_by(fax=field.data).first():
            raise ValidationError('Fax déja existe !')

    def validate_email(self, field):
        if Societe.query.filter_by(email=field.data).first():
            raise ValidationError('Cet email est déjà enregistré !')


class EditSocieteForm(FlaskForm):
    id = StringField("id",
                     validators=[DataRequired()])
    nom = StringField("Nom",
                      validators=[DataRequired()])
    type = StringField("Type",
                       validators=[DataRequired()])

    domaine = StringField('Domaine',
                          validators=[DataRequired()])

    tel1 = StringField('Tel1',
                       validators=[DataRequired()])

    tel2 = StringField('Tel2',
                       validators=[DataRequired()])

    fax = StringField('Fax',
                      validators=[DataRequired()])

    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    adresse = StringField('Adresse',
                          validators=[DataRequired()])


class PersonneForm(FlaskForm):
    nom = StringField("Nom",
                      validators=[DataRequired()])
    prenom = StringField("Prénom",
                         validators=[DataRequired()])
    profession = StringField('Profession',
                             validators=[DataRequired()])

    tel1 = StringField('Tel1',
                       validators=[DataRequired()])

    tel2 = StringField('Tel2',
                       validators=[DataRequired()])

    fax = StringField('Fax',
                      validators=[DataRequired()])

    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    adresse = StringField('Adresse',
                          validators=[DataRequired()])

    def validate_tel1(self, field):
        if Personne.query.filter_by(tel1=field.data).first():
            raise ValidationError('Ce N° de téléphone déja existe !')

    def validate_tel2(self, field):
        if Personne.query.filter_by(tel2=field.data).first():
            raise ValidationError('Ce N° de téléphone déja existe !')

    def validate_fax(self, field):
        if Personne.query.filter_by(fax=field.data).first():
            raise ValidationError('Fax déja existe !')

    def validate_email(self, field):
        if Personne.query.filter_by(email=field.data).first():
            raise ValidationError('Cet émail déja existe !')


class EditPersonneForm(FlaskForm):
    id = StringField("id",
                     validators=[DataRequired()])
    nom = StringField("Nom",
                      validators=[DataRequired()])
    prenom = StringField("Prénom",
                         validators=[DataRequired()])

    profession = StringField('Profession',
                             validators=[DataRequired()])

    tel1 = StringField('Tel1',
                       validators=[DataRequired()])

    tel2 = StringField('Tel2',
                       validators=[DataRequired()])

    fax = StringField('Fax',
                      validators=[DataRequired()])

    email = StringField('Email',
                        validators=[DataRequired(), Email()])

    adresse = StringField('Adresse',
                          validators=[DataRequired()])


class AdministrationForm(FlaskForm):
    nom = StringField("Nom",
                      validators=[DataRequired()])
    type = StringField("Type",
                       validators=[DataRequired()])

    domaine = StringField('Domaine',
                          validators=[DataRequired()])

    tel1 = StringField('Tel1',
                       validators=[DataRequired()])

    tel2 = StringField('Tel2',
                       validators=[DataRequired()])

    fax = StringField('Fax',
                      validators=[DataRequired()])

    email = StringField('Email',
                        validators=[DataRequired(), Email()])

    adresse = StringField('Adresse',
                          validators=[DataRequired()])

    def validate_nom(self, field):
        if Administration.query.filter_by(nom=field.data).first():
            raise ValidationError('Ce nom déja existe !')

    def validate_tel1(self, field):
        if Administration.query.filter_by(tel1=field.data).first():
            raise ValidationError('Ce N° de téléphone déja existe !')

    def validate_tel2(self, field):
        if Administration.query.filter_by(tel2=field.data).first():
            raise ValidationError('Ce N° de téléphone déja existe !')

    def validate_fax(self, field):
        if Administration.query.filter_by(fax=field.data).first():
            raise ValidationError('Fax déja existe !')

    def validate_email(self, field):
        if Administration.query.filter_by(email=field.data).first():
            raise ValidationError('Cet email est déjà enregistré !')


class EditAdministrationForm(FlaskForm):
    id = StringField("id",
                     validators=[DataRequired()])
    nom = StringField("Nom",
                      validators=[DataRequired()])
    type = StringField("Type",
                       validators=[DataRequired()])

    domaine = StringField('Domaine',
                          validators=[DataRequired()])

    tel1 = StringField('Tel1',
                       validators=[DataRequired()])

    tel2 = StringField('Tel2',
                       validators=[DataRequired()])

    fax = StringField('Fax',
                      validators=[DataRequired()])

    email = StringField('Email',
                        validators=[DataRequired(), Email()])

    adresse = StringField('Adresse',
                          validators=[DataRequired()])


class PrestationForm(FlaskForm):
    type_prestation = StringField("Type de prestation",
                                  validators=[DataRequired()])
    code_prestation = StringField("code de prestation",
                                  validators=[DataRequired(),
                                              validators.Length(max=2,
                                                                message='code prestation doit contenir au maximum 2 caractère !')])

    def validate_type_prestation(self, field):
        if Prestation.query.filter_by(type_prestation=field.data).first():
            raise ValidationError('Ce type déja existe !')

    def validate_code_prestation(self, field):
        if Prestation.query.filter_by(code_prestation=field.data).first():
            raise ValidationError('Ce code déja existe !')


class OuvrageForm(FlaskForm):
    type_ouvrage = StringField("Type d'ouvrage",
                               validators=[DataRequired()])
    code_ouvrage = StringField("Code d'ouvrage",
                               validators=[DataRequired(),
                                           validators.Length(max=2,
                                                             message='code ouvrage doit contenir au maximum 2 caractère !')])

    def validate_type_ouvrage(self, field):
        if Ouvrage.query.filter_by(type_ouvrage=field.data).first():
            raise ValidationError('Ce type déja existe !')

    def validate_code_ouvrage(self, field):
        if Ouvrage.query.filter_by(code_ouvrage=field.data).first():
            raise ValidationError('Ce code déja existe !')


class EditPrestationForm(FlaskForm):

    type_prestation = StringField("type_prestation",
                                  validators=[DataRequired()])
    code_prestation = StringField("code_prestation",
                                  validators=[DataRequired(),
                                              validators.Length(max=2,
                                                                message='code prestation doit contenir au maximum 2 caractère !')])


class EditOuvrageForm(FlaskForm):

    type_ouvrage = StringField("type_ouvrage",
                               validators=[DataRequired()])
    code_ouvrage = StringField("code_ouvrage",
                               validators=[DataRequired(),
                                           validators.Length(max=2,
                                                             message='code ouvrage doit contenir au maximum 2 caractère !')])


def get_prestation_label(prestation):
    return f"{prestation.code_prestation} - {prestation.type_prestation}"


def get_ouvrage_label(ouvrage):
    return f"{ouvrage.code_ouvrage} - {ouvrage.type_ouvrage}"


def get_agent_label(user):
    return f"{user.first_name} {user.last_name}"


class ProjetForm(FlaskForm):
    titre = StringField("Titre du projet", validators=[DataRequired()])

    prestation = QuerySelectField("Type de prestation",
                                  query_factory=lambda: Prestation.query.order_by(Prestation.code_prestation).all(),
                                  get_label=get_prestation_label)
    ouvrage = QuerySelectField("Type d'ouvrage",
                               query_factory=lambda: Ouvrage.query.order_by(Ouvrage.code_ouvrage).all(),
                               get_label=get_ouvrage_label)
    client_id = HiddenField()
    date = StringField('Date', validators=[DataRequired()])
    agent = QuerySelectField("Agent de suivi",
                             query_factory=lambda: User.query.order_by(User.first_name).all(),
                             get_label=get_agent_label)


class EditProjetForm(FlaskForm):

    titre = StringField("Titre du projet",
                     validators=[DataRequired()])

    prestation = QuerySelectField("Type de prestation",
                                  query_factory=lambda: Prestation.query.order_by(Prestation.code_prestation).all(),
                                  get_label=get_prestation_label)
    ouvrage = QuerySelectField("Type d'ouvrage",
                               query_factory=lambda: Ouvrage.query.order_by(Ouvrage.code_ouvrage).all(),
                               get_label=get_ouvrage_label)
    date = StringField('Date',
                       validators=[DataRequired()])
    agent = QuerySelectField("Agent de suivi",
                             query_factory=lambda: User.query.order_by(User.first_name).all(),
                             get_label=get_agent_label)


def devis_chapitre(current_devis_id):
    return Chapitre.query.filter_by(devis_id=current_devis_id)


class ArticleForm(FlaskForm):

    titre = StringField("Article", validators=[DataRequired()])
    info = TextAreaField("Informations supplémentaires", validators=[Optional()])
    quantite = IntegerField("Quantité", validators=[DataRequired()])
    prix_unitaire = DecimalField("prix", places=2, validators=[DataRequired()])


class EditArticleForm(FlaskForm):
    id = StringField("id", validators=[DataRequired()])
    titre = StringField("Article", validators=[DataRequired()])
    info = TextAreaField("Informations supplémentaires", validators=[Optional()])
    quantite = IntegerField("Quantité", validators=[DataRequired()])
    prix_unitaire = DecimalField("prix", places=2, validators=[DataRequired()])



class SousArticleForm(FlaskForm):

    titre = StringField("Sous article", validators=[DataRequired()])
    info = TextAreaField("Informations supplémentaires", validators=[Optional()])
    quantite = IntegerField("Quantité", validators=[Optional()])
    prix_unitaire = DecimalField("prix", places=2, validators=[Optional()])


class EditSousArticleForm(FlaskForm):
    titre = StringField("Article", validators=[DataRequired()])
    info = TextAreaField("Informations supplémentaires", validators=[Optional()])
    quantite = IntegerField("Quantité", validators=[Optional()])
    prix_unitaire = DecimalField("prix", places=2, validators=[Optional()])


class ChapitreForm(FlaskForm):

    titre = StringField("Chapitre", validators=[DataRequired()])



class EditChapitreForm(FlaskForm):
    id = StringField("id",
                     validators=[DataRequired()])

    titre = StringField("Chapitre", validators=[DataRequired()])



class DevisForm(FlaskForm):

    info = TextAreaField("Informations complémentaires", validators=[Optional()])



class EditDevisForm(FlaskForm):
    montant_ht = StringField("Montant_ht", validators=[DataRequired()])
    chapitres = StringField("Chapitre", validators=[DataRequired()])
    articles = StringField("articles", validators=[DataRequired()])





