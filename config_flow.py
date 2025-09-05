# config_flow.py
from __future__ import annotations
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers import selector as sel
from homeassistant.helpers import area_registry as ar

DOMAIN = "REPTILE"  # change to your domain

class ReptileConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow: two strings + Area picker."""

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            # Persist as entry data
            area_id = user_input["area_id"]
            area = ar.async_get(self.hass).async_get_area(area_id)
            title = area.name if area and area.name else area_id
            return self.async_create_entry(
                title=title,
                data={
                    "name": user_input["name"],
                    "species": user_input["species"],
                    "area_id": area_id,
                },
            )

        # Build schema dynamically (rooms = Areas)
        schema = vol.Schema({
            vol.Required("name"): sel.selector({"text": {}}),     # free-form string
            vol.Required("species"): sel.selector({"text": {}}),  # free-form string
            vol.Required("area_id"): sel.selector({"area": {}}),  # dropdown of Areas
        })
        return self.async_show_form(step_id="user", data_schema=schema)
