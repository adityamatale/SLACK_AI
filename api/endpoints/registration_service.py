from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from SLLACK.api.logger import logger
from SLLACK.security.auth import Hash
from SLLACK.api import schema
print("Imported main in registration_service:")
from sqlalchemy.orm import Session
from SLLACK.db.database import get_db
from SLLACK.api.utils import utils

logger.info("Setting up registration_service routerr")

router = APIRouter()
@router.post("/register", response_model=schema.UserResponse)
async def register_user(request: schema.UserRegisterRequest, db: Session = Depends(get_db)):
    # Logic to register a new user
    # logic for checking password match and email existence would go here
    # return unique user ID....store it in session of interface...needed for profile management
    """
    Register a new user and generate an access token.
    """
    try:
        user_data = utils.get_user_details(db, request)
        if user_data:
            logger.error("User already registered")
            return JSONResponse(
                status_code=status.HTTP_409_CONFLICT,
                content={"detail": "User already registered."}
            )

        if not utils.is_valid_password(request.password):
            logger.error("Password not valid")
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"detail": "Password not valid"}
            )

        request.password = Hash.encode_password(request.password)
        new_user = utils.save_user_details(db, request)

        # Create a UserResponse object instead of a dictionary
        user_response = schema.UserResponse(
            id=new_user.id,
            first_name=new_user.first_name,
            last_name=new_user.last_name,
            email=new_user.email
        )

        logger.info("Customer sign up successful.")
        return user_response
    except Exception as e:
        logger.error(f"Error during signup: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail="FAILED"
        )
    finally:
        db.close()

@router.post("/login", response_model=schema.UserResponse)
async def login_user(request: schema.UserLoginRequest, db: Session = Depends(get_db)):
    # Logic to authenticate a user
    # check if email exists and password matches
    # return unique user ID ...stored in session for chatting. 
    """Authenticate a user and generate an access token."""
    try:
        logger.info(f"Received sign in request: {request.email}")
        user_data = utils.get_user_details(db, request)
        if not user_data:
            logger.error(f"Error: User with email {request.email} not found")
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "User not found."}
            )
            
        elif not Hash.verify(user_data.encrypted_password, request.password):
            logger.error("Error: Password verification failed")
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Incorrect password."}
            )
        else:
            # Create a UserSignInResponse object instead of a dictionary
            user_response = schema.UserResponse(
                id=user_data.id,
                first_name=user_data.first_name,
                last_name=user_data.last_name,
                email=user_data.email
            )
            logger.info("Customer sign in successful. Sending jwt token")
            return user_response
    except Exception as e:
        logger.error(f"Error during sign in: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail="FAILED"
        )
    finally:
        db.close()