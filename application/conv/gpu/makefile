TARGET=cufft
TARGET_OS=drawin
NVCC=nvcc -ccbin clang++ -v
CUFLAGS := -m64 -g -G

TARGET_ARCH ?= $(shell uname -m)
LDFLAGS :=
LDFLAGS += -arch $(TARGET_ARCH)

exec=./bin/$(TARGET_ARCH)/$(TARGET_OS)/
include=./include
lib=./lib

CUFILES=$(wildcard ./src/*.cu)
OBJ=$(patsubst %.cu, %.o, $(CUFILES))

LIBS= -L/Developer/NVIDIA/CUDA-8.0/nvvm/lib/ \
      -L/Developer/NVIDIA/CUDA-8.0/nvvm/libdevice \
      -L/Developer/NVIDIA/CUDA-8.0/lib/ \
	  -lcufft

CUFLAGS= -std=c++11 -arch sm_20 \
      -I/Developer/NVIDIA/CUDA-8.0/include \
	  -I/Developer/NVIDIA/CUDA-8.0/samples/common/inc

$(TARGET): $(OBJ)
	$(NVCC) $(CUFLAGS) -I$(include)  $^ $(LIBS) -o $@
	mkdir -p $(exec)
	mv $@ $(exec)/

%.o: %.cu
	$(NVCC) $(CUFLAGS) -I$(include) -o $@ -c $<


COLOR_OFF='\033[0m'
GREEN='\033[0;32m'

all: $(TARGET)
	@echo $(GREEN) [INFO] $(COLOR_OFF) "find sources: " $(CUFILES)
	@echo $(GREEN) [INFO] $(COLOR_OFF) "target has been compiled!"

RM=rm
.PHONY: clean
clean: 
	$(RM) $(OBJ) $(exec)/$(TARGET)
