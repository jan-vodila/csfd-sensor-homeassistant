from bs4 import BeautifulSoup
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)
import logging
import re
import requests
from datetime import timedelta

_LOGGER = logging.getLogger(__name__)

DOMAIN = "csfd"

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Your controller/hub specific code."""
    hass.data[DOMAIN] = {
        'coordinator': CSFDCoordinator(hass, CSFDApi(hass))
    }
    hass.async_add_job(hass.helpers.discovery.async_load_platform('sensor', DOMAIN, {}, config))

    return True

class CSFDApi:
    def __init__(self, hass: HomeAssistant):
        self._hass = hass
        self.movies = {}

    async def fetch_movies(self):
        def getProgram():
            return requests.get("https://www.csfd.sk/kino/", params = {'period': 'tomorrow', 'district': 94}, headers = {'User-agent': 'HomeAssistant'})

        try:
            page = await self._hass.async_add_executor_job(getProgram);
            soup = BeautifulSoup(page.content, "html.parser")
            movies_elements = soup.find_all(class_="film-title-nooverflow")
            for movie_element in movies_elements:
                if "red" in movie_element.i['class']:
                    link_element = movie_element.a
                    id = re.search('\/film\/([0-9]*)-', link_element['href']).group(1)
                    self.movies[id] = {
                        'title': link_element.get_text(),
                        'link': "https://www.csfd.sk" + link_element['href'],
                        'rating': 0
                    }
        except Exception:
            _LOGGER.exception("Error retrieving program from CSFD.")

    async def fetch_movies_rating(self):
        def getMovie(link):
            return requests.get(link, headers = {'User-agent': 'HomeAssistant'})

        for key in self.movies:
            try:
                page = await self._hass.async_add_executor_job(lambda: getMovie(self.movies[key]['link']));
                soup = BeautifulSoup(page.content, "html.parser")
                rating_element = soup.select_one(".aside-movie-profile .film-rating-average")
                self.movies[key]['rating'] = rating_element.get_text().strip().strip('%')

            except Exception:
                _LOGGER.exception("Error retrieving movie " + self.movies[key]['title'] + " from CSFD (" + self.movies[key]['link'] + ").")

    def sort_movies(self):
        self.movies = sorted(self.movies.items(),key=(lambda i: i[1]['rating']),reverse=True)

    async def update(self):
        self.movies = {}
        await self.fetch_movies()
        await self.fetch_movies_rating()
        self.sort_movies()
        return self.movies

class CSFDCoordinator(DataUpdateCoordinator):
    """CSFD coordinator."""

    def __init__(self, hass: HomeAssistant, csfd_api):
        """Initialize my coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            # Name of the data. For logging purposes.
            name=DOMAIN,
            # Polling interval. Will only be polled if there are subscribers.
            update_interval=timedelta(days=1),
        )
        self.csfd_api = csfd_api

    async def _async_update_data(self):
        """Fetch data from API endpoint."""
        return await self.csfd_api.update()