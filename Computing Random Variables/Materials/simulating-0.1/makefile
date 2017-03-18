PWD=.
project_name=simulating_rv
TARGET=$(project_name)

exclude_dirs= include bin lib
CC=clang++
RM=rm -rf

exec=./bin
include=./include
lib=./lib

LIBS=-lm -I/usr/local/include/ \
	 -I/usr/local/Cellar/boost157/1.57.0/include/ \
	 -L/usr/local/lib \
	 -lglog
CPPFLAGS= -g -Wall -Wno-unused -Wno-write-strings

SRCS=$(wildcard *.cpp) \
     $(wildcard $(SRCS_DIR)/*.cpp)
SRCS_DIR=./src
# OBJ=$(SRCS: .cpp=.o)
OBJ=$(patsubst %.cpp, %.o, $(SRCS))
HEADERS=$(wildcard *.h) \
		$(wildcard *.hpp)

# LINK WITH link flags
$(TARGET): $(OBJ)
	$(CC) $(CPPFLAGS) -I$(include) $(LIBS) -stdlib=libc++ -o $@ $^
	mv $@ $(exec)/

# COMPILE with compile flags
%.o : %.cpp
	$(CC) -std=c++11 -stdlib=libc++ -I$(include) $(LIBS) -c $< -o $@

.PHONY: clean
clean:
	$(RM) $(OBJ) $(exec)/$(TARGET)

all: $(TARGET)
	@echo $(GREEN) [INFO] $(COLOR_OFF) "find sources: " $(SRCS)
	@echo $(GREEN) [INFO] $(COLOR_OFF) "target has been complied!"

run: $(TARGET)
	$(exec)/$(TARGET)

COLOR_OFF='\033[0m'
GREEN='\033[0;32m'
init:
		@ echo $(GREEN) [INFO] $(COLOR_OFF) "headers are : " "$(HEADERS)"
		@ echo $(GREEN) [INFO] $(COLOR_OFF) "srcs are" : "$(SRCS)"
		@[ -d include ] || (mkdir include && -mv "$(HEADERS)" --target-directory=include/)
		@[ -d bin ] || mkdir bin
		@[ -d lib ] || mkdir lib
		@[ -d src ] || (mkdir src && -mv "$(SRCS)" --target-directory=src/)
