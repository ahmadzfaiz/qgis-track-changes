open_qtdesign:
	/Applications/QGIS-LTR.app/Contents/MacOS/bin/designer

create_ui:
	qgis-python -m PyQt5.uic.pyuic -o track_changes/ui/${name}.py track_changes/ui/${name}.ui