# qgis-track-changes
QGIS Plugin to track data changes

## Tracking Changes of Vector Data
Format tracking changes log: <br>
`<asc_time> - <level_name> - <tracking_code> | <messages>`

### Tracking Code
| Code | Explanation | Status |
|----------|----------|----------|
| 00 | activate layer track change | ✅ Live |
| 01 | deactivate layer track change | ✅ Live |
| 10 | start editing | ✅ Live |
| 11 | stop editing | ✅ Live |
| 20 | features selection | ✅ Live |
| 21 | feature add | ✅ Live |
| 22 | feature delete | ✅ Live |
| 23 | feature geometry change | ✅ Live |
| 24 | feature add committed | ✅ Live |
| 25 | feature delete committed | ✅ Live |
| 26 | features geometry change committed | ✅ Live |
| 30 | attribute add | ✅ Live |
| 31 | attribute delete | ✅ Live |
| 32 | attribute value change | ✅ Live |
| 33 | attribute add committed | ✅ Live |
| 34 | attribute delete committed | ✅ Live |
| 35 | attribute values change committed | ✅ Live |
| 50 | version change committed | ✅ Live |

## Code Changelog
- [Detail Change Logs](./CHANGELOG.md)

## Testing
This project uses tests that don't rely on QGIS imports, using mocks to simulate QGIS components. These can be run in any Python environment:

```bash
# Run all default tests
python -m pytest tests/

# Run a specific test file
python -m pytest tests/test_about_widget.py
```

## Contributors guide
### Before you contribute
1. Read this guide carefully if you want to contribute on this plugin.
2. Please create a pull request when change the code.
3. After clone this repository into your local machine, please run `make setup-hooks` to prevent direct push into main branch.

### Commit types for Version Change
We use Semantic Versioning. Semantic Release automatically bumps versions based on commit messages. Here is the rule:
- `fix: something` → Patch release (e.g., 0.3.1 → 0.3.2)
- `feat: something` → Minor release (e.g., 0.3.2 → 0.4.0)
- `BREAKING CHANGE: something` → Major release (e.g., 0.4.0 → 1.0.0)
- `chore:` / `docs:` / `refactor:` → No version change

What is major, minor and patch version?
1. **Major** (<u>X</u>.0.0) <br>
Breaking changes that are not backward-compatible.
2. **Minor** (X.<u>Y</u>.0) <br>
New features that are backward-compatible.
3. **Patch** (X.Y.<u>Z</u>) <br>
Bug fixes that do not introduce new features.

### Commit Message Rules
| Type | When use |
|----------|----------|
| fix  | Fix a bug or issue  |
| feat | Add a new feature  |
| build | Modify build tools, dependencies, or packaging configurations  |
| chore | General maintenance  |
| ci | Modify CI/CD pipelines  |
| docs | Update documentation  |
| refactor | Improve code without changing behavior  |
| style | Formatting, whitespace, linting  |
| test | Add or update tests  |
| perf | Improve performance  |

Use the commit message with this format: <br>
`<type>(<scope>): <short description> (#<issue-number>)`
