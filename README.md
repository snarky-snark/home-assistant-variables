# home-assistant-variables

A custom Home Assistant component for declaring and setting generic variable entities dynamically.

## Installation

Copy the `var` directory into the `custom_components` directory of your Home Assistant installation.

## Configuration

To add a variable, include it under the `var` component in your `configuration.yaml`. The following example adds two variable entities, `x` and `y`:
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
* **friendly_name**
  *(string)(Optional)*
  Name to use in the frontend.
* **friendly_name_template**
  *(template)(Optional)*
  Defines a template for the name to be used in the frontend (this overrides `friendly_name`).
* **initial_value**
  *(match_all)(Optional)*
  Initial value when Home Assistant starts.
* **value_template**
  *(template)(Optional)*
  Defines a template for the value (this overrides `initial_value`).
* **tracked_entity_id**
  *(string | list)(Optional)*
  A list of entity IDs so the variable reacts to state changes of these entities. This can be used if the automatic analysis fails to find all relevant entities to monitor in the templates.
* **tracked_event_type**
  *(string | list)(Optional)*
  A list of event types so the variable reacts to these events firing.
* **db_url**
  *(string)(Optional)*
  The URL which points to your database. See [supported engines](https://www.home-assistant.io/components/recorder/#custom-database-engines).
* **query**
  *(string)(Optional)*
  An SQL QUERY string, should return 1 result at most.
* **column**
  *(string)(Optional)*
  The SQL COLUMN to select from the result of the SQL QUERY.
* **restore**
  *(boolean)(Optional)*
  Restores the value of the variable whenever Home Assistant is restarted.
  
  Default value:
  true
* **unit_of_measurement**
  *(string)(Optional)*
  Defines the units of measurement of the variable, if any. This will also influence the graphical presentation in the history visualization as a continuous value. Variables with missing `unit_of_measurement` are showing as discrete values.
  
  Default value:
  None
* **icon**
  *(string)(Optional)*
  Icon to display for the component.
* **icon_template**
  *(template)(Optional)*
  Defines a template for the icon to be used in the frontend (this overrides icon).
* **entity_picture**
  *(string)(Optional)*
  Icon to display for the component.
* **entity_picture_template**
  *(template)(Optional)*
  Defines a template for the `entity_picture` to be used in the frontend (this overrides `entity_picture`).

## Services

### `set`
The `set` service can be used to update any of the attributes of the variable entity from an automation or a script (with the exception of `db_url`).

```yaml
var:
  daily_diaper_count:
    friendly_name: "Daily Diaper Count"
    initial_value: 0
    icon: mdi:toilet
  daily_bottle_feed_volume_milk:
    friendly_name: "Daily Milk Intake"
    initial_value: 0
    unit_of_measurement: 'ounces'
    icon: mdi:baby-bottle-outline
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
            - var.daily_bottle_feed_volume_milk
            - var.daily_bottle_feed_volume_formula
          value: 0
          icon: mdi:null
```

## Templates

The `var` component is modeled after the template sensor and SQL sensor components,
and many of the same features of these components are supported by the variable
component. In fact, a variable is basically a template sensor and an SQL sensor
with a service to set its state and attributes directly.

### SELECTING ENTITY/VALUE USING TEMPLATES
Templates can be used with the variable `set` service to select the `entity_id` and to set any of the attributes of a variable entity. This example shows `entity_id` and `value` being selected via template.
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
```
### DYNAMIC VARIABLE UPDATES USING TEMPLATES
This example shows how the value, and other attributes of the variable, can be set to update automatically based on the state of another entity. Template values will be updated whenever the state changes for any of the tracked entities listed below `tracked_entity_id`. 
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

### DYNAMIC VARIABLE UPDATES USING AN SQL QUERY
This example shows how the value, and other attributes of the variable, can be set to update automatically based on an SQL query. Template values will be updated whenever the state changes for any of the tracked entities listed below `tracked_entity_id` or when any event fires with the same event type
as any of the event types listed below `tracked_event_type`.
```yaml
var:
  todays_diaper_count:
    friendly_name: "Today's Diaper Count"
    unit_of_measurement: ' '
    query: "select count(*) as diaper_count from events where event_type = 'diaper_event' and time_fired between datetime('now', 'start of day') and datetime('now');"
    column: 'diaper_count'
    icon: mdi:toilet
    tracked_event_type:
      - diaper_event
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

Setting a `unit_of_measurement` will prompt Home Assistant to display
a two dimensional graph in its history panel and `history-graph` card.
```yaml
cards:
  - type: history-graph
    title: "Baby Plots"
    hours_to_show: 24
    entities:
      - entity: var.daily_bottle_feed_volume_milk
      - entity: var.daily_bottle_feed_volume_formula
```

Tip: Using a unit of `' '` can be useful if you want to group unit-less variables
together in a single 2D graph.

## Related Documentation

* [Template Sensor](https://www.home-assistant.io/components/template/)
* [SQL Sensor](https://www.home-assistant.io/components/sql/)

## Why?

I assembled this component for a few reasons:
* It was tedious to create a corresponding separate template sensor for each entity in the UI.
* I wanted a single general-purpose component, with a generic name, that could be used to store, update, and display values using templates.
* I didn't like using named UI components to store first-class data (e.g. `input_text`).
* I wanted a custom component that I could extend with more features in the future.
