# Requires bison 3.7
#
CC = g++ -g
LIBS = -ly -ll
LEX = flex
GRAM = /usr/local/opt/bison/bin/bison

SOURCEDIR = src
BUILDDIR = build
EXECUTABLE = main

all: clean makedir $(BUILDDIR)/$(EXECUTABLE)

makedir:
	@mkdir -p $(BUILDDIR)

clean:
	rm -rf $(BUILDDIR)

$(BUILDDIR)/parser.cpp: $(SOURCEDIR)/parser.y
	@mkdir -p $(BUILDDIR)
	$(GRAM) -d -o $@ $^

$(BUILDDIR)/lexer.cpp: $(SOURCEDIR)/lexer.l $(BUILDDIR)/parser.hpp
	@mkdir -p $(BUILDDIR)
	$(LEX) -o $@ $^

$(BUILDDIR)/main.cpp: $(SOURCEDIR)/main.cpp
	@mkdir -p $(BUILDDIR)
	cp $^ $@

$(BUILDDIR)/ast.cpp: $(SOURCEDIR)/ast.cpp
	@mkdir -p $(BUILDDIR)
	cp $^ $@
	cp $(subst .cpp,.hpp,$^) $(subst .cpp,.hpp,$@)

$(BUILDDIR)/$(EXECUTABLE): $(BUILDDIR)/parser.cpp $(BUILDDIR)/main.cpp $(BUILDDIR)/lexer.cpp $(BUILDDIR)/ast.cpp
	$(CC) $(LIBS) -o $@ $^

.PHONY: run
run: clean $(BUILDDIR)/$(EXECUTABLE)
	$(BUILDDIR)/$(EXECUTABLE) test.sql

.PHONY: format
format:
	find . -name "*.hpp" -o -name "*.cpp" -not -path "./build/*" | xargs clang-format -i
