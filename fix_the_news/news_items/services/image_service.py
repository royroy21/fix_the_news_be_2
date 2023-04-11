import io
import logging
import tempfile
from io import BytesIO

import requests
from django.core.files.base import ContentFile
from PIL import Image
from django.utils.text import slugify
from pyquery import PyQuery
from requests import exceptions as requests_exceptions

logger = logging.getLogger(__name__)


class ImageService:

    HEADERS = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/83.0.4103.61 Safari/537.36",
    }
    SIZE = (150, 150)

    def run(self, news_item):
        logger.info(
            "Getting image for news item #%i:%s",
            news_item.id,
            news_item.title,
        )
        image_url = self.get_image_url(news_item)
        if not image_url:
            logger.warning(
                "No image URL found for #%i:%s",
                news_item.id,
                news_item.title,
            )
            return None
        self.get_image(news_item, image_url)
        news_item.tried_to_add_image = True
        news_item.save()

    def get_image_url(self, news_item):
        response = self.get_request(news_item.url)
        if not response:
            return None

        d = PyQuery(response.content)
        meta = d("meta")

        # TODO - this is hard and fast coding. Improve later ..
        meta_image = None
        for tag in meta:
            if "property" in tag.keys():
                if tag.get("property") == "og:image":
                    meta_image = tag

        if meta_image is None:
            logger.warning(
                "No og:image meta tag found for #%i:%s",
                news_item.id,
                news_item.title,
            )
            return None

        return meta_image.get("content")

    def get_request(self, url, stream=False):
        try:
            response = requests.get(
                url,
                headers=self.HEADERS,
                stream=stream,
            )
        except (
            requests_exceptions.ConnectionError,
            requests_exceptions.ConnectTimeout,
            requests_exceptions.InvalidURL,
        ):
            return None

        if not response.ok:
            return None

        return response

    def get_image(self, news_item, image_url):
        buffer = tempfile.SpooledTemporaryFile()

        response = self.get_request(image_url, stream=True)
        if not response:
            return None

        downloaded = 0
        for chunk in response.iter_content():
            downloaded += len(chunk)
            buffer.write(chunk)

        buffer.seek(0)
        image = Image.open(io.BytesIO(buffer.read()))
        buffer.close()

        resized_image, image_io = self.resize_image(image)
        return self.save_image(news_item, image_url, resized_image, image_io)

    def resize_image(self, image):
        image.thumbnail(self.SIZE)
        image_io = BytesIO()
        image.save(
            image_io,
            format=image.format,
            compress_level=5,
            optimize=True,
            quality=100,
            subsampling=0,
        )
        return image, image_io

    def save_image(self, news_item, news_image_url, image, image_io):
        news_item.original_image_url = news_image_url
        news_item.image.save(
            f"{slugify(news_item.title)}.{image.format.lower()}",
            ContentFile(image_io.getvalue()),
        )
        logger.info(
            "Saving image for news item #%i:%s",
            news_item.id,
            news_item.title,
        )
        news_item.save()
