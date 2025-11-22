from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError, DataError
from datetime import datetime
from SLLACK.db.models import User
from SLLACK.api.schema import UserRegisterRequest
from typing import Optional
from SLLACK.api.logger import logger  # Assuming logger is imported from api_logging

class CRUDUser :
    def create_user(self, db: Session, user_data: UserRegisterRequest) -> Optional[User ]:
        """
        Create a new user in the database.
        
        Args:
            db: Database session
            user_data: User data for registration
            
        Returns:
            User object if successful, None otherwise
        """
        try:
            new_user = User(
                first_name=user_data.first_name,
                last_name=user_data.last_name,
                email=user_data.email,
                encrypted_password=user_data.password,
                created_at=datetime.now()
            )
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            logger.info(f"User  created successfully: {user_data.email}")
            return new_user
            
        except IntegrityError as e:
            db.rollback()
            logger.error(f"IntegrityError while creating user {user_data.email}: {str(e)}")
            return None
            
        except DataError as e:
            db.rollback()
            logger.error(f"DataError while creating user {user_data.email}: {str(e)}")
            return None
            
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"Database error while creating user {user_data.email}: {str(e)}")
            return None
            
        except Exception as e:
            db.rollback()
            logger.error(f"Unexpected error while creating user {user_data.email}: {str(e)}")
            return None

    def get_user_by_email(self, db: Session, email: str) -> Optional[User ]:
        """
        Retrieve a user by email address.
        
        Args:
            db: Database session
            email: User's email address
            
        Returns:
            User object if found, None otherwise
        """
        try:
            user = db.query(User).filter(User.email == email).first()
            if not user:
                logger.info(f"User  not found with email: {email}")
            return user
            
        except SQLAlchemyError as e:
            logger.error(f"Database error while fetching user by email {email}: {str(e)}")
            return None
            
        except Exception as e:
            logger.error(f"Unexpected error while fetching user by email {email}: {str(e)}")
            return None


try:
    crud_user = CRUDUser ()
    logger.info("CRUDUser  initialized successfully")
except Exception as e:
    logger.critical(f"Failed to initialize CRUD:User  {str(e)}")
    raise  # Critical error that should stop application startup