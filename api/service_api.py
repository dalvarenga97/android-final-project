from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from domain import Service
from db import Session

service_ns = Namespace('services', description='Service operations')

# Service model for Swagger documentation
service_model = service_ns.model('Service', {
    'id': fields.Integer(readonly=True, description='The unique identifier of a service'),
    'name': fields.String(required=True, description='The name of the service'),
    'description': fields.String(required=True, description='The description of the service'),
    'price': fields.Float(required=True, description='The price of the service'),
})

@service_ns.route('/')
class ServiceList(Resource):
    @service_ns.doc('list_services')
    @service_ns.marshal_list_with(service_model)
    @jwt_required()  # Ensure the user is authenticated
    def get(self):
        """List all services"""
        session = Session()
        try:
            services = session.query(Service).all()  # List all services
        finally:
            session.close()
        return services

    @service_ns.doc('create_service')
    @service_ns.expect(service_model)
    @service_ns.marshal_with(service_model, code=201)
    @jwt_required()  # Ensure the user is authenticated
    def post(self):
        """Create a new service"""
        data = request.get_json()
        session = Session()
        try:
            new_service = Service(
                name=data['name'],
                description=data['description'],
                price=data['price']
            )
            session.add(new_service)
            session.commit()
        finally:
            session.close()
        return new_service, 201


@service_ns.route('/<int:id>')
@service_ns.response(404, 'Service not found')
class ServiceResource(Resource):
    @service_ns.doc('get_service')
    @service_ns.marshal_with(service_model)
    def get(self, id):
        """Fetch a service given its identifier"""
        session = Session()
        try:
            service = session.query(Service).filter_by(id=id).first()
            if service is None:
                service_ns.abort(404, f"Service {id} not found")
        finally:
            session.close()
        return service

    @service_ns.doc('update_service')
    @service_ns.expect(service_model)
    @service_ns.marshal_with(service_model)
    def put(self, id):
        """Update a service given its identifier"""
        data = request.get_json()
        session = Session()
        try:
            service = session.query(Service).filter_by(id=id).first()
            if service is None:
                service_ns.abort(404, f"Service {id} not found")
            
            service.name = data.get('name', service.name)
            service.description = data.get('description', service.description)
            service.price = data.get('price', service.price)
            
            session.commit()  # Commit the transaction
        except Exception as e:
            session.rollback()  # Rollback in case of error
            print(f"Error updating service: {e}")  # Log the error for debugging
            service_ns.abort(500, "Internal server error")
        finally:
            session.close()
        
        return service

    @service_ns.doc('delete_service')
    @service_ns.response(204, 'Service deleted')
    def delete(self, id):
        """Delete a service given its identifier"""
        session = Session()
        try:
            service = session.query(Service).filter_by(id=id).first()
            if service is None:
                service_ns.abort(404, f"Service {id} not found")
            
            session.delete(service)
            session.commit()
        finally:
            session.close()
        return '', 204
