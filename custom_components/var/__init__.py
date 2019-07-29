"""Allows the creation of generic variable entities."""

import logging

import voluptuous as vol

from homeassistant.core import callback
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.config_validation import ENTITY_SERVICE_SCHEMA
from homeassistant.const import (
    ATTR_FRIENDLY_NAME, ATTR_UNIT_OF_MEASUREMENT, CONF_VALUE_TEMPLATE,
    CONF_ICON, CONF_ICON_TEMPLATE, ATTR_ENTITY_PICTURE,
    CONF_ENTITY_PICTURE_TEMPLATE, ATTR_ENTITY_ID,
    EVENT_HOMEASSISTANT_START, CONF_FRIENDLY_NAME_TEMPLATE, MATCH_ALL)
from homeassistant.exceptions import TemplateError
from homeassistant.helpers.entity import async_generate_entity_id
from homeassistant.helpers.entity_component import EntityComponent
from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.helpers.event import async_track_state_change

_LOGGER = logging.getLogger(__name__)

DOMAIN = 'var'
ENTITY_ID_FORMAT = DOMAIN + '.{}'

CONF_INITIAL_VALUE = "initial_value"
CONF_RESTORE = "restore"

ATTR_VALUE = 'value'
ATTR_TRACKED_ENTITY_ID = 'tracked_entity_id'

SERVICE_SET = "set"
SERVICE_SET_SCHEMA = ENTITY_SERVICE_SCHEMA.extend({
        vol.Optional(ATTR_VALUE): cv.match_all,
        vol.Optional(CONF_VALUE_TEMPLATE): cv.template,
        vol.Optional(ATTR_UNIT_OF_MEASUREMENT): cv.string,
        vol.Optional(CONF_RESTORE): cv.boolean,
        vol.Optional(ATTR_FRIENDLY_NAME): cv.string,
        vol.Optional(CONF_FRIENDLY_NAME_TEMPLATE): cv.template,
        vol.Optional(CONF_ICON): cv.icon,
        vol.Optional(CONF_ICON_TEMPLATE): cv.template,
        vol.Optional(ATTR_ENTITY_PICTURE): cv.string,
        vol.Optional(CONF_ENTITY_PICTURE_TEMPLATE): cv.template,
        vol.Optional(ATTR_TRACKED_ENTITY_ID): cv.entity_ids,
})

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        cv.slug: vol.Any({
            vol.Optional(CONF_INITIAL_VALUE): cv.match_all,
            vol.Optional(CONF_VALUE_TEMPLATE): cv.template,
            vol.Optional(ATTR_UNIT_OF_MEASUREMENT): cv.string,
            vol.Optional(CONF_RESTORE): cv.boolean,
            vol.Optional(ATTR_FRIENDLY_NAME): cv.string,
            vol.Optional(CONF_FRIENDLY_NAME_TEMPLATE): cv.template,
            vol.Optional(CONF_ICON): cv.icon,
            vol.Optional(CONF_ICON_TEMPLATE): cv.template,
            vol.Optional(ATTR_ENTITY_PICTURE): cv.string,
            vol.Optional(CONF_ENTITY_PICTURE_TEMPLATE): cv.template,
            vol.Optional(ATTR_TRACKED_ENTITY_ID): cv.entity_ids,
        }, None)
    })
}, extra=vol.ALLOW_EXTRA)

def parse_template_entity_ids(hass, object_id, value_template,
                              icon_template, entity_picture_template,
                              friendly_name_template):
    """Parse entity_ids from templates."""
    entity_ids = set()
    invalid_templates = []

    for tpl_name, template in (
       (CONF_VALUE_TEMPLATE, value_template),
       (CONF_ICON_TEMPLATE, icon_template),
       (CONF_ENTITY_PICTURE_TEMPLATE, entity_picture_template),
       (CONF_FRIENDLY_NAME_TEMPLATE, friendly_name_template),
    ):
        if template is None:
            continue
        template.hass = hass

        template_entity_ids = template.extract_entities()
        if template_entity_ids == MATCH_ALL:
            entity_ids = None
            # Cut off _template from name
            invalid_templates.append(tpl_name[:-9])
        elif entity_ids is not None:
            entity_ids |= set(template_entity_ids)

    if invalid_templates:
        _LOGGER.warning(
            'Variable %s has no entity ids configured to track nor'
            ' were we able to extract the entities to track from the %s '
            'template(s). This entity will only be able to be updated '
            'manually.', object_id, ', '.join(invalid_templates))

    if entity_ids is not None:
        entity_ids = list(entity_ids)

    return entity_ids

async def async_setup(hass, config):
    """Set up variables from config."""
    component = EntityComponent(_LOGGER, DOMAIN, hass)
    await component.async_setup(config)

    entities = []

    for object_id, cfg in config[DOMAIN].items():
        if not cfg:
            cfg = {}

        initial_value = cfg.get(CONF_INITIAL_VALUE)
        unit = cfg.get(ATTR_UNIT_OF_MEASUREMENT)
        restore = cfg.get(CONF_RESTORE, True)
        friendly_name = cfg.get(ATTR_FRIENDLY_NAME, object_id)
        icon = cfg.get(CONF_ICON)
        entity_picture = cfg.get(ATTR_ENTITY_PICTURE)

        value_template = cfg.get(CONF_VALUE_TEMPLATE)
        friendly_name_template = cfg.get(CONF_FRIENDLY_NAME_TEMPLATE)
        icon_template = cfg.get(CONF_ICON_TEMPLATE)
        entity_picture_template = cfg.get(CONF_ENTITY_PICTURE_TEMPLATE)

        manual_entity_ids = cfg.get(ATTR_ENTITY_ID)
        
        tracked_entity_ids = list()
        if manual_entity_ids is not None:
            tracked_entity_ids = list(set(manual_entity_ids))
        else:
            template_entity_ids = parse_template_entity_ids(
                hass, object_id, value_template, icon_template,
                entity_picture_template, friendly_name_template)
            if template_entity_ids is not None:
                tracked_entity_ids = template_entity_ids

        entities.append(
            Variable(
                hass,
                object_id,
                initial_value,
                value_template,
                unit,
                restore,
                friendly_name,
                friendly_name_template,
                icon,
                icon_template,
                entity_picture,
                entity_picture_template,
                tracked_entity_ids)
            )

    if not entities:
        return False

    component.async_register_entity_service(
        SERVICE_SET, SERVICE_SET_SCHEMA,
        'async_set'
    )

    await component.async_add_entities(entities)
    return True

class Variable(RestoreEntity):
    """Representation of a variable."""

    def __init__(self, hass, object_id, initial_value, value_template, unit,
                 restore, friendly_name, friendly_name_template, icon,
                 icon_template, entity_picture, entity_picture_template,
                 tracked_entity_ids):
        """Initialize a variable."""
        self.hass = hass
        self.entity_id = ENTITY_ID_FORMAT.format(object_id)
        self._value = initial_value
        self._initial_value = initial_value
        self._value_template = value_template
        self._unit = unit
        self._restore = restore
        self._friendly_name = friendly_name
        self._friendly_name_template = friendly_name_template
        self._icon = icon
        self._icon_template = icon_template
        self._entity_picture = entity_picture
        self._entity_picture_template = entity_picture_template
        self._tracked_entity_ids = tracked_entity_ids
        self._stop_track_state_change = None

    def _get_variable_template_state_listener(self):
        @callback
        def listener(entity, old_state, new_state):
            """Handle device state changes."""
            self.async_schedule_update_ha_state(True)
        return listener

    async def async_added_to_hass(self):
        """Register callbacks."""

        @callback
        def variable_template_startup(event):
            """Update template on startup."""
            if self._tracked_entity_ids:
                # Track state changes for specified entities
                listener = self._get_variable_template_state_listener()
                self._stop_track_state_change = async_track_state_change(
                    self.hass, self._tracked_entity_ids, listener)

            self.async_schedule_update_ha_state(True)

        self.hass.bus.async_listen_once(
            EVENT_HOMEASSISTANT_START, variable_template_startup)
        
        # Restore previous value on startup
        await super().async_added_to_hass()
        if self._restore == True:
            state = await self.async_get_last_state()
            if state:
                self._value = state.state

    @property
    def should_poll(self):
        """If entity should be polled."""
        return False

    @property
    def name(self):
        """Return the name of the variable."""
        return self._friendly_name

    @property
    def icon(self):
        """Return the icon to be used for this entity."""
        return self._icon

    @property
    def entity_picture(self):
        """Return the entity_picture to be used for this entity."""
        return self._entity_picture

    @property
    def state(self):
        """Return the state of the component."""
        return self._value

    @property
    def unit_of_measurement(self):
        """Return the unit the value is expressed in."""
        return self._unit

    @property
    def _templates_dict(self):
        return {'_value': self._value_template,
                '_name': self._friendly_name_template,
                '_icon': self._icon_template,
                '_entity_picture': self._entity_picture_template}

    async def async_set(self,
            value=None,
            value_template=None,
            unit=None,
            restore=None,
            friendly_name=None,
            friendly_name_template=None,
            icon=None,
            icon_template=None,
            entity_picture=None,
            entity_picture_template=None,
            manual_tracked_entity_ids=None):
        """Set new attributes for the variable."""
        if value is not None:
            self._value = value
        if unit is not None:
            self._unit = unit
        if restore is not None:
            self._restore = restore
        if friendly_name is not None:
            self._friendly_name = friendly_name
        if icon is not None:
            self._icon = icon
        if entity_picture is not None:
            self._entity_picture = entity_picture
        for property_name, template in self._templates_dict.items():
            if template is not None:
                setattr(self, property_name, template.async_render())

        tracked_entity_ids = None
        if manual_tracked_entity_ids is not None:
            tracked_entity_ids = manual_tracked_entity_ids
        elif any(t is not None for t in self._templates_dict.values()):
            template_entity_ids = parse_template_entity_ids(
                hass, object_id, *self._templates_dict.values())
            if template_entity_ids is not None:
                tracked_entity_ids = template_entity_ids

        if tracked_entity_ids is not None:
            if self._stop_track_state_change:
                self._stop_track_state_change()
            self._tracked_entity_ids = tracked_entity_ids
            listener = self._get_variable_template_state_listener()
            self._stop_track_state_change = async_track_state_change(
                self.hass, self._tracked_entity_ids, listener)

        await self.async_update_ha_state()

    async def async_update(self):
        """Update the state from the template."""
        for property_name, template in self._templates_dict.items():
            if template is None:
                continue

            try:
                setattr(self, property_name, template.async_render())
            except TemplateError as ex:
                friendly_property_name = property_name[1:].replace('_', ' ')
                if ex.args and ex.args[0].startswith(
                        "UndefinedError: 'None' has no attribute"):
                    # Common during HA startup - so just a warning
                    _LOGGER.warning('Could not render %s template %s,'
                                    ' the state is unknown.',
                                    friendly_property_name, self._friendly_name)
                    continue

                try:
                    setattr(self, property_name, getattr(super(), property_name))
                except AttributeError:
                    _LOGGER.error('Could not render %s template %s: %s',
                                  friendly_property_name, self._friendly_name, ex)

