all: compile

.SILENT:
compile:
	python compiler.py scripts/*.bpy
