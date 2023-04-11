import logging

import requests
from pyquery import PyQuery
from requests import exceptions as requests_exceptions

logger = logging.getLogger(__name__)


class MetaDataService:
    """
    For a provided URL attempts to get title and description from page source.
    """

    HEADERS = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/83.0.4103.61 Safari/537.36",
    }

    def run(self, url):
        page_source = self.get_page_source(url)
        if not page_source:
            return {
                "title": None,
                "description": None,
            }

        title = self.get_title_by_title_tag(page_source, url)
        if not title:
            title = self.get_title_by_h1_tag(page_source, url)
        return {
            "title": title,
            "description": self.get_description(page_source, url),
        }

    def get_page_source(self, url):
        response = self.get_request(url)
        if not response:
            return None

        return response.content

    def get_request(self, url):
        try:
            response = requests.get(url,headers=self.HEADERS)
        except (
                requests_exceptions.ConnectionError,
                requests_exceptions.ConnectTimeout,
                requests_exceptions.InvalidURL,
        ) as e:
            logger.warning("Problem getting meta data for %s, %s", url, e)
            return None

        if not response.ok:
            logger.warning(
                "Problem getting meta data for %s, %s",
                url, response.status_code,
            )
            return None

        return response

    def get_title_by_h1_tag(self, page_source, url):
        d = PyQuery(page_source)
        header = d("h1")

        if not header:
            logger.warning("Problem getting header for %s", url)
            return None

        if len(header) < 1:
            logger.warning("Problem getting header for %s", url)
            return None

        return header[0].text

    def get_title_by_title_tag(self, page_source, url):
        d = PyQuery(page_source)
        title = d("title")

        if not title:
            logger.warning("Problem getting title tag for %s", url)
            return None

        if len(title) < 1:
            logger.warning("Problem getting title tag for %s", url)
            return None

        return title[0].text

    def get_description(self, page_source, url):
        d = PyQuery(page_source)
        meta = d("meta")
        if not meta:
            logger.warning("Problem getting meta tag for %s", url)
            return None

        for tag in meta:
            if "name" in tag.keys():
                if tag.get("name") == "description":
                    return tag.get("content")

        logger.warning("Problem getting meta tag for %s", url)
        return None
