from io import BytesIO

from PIL import Image
from django.core.files.base import ContentFile


class ImageThumbnailService:

    SIZE = (50, 50)
    QUALITY = 100

    def create_thumbnail(self, instance, image_field, save_field=None):
        """
        Converts the instance image to a thumbnail. The thumbnail
        is saved to save_field if this is specified otherwise it
        is saved to instance image_field.
        """
        image = getattr(instance, image_field)
        if not image:
            return None

        thumbnail = Image.open(image)
        thumbnail.thumbnail(self.SIZE)
        thumb_io = BytesIO()
        thumbnail.save(thumb_io, thumbnail.format, quality=self.QUALITY)

        thumbnail_field = save_field or image_field
        file_name = image.name.split("/")[-1].split(".")[0]
        getattr(instance, thumbnail_field).save(
            f"{file_name}.{thumbnail.format.lower()}",
            ContentFile(thumb_io.getvalue()),
            save=False,
        )
        instance.save()
        return True
