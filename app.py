from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
import os

app = Flask(__name__)
entorno = os.getenv('DATABASE_URL')
ent = entorno[:8] + 'ql' + entorno[8:] 
app.config['SQLALCHEMY_DATABASE_URI'] = ent
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db = SQLAlchemy(app)
ma = Marshmallow(app)

CORS(app)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    lastname = db.Column(db.String(30), nullable=False)
    company = db.Column(db.String(50))
    phone = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(30), nullable=False, unique=True)

    def __int__(self, name, lastname, company, phone, email):
        self.name = name
        self.lastname = lastname
        self.company = company
        self.phone = phone
        self.email = email


class ContactsSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'lastname', 'company', 'phone', 'email')

contact_schema = ContactsSchema()
contacts_schema = ContactsSchema(many=True)

db.create_all()
db.session.commit()

@app.route('/contacts', methods=['POST'])
def create_contact():
    name = request.json['name']
    lastname = request.json['lastname']
    company = request.json['company']
    phone = request.json['phone']
    email = request.json['email']

    new_contact = Contact(name=name, lastname=lastname, company=company, phone=phone, email=email)
    db.session.add(new_contact)
    db.session.commit()

    return contact_schema.jsonify(new_contact['id'])

@app.route('/contacts', methods=['GET'])
def get_contacts():
    all_contacts = Contact.query.all()
    result = contacts_schema.dump(all_contacts)
    return jsonify(result)

@app.route('/contacts/<id>', methods=['GET'])
def get_contact(id):
    contact = Contact.query.get(id)
    return contact_schema.jsonify(contact)

@app.route('/contacts/<id>', methods=['PUT'])
def update_contact(id):
    contact = Contact.query.get(id)

    name = request.json['name']
    lastname = request.json['lastname']
    company = request.json['company']
    phone = request.json['phone']
    email = request.json['email']

    if name == "" or lastname == "" or email == "":
        return {"statuscode":400}

    contact.name = name
    contact.lastname = lastname
    contact.company = company
    contact.phone = phone
    contact.email = email

    db.session.commit()
    return contact_schema.jsonify(contact)

@app.route('/contacts/<id>', methods=['Delete'])
def delete_task(id):
    contact = Contact.query.get(id)
    db.session.delete(contact)
    db.session.commit()

    return contact_schema.jsonify(contact)

@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'Carlos API'})

if __name__ == "__main__":
    app.run(debug=True)