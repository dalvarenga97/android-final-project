from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from domain import Base, User, Pet, Appointment, Service  # Import all models
from werkzeug.security import generate_password_hash

# Database setup
engine = create_engine('postgresql://user:password@db/vetdb')
Base.metadata.create_all(engine)  # Create all tables
Session = sessionmaker(bind=engine)  # Define the Session factory 

# Revoked tokens storage
revoked_tokens = {}

def create_default_user():
    session = Session()
    admin_user = session.query(User).filter_by(username='admin').first()
    if not admin_user:
        admin_user = User(username='admin')
        admin_user.set_password('admin')  # Ensure this method hashes the password
        session.add(admin_user)
        session.commit()
        print("Default admin user created.")
    else:
        print("Admin user already exists.")
    session.close()

# Call the function to create the default user
create_default_user()