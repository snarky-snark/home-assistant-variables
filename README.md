# home-assistant-variables

The `var` component is a Home Assistant integration for declaring and
setting generic variable entities. Variables can be set manually using
the `var.set` service or they can be set using templates or SQL queries
which will be run automatically whenever a specified event fires. The
`var` component depends on the `recorder` component for up-to-date SQL
queries and uses the same database setting.

<a href="https://www.buymeacoffee.com/snarkysnark" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy Me A Coffee" style="height: auto !important;width: auto !important;" ></a><br>

## Table of Contents
* [Installation](#installation)
  + [Manual Installation](#manual-installation)
  + [Installation via HACS](#installation-via-hacs)
* [Configuration](#configuration)
  + [Configuration Variables](#configuration-variables)
* [Services](#services)
  + [`var.set`](#varset)
    - [Parameters](#parameters)
    - [Example](#example)
  + [`var.update`](#varupdate)
    - [Parameters](#parameters-1)
    - [Example](#example-1)
* [Automatic Updates](#automatic-updates)
  + [Updating Using Tracked Entities](#updating-using-tracked-entities)
  + [Updating Using Tracked Event Types](#updating-using-tracked-event-types)
* [Templates](#templates)
  + [Selecting Entity/Value Using Templates](#selecting-entityvalue-using-templates)
  + [Dynamic Variable Updates Using Templates](#dynamic-variable-updates-using-templates)
* [SQL Queries](#sql-queries)
  + [Dynamic Variable Updates Using an SQL Query](#dynamic-variable-updates-using-an-sql-query)
  + [Filtering Event Data Using an SQL Query](#filtering-event-data-using-an-sql-query)
  + [Using an SQL Query in a Template](#using-an-sql-query-in-a-template)
* [Scenes](#scenes)
* [Lovelace UI](#lovelace-ui)
* [Reload](#reload)
* [Why?](#why)
* [Useful Links](#useful-links)

## Installation

### MANUAL INSTALLATION
1. Download the
   [latest release](https://github.com/snarky-snark/home-assistant-variables/releases/latest).
2. Unpack the release and copy the `custom_components/var` directory
   into the `custom_components` directory of your Home Assistant
   installation.
3. Add a `var` entry to your `configuration.yaml`.
4. Restart Home Assistant.

### INSTALLATION VIA HACS
1. Ensure that [HACS](https://custom-components.github.io/hacs/) is installed.
2. Search for and install the "Variable" integration.
3. Add a `var` entry to your `configuration.yaml`.
4. Restart Home Assistant.

## Configuration

To add a variable, include it under the `var` component in your
`configuration.yaml`. The following example adds two variable entities,
`x` and `y`:
```yaml
# Example configuration.yaml entry
var:
  x:
    friendly_name: 'X'
    initial_value: 0
    icon: mdi:bug
  y:
    friendly_name: 'Y'
    initial_value: 'Sleeping'
    entity_picture: '/local/sleep.png'
```

### CONFIGURATION VARIABLES

**var**
*(map) (Required)*
* **unique_id**
  *(string)(Optional)*
  Unique identifier for VAR entity, to enable overriding settings from within the UI, such as the entity name or room. Use with care, and only if explicitly required!
* **friendly_name**
  *(string)(Optional)*
  Name to use in the frontend.
* **friendly_name_template**
  *(template)(Optional)*
  Defines a template for the name to be used in the frontend (this
  overrides `friendly_name`).

  Note: `friendly_name_template` is evaluated every time an update
  is triggered for the variable (i.e., via `tracked_entity_id`, 
  `tracked_event_type`, or `var.update`). To pass a template to
  be evaluated once by `var.set`, use the `friendly_name`
  parameter in a `data_template`.
* **initial_value**
  *(match_all)(Optional)*
  Initial value when Home Assistant starts.
* **value_template**
  *(template)(Optional)*
  Defines a template for the value (this overrides `initial_value`).

  Note: `value_template` is evaluated every time an update
  is triggered for the variable (i.e., via `tracked_entity_id`, 
  `tracked_event_type`, or `var.update`). To pass a template to
  be evaluated once by `var.set`, use the `value`
  parameter in a `data_template`.
* **attributes**
  *(map)(Optional)*
  Dictionary of attributes equivalent to that of HomeAssistant [template sensor attributes](https://www.home-assistant.io/integrations/template/#attributes).

  Similar to *value_template*, attributes are evaluated on every update.
* **tracked_entity_id**
  *(string | list)(Optional)*
  A list of entity IDs so the variable reacts to state changes of these
  entities.
* **tracked_event_type**
  *(string | list)(Optional)*
  A list of event types so the variable reacts to these events firing.
* **query**
  *(string)(Optional)*
  An SQL QUERY string, should return 1 result at most.
* **column**
  *(string)(Optional)*
  The SQL COLUMN to select from the result of the SQL QUERY.
* **restore**
  *(boolean)(Optional)*
  Restores the value of the variable whenever Home Assistant is
  restarted.

  Default value:
  true
* **force_update**
  *(boolean)(Optional)*
  Trigger a state change event every time the value of the variable is
  updated, even if the value hasn't changed. If false, state change
  events will only be triggered by distinct changes in value.

  Default value:
  false
* **unit_of_measurement**
  *(string)(Optional)*
  Defines the units of measurement of the variable, if any. This will
  also influence the graphical presentation in the history visualization
  as a continuous value. Variables with missing `unit_of_measurement`
  are shown as discrete values.

  Default value:
  None
* **icon**
  *(string)(Optional)*
  Icon to display for the component.
* **icon_template**
  *(template)(Optional)*
  Defines a template for the icon to be used in the frontend (this
  overrides icon).

  Note: `icon_template` is evaluated every time an update
  is triggered for the variable (i.e., via `tracked_entity_id`, 
  `tracked_event_type`, or `var.update`). To pass a template to
  be evaluated once by `var.set`, use the `icon`
  parameter in a `data_template`.
* **entity_picture**
  *(string)(Optional)*
  Picture to display for the component.
* **entity_picture_template**
  *(template)(Optional)*
  Defines a template for the `entity_picture` to be used in the frontend
  (this overrides `entity_picture`).

  Note: `entity_picture_template` is evaluated every time an update
  is triggered for the variable (i.e., via `tracked_entity_id`, 
  `tracked_event_type`, or `var.update`). To pass a template to
  be evaluated once by `var.set`, use the `entity_picture`
  parameter in a `data_template`.

## Services

### `var.set`
The `set` service can be used to set the state or attributes of the
variable entity from an automation or a script. All config
parameters can also be set using `var.set`.

#### PARAMETERS
* **entity_id**
  *(string | list)(Required)*
  A list of `var` entity IDs to be set by the service.
* **friendly_name**
  *(string)(Optional)*
* **friendly_name_template**
  *(template)(Optional)*
* **value**
  *(match_all)(Optional)*
* **value_template**
  *(template)(Optional)*
* **attributes**
  *(map)(Optional)*
* **tracked_entity_id**
  *(string | list)(Optional)*
* **tracked_event_type**
  *(string | list)(Optional)*
* **query**
  *(string)(Optional)*
* **column**
  *(string)(Optional)*
* **restore**
  *(boolean)(Optional)*
* **force_update**
  *(boolean)(Optional)*
* **unit_of_measurement**
  *(string)(Optional)*
* **icon**
  *(string)(Optional)*
* **icon_template**
  *(template)(Optional)*
* **entity_picture**
  *(string)(Optional)*
* **entity_picture_template**
  *(template)(Optional)*

#### EXAMPLE
This example sets up an automation that resets the values of the
variables at midnight.
```yaml
var:
  daily_diaper_count:
    friendly_name: "Daily Diaper Count"
    initial_value: 0
    icon: mdi:toilet
  daily_bottle_feed_volume_formula:
    friendly_name: "Daily Formula Intake"
    initial_value: 0
    unit_of_measurement: 'ounces'
    icon: mdi:baby-bottle-outline

automation:
  - alias: "Reset Baby Counters"
    trigger:
      - platform: time
        at: '00:00:00'
    action:
      - service: var.set
        data:
          entity_id:
            - var.daily_diaper_count
            - var.daily_bottle_feed_volume_formula
          value: 0
          icon: mdi:null
```

### `var.update`
The `update` service can be used to force the variable entity to update
from an automation or a script.

#### PARAMETERS
* **entity_id**
  *(string | list)(Required)*
  A list of `var` entity IDs to be updated by the service.

#### EXAMPLE
This example sets up an automation that updates the variable every 5
minutes.
```yaml
var:
  temp_sensor_battery:
    friendly_name: "Temp Sensor Battery"
    value_template: "{{ state.attr('sensor.temperature', 'battery') }}"

automation:
  - alias: "Update Temp Sensor Battery Var Every 5 Minutes"
    trigger:
      - platform: time_pattern
        minutes: '/5'
    action:
      - service: var.update
        data:
          entity_id: var.temp_sensor_battery
```

Note: The `homeassistant.update_entity` service can be used more generally to update any entity, including `var` entities.

## Automatic Updates

### UPDATING USING TRACKED ENTITIES
A variable can be set to update whenever the state of an entity changes.
This example counts the number of times the state changes for
`input_boolean.foo` and `input_boolean.bar`.
```yaml
var:
  toggle_count:
    friendly_name: "Toggle Count"
    initial_value: 0
    value_template: "{{ (states('var.toggle_count') | int) + 1 }}"
    tracked_entity_id:
      - input_boolean.foo
      - input_boolean.bar
```

### UPDATING USING TRACKED EVENT TYPES
A variable can be set to update whenever an event fires. This example
multiplies variables `y` and `z` whenever `my_custom_event` fires.
```yaml
var:
  x:
    friendly_name: 'yz'
    value_template: "{{ (states('var.y') | int) * ( states('var.z') | int) }}"
    tracked_event_type: my_custom_event
    attributes:
      y: "{{ states('var.y') }}"
      z: "{{ states('var.z') }}"
```

## Templates

The `var` component shares features with the
[template sensor](https://www.home-assistant.io/components/template/).
Many of a variable's attributes can be set using templates.

### SELECTING ENTITY/VALUE USING TEMPLATES
Templates can be used with the variable `set` service to select the
`entity_id` and to set any of the attributes of a variable entity. This
example shows `entity_id` and `value` being selected via template.
```yaml
automation:
  - alias: "Handle Bottle Feed Event"
    trigger:
      platform: event
      event_type: bottle_feed_event
    action:
      service: var.set
      data_template:
        entity_id: >-
          {% if trigger.event.data.contents == 'milk' %}
            var.daily_bottle_feed_volume_milk
          {% elif trigger.event.data.contents == 'formula' %}
            var.daily_bottle_feed_volume_formula
          {% endif %}
        value: >-
          {% if trigger.event.data.contents == 'milk' %}
            {{ (states('var.daily_bottle_feed_volume_milk') | int) + (trigger.event.data.volume | int) }}
          {% elif trigger.event.data.contents == 'formula' %}
            {{ (states('var.daily_bottle_feed_volume_formula') | int) + (trigger.event.data.volume | int) }}
          {% endif %}
        attributes: >-
          last_feed_volume: "{{ trigger.event.data.volume }}"


```
### DYNAMIC VARIABLE UPDATES USING TEMPLATES
This example shows how the value, and other attributes of the variable,
can be set to update automatically based on the state of another entity.
Template values will be updated whenever the state changes for any of
the tracked entities listed below `tracked_entity_id`.
```yaml
var:
  waldo_location_status:
    friendly_name: "Waldo Location Status"
    value_template: >-
      {% if states('device_tracker.waldo_phone_wifi') == 'home' and states('device_tracker.waldo_phone_bluetooth') == 'home' %}
        Home
      {% else %}
        Unknown
      {% endif %}
    entity_picture_template: >-
      {% if states('var.waldo_location_status') == 'Home' %}
        /local/home.jpg
      {% else %}
        /local/question_mark.jpg
      {% endif %}
    tracked_entity_id:
      - device_tracker.waldo_phone_wifi
      - device_tracker.waldo_phone_bluetooth
      - var.waldo_location_status
```

## SQL Queries
The `var` component also shares features with the
[SQL sensor](https://www.home-assistant.io/components/sql/). When a
variable updates, it will run the SQL query against the Home Assistant
database updating the variable with the value of the query.

### DYNAMIC VARIABLE UPDATES USING AN SQL QUERY
This example shows how the value, and other attributes of the variable,
can be set to update automatically based on an SQL query. Template
values will be updated whenever the state changes for any of the tracked
entities listed below `tracked_entity_id` or when any event fires with
the same event type as any of the event types listed below
`tracked_event_type`.
```yaml
var:
  todays_diaper_count:
    friendly_name: "Today's Diaper Count"
    icon: mdi:toilet
    query: "SELECT COUNT(*) AS diaper_count FROM events WHERE event_type = 'diaper_event' AND time_fired BETWEEN DATETIME('now', 'start of day') AND DATETIME('now');"
    column: 'diaper_count'
    tracked_event_type: diaper_event
```

### FILTERING EVENT DATA USING AN SQL QUERY
This example shows how to use an SQL query to filter events based on
their `event_data`. In the example, `diaper_event` contains an
`event_data` entry called `type` that is either `wet`, `dirty`, or
`both`.
```yaml
var:
  todays_wet_diaper_count:
    friendly_name: "Today's Wet Diaper Count"
    icon: mdi:water
    query: "SELECT COUNT(*) AS diaper_count FROM events WHERE event_type = 'diaper_event' AND JSON_EXTRACT(event_data, '$.type') LIKE '%wet%' AND time_fired BETWEEN DATETIME('now', 'start of day') AND DATETIME('now');"
    column: 'diaper_count'
    tracked_event_type: diaper_event
```

### USING AN SQL QUERY IN A TEMPLATE
The result of a variable's SQL query can also be used within templates.
This example computes the average formula volume over the past week and
adds it to the variable `z`. In this example, `bottle_event` contains an
`event_data` entry called `volume` that contains the volume of formula.
```yaml
var:
  avg_formula_plus_z:
    friendly_name: "Average Formula Plus z"
    value_template: "{{ ( avg_formula | float) + ( states('var.z') | float) }}"
    query: "SELECT COALESCE(SUM(CAST(JSON_EXTRACT(event_data, '$.volume') AS FLOAT))/7.0, 0) AS avg_formula FROM events WHERE event_type = 'bottle_event' AND time_fired BETWEEN DATETIME('now', 'start of day', '-7 days') AND DATETIME('now', 'start of day');"
    column: 'avg_formula'
    tracked_event_type: bottle_event
```

## SCENES

You may set the values of variables with scenes:

```yaml
- name: My Scene
  entities:
    var.my_var: 'New Value'
```

## Lovelace UI

Variables can be displayed in the Lovelace frontend like other entities.

```yaml
cards:
  - type: entities
    title: "Baby Variables"
    entities:
      - entity: var.daily_diaper_count
      - entity: var.daily_bottle_feed_volume_milk
      - entity: var.daily_bottle_feed_volume_formula
```

Setting a `unit_of_measurement` will prompt Home Assistant to display a
two dimensional graph in its history panel and `history-graph` card.
```yaml
cards:
  - type: history-graph
    title: "Baby Plots"
    hours_to_show: 24
    entities:
      - entity: var.daily_bottle_feed_volume_milk
      - entity: var.daily_bottle_feed_volume_formula
```

Tip: Using a unit of `' '` can be useful if you want to group unit-less
variables together in a single 2D graph.

## Reload

Variable configuration can be reloaded without restarting HA using the 
YAML tab on the Developer Tools page. When the `var` component is loaded
an option will be added to the `YAML configuration reloading` section 
named `Variables`. Clicking this option will reload all `var` 
configuration.

Note: the component is only loaded by HA at startup when configuration 
is defined for the component. This means that if the `var` component is
installed and HA is restarted without `var` configuration the reload
option is not available yet. You have to add some configuration first 
and restart HA again before the reload option becomes available.

## Why?

I assembled this component for a few reasons:
* It was tedious to create a corresponding separate template sensor for
  each entity in the UI.
* I wanted a single general-purpose component, with a generic name, that
  could be used to store, update, and display values using templates.
* I didn't like using named UI components to store first-class data
  (e.g. `input_text`).
* I wanted to be able to work with data directly from the home assistant
  database (especially custom events) without having to create and
  flip-flop between a bunch of different entities.
* I wanted a custom component that I could extend with more features in
  the future.

## Useful Links

* [Template Sensor Documentation](https://www.home-assistant.io/components/template/)
* [SQL Sensor Documentation](https://www.home-assistant.io/components/sql/)
* [BuyMeACoffee?](https://www.buymeacoffee.com/snarkysnark) :persevere:

