from homeassistant.core import CALLBACK_TYPE, callback
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.typing import (
    ConfigType,
    DiscoveryInfoType,
    HomeAssistantType,
)
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)
from typing import Any, Callable, Dict, Optional
import logging

_LOGGER = logging.getLogger(__name__)

DOMAIN = "csfd"

async def async_setup_platform(
    hass: HomeAssistantType,
    config: ConfigType,
    async_add_entities: Callable,
    discovery_info: Optional[DiscoveryInfoType] = None,
) -> None:
    """Set up the sensor platform."""
    # assuming API object stored here by __init__.py
    coordinator = hass.data[DOMAIN]['coordinator']

    async_add_entities([
        CSFDSensor(coordinator, 1),
        CSFDSensor(coordinator, 2),
        CSFDSensor(coordinator, 3)
    ])

    # Fetch initial data so we have data when entities subscribe
    await coordinator.async_refresh()

class CSFDSensor(CoordinatorEntity, SensorEntity):
    """Representation of a CSFD sensor."""

    def __init__(self, coordinator, idx):
        """Pass coordinator to CoordinatorEntity."""
        super().__init__(coordinator)
        self.idx = idx
        self._attr_movie_name = ''
        self._attr_movie_link = ''
        self._state = None
        self._available = True

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return self._available

    @property
    def movie_name(self):
        return self._attr_movie_name

    @property
    def movie_link(self):
        return self._attr_movie_link

    @property
    def name(self):
        """Return the name of the entity."""
        return self.movie_name

    @property
    def state(self):
        return self._state

    @property
    def state_attributes(self) -> dict[str, Any]:
        """Return the state attributes."""
        data = {}

        data["movie_name"] = self.movie_name
        data["movie_link"] = self.movie_link

        return data

    @property
    def unique_id(self):
        """Return the unique ID of the sensor."""
        return "csfd-movie-" + str(self.idx)

    @callback
    def _handle_coordinator_update(self):
        """Handle updated data from the coordinator."""
        movies = self.coordinator.data
        movie = movies[self.idx - 1]

        self._state = movie[1].get('rating', 0)
        self._attr_movie_name = movie[1].get('title', '')
        self._attr_movie_link = movie[1].get('link', '')

        self.async_write_ha_state()


