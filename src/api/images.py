from fastapi import APIRouter, UploadFile

from src.services.images import ImagesService


router = APIRouter(prefix="/images", tags=["Изображения отелей"])


@router.post("")
def upload_image(file: UploadFile):
    ImagesService().upload_image(file)
