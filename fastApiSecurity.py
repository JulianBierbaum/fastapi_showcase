from datetime import datetime, timedelta, timezone
from typing import Annotated
import jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from pydantic import BaseModel

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# create a fake user with a hashed password
# this will get saved on the database in production
# if you want to create a user yourself insert the HS256 hashed password into the table
# login for this: username: johndoe, password: secret
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}

# Model for Token with the access_token and the type of the token
class Token(BaseModel):
    access_token: str
    token_type: str

# TokenData Model with username as string
class TokenData(BaseModel):
    username: str | None = None

# Model for a User
# Includes username, email, full_name and a flag if the account is disabled
class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None

# Model for a User in the Database with the hashed_password of the user
class UserInDB(User):
    hashed_password: str

# Model for the en- and decryption with CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Schema for the OAuth2 System
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()

# Method to verify if a password and a hashed_password are the same
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# Returns the hash of a password
def get_password_hash(password):
    return pwd_context.hash(password)


# Gets a user object from a list using the users username
def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

# If the user doesn't exist 
# or the inputed password doesn't match with the hashed password false is returned
def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

# Method to create the JWT access token (json web tokens)
# jwt tokens get saved in the browser storage to authenticate the user
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Method decodes the jwt token using the shared security key
# returns the user object from the authenticated user
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    # unauthorized access
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # gets the user name from the token
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    # Retrieve user from the db using the username
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

# Get the current user from the jwt token (previous function)
# Throws an exeption if the user is disabled
# Returns the user (if not disabled)
async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    # checks the hashed passwords and the username with the db
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # Set access token expiration time
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # Create a new access token with user's username as the subject (sub)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

# Return the currently authenticated user's object
@app.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user

# Return a list of attributes from the current user
@app.get("/users/me/items/")
async def read_own_items(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return [{"item_id": "Foo", "owner": current_user.username}]
