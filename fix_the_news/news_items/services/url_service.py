import logging
import time

import requests
from requests import exceptions as requests_exceptions


logger = logging.getLogger(__name__)


class NewsItemURLService:

    PREPEND_HTTP = "http://"
    PREPEND_HTTPS = "https://"
    MAX_RETRIES = 3
    SECONDS_TO_WAIT_BEFORE_RETRY = 2
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/83.0.4103.61 Safari/537.36",
    }

    def parse_and_validate(self, url):
        """ Returns parsed url and validation error if error exists """
        cleaned_url = url.strip()
        https_url = self.parse(cleaned_url)
        error = self.validate(https_url)
        if error:
            http_url = self.parse(cleaned_url, force_http=True)
            error = self.validate(http_url)
            if error:
                return cleaned_url, error
            return http_url, None
        return https_url, None

    def parse(self, url, force_http=False):
        if url.startswith(self.PREPEND_HTTP) \
                or url.startswith(self.PREPEND_HTTPS):
            return url

        if force_http:
            return f"{self.PREPEND_HTTP}{url}"

        return f"{self.PREPEND_HTTPS}{url}"

    def validate(self, url, retry=1):
        """ Returns an error if URL is not valid otherwise None """
        exception_message = "Error validating URL:%s error:%s"
        try:
            response = requests.get(url, headers=self.HEADERS)
        except (
            requests_exceptions.ConnectionError,
            requests_exceptions.ConnectTimeout,
        ) as error:
            if retry <= self.MAX_RETRIES:
                logger.debug(
                    "Error validating URL:%s error:%s retry:%s",
                    url, error, retry,
                )
                time.sleep(self.SECONDS_TO_WAIT_BEFORE_RETRY)
                return self.validate(url, retry + 1)
            else:
                logger.error(exception_message, url, error)
                return "Connection error"
        except requests_exceptions.SSLError as error:
            logger.error(exception_message, url, error)
            return "Site certificate not valid"

        if not response.ok:
            logger.error(
                "Error validating URL:%s status_code:%s response:%s",
                url, response.status_code, response.text,
            )
            return response.reason

        return None
