import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

_LOGGER = logging.getLogger(__name__)

DOMAIN = "energy_proxy"
PLATFORMS = ["sensor"]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Imposta l'integrazione tramite UI."""
    _LOGGER.info("Inizializzazione Energy Dashboard Proxy")
    
    # Inoltra la configurazione alla piattaforma sensor.py
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Rimuove l'integrazione."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
