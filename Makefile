configure:
	cmake -S . -B build

build: configure
	cmake --build build

test: build
	cmake --build build --target test

docs: build
	cmake --build build --target docs

run: build
	./build/apps/app_main

.PHONY: format
format:
	find . -name "*.hpp" -o -name "*.cpp" -not -path "./build/*" | xargs clang-format -i

.PHONY: clean
clean:
	rm -rf ./build/
