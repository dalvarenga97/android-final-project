from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from domain import Pet  # Ensure this imports the Pet model
from db import Session  # Import the Session from db.py

pet_ns = Namespace('pets', description='Pet operations')

# Define the Pet model for Swagger documentation
pet_model = pet_ns.model('Pet', {
    'id': fields.Integer(readonly=True, description='The unique identifier of a pet'),
    'name': fields.String(required=True, description='The name of the pet'),
    'species': fields.String(required=True, description='The species of the pet'),
    'breed': fields.String(required=True, description='The breed of the pet'),
    'age': fields.Integer(required=True, description='The age of the pet'),
    'weight': fields.Float(required=True, description='The weight of the pet')
})

@pet_ns.route('/')
class PetList(Resource):
    @pet_ns.doc('list_pets')
    @pet_ns.marshal_list_with(pet_model)
    @jwt_required()  # Ensure the user is authenticated
    def get(self):
        """List all pets for the logged-in user"""
        current_user = get_jwt_identity()  # Get the current user's identity
        session = Session()
        pets = session.query(Pet).filter_by(user_id=current_user['id']).all()  # Filter pets by user_id
        session.close()
        return pets

    @pet_ns.doc('create_pet')
    @pet_ns.expect(pet_model)
    @pet_ns.marshal_with(pet_model, code=201)
    @jwt_required()  # Ensure the user is authenticated
    def post(self):
        """Create a new pet"""
        data = request.get_json()
        session = Session()
        try:
            new_pet = Pet(
                name=data['name'],
                species=data['species'],
                breed=data['breed'],
                age=data['age'],
                weight=data['weight'],
                user_id=get_jwt_identity()['id']  # Associate the pet with the logged-in user
            )
            session.add(new_pet)
            session.commit()
            pet_data = {
                'id': new_pet.id,
                'name': new_pet.name,
                'species': new_pet.species,
                'breed': new_pet.breed,
                'age': new_pet.age,
                'weight': new_pet.weight
            }
        finally:
            session.close()
        return new_pet, 201

@pet_ns.route('/<int:id>')
@pet_ns.response(404, 'Pet not found')
class PetResource(Resource):
    @pet_ns.doc('get_pet')
    @pet_ns.marshal_with(pet_model)
    def get(self, id):
        """Fetch a pet given its identifier"""
        session = Session()
        pet = session.query(Pet).filter_by(id=id).first()
        session.close()
        if pet is None:
            pet_ns.abort(404, f"Pet {id} not found")
        return pet

    @pet_ns.doc('update_pet')
    @pet_ns.expect(pet_model)
    @pet_ns.marshal_with(pet_model)
    def put(self, id):
        """Update a pet given its identifier"""
        data = request.get_json()
        session = Session()
        pet = session.query(Pet).filter_by(id=id).first()
        if pet is None:
            session.close()
            pet_ns.abort(404, f"Pet {id} not found")
        
        pet.name = data.get('name', pet.name)
        pet.species = data.get('species', pet.species)
        pet.breed = data.get('breed', pet.breed)
        pet.age = data.get('age', pet.age)
        pet.weight = data.get('weight', pet.weight)
        
        session.commit()
        session.close()
        return pet

    @pet_ns.doc('delete_pet')
    @pet_ns.response(204, 'Pet deleted')
    def delete(self, id):
        """Delete a pet given its identifier"""
        session = Session()
        pet = session.query(Pet).filter_by(id=id).first()
        if pet is None:
            session.close()
            pet_ns.abort(404, f"Pet {id} not found")
        
        session.delete(pet)
        session.commit()
        session.close()
        return '', 204