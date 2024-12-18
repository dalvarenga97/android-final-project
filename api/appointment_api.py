from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from domain import Appointment, Pet
from db import Session

appointment_ns = Namespace('appointments', description='Appointment operations')

# Appointment model for Swagger documentation
appointment_model = appointment_ns.model('Appointment', {
    'id': fields.Integer(readonly=True, description='The unique identifier of an appointment'),
    'pet_id': fields.Integer(required=True, description='The ID of the pet'),
    'date': fields.String(required=True, description='The date of the appointment'),
    'reason': fields.String(required=True, description='The reason for the appointment'),
})

@appointment_ns.route('/')
class AppointmentList(Resource):
    @appointment_ns.doc('list_appointments')
    @appointment_ns.marshal_list_with(appointment_model)
    @jwt_required()
    def get(self):
        """List all appointments for the logged-in user"""
        current_user = get_jwt_identity()  # Get the current user's identity
        session = Session()

        # Get all pets of the logged-in user to filter appointments by pet
        pets = session.query(Pet).filter_by(user_id=current_user['id']).all()
        pet_ids = [pet.id for pet in pets]

        # Filter appointments by pet_id related to the current user
        appointments = session.query(Appointment).filter(Appointment.pet_id.in_(pet_ids)).all()
        session.close()
        return appointments

    @appointment_ns.doc('create_appointment')
    @appointment_ns.expect(appointment_model)
    @appointment_ns.marshal_with(appointment_model, code=201)
    @jwt_required()  # Ensure the user is authenticated
    def post(self):
        """Create a new appointment"""
        data = request.get_json()
        session = Session()
        
        # Validate if the pet_id exists and belongs to the current user
        pet = session.query(Pet).filter_by(id=data['pet_id'], user_id=get_jwt_identity()['id']).first()
        if not pet:
            session.close()
            return {"message": "Pet not found or does not belong to the current user"}, 404
        
        # Create the new appointment and associate it with the pet
        new_appointment = Appointment(
            pet_id=data['pet_id'],
            date=data['date'],
            reason=data['reason'],
        )
        
        session.add(new_appointment)
        session.commit()
        session.close()

        return new_appointment, 201


@appointment_ns.route('/<int:id>')
@appointment_ns.response(404, 'Appointment not found')
class AppointmentResource(Resource):
    @appointment_ns.doc('get_appointment')
    @appointment_ns.marshal_with(appointment_model)
    def get(self, id):
        """Fetch an appointment given its identifier"""
        session = Session()
        appointment = session.query(Appointment).filter_by(id=id).first()
        session.close()
        if appointment is None:
            appointment_ns.abort(404, f"Appointment {id} not found")
        return appointment

    @appointment_ns.doc('update_appointment')
    @appointment_ns.expect(appointment_model)
    @appointment_ns.marshal_with(appointment_model)
    def put(self, id):
        """Update an appointment given its identifier"""
        data = request.get_json()
        session = Session()
        appointment = session.query(Appointment).filter_by(id=id).first()
        if appointment is None:
            session.close()
            appointment_ns.abort(404, f"Appointment {id} not found")
        
        try:
            # Update the appointment details
            appointment.pet_id = data.get('pet_id', appointment.pet_id)
            appointment.date = data.get('date', appointment.date)
            appointment.reason = data.get('reason', appointment.reason)
            
            session.commit()  # Commit the transaction
        except Exception as e:
            session.rollback()  # Rollback in case of error
            print(f"Error updating appointment: {e}")  # Log the error for debugging
            appointment_ns.abort(500, "Internal server error")
        finally:
            session.close()
        
        return appointment

    @appointment_ns.doc('delete_appointment')
    @appointment_ns.response(204, 'Appointment deleted')
    def delete(self, id):
        """Delete an appointment given its identifier"""
        session = Session()
        appointment = session.query(Appointment).filter_by(id=id).first()
        if appointment is None:
            session.close()
            appointment_ns.abort(404, f"Appointment {id} not found")
        
        session.delete(appointment)
        session.commit()
        session.close()
        return '', 204
