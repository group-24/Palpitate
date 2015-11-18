# Paths
OPENCV_PATH=include/opencv2

# Programs
CC=
CXX=g++

# Flags
ARCH_FLAGS=
CFLAGS=-Wc++11-extensions -Wextra -Wall -pedantic-errors $(ARCH_FLAGS) -O3 -Wno-long-long -Wnested-anon-types  -Wgnu-anonymous-struct
LDFLAGS=$(ARCH_FLAGS)
DEFINES=
INCLUDES=-I$(OPENCV_PATH)/include -Iinclude/
LIBRARIES=-L$(OPENCV_PATH)/lib -lopencv_core -lopencv_highgui -lopencv_imgproc -lopencv_objdetect

# Files which require compiling
SOURCE_FILES=

# Source files which contain a int main(..) function
SOURCE_FILES_WITH_MAIN=Chehra/Chehra_Main.cpp

# End Configuration
SOURCE_OBJECTS=$(patsubst %.cpp,%.o,$(SOURCE_FILES))

ALL_OBJECTS=\
	$(SOURCE_OBJECTS) \
	$(patsubst %.cpp,%.o,$(SOURCE_FILES_WITH_MAIN))

DEPENDENCY_FILES=\
	$(patsubst %.o,%.d,$(ALL_OBJECTS))

all: bin/chehra

%.o: %.cpp Makefile
	@# Make dependecy file
	$(CXX) -MM -MT $@ -MF $(patsubst %.cpp,%.d,$<) $(CFLAGS) $(DEFINES) $(INCLUDES) $<
	@# Compile
	$(CXX) $(CFLAGS) $(DEFINES) -c -o $@ $< $(INCLUDES)

-include $(DEPENDENCY_FILES)

bin/chehra: $(ALL_OBJECTS)
	$(CXX) $(LDFLAGS)  -o $@ $(ALL_OBJECTS) $(LIBRARIES)

.PHONY: clean
clean:
	@echo "Cleaning"
	@for pattern in '*~' '*.o' '*.d' ; do \
		find . -name "$$pattern" | xargs rm ; \
	done
