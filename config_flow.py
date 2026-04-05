from homeassistant import config_entries
from .const import DOMAIN = "Incentivi-GSE---SSP-e-RID"

class IncentiviGSEConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Gestisce il processo di setup iniziale."""
    async def async_step_user(self, user_input=None):
        if self._async_current_entries():
            return self.async_abort(reason="already_configured")
        
        if user_input is not None:
            return self.async_create_entry(title="Incentivi-GSE---SSP-e-RID", data={})

        return self.async_show_form(step_id="user")
