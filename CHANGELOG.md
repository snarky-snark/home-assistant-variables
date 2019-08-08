# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.0] - 2019-08-07
### Added
- Variables can be backed by SQL queries.
- Variable updates occur when any tracked events fire.
- Updated README with documentation of SQL features.
- This CHANGELOG file.
### Changed
- Variable updates are now triggered after a database poll confirms that
  tracked events and state changes have been recorded in the databse.
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

[Unreleased]: https://github.com/snarky-snark/home-assistant-variables/compare/v0.2.0...develop
[0.2.0]: https://github.com/snarky-snark/home-assistant-variables/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/snarky-snark/home-assistant-variables/releases/tag/v0.1.0
