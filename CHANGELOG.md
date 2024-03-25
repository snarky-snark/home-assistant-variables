# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unrelease]

## [0.15.2] - 2024-03-25
### Fixed
- Fixed bad async call to synchronous method. Fixes #107. Thanks to [gamba69](https://github.com/gamba69).

## [0.15.1] - 2024-03-19
### Fixed
- Fixed startup warnings by replacing deprecated call to `async_update_ha_state`. Fixes #99. Thanks to [danielbrunt57](https://github.com/danielbrunt57).
- Sorted manifest entries.

## [0.15.0] - 2022-07-17
### Added
- Added configuration option to provide `unique_id` for var entities. Adding a `unique_id` allows variables to be edited via the Home Assistant GUI. Thanks again to [RoboMagus](https://github.com/RoboMagus)!

## [0.14.2] - 2022-06-29
### Fixed
- Updated import to account for [refactoring in the recorder component](https://github.com/home-assistant/core/pull/72977/commits/2a3cc48f921d7c4d6b5772989dc9466f730024b6#diff-3081799db8a9325527d03012208ed66e8667d5d0f807bcd499424fabb99c32ff) in HA 2022.7.0.

## [0.14.1] - 2022-06-08
### Fixed
- Fixed issue with tracked event listeners being dropped when var config reloads.

## [0.14.0] - 2022-06-08
### Added
- Added support by for variable attributes. Thanks to [RoboMagus](https://github.com/RoboMagus)!

## [0.13.1] - 2022-06-05
### Fixed
- Fixed broken database queries by moving database accesses off of the event thread. This addresses the [breaking change](https://github.com/home-assistant/core/pull/71547) introduced in Home Assistant 2022.04.

## [0.13.0] - 2022-06-01
### Added
- Added support for live reloading of var config. Thanks to [gertjanstulp](https://github.com/snarky-snark/home-assistant-variables/pull/69)!

## [0.12.3] - 2021-05-13
### Fixed
- Fixed stale version number in manifest that was stuck on v0.12.1.

## [0.12.2] - 2021-05-13
### Fixed
- The minimum supported version of HA is actually 2021.5.1.
  That is the HA release where sqlalchemy was upgraded to 1.4.

## [0.12.1] - 2021-05-13
### Fixed
- Fixed database calls to support HA's upgrade to sqlalchemy 1.4.
  The minimum supported version of HA is now 2021.5.3.
- Fixed stale version number in manifest that was stuck on v0.11.0.

## [0.12.0] - 2021-04-28
### Added
- Added `iot_class` entry to `manifest.json` to comply with latest HA requirements.

## [0.11.0] - 2021-03-05
### Added
- Added `version` entry to `manifest.json` in conformance with latest HA requirements.
- Added hassfest GitHub Action for automatic validation of commits against HA requirements.

## [0.10.0] - 2021-01-17
### Fixed
- Bad link in changelog
### Added
- Added support for setting vars via scenes.

## [0.9.3] - 2020-04-08
### Fixed
- Fix var component config error when component is loaded on HA startup. 
- Typos in README.
- Add pycache to .gitignore.

## [0.9.2] - 2019-12-12
### Fixed
- Fix schema for `var.update` service (broken in 0.9.0).

## [0.9.1] - 2019-12-11
### Fixed
- Changed minimum supported HA version in hacs.json to support HA 0.103.0. Due to a bug in HACS, this didn't work in v0.9.0.

## [0.9.0] - 2019-12-06
### Removed
- Remove deprecated documentation in README regarding automatic entity analysis.
### Fixed
- Updated component to be compatible with Home Assistant 0.103.0. This release is not backward compatible with previous versions of Home Assistant.

## [0.8.0] - 2019-10-06
### Added
- Added more documentation on template parameters.
- Added HACS manifest.
- New `force_update` parameter to trigger variable state change
  events when the variable state is updated but the value is unchanged.
### Removed
- Removed obsolete HACS `info.md`.
### Fixed
- Fixed a broken link in README table of contents.

## [0.7.0] - 2019-08-14
### Added
- Added info page for display in HACS.

## [0.6.0] - 2019-08-11
### Changed
- An update is no longer triggered by default on Home Assistant startup.
  To force a variable to update on startup, add `homeassistant_start` to
  the variable's `tracked_event_type` list.

## [0.5.0] - 2019-08-09
### Removed
- Tracked entities are no longer parsed from templates automatically.
  This was an undocumented feature that was confusing as implemented.

## [0.4.0] - 2019-08-09
### Added
- `var.update` service used to force a variable to update from an
  automation or script.
### Fixed
- Template processing was broken for `var.set` service. It is now fixed.

## [0.3.0] - 2019-08-09
### Added
- More examples, detail, and table of contents to README
### Fixed
- In addition to a list of events, `tracked_event_type` now accepts a
  string containing a single event or a string containing multiple
  events separated by commas.

## [0.2.1] - 2019-08-08
### Added
- README now contains instructions for installing via HACS.
- README now contains a link to the latest release on GitHub.
### Changed
- Variables only poll the database if a query has been specified.
### Fixed
- CHANGELOG version links now point to correct git repository.
- CHANGELOG typos.
- Values are no longer erased when the `var.set` service is called. This
  bug was introduced in 0.2.0.

## [0.2.0] - 2019-08-07
### Added
- Variables can be backed by SQL queries.
- Variable updates occur when any tracked events fire.
- Updated README with documentation of SQL features.
- This CHANGELOG file.
### Changed
- Variable updates are now triggered after a database poll confirms that
  tracked events and state changes have been recorded in the database.
  Before, variables updated immediately after a state change event
  fired.
- `var` integration now depends on `recorder`.

## [0.1.0] - 2019-08-01
### Added
- Initial `var` integration.
- `var.set` service for updating variable state and attributes.
- Variables update automatically based on state and attribute templates.
- Variable updates occur when the state of any tracked entity changes.
- README with initial documentation.

[Unreleased]: https://github.com/snarky-snark/home-assistant-variables/compare/v0.15.2...develop
[0.15.2]: https://github.com/snarky-snark/home-assistant-variables/compare/v0.15.1...v0.15.2
[0.15.1]: https://github.com/snarky-snark/home-assistant-variables/compare/v0.15.0...v0.15.1
[0.15.0]: https://github.com/snarky-snark/home-assistant-variables/compare/v0.14.2...v0.15.0
[0.14.2]: https://github.com/snarky-snark/home-assistant-variables/compare/v0.14.1...v0.14.2
[0.14.1]: https://github.com/snarky-snark/home-assistant-variables/compare/v0.14.0...v0.14.1
[0.14.0]: https://github.com/snarky-snark/home-assistant-variables/compare/v0.13.1...v0.14.0
[0.13.1]: https://github.com/snarky-snark/home-assistant-variables/compare/v0.13.0...v0.13.1
[0.13.0]: https://github.com/snarky-snark/home-assistant-variables/compare/v0.12.3...v0.13.0
[0.12.3]: https://github.com/snarky-snark/home-assistant-variables/compare/v0.12.2...v0.12.3
[0.12.2]: https://github.com/snarky-snark/home-assistant-variables/compare/v0.12.1...v0.12.2
[0.12.1]: https://github.com/snarky-snark/home-assistant-variables/compare/v0.12.0...v0.12.1
[0.12.0]: https://github.com/snarky-snark/home-assistant-variables/compare/v0.11.0...v0.12.0
[0.11.0]: https://github.com/snarky-snark/home-assistant-variables/compare/v0.10.0...v0.11.0
[0.10.0]: https://github.com/snarky-snark/home-assistant-variables/compare/v0.9.3...v0.10.0
[0.9.3]: https://github.com/snarky-snark/home-assistant-variables/compare/v0.9.2...v0.9.3
[0.9.2]: https://github.com/snarky-snark/home-assistant-variables/compare/v0.9.1...v0.9.2
[0.9.1]: https://github.com/snarky-snark/home-assistant-variables/compare/v0.9.0...v0.9.1
[0.9.0]: https://github.com/snarky-snark/home-assistant-variables/compare/v0.8.0...v0.9.0
[0.8.0]: https://github.com/snarky-snark/home-assistant-variables/compare/v0.7.0...v0.8.0
[0.7.0]: https://github.com/snarky-snark/home-assistant-variables/compare/v0.6.0...v0.7.0
[0.6.0]: https://github.com/snarky-snark/home-assistant-variables/compare/v0.5.0...v0.6.0
[0.5.0]: https://github.com/snarky-snark/home-assistant-variables/compare/v0.4.0...v0.5.0
[0.4.0]: https://github.com/snarky-snark/home-assistant-variables/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/snarky-snark/home-assistant-variables/compare/v0.2.1...v0.3.0
[0.2.1]: https://github.com/snarky-snark/home-assistant-variables/compare/v0.2.0...v0.2.1
[0.2.0]: https://github.com/snarky-snark/home-assistant-variables/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/snarky-snark/home-assistant-variables/releases/tag/v0.1.0
