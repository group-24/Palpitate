# Paths
OPENCV_PATH=../opencv-compiled/build
FACETRACKER_PATH=../Facetracker

# Programs
cpp=
CXX=g++

# Flags
ARCH_FLAGS=
CFLAGS=-Wextra -Wall -pedantic-errors $(ARCH_FLAGS) -O3 -Wno-long-long
LDFLAGS=$(ARCH_FLAGS)
DEFINES=
# INCLUDES=-I$(OPENCV_PATH)/include -Iinclude/
INCLUDES=-I$(FACETRACKER_PATH)/include -Iinclude/
# LIBRARIES=-L$(OPENCV_PATH)/lib -lopencv_core -lopencv_highgui -lopencv_imgproc -lopencv_objdetect
LIBRARIES=-L$(FACETRACKER_PATH)/src/lib -lopencv_core -lopencv_highgui -lopencv_imgproc -lopencv_objdetect

# Files which require compiling
SOURCE_FILES=\
	# src/main.cpp

# Source files which contain a int main(..) function
SOURCE_FILES_WITH_MAIN=src/exe/main.cpp

# End Configuration
SOURCE_OBJECTS=$(patsubst %.cpp,%.o,$(SOURCE_FILES))

ALL_OBJECTS=\
	$(SOURCE_OBJECTS) \
	$(patsubst %.cpp,%.o,$(SOURCE_FILES_WITH_MAIN))

DEPENDENCY_FILES=\
	$(patsubst %.o,%.d,$(ALL_OBJECTS))

all: bin/video-analyser

%.o: %.cpp Makefile
	@# Make dependecy file
	$(CXX) -MM -MT $@ -MF $(patsubst %.cpp,%.d,$<) $(CFLAGS) $(DEFINES) $(INCLUDES) $<
	@# Compile
	$(CXX) $(CFLAGS) $(DEFINES) -c -o $@ $< $(INCLUDES)

-include $(DEPENDENCY_FILES)

bin/video-analyser: $(ALL_OBJECTS)
	$(CXX) $(LDFLAGS)  -o $@ $(ALL_OBJECTS) $(LIBRARIES)

.PHONY: clean
clean:
	@echo "Cleaning"
	@for pattern in '*~' '*.o' '*.d' ; do \
		find . -name "$$pattern" | xargs rm ; \
	done
