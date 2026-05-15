from fastapi import UploadFile

from src.services.base import BaseService
from src.tasks.tasks import resize_image


class ImagesService(BaseService):
    def upload_image(self, file: UploadFile):
        image_path = f"src/static/images/{file.filename}"
        with open(image_path, "wb+") as new_file:
            new_file.write(file.file.read())

        resize_image.delay(image_path)