# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Fixed
- Bad link in changelog

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

[Unreleased]: https://github.com/snarky-snark/home-assistant-variables/compare/v0.9.3...develop
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
