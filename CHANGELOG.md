# CHANGELOG


## v1.0.0 (2025-04-16)

### Bug Fixes

- **change_history**: Missing author name on committed remove field
  ([`42481fb`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/42481fb95764b96361148923e50ff60304a32d07))

### Features

- Breaking CHANGE: major release for QGIS Track Changes 1.0.0
  ([`7834c60`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/7834c609882138e4f799536815565165756fb49e))

### Refactoring

- Add pre commit hook for ruff formatter
  ([#78](https://github.com/ahmadzfaiz/qgis-track-changes/pull/78),
  [`cffcb49`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/cffcb49c0fc2ee2d024575da7811238a54362425))

- Linting default logger and resources
  ([`2cc3a0d`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/2cc3a0d5b538db9d0ca5f2e0767e11935e5070e4))

- Reapply ruff formatting ([#78](https://github.com/ahmadzfaiz/qgis-track-changes/pull/78),
  [`dc7a133`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/dc7a1334ba2ebb716e260a1b9b2ee2bc764be4b8))

- **about**: Linting on about page ([#78](https://github.com/ahmadzfaiz/qgis-track-changes/pull/78),
  [`8f2ecb6`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/8f2ecb6877bcd0a22d1be96d37772b069836fba8))

- **gpkg_logger**: Linting gpkg logger
  ([#78](https://github.com/ahmadzfaiz/qgis-track-changes/pull/78),
  [`37d711b`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/37d711b9b6eaf4b52d9e9a59552480e87593ea5b))

- **main_code**: Refactor all the main code with ruff
  ([#78](https://github.com/ahmadzfaiz/qgis-track-changes/pull/78),
  [`4f86cfc`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/4f86cfcb78795176d4fd84b53a66877e384ba769))

- **main_plugin**: Linting main_plugin functionality
  ([#78](https://github.com/ahmadzfaiz/qgis-track-changes/pull/78),
  [`ee5eaf9`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/ee5eaf9018f1e97493fa4879f00c87e482e75672))

- **ui**: Ruff formating on UI scripts
  ([#78](https://github.com/ahmadzfaiz/qgis-track-changes/pull/78),
  [`da7b9e1`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/da7b9e1c6c7f557b3ea131c4595f9404eaabbd6f))

### Testing

- **main_plugin**: Temporary disable test initGui
  ([`dc4ead4`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/dc4ead4f92e2023ff6e7b80c6460bdb350f5739f))

### Breaking Changes

- Major release for QGIS Track Changes 1.0.0


## v0.13.0 (2025-04-15)

### Bug Fixes

- **default_logger**: Fix different change code
  ([#77](https://github.com/ahmadzfaiz/qgis-track-changes/pull/77),
  [`ce5bd15`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/ce5bd15f3637b70e6c5c743a67243c6c0e9b4d8c))

### Chores

- **change_history**: Remove label that only support GPKG in table
  ([#77](https://github.com/ahmadzfaiz/qgis-track-changes/pull/77),
  [`c6b217f`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/c6b217f92aaa2811a7d7a7cf9c7474b628d6cf32))

- **logger**: Add qgis track changes into GPKG extension list
  ([#85](https://github.com/ahmadzfaiz/qgis-track-changes/pull/85),
  [`2e4cc83`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/2e4cc83cf9091a381ea67ff8d532e7e3996783ac))

### Features

- **change_history**: Add dashboard for logfile
  ([#77](https://github.com/ahmadzfaiz/qgis-track-changes/pull/77),
  [`f2f34d7`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/f2f34d7a9d9d8a4f5f5daf187b761615dc64c4c9))

- **change_history**: Add log file to track the changes
  ([#77](https://github.com/ahmadzfaiz/qgis-track-changes/pull/77),
  [`ac00c89`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/ac00c892604715ebb87fa8defb7bceceac679dc3))


## v0.12.0 (2025-04-13)

### Continuous Integration

- **release**: Add pandas library
  ([`3fec722`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/3fec7223f12a2f594b3ba471468945f4d3044a28))

### Documentation

- Update tracking code status
  ([`f6a31b6`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/f6a31b6655d5a578cd649aada664de14a5a0bd4c))

### Features

- **data_comparison**: Add feature to compare gpkg data
  ([#76](https://github.com/ahmadzfaiz/qgis-track-changes/pull/76),
  [`59f607f`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/59f607f10820f26b92cec16719c2716fd2746635))

- **data_comparison**: Close connection after compare
  ([#76](https://github.com/ahmadzfaiz/qgis-track-changes/pull/76),
  [`ad71757`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/ad71757d04870cc099e8adc7f28bee6be93a8acd))


## v0.11.0 (2025-04-13)

### Bug Fixes

- **change_history**: Humanize datetime now with utc fix error
  ([#75](https://github.com/ahmadzfaiz/qgis-track-changes/pull/75),
  [`0662d20`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/0662d20acea9e99e4f0ea53d1532eb4d1a538de4))

### Features

- **change_history**: Add dashboard
  ([#70](https://github.com/ahmadzfaiz/qgis-track-changes/pull/70),
  [`d24a815`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/d24a815399244458b192c9ca7c4ee850f4b9a3c8))

- **change_history**: Changing dashboard with dropdown picker
  ([#70](https://github.com/ahmadzfaiz/qgis-track-changes/pull/70),
  [`c601e12`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/c601e124c947356ad8be3956eaba9c1f17ad2f0b))

- **change_history**: Changing gpkg path will refresh the chart canvas
  ([#70](https://github.com/ahmadzfaiz/qgis-track-changes/pull/70),
  [`fab8bd3`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/fab8bd3cd8602b63f463ca9290a3b36a2d57b411))

- **change_history**: Use committed data tracking, not current data tracking
  ([#70](https://github.com/ahmadzfaiz/qgis-track-changes/pull/70),
  [`074799b`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/074799bc6b64180180c45002eb03fa5350fe7e76))

### Testing

- **about_widget**: Fix unittest
  ([`2940154`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/294015453cbca118dcb549924e6e4ec8e3431e5a))

- **about_widget**: Fix unittest
  ([`75018a4`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/75018a4252eb82368899e82b363aa447fb503c41))


## v0.10.1 (2025-04-11)

### Bug Fixes

- **default_logger**: Convert asctime logger to UTC time
  ([#75](https://github.com/ahmadzfaiz/qgis-track-changes/pull/75),
  [`a0afcd7`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/a0afcd71230d7c0efd3e193e6fc34830e34bc0f8))

- **gpkg_logger**: Convert timestamp logger to UTC time
  ([#75](https://github.com/ahmadzfaiz/qgis-track-changes/pull/75),
  [`571165d`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/571165dc5e4fd08df58dfd75cb93fa3dc1cd3542))


## v0.10.0 (2025-04-09)

### Bug Fixes

- **gpkg_logger**: Fixing health check database connection
  ([#71](https://github.com/ahmadzfaiz/qgis-track-changes/pull/71),
  [`71e9323`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/71e93235650340f84f08f646653090c074aa9b73))

- **gpkg_logger**: Version commit with no version change don't create new data version id
  ([#71](https://github.com/ahmadzfaiz/qgis-track-changes/pull/71),
  [`1c9a5eb`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/1c9a5ebdbc48b9c02cfade349b4cee7c11ff6daf))

### Features

- **gpkg_logger**: Add actions number 25 and 26
  ([#71](https://github.com/ahmadzfaiz/qgis-track-changes/pull/71),
  [`7dabe33`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/7dabe333c0cae74d3ff986185f6b58b538ff1e2f))

- **gpkg_logger**: Add versioning functionality on commit changes
  ([#71](https://github.com/ahmadzfaiz/qgis-track-changes/pull/71),
  [`fb0685b`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/fb0685bbcabfa54c6fa0b0334df3b9de56dd550f))


## v0.9.2 (2025-04-08)

### Bug Fixes

- **change_history**: Handle error on sqlite query of gpkg changelog
  ([#67](https://github.com/ahmadzfaiz/qgis-track-changes/pull/67),
  [`18006b6`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/18006b6fb38b46b68443574e976e4e83e3d9d924))

### Chores

- **metadata**: Add new tag
  ([`68755f2`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/68755f25762a4163af5d7b825a4a28e7f9599337))

- **metadata**: Remove experimental tag
  ([`0c6cb20`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/0c6cb205895f75263f418531d01824c3b7be3b39))

### Continuous Integration

- **unittest**: Add unittest in CI/CD
  ([#69](https://github.com/ahmadzfaiz/qgis-track-changes/pull/69),
  [`3091f97`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/3091f97fa1b5ee888ac0196dc20bbcd1f14de0cf))

- **unittest**: Fix QGIS related test CI/CD
  ([#69](https://github.com/ahmadzfaiz/qgis-track-changes/pull/69),
  [`3581f65`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/3581f65eca1c1edd05d172fc82827d58f5b782ae))

### Testing

- Add unittests for all functionality
  ([#69](https://github.com/ahmadzfaiz/qgis-track-changes/pull/69),
  [`a5d7c36`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/a5d7c36a1f46fa159ea0d60964c8a231c32c82ee))

- **change_history**: Create a proper test to check gpkg with, without or empty changelog
  ([#67](https://github.com/ahmadzfaiz/qgis-track-changes/pull/67),
  [`976be3e`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/976be3e133017af7abfa2143c73a4c229c92d3f5))


## v0.9.1 (2025-04-07)

### Bug Fixes

- **gpkg_logger**: Add highlight in initial active layer
  ([#66](https://github.com/ahmadzfaiz/qgis-track-changes/pull/66),
  [`e6bb9a4`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/e6bb9a4dae653bf51e8b15736e209479bee3fe79))

- **gpkg_logger**: After refresh the file selection, remove highlight not working
  ([#66](https://github.com/ahmadzfaiz/qgis-track-changes/pull/66),
  [`bdd1ce0`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/bdd1ce05112c3756e6498e20b9bafcb5ecb8d6a0))

- **gpkg_logger**: Fix first selection that not trigger highlight
  ([#66](https://github.com/ahmadzfaiz/qgis-track-changes/pull/66),
  [`6c9a7d1`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/6c9a7d14783245d4dca76903a72a8629565628f0))

### Chores

- **about**: Remove color in version number text
  ([`e6fda1a`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/e6fda1a9acb8a12b2c75d2dc6206f3f38e4e3557))


## v0.9.0 (2025-04-07)

### Chores

- **about**: Display tab ([#41](https://github.com/ahmadzfaiz/qgis-track-changes/pull/41),
  [`94334ce`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/94334ce3cf9c06a09e02d0102424c9ee83eacbc3))

### Features

- **info**: Add table info to display data changes
  ([#41](https://github.com/ahmadzfaiz/qgis-track-changes/pull/41),
  [`484f623`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/484f623cdf93bb2da063127c77fab33e61405ff0))


## v0.8.8 (2025-04-07)

### Bug Fixes

- **gpkg_logger**: Add proper unload for geopackage tracker in plugin menu
  ([#63](https://github.com/ahmadzfaiz/qgis-track-changes/pull/63),
  [`2cbb791`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/2cbb7911340556b1b687f39eb7f8f0e30ed5c487))

### Chores

- **about**: Create dynamic version text in about page
  ([#63](https://github.com/ahmadzfaiz/qgis-track-changes/pull/63),
  [`62de476`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/62de476e98b5a0110677b02e72f8e975f9348e4c))

- **metadata**: Add proper description
  ([#63](https://github.com/ahmadzfaiz/qgis-track-changes/pull/63),
  [`6649072`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/66490724c08391af00d508551c2988094ec1ffa1))


## v0.8.7 (2025-04-06)

### Bug Fixes

- **release**: Ci/cd fix
  ([`8e2322d`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/8e2322d57a7dc080b26fb569896bf691dfa4a80c))


## v0.8.6 (2025-04-06)

### Bug Fixes

- Ci/cd
  ([`4e1a73b`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/4e1a73bfa1fc7f0c9a56241f8c4fcbe12077b483))


## v0.8.5 (2025-04-06)

### Bug Fixes

- Use correct GitHub Actions bot identity
  ([`44d1fb3`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/44d1fb3d8bf8c2e4fe6366eefdbe83941a8b9af2))


## v0.8.4 (2025-04-06)

### Bug Fixes

- Properly format repository URL in workflow
  ([`7812fda`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/7812fda6fddffac2938be3f6e72a72bf2bc87e81))


## v0.8.3 (2025-04-06)

### Bug Fixes

- Bump patch version for RC cleanup
  ([`a7a27ef`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/a7a27efb2a8a7517a044fa4a1e1dc68813c61d94))


## v0.8.2 (2025-04-06)

### Bug Fixes

- Bump patch version for RC cleanup
  ([`2f00edb`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/2f00edbb0442ae8e1a261b967463f8a34ed2fdcd))


## v0.8.1 (2025-04-06)

### Bug Fixes

- Only run version on main branch
  ([`92949a1`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/92949a179791720b7e3ca8967d93b6e4d90ee7ec))


## v0.8.0 (2025-04-06)

### Bug Fixes

- Bump minor version
  ([`50b617a`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/50b617a6fc5d2bb32e44bab2a08c0007100b8a9d))

### Features

- Bump minor version
  ([`fba638b`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/fba638b95d7dbb8ab8c154e0aedb101f80111fac))


## v0.7.7 (2025-04-06)

### Bug Fixes

- Bump minor version for RC cleanup
  ([`b508e3d`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/b508e3d03b06592343bcf0295767bb3f48ea4c75))


## v0.7.6 (2025-04-06)

### Bug Fixes

- **release**: Remove all RC versioning, keep versioning only on main
  ([`5ef6d4c`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/5ef6d4c97939ed59f1ed4cb8e8f78ec84bc1c882))


## v0.7.5 (2025-04-06)

### Bug Fixes

- **ci**: Improve RC tag handling and fix token usage
  ([`7fa7433`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/7fa7433a0f671f533b1bb7272130877af47dce35))


## v0.7.4 (2025-04-06)

### Bug Fixes

- **ci**: Skip changelog updates on non-main branches
  ([`5e1e587`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/5e1e5877a242394612327f58df63b70f90f16043))

- **ci**: Update GitHub token permissions for releases
  ([`2c52107`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/2c52107b00fdbe70c12fb634a57c42afdf5ce3bf))

- **ci**: Use GITHUB_TOKEN with proper permissions
  ([`1cb8990`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/1cb89902978b280b34ea22c11ff3a2b06920c270))


## v0.7.3 (2025-04-06)

### Bug Fixes

- **release**: Completely revise semantic-release configuration and workflow
  ([`88575e2`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/88575e2a88dbeaaea37a5f5cec69606eff8a7cba))


## v0.7.2 (2025-04-06)

### Bug Fixes

- **changelog**: Use changelog components and filters to exclude RC versions
  ([`e94106f`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/e94106f0168d5df13fc5c1951d7335935c89bec7))


## v0.7.1 (2025-04-06)

### Bug Fixes

- **changelog**: Add explicit regex to exclude RC versions
  ([`d903047`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/d90304718ffba28e676a6c6bf23a46c0863872eb))


## v0.7.0 (2025-04-06)

### Bug Fixes

- **ci**: Update semantic-release commands in GitHub Actions
  ([`59e0cb2`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/59e0cb297c80760cae6ae498c2f0ee275cc59f1e))

### Features

- **changelog**: Add all conventional commit types to changelog sections
  ([`ce6dffb`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/ce6dffb85f1a6d5e9ab823bc8603fae29a3289d0))


## v0.6.0 (2025-04-06)

### Bug Fixes

- **release**: Update branch-specific settings for RC version handling
  ([`fc92d7f`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/fc92d7ffa5ed093122048aa85df1477004b1afc0))


## v0.6.2 (2025-04-06)


## v0.6.1 (2025-04-06)

### Bug Fixes

- **release**: Improve RC version handling in changelog
  ([`2f7bec0`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/2f7bec0341c339293e7c01c6dfe416b51bea2a78))

- **release**: Improve RC version handling in changelog with prerelease tag format
  ([`fb6f686`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/fb6f68652a291e1ee23fc120ba035fdc8d79178a))

### Features

- Add test file for changelog testing
  ([`1c5b8a0`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/1c5b8a0a8c6953c54ae18871cbefb62e1842cc00))

- **release**: Update changelog configuration to handle RC versions
  ([`846c367`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/846c367e2b90209d0bb400dacfe7cc74aacdb654))


## v0.5.1 (2025-04-06)

### Bug Fixes

- **gpkg_logger**: Disable editing when deactivate and reconnect changelog after reactivate
  ([#42](https://github.com/ahmadzfaiz/qgis-track-changes/pull/42),
  [`94de4f8`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/94de4f88385354c87684850700c7ce8e9189a96d))

- **gpkg_logger**: Make deactivate logger will deactivate editing
  ([#42](https://github.com/ahmadzfaiz/qgis-track-changes/pull/42),
  [`c97ba8a`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/c97ba8aa27003cea7c33bac9258f0d9589231625))

- **gpkg_logger**: Optimize gpkg database transaction for logger
  ([#42](https://github.com/ahmadzfaiz/qgis-track-changes/pull/42),
  [`4fbaded`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/4fbadedac05c02fc72c78288be1872aafef6177d))

- **gpkg_logger**: When gpkg file is changed, reset the editing configurations
  ([#42](https://github.com/ahmadzfaiz/qgis-track-changes/pull/42),
  [`ec1eb08`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/ec1eb087b8ab5b6cf698920a0d3ec9c958e86a6d))

### Chores

- **gpkg_logger**: Add logger message
  ([#42](https://github.com/ahmadzfaiz/qgis-track-changes/pull/42),
  [`471471b`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/471471b50153b6c3d62eaf6b964b55c7a23e8cd2))

- **gpkg_logger**: Change list of layers from dot to geometry icon
  ([#42](https://github.com/ahmadzfaiz/qgis-track-changes/pull/42),
  [`6be8edb`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/6be8edb5a7daff9a935709df4a48de31af33e0eb))

- **gpkg_logger**: Selection highlight on active layer
  ([#42](https://github.com/ahmadzfaiz/qgis-track-changes/pull/42),
  [`bf98d4a`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/bf98d4a209faaeb3dfde05491a2d950690a795e8))

- **release**: Fix merge main release changelog
  ([`8d5a221`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/8d5a221219a3a9d8da14009e7ca1f262aaa8e4d0))


## v0.5.0 (2025-04-06)


## v0.4.3 (2025-03-26)

### Bug Fixes

- **version**: Bump a version release to match with current software version
  ([`9b7ca22`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/9b7ca226212b90ab34c83b03cc5b30176a37f4a9))

### Chores

- Update metadata.txt with new version
  ([`d0964af`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/d0964af5225659ea8661923104fe5b62e46e3548))

- **default_logger**: Rename main_dock to default_logger
  ([#32](https://github.com/ahmadzfaiz/qgis-track-changes/pull/32),
  [`6758d8d`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/6758d8d3f1af7e028bd1c44922eb76b5ef85d7dc))

- **metadata**: Bump metadata versioning into __init__.py and metadata.txt
  ([`e889a13`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/e889a135937ff06c452250ac3203be353e6d7f1b))

- **package**: Rename main.py to package.py for better readibility
  ([`8e7b884`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/8e7b884e35f29a2f30f3b7837058018907efac08))

- **version**: Include release candidate on merging into new published version
  ([`a796d28`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/a796d283187a97892d7b3fd23f6f3de9aba31282))

### Continuous Integration

- **release**: Update metadata.txt for commit
  ([`03bc86c`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/03bc86c172fa9cbe47c2006c81828c05a392639e))

### Documentation

- **changelog**: Fix changelog pattern
  ([`3c77f6c`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/3c77f6c20db862a250cd5d5ef9cc022e3e8cc5a7))

### Features

- **gpkg_log**: Add new icon and widget for gpkg logger
  ([#32](https://github.com/ahmadzfaiz/qgis-track-changes/pull/32),
  [`7b9dd20`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/7b9dd206aa06f516622438df3869d746d1c5a06d))

- **gpkg_logger**: Add actions for attribute modifications
  ([#32](https://github.com/ahmadzfaiz/qgis-track-changes/pull/32),
  [`13316ea`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/13316ea8e809d5906b35840e41193821550b67a2))

- **gpkg_logger**: Add feature-related data changes
  ([#32](https://github.com/ahmadzfaiz/qgis-track-changes/pull/32),
  [`0779cb9`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/0779cb967236fe3e51b3236c0af548e4d878c1ec))

- **gpkg_logger**: Add fields per layer logic and log add/remove field
  ([#32](https://github.com/ahmadzfaiz/qgis-track-changes/pull/32),
  [`8fcf6d4`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/8fcf6d4fa051aed5c6484186e510051e3427a629))

- **gpkg_logger**: Add functionality to list gpkg layers
  ([#32](https://github.com/ahmadzfaiz/qgis-track-changes/pull/32),
  [`7308d52`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/7308d52effd873b68e8be0878cd0ec5612eaa646))

- **gpkg_logger**: Add start/stop edit logger in gpkg
  ([#32](https://github.com/ahmadzfaiz/qgis-track-changes/pull/32),
  [`6bd0ded`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/6bd0ded1084a5f15475f0dbb908315e9f7950def))

- **gpkg_logger**: Save a proper start/stop editig log
  ([#32](https://github.com/ahmadzfaiz/qgis-track-changes/pull/32),
  [`b558daa`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/b558daa10ffc251d983d40968a62630e45c27fdb))

- **main_ui**: Create toggle button to trigger dialog for gpkg
  ([#32](https://github.com/ahmadzfaiz/qgis-track-changes/pull/32),
  [`8e0265d`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/8e0265d9daa6ef0b7e0b946930c57412b683ba3f))


## v0.4.2 (2025-03-26)

### Bug Fixes

- Bump to new minor
  ([`3a488f4`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/3a488f4d8fd2a4672f5fe43fc0dedc65a6d935a9))

### Chores

- Remove rc tags
  ([`420f953`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/420f953098eb5d1624e6080a4bb7b3921609962d))

### Continuous Integration

- Fix version
  ([`24ab258`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/24ab2589c87a37ec61115d62a430a51f876b110c))

- **release**: Remove version
  ([`545fd8a`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/545fd8a9d1bb947424fdd68530cd894bb6b5d36b))

- **release**: Remove version
  ([`84cae98`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/84cae980d4a98c4a8d310cf6505e0f578dca9694))


## v0.4.1 (2025-03-26)

### Bug Fixes

- **about**: Remove duplicate sub-menu About on reinstalling
  ([#31](https://github.com/ahmadzfaiz/qgis-track-changes/pull/31),
  [`eafd0c6`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/eafd0c65bf2cc223c633ac16d4bda414e24ea194))

### Build System

- **plugin**: Create build function to ship zipfile into QGIS Plugin Web
  ([`80eedf8`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/80eedf87d1ae1ef7b0c2a8d0f0b4de6652510c06))

### Continuous Integration

- **release**: Change noop with dry-run
  ([`f61a0a0`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/f61a0a00c6b1684c23df9737732bfe1f3827f666))

- **release**: Fix release by merging rc
  ([`bd5c184`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/bd5c184cefe60db3edba8920055e101377d0ce75))

- **release**: Go back to version
  ([`9995694`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/999569468884d48c9361cc2a701d3960b2124d6d))

- **release**: Release version in debug and noop mode
  ([`08d61c0`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/08d61c0311d17ae1224fce67b21cd8e3fce2d422))

- **release**: Remove version and make it more generic
  ([`d155ba1`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/d155ba149d1a81019d02762f69def240ffe20c9d))

### Documentation

- **api**: Add api documentation ([#29](https://github.com/ahmadzfaiz/qgis-track-changes/pull/29),
  [`e9c9e2f`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/e9c9e2f97beff8708430f8d426a5e9b5b8019100))

- **contributing**: Reserve contributing page for future
  ([#29](https://github.com/ahmadzfaiz/qgis-track-changes/pull/29),
  [`d15f80a`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/d15f80a8be92cba99a5f75943af8ed60199d81ad))

- **faq**: Add proper faq about the plugin
  ([#29](https://github.com/ahmadzfaiz/qgis-track-changes/pull/29),
  [`06ddbb2`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/06ddbb2268bc12f0f27cc7a90d00bcaacac58e0a))

- **installation**: Add next step in installation
  ([#29](https://github.com/ahmadzfaiz/qgis-track-changes/pull/29),
  [`72ad69a`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/72ad69a8a52e64c145d48586fc5fbd050fbc50b2))

- **installation**: Add proper installation of the plugin
  ([#29](https://github.com/ahmadzfaiz/qgis-track-changes/pull/29),
  [`2fd9239`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/2fd923963dd62345c415ef1b91f4fe11148538a4))

- **template**: Create template docs
  ([#29](https://github.com/ahmadzfaiz/qgis-track-changes/pull/29),
  [`a1f1e8b`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/a1f1e8b963c28f1c9cd9d429d6ff1cbe0e4902d1))

- **usage**: Add usage instruction ([#29](https://github.com/ahmadzfaiz/qgis-track-changes/pull/29),
  [`1b1199d`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/1b1199d2e4ef8303d2eca1c0e3d0b222c8493c3b))


## v0.4.0 (2025-03-16)

### Continuous Integration

- **release**: Change the removal version into latest one
  ([`fc530c6`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/fc530c6244e3cac8d2c424daedf327033e247a03))

- **release**: Cleaner ci/cd to manage release and changelog
  ([`b48db28`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/b48db28ca49504ce19da1bee25baadb84715afa4))

- **release**: Make publish when merge into main
  ([`ac7aec1`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/ac7aec171afed308d95bc4e92f0c0dd19e3aff58))

- **release**: Properly update rc tags into final release tag
  ([`bfd556c`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/bfd556c80f4a10a266445237583cbd5f9b6e43b9))

### Features

- **about**: Create about dialog
  ([`a010dbe`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/a010dbed64e676af3423fa199d5d23255a8ef811))


## v0.3.2 (2025-03-16)

### Bug Fixes

- **release**: Fix the CI/CD about rc tag version is not changed after release
  ([`0860aa9`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/0860aa942b0dfc88f10a41451b3b1059e42a95d8))

### Continuous Integration

- **release**: Fix release versioning by migrating release candidate tag to release tag
  ([#20](https://github.com/ahmadzfaiz/qgis-track-changes/pull/20),
  [`243f160`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/243f1605f98e80e90b21d29965650075cae49508))


## v0.3.1 (2025-03-16)

### Bug Fixes

- **logger**: Fix mistype message from "added" to "deleted"
  ([#18](https://github.com/ahmadzfaiz/qgis-track-changes/pull/18),
  [`9d3e6e8`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/9d3e6e88bba88b98627bf2297d44317800ae28b9))

### Chores

- Github action bot will revert the changes if it pushes directly to main
  ([`662ab11`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/662ab1154ddb9df81b12312f6f1d2af990c5217b))

- Remove hello.txt
  ([`60b35ff`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/60b35ffc8101d4cd864dc274552ced4fe8be88e4))

- Test push directly to main
  ([`6b421a7`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/6b421a7fe91a361233582450de05b7083fefa113))

- Test upload hello.txt directly to main
  ([`7908e47`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/7908e47d7bac0168e6d536ac418d85f7316a97a2))

- Update permission to write and commit revert
  ([`d7c5ef5`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/d7c5ef59457f225b15b8bd813c289780e7bc09dd))

- **makefile**: Create makefile command to prevent direct push to main
  ([#6](https://github.com/ahmadzfaiz/qgis-track-changes/pull/6),
  [`fb7abf4`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/fb7abf42ee799b477c79235dc60ba8a8c62c3d48))

- **test**: Test upload directly to main
  ([`cb37082`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/cb37082b50bdf70200d19ceafa995cd8684eae72))

### Continuous Integration

- **release**: Fix unclosed ci/cd for release
  ([`5bbcabc`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/5bbcabc044e2d9d43147754dde20375f90a59a28))

- **release**: Revert direct commit to main
  ([`ba59bd0`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/ba59bd0aed795b7fc7ea53006df9128d2088f0ed))

- **release**: Revert the change if push directly to main
  ([`1f0bd31`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/1f0bd3142347309fe78ee1b5bcdbcc47f7c89080))

### Documentation

- **readme**: Add section of tracking changes code and contributor guides
  ([#5](https://github.com/ahmadzfaiz/qgis-track-changes/pull/5),
  [`b9d971d`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/b9d971db879044ed6f169f7ec68c455f8d202876))

- **readthedocs**: Add read the docs configuration
  ([#15](https://github.com/ahmadzfaiz/qgis-track-changes/pull/15),
  [`05e99e3`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/05e99e39f1f159cafb78f3da0b5dd808fa3cdf71))

- **readthedocs**: Define readthedocs configuration
  ([#15](https://github.com/ahmadzfaiz/qgis-track-changes/pull/15),
  [`bfccdaf`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/bfccdaf8700fc7c4f8b67973ec5267d1bdf92d5b))


## v0.3.0 (2025-03-15)

### Bug Fixes

- Direct push is blocked but merge PR is allowed
  ([`a3100f4`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/a3100f47eb528337ddc4271d39cb8098c27982df))

- Only trigger changelog version in working branch
  ([`b1f8310`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/b1f831009d047400a90634a75dc2881c96440fc3))

- Prevent semantic versioning action in main
  ([`8761e3a`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/8761e3aaaad39899486cab26f4f75ee82d24db6d))

- **release**: Fix pyproject.toml to allow stable release in main
  ([`ee941e3`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/ee941e397944f02e433b4d47791d815bc129da61))

- **release**: Only allow Semantic Release Bot to commit
  ([`c685689`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/c6856894ae1de92ddac335d9094f9cc9894efcbb))

### Chores

- Update changelog
  ([`d088eb0`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/d088eb00c5d64443c73ea4455ee75b9b0b7d5ede))

- Update changelog
  ([`371639f`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/371639f3737537708303ae04d2e320c999d86364))

- Update changelog
  ([`7703487`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/7703487ab1514353a9c1bc76234a7efe632f5c8b))

- Update changelog
  ([`5f4eb15`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/5f4eb1546a92584524fe931c92e6d3af58ce24f2))

- Update changelog
  ([`4a6bafb`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/4a6bafbe004bb573c669833489a30c3e0b1fed7d))

### Continuous Integration

- **release**: Add workflow dispatch
  ([`5841b41`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/5841b4115e5a12eab0055a30ad9516284e761c42))

- **release**: Generate changelog on commit
  ([#6](https://github.com/ahmadzfaiz/qgis-track-changes/pull/6),
  [`70357cc`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/70357cc8caecd0b08093a138d30e07b6879a3ccc))

### Features

- Changelogs only written in changelog branch
  ([`83949be`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/83949bee0de49359eb595d8bd4000964f144258a))

- Prevent direct push into main
  ([`468ae2f`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/468ae2f352f4b358e78a71034f10ec022374f4bc))


## v0.2.0 (2025-03-15)

### Features

- Add github permission to push tag and create issue on release version
  ([`50ce45a`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/50ce45a29e44d2121767aba4305015ecab5365c0))


## v0.1.0 (2025-03-15)

### Bug Fixes

- Change the semantic version configuration to python
  ([`14d61fb`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/14d61fb73ebf71f4d77a2a40df97e66dff9c6a3b))

- Fixing semantic version release configuration
  ([`3cde676`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/3cde676b6e8f51831b9d2efb7a25f9bbd1e67743))

- Update GitHub personal access token
  ([`236c5ca`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/236c5cac792777fb66ba5f0614b77a2e8528e211))

### Features

- Add active layer label
  ([`3d2b62f`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/3d2b62fb88d37dbd0fe2a18be591cb09382b04a7))

- Add change logs for adding, deleting and changing attributes
  ([`f42655e`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/f42655efa17f06b964e2e5c16bd3e75c99aa2c44))

- Add functionality to select the layer and activate/deactivate the track changes
  ([`04159ca`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/04159ca5e98f5a515b0266dd61f4a3c84d9a12e7))

- Add log file destination
  ([`d5b9a88`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/d5b9a8843f206333dcb3bb2d3c2d993a22811119))

- Add logger for starting and stopping editing
  ([`f5a67fa`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/f5a67fa48b0929e4e2931be543806bbc9a71ddc8))

- Add refresh layers
  ([`72dd630`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/72dd630616ce2f70ffd8299f50e79a7e79b5426b))

- Add semantic version release
  ([`7e0b154`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/7e0b15467d5f56f843623ff7f495ea8a0645773e))

- Add track change log for adding feature, deleting feature and modify geometry
  ([`9b0943c`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/9b0943c734084b2ed87187a077860978f61cd046))

- Change dialog widget with dock widget
  ([`2d5cd5a`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/2d5cd5a0c23ec73d5a966f66f0449d798c336349))

- Create initial log interactions
  ([`bf2bba6`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/bf2bba656a8ff4b82de24d7c19e239d15afb15d4))

- Create initial project for plugin development
  ([`4cdf1a8`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/4cdf1a82caee325ea11ff07c3e391582207ca276))
