.PHONY: setup-hooks

open_qtdesign:
	/Applications/QGIS-LTR.app/Contents/MacOS/bin/designer

create_ui:
	qgis-python -m PyQt5.uic.pyuic -o track_changes/ui/${name}.py track_changes/ui/${name}.ui

setup-hooks:
	@echo "Setting up Git pre-push hook..."
	mkdir -p .git/hooks
	echo '#!/bin/bash\n\nbranch=$$(git rev-parse --abbrev-ref HEAD)\nif [ "$$branch" == "main" ]; then\n    echo "⛔ Direct push to 'main' is not allowed! Use a Pull Request instead."\n    exit 1\nfi' > .git/hooks/pre-push
	chmod +x .git/hooks/pre-push
	@echo "✅ Pre-push hook installed successfully!"
