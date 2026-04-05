import logging
from homeassistant.components.energy import async_get_container
from homeassistant.components.sensor import SensorEntity
from homeassistant.components.recorder import get_instance
from homeassistant.components.recorder.statistics import statistics_during_period
from homeassistant.util import dt as dt_util

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Setup dei sensori basati sulla Energy Dashboard."""
    # Otteniamo i dati della dashboard energia
    energy_manager = await async_get_container(hass)
    energy_data = energy_manager.async_get_config()

    if not energy_data:
        _LOGGER.error("Energy Dashboard non configurata!")
        return

    entities = []
    # Cerchiamo i sensori di prelievo (flow_from) e immissione (flow_to)
    for source in energy_data.get("energy_sources", []):
        if source["type"] == "grid":
            for flow in source.get("flow_from", []):
                entities.append(EnergyProxySensor(hass, flow["stat_id"], "Prelievo"))
            for flow in source.get("flow_to", []):
                entities.append(EnergyProxySensor(hass, flow["stat_id"], "Immissione"))
    
    async_add_entities(entities, True)

class EnergyProxySensor(SensorEntity):
    """Sensore che estrae i dati annuali dalle LTS."""

    def __init__(self, hass, stat_id, type_name):
        self._hass = hass
        self._stat_id = stat_id
        self._attr_name = f"Energia Annua {type_name} ({stat_id})"
        self._attr_native_unit_of_measurement = "kWh"
        self._attr_state_class = "total_increasing"
        self._state = None

    @property
    def state(self):
        return self._state

    async def async_update(self):
        """Recupera i dati dalle statistiche a lungo termine."""
        start = dt_util.start_of_local_year()
        
        # Interroga il recorder per le statistiche
        stats = await get_instance(self._hass).async_add_executor_job(
            statistics_during_period,
            self._hass,
            start,
            None,
            {self._stat_id},
            "hour",
            None,
            {"change"}
        )

        if self._stat_id in stats:
            # Calcoliamo la somma dei cambiamenti (consumo/immissione) dall'inizio dell'anno
            total = sum(s["change"] for s in stats[self._stat_id] if s["change"] is not None)
            self._state = round(total, 2)
