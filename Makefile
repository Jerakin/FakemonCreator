clean:
	rm -rf *.egg-info
	rm -rf dist

build:
	pyinstaller "FakemonCreator.spec"

run:
	./dist/Fakemon\ Creator

setup:
	pip install -r requirements.txt

.PHONY: clean build run setup

