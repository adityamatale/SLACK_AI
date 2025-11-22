import re
from SLLACK.api.crud import crud_user

def get_user_details(db, user_data):
    """
    This function takes user data and fetches the data from username
    """
    user = crud_user.get_user_by_email(db, user_data.email)
    return user

def save_user_details(db, user_details):
    """
    This function will take the user details while signing up and save them in database
    """
    user = crud_user.create_user(db, user_details)
    return user

def is_valid_password(password):
    # code for checking if password has 6 characters, 1 uppercase, 1 lower case and a special character
    reg = r"^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=.*\W)(?!.* ).{6,}$"
    match = re.search(reg, password)
    return match