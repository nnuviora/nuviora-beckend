from fastapi import APIRouter, Depends, HTTPException, Query, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from starlette.responses import StreamingResponse
from typing import Any, List, Optional
import cloudinary
import uuid
from cloudinary.uploader import upload
import cloudinary.api
import cloudinary.utils
import qrcode
import logging
from io import BytesIO
from starlette.status import HTTP_404_NOT_FOUND
from datetime import datetime
from cloudinary.uploader import upload, destroy

from scr.conf.config import config  # settings
from scr.conf import messages
from scr.database.db import get_db
from scr.database.models import Role, Image, Tag
from scr.services.auth import auth_service
from scr.services.cloudsrv import cloudinary
from scr.schemas import PostCreate, PostList, PostSingle, UserResponse, UserDb, User
from scr.services.posts import PostServices
from scr.services.roles import RoleAccess

class CloudinaryService:
    cloudinary.config(
        cloud_name=config.CLD_NAME,
        api_key=config.CLD_API_KEY,
        api_secret=config.CLD_API_SECRET,
        secure=True,
    )


router = APIRouter(prefix='/cloud', tags=["Cloudinary image operations"])

post_services = PostServices(Image)

allowed_operation_create = RoleAccess([Role.admin, Role.moderator, Role.user])
allowed_operation_read = RoleAccess([Role.admin, Role.moderator, Role.user])
allowed_operation_update = RoleAccess([Role.admin, Role.moderator, Role.user])
allowed_operation_delete = RoleAccess([Role.admin, Role.moderator, Role.user])

# публікуємо світлину
@router.post("/publication",
                   response_model=PostSingle,
                   response_model_exclude_unset=True,
                   dependencies=[Depends(allowed_operation_create)])
async def upload_images_user(
        file: UploadFile = File(),
        text: str = Form(...),
        tags: List[str] = Form([]),
        current_user: UserDb = Depends(auth_service.get_current_user),
        db: Session = Depends(get_db),
):
    """
    The upload_images_user function uploads an image to the Cloudinary cloud storage service.
    The function also saves the image's metadata in a PostgreSQL database.


    :param file: UploadFile: Receive the file from the user
    :param text: str: Get the description of the image
    :param tags: List[str]: Get a list of tags from the form
    :param current_user: UserDb: Get the current user
    :param db: Session: Access the database
    :param : Get the current user
    :return: The following data:
    :doc-author: Trelent
    """
    try:
        img_content = await file.read()
        public_id = f"image_{current_user.id}_{uuid.uuid4()}"

        # Завантаження на Cloudinary
        response = cloudinary.uploader.upload(
            img_content, public_id=public_id, overwrite=True, folder="publication"
        )

        # Зберігання в базі даних
        image = Image(
            owner_id=current_user.id,
            url_original=response["secure_url"],
            description=text,
            url_original_qr="",
            updated_at=datetime.now(),
        )
        #
        # # Розділення тегів та перевірка кількості
        # for tags_str in tags:
        #     tag_list = tags_str.split(",")
        #     tag_count = len(tag_list)
        #     print(f"Кількість тегів: {tag_count}")
        #
        #     if tag_count > 5:
        #         raise HTTPException(
        #             status_code=400, detail="Максимальна кількість тегів - 5"
        #         )
        #
        #     for tag_name in tag_list:
        #         tag_name = tag_name.strip()
        #
        #         # Чи існує тег з таким іменем
        #         tag = db.query(Tag).filter_by(name=tag_name).first()
        #         if tag is None:
        #             # Якщо тег не існує, створюємо та зберігаємо
        #             tag = Tag(name=tag_name)
        #             db.add(tag)
        #             db.commit()
        #             db.refresh(tag)
        #
        #         # Перевірка, чи тег вже приєднаний до світлини
        #         if tag not in image.tags:
        #             image.tags.append(tag)
        #
        db.add(image)
        db.commit()

        # інформація про світлину
        item = await post_services.get_p(db=db, id=image.id)

        if not item:
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND, detail="Запис не знайдений"
            )

        post_data = {
            "id": item.id,
            "owner_id": item.owner_id,
            "url_original": item.url_original,
            "tags": [tag.name for tag in item.tags],
            "description": item.description,
            "pub_date": item.created_at,
            "img": item.url_original,
            "text": "",
            "user": "",
        }

        return PostSingle(**post_data)
    except HTTPException as e:
        logging.error(f"Помилка валідації форми: {e}")
        raise
    except Exception as e:
        logging.error(f"Помилка завантаження зображення: {e}")
        raise

# @router.post("/publication",
#                    response_model=PostSingle,
#                    response_model_exclude_unset=True,
#                    dependencies=[Depends(allowed_operation_create)])
# async def upload_images_user(
#         file: UploadFile = File(),
#         text: str = Form(...),
#         tags: List[str] = Form([]),
#         current_user: UserDb = Depends(auth_service.get_current_user),
#         db: Session = Depends(get_db),
# ):
#     """
#     The upload_images_user function uploads an image to the Cloudinary cloud storage service.
#     The function also saves the image's metadata in a PostgreSQL database.
#
#
#     :param file: UploadFile: Receive the file from the user
#     :param text: str: Get the description of the image
#     :param tags: List[str]: Get a list of tags from the form
#     :param current_user: UserDb: Get the current user
#     :param db: Session: Access the database
#     :param : Get the current user
#     :return: The following data:
#     :doc-author: Trelent
#     """
#     try:
#         img_content = await file.read()
#         public_id = f"image_{current_user.id}_{uuid.uuid4()}"
#
#         # Завантаження на Cloudinary
#         response = cloudinary.uploader.upload(
#             img_content, public_id=public_id, overwrite=True, folder="publication"
#         )
#
#         # Зберігання в базі даних
#         image = Image(
#             owner_id=current_user.id,
#             url_original=response["secure_url"],
#             description=text,
#             url_original_qr="",
#             updated_at=datetime.now(),
#         )
#         #
#         # # Розділення тегів та перевірка кількості
#         # for tags_str in tags:
#         #     tag_list = tags_str.split(",")
#         #     tag_count = len(tag_list)
#         #     print(f"Кількість тегів: {tag_count}")
#         #
#         #     if tag_count > 5:
#         #         raise HTTPException(
#         #             status_code=400, detail="Максимальна кількість тегів - 5"
#         #         )
#         #
#         #     for tag_name in tag_list:
#         #         tag_name = tag_name.strip()
#         #
#         #         # Чи існує тег з таким іменем
#         #         tag = db.query(Tag).filter_by(name=tag_name).first()
#         #         if tag is None:
#         #             # Якщо тег не існує, створюємо та зберігаємо
#         #             tag = Tag(name=tag_name)
#         #             db.add(tag)
#         #             db.commit()
#         #             db.refresh(tag)
#         #
#         #         # Перевірка, чи тег вже приєднаний до світлини
#         #         if tag not in image.tags:
#         #             image.tags.append(tag)
#         #
#         db.add(image)
#         db.commit()
#
#         # інформація про світлину
#         item = await post_services.get_p(db=db, id=image.id)
#
#         if not item:
#             raise HTTPException(
#                 status_code=HTTP_404_NOT_FOUND, detail="Запис не знайдений"
#             )
#
#         post_data = {
#             "id": item.id,
#             "owner_id": item.owner_id,
#             "url_original": item.url_original,
#             "tags": [tag.name for tag in item.tags],
#             "description": item.description,
#             "pub_date": item.created_at,
#             "img": item.url_original,
#             "text": "",
#             "user": "",
#         }
#
#         return PostSingle(**post_data)
#     except HTTPException as e:
#         logging.error(f"Помилка валідації форми: {e}")
#         raise
#     except Exception as e:
#         logging.error(f"Помилка завантаження зображення: {e}")
#         raise


@router.get("/transformed_image/{image_id}")
def transform_and_update_image(image_id: str, angle: int = 45, db: Session = Depends(get_db)):
    """
    The transform_and_update_image function takes an image_id and angle as input,
        transforms the original image by rotating it by the specified angle,
        uploads the transformed image to Cloudinary, and updates the database with
        a new url for that transformed image.

    :param image_id: str: Identify the image to be transformed
    :param angle: int: Specify the angle by which the image should be rotated
    :param db: Session: Get the database session
    :return: The following:
    :doc-author: Trelent
    """
    image = db.query(Image).filter(Image.id == image_id).first()
    print("1:", image)
    print("Start:", image_id)

    if image:
        url_original = image.url_original
        public_id = cloudinary.utils.cloudinary_url(url_original)[0].split("/")[-1]
        print("Start URL:", url_original)

        folder_path = "transform"
        transformation = {"angle": angle}

        public_id = f"{folder_path}/{public_id}"

        response = upload(url_original, transformation=transformation, public_id=public_id)

        transformed_image_url = response['secure_url']

        db.query(Image).filter(Image.id == image_id).update({"url_transformed": transformed_image_url})
        db.commit()

        print("1:", image_id)
        print("Original Image URL:", url_original)
        print("Transformed Image URL:", transformed_image_url)

        return {"message": f"Image transformed and updated successfully. Rotated by {angle} degrees.",
                "transformed_image_url": transformed_image_url}

    return {"error": "Image not found."}


@router.get("/qr_codes_image/{image_id}")
def qr_codes_and_update_image(image_id: str, db: Session = Depends(get_db)):
    """
    The qr_codes_and_update_image function generates a QR code for the original image and updates the database with it.


    :param image_id: str: Pass the image id to the function
    :param db: Session: Access the database
    :return: The following:
    :doc-author: Trelent
    """
    image = db.query(Image).filter(Image.id == image_id).first()
    print("1:", image)
    print("Start:", image_id)

    if image:
        url_original = image.url_original
        public_id = cloudinary.utils.cloudinary_url(url_original)[0].split("/")[-1]
        print("Start URL:", url_original)

        folder_path = "qr_codes"

        # Create QR
        qr_original = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=10,
            border=4,
        )
        qr_original.add_data(url_original)
        qr_original.make(fit=True)

        # Save QR
        qr_code_original_image = qr_original.make_image(fill_color="black", back_color="white")
        qr_code_original_image_io = BytesIO()
        qr_code_original_image.save(qr_code_original_image_io)

        # Upload QR
        qr_code_original_response = upload(
            qr_code_original_image_io.getvalue(),
            folder=folder_path,
            public_id=f"{folder_path}/{public_id}_qr_code",
            format="png",
            overwrite=True
        )

        qr_code_original_url = qr_code_original_response['secure_url']

        db.query(Image).filter(Image.id == image_id).update({"url_original_qr": qr_code_original_url})
        db.commit()

        print("1:", image_id)
        print("Original Image URL:", url_original)
        print("QR Code URL for Original Image:", qr_code_original_url)

        return {"message": f"QR Code generated and updated successfully for the original image.",
                "url_original_qr": qr_code_original_url}

    return {"error": "Image not found."}


@router.get("/qr_codes_transformed_image/{image_id}")
def qr_codes_and_update_transformed_image(image_id: str, db: Session = Depends(get_db)):
    """
    The qr_codes_and_update_transformed_image function generates a QR code for the transformed image and updates the url_transformed_qr field in the database.

    :param image_id: str: Get the image from the database
    :param db: Session: Get the database session
    :return: A dictionary with the url_transformed_qr key
    :doc-author: Trelent
    """
    image = db.query(Image).filter(Image.id == image_id).first()

    if image:
        if not image.url_transformed:
            # Якщо url_transformed пустий, викликаємо transform_and_update_image
            transform_and_update_image(image_id=image_id, db=db)

        url_transformed = image.url_transformed
        public_id = cloudinary.utils.cloudinary_url(url_transformed)[0].split("/")[-1]

        folder_path = "qr_codes"

        # Створення QR-коду
        qr_transformed = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=10,
            border=4,
        )
        qr_transformed.add_data(url_transformed)
        qr_transformed.make(fit=True)

        # Збереження QR-коду
        qr_code_transformed_image = qr_transformed.make_image(fill_color="navy", back_color="lightyellow")
        qr_code_transformed_image_io = BytesIO()
        qr_code_transformed_image.save(qr_code_transformed_image_io)

        # Завантаження QR-коду
        qr_code_transformed_response = upload(
            qr_code_transformed_image_io.getvalue(),
            folder=folder_path,
            public_id=f"{folder_path}/{public_id}_qr_code_transformed",
            format="png",
            overwrite=True
        )

        qr_code_transformed_url = qr_code_transformed_response['secure_url']

        image = db.query(Image).filter(Image.id == image_id).first()
        # Оновлення поля url_transformed_qr у базі даних
        db.query(Image).filter(Image.id == image_id).update({"url_transformed_qr": qr_code_transformed_url})
        db.commit()

        return {"message": f"QR Code generated and updated successfully for the transformed image.",
                "url_transformed_qr": qr_code_transformed_url}

    return {"error": "Image not found."}

"""
@router.get("/qr_load/{image_id}")
def qr_codes_image_load(
        image_id: str,
        option: str
                | None = Query(
            title="Type of source of image to use", default="original",
            description="Type of source of image to use. Can be: original or transformed. By default used  original"
        ),
        db: Session = Depends(get_db),
):
    image: Image = db.query(Image).filter(Image.id == image_id).first()
    if image:
        qr_original = qrcode.QRCode(  # type: ignore
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M,  # type: ignore
            box_size=10,
            border=4,
        )
        url_str: str = (
            image.url_transformed if option == "transformed" else image.url_original
        )  # type: ignore
        if url_str:
            qr_original.add_data(url_str)
            qr_original.make(fit=True)

            # Save QR
            qr_code_original_image = qr_original.make_image(
                fill_color="black", back_color="white"
            )
            qr_code_original_image_io = BytesIO()
            qr_code_original_image.save(qr_code_original_image_io)
            qr_code_original_image_io.seek(0)  # Return cursor to starting point
            return StreamingResponse(qr_code_original_image_io, media_type="image/png")

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=messages.IMAGE_NOT_FOUND)
"""