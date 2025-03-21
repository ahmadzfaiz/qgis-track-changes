# CHANGELOG


## v0.4.0 (2025-03-16)

### Continuous Integration

- **release**: Make publish when merge into main
  ([`ac7aec1`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/ac7aec171afed308d95bc4e92f0c0dd19e3aff58))

### Features

- **about**: Create about dialog
  ([`a010dbe`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/a010dbed64e676af3423fa199d5d23255a8ef811))


## v0.3.2 (2025-03-16)

### Bug Fixes

- **release**: Fix the CI/CD about rc tag version is not changed after release
  ([`0860aa9`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/0860aa942b0dfc88f10a41451b3b1059e42a95d8))

### Continuous Integration

- **release**: Change the removal version into latest one
  ([`fc530c6`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/fc530c6244e3cac8d2c424daedf327033e247a03))

- **release**: Cleaner ci/cd to manage release and changelog
  ([`b48db28`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/b48db28ca49504ce19da1bee25baadb84715afa4))

- **release**: Properly update rc tags into final release tag
  ([`bfd556c`](https://github.com/ahmadzfaiz/qgis-track-changes/commit/bfd556c80f4a10a266445237583cbd5f9b6e43b9))

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
