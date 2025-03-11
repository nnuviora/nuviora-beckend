from typing import List

from fastapi import APIRouter, HTTPException, Depends, status, Security, BackgroundTasks, Request
from fastapi_limiter.depends import RateLimiter
from fastapi.security import (
    OAuth2PasswordRequestForm,
    HTTPAuthorizationCredentials,
    HTTPBearer,
)
from sqlalchemy.orm import Session

from scr.database.db import get_db
from scr.schemas import UserModel, UserResponse, TokenModel, RequestEmail
from scr.repository import users as repository_users
from scr.services.auth import auth_service
from scr.services.email import send_email
from scr.conf import messages

router = APIRouter(prefix="/auth", tags=["auth"])
security = HTTPBearer()


# @router.post(
#     "/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED
# )
# async def signup(body: UserModel, db: Session = Depends(get_db)):
#     exist_user = await repository_users.get_user_by_email(body.email, db)
#     if exist_user:
#         raise HTTPException(
#             status_code=status.HTTP_409_CONFLICT, detail="Account already exists"
#         )
#     body.password = auth_service.get_password_hash(body.password)
#     new_user = await repository_users.create_user(body, db)
#     return {"user": new_user, "detail": "User successfully created"}

@router.post("/signup", response_model=UserResponse, description='No more than 2 requests per 60 sec',
            dependencies=[Depends(RateLimiter(times=2, seconds=60))], status_code=status.HTTP_201_CREATED)
async def signup(body: UserModel, background_tasks: BackgroundTasks, request: Request, db: Session = Depends(get_db)):
    """
    The signup function creates a new user in the database.
        It takes a UserModel object as input, which is validated by pydantic.
        If the email address already exists in the database, an HTTP 409 error is raised.
        The password field of the UserModel object is hashed using Argon2 and stored in that form.
        A new user record is created with this information and returned to the client.

    :param body: UserModel: Get the request body and validate it against the usermodel schema
    :param background_tasks: BackgroundTasks: Add a task to the background tasks queue
    :param request: Request: Get the base_url of the application
    :param db: Session: Get the database session
    :return: A dict with the user and a message
    :doc-author: Trelent
    """

    exist_user = await repository_users.get_user_by_email(body.email, db)
    if exist_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=messages.ACCOUNT_EXIST)
    body.password = auth_service.get_password_hash(body.password)
    new_user = await repository_users.create_user(body, db)
    background_tasks.add_task(send_email, new_user.email, new_user.username, request.base_url)
    return {"user": new_user, "detail": "User successfully created. Check your email for confirmation."}

# @router.post("/login", response_model=TokenModel)
# async def login(
#     body: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
# ):
#     user = await repository_users.get_user_by_email(body.username, db)
#     if user is None:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email"
#         )
#     if not auth_service.verify_password(body.password, user.password):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password"
#         )
#     # Generate JWT
#     access_token = await auth_service.create_access_token(data={"sub": user.email})
#     refresh_token = await auth_service.create_refresh_token(data={"sub": user.email})
#     await repository_users.update_token(user, refresh_token, db)
#     return {
#         "access_token": access_token,
#         "refresh_token": refresh_token,
#         "token_type": "bearer",
#     }
@router.post("/login", response_model=TokenModel)
async def login(body: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    The login function is used to authenticate a user.
        It takes the username and password from the request body,
        verifies them against the database, and returns an access token if successful.

    :param body: OAuth2PasswordRequestForm: Validate the request body
    :param db: Session: Access the database
    :return: A dictionary with three keys
    :doc-author: Trelent
    """

    user = await repository_users.get_user_by_email(body.username, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=messages.INVALID_EMAIL)
    if not user.confirmed:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=messages.EMAIL_NOT_CONFIRMED)
    if not auth_service.verify_password(body.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=messages.INVALID_EMAIL)
    # Generate JWT
    access_token = await auth_service.create_access_token(data={"sub": user.email})
    refresh_token = await auth_service.create_refresh_token(data={"sub": user.email})
    await repository_users.update_token(user, refresh_token, db)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

@router.get('/confirmed_email/{token}')
async def confirmed_email(token: str, db: Session = Depends(get_db)):
    """
    The confirmed_email function is used to confirm a user's email address.
        It takes the token from the URL and uses it to get the user's email address.
        The function then checks if there is a user with that email in our database, and if not, returns an error message.
        If there is a user with that email in our database, we check whether their account has already been confirmed or not.
            If it has been confirmed already, we return another error message saying so; otherwise we call repository_users'
            confirmed_email function which sets the 'confirmed' field of that particular record to

    :param token: str: Get the token from the url
    :param db: Session: Get the database session from the dependency injection
    :return: A message that the email is already confirmed or a message that the email has been confirmed
    :doc-author: Trelent
    """

    email = await auth_service.get_email_from_token(token)
    user = await repository_users.get_user_by_email(email, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Verification error")
    if user.confirmed:
        return {"message": "Your email is already confirmed"}
    await repository_users.confirmed_email(email, db)
    return {"message": "Email confirmed"}

@router.get("/refresh_token", response_model=TokenModel)
async def refresh_token(
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db),
):
    """
    The refresh_token function is used to refresh the access token.
    It takes in a refresh token and returns a new access token.
    The function first decodes the refresh_token to get the email of the user who owns it, then checks if that user exists in our database. If not, we raise an HTTPException with status code 401 (Unauthorized).
    If they do exist, we create a new access_token and refresh_token for them using auth_service's create functions. We update their record in our database with this new information before returning both tokens as well as &quot;bearer&quot; which is just how you tell

    :param credentials: HTTPAuthorizationCredentials: Get the token from the request header
    :param db: Session: Pass the database session to the function
    :param : Get the user's email from the token
    :return: A new set of tokens
    :doc-author: Trelent
    """

    token = credentials.credentials
    email = await auth_service.decode_refresh_token(token)
    user = await repository_users.get_user_by_email(email, db)
    if user.refresh_token != token:
        await repository_users.update_token(user, None, db)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
        )
    access_token = await auth_service.create_access_token(data={"sub": email})
    refresh_token = await auth_service.create_refresh_token(data={"sub": email})
    await repository_users.update_token(user, refresh_token, db)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }

@router.post('/request_email')
async def request_email(body: RequestEmail, background_tasks: BackgroundTasks, request: Request,
                        db: Session = Depends(get_db)):
    """
    The request_email function is used to send an email to the user with a link that they can click on
    to confirm their email address. The function takes in a RequestEmail object, which contains the
    email of the user who wants to confirm their account. It then checks if there is already a confirmed
    user with that email address, and if so returns an error message saying as much. If not, it sends
    an email containing a confirmation link.

    :param body: RequestEmail: Validate the request body
    :param background_tasks: BackgroundTasks: Add tasks to the background task queue
    :param request: Request: Get the base url of the server
    :param db: Session: Get the database session
    :return: A message
    :doc-author: Trelent
    """

    user = await repository_users.get_user_by_email(body.email, db)
    if user.confirmed:
        return {"message": "Your email is already confirmed"}
    if user:
        background_tasks.add_task(send_email, user.email, user.username, request.base_url)
    return {"message": "Check your email for confirmation."}
