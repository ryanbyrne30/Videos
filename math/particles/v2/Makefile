CC = g++
CFLAGS = -g -Wall 
TARGET = sim

all: $(TARGET)

$(TARGET): $(TARGET).cpp
	$(CC) $(CFLAGS) -o $(TARGET) $(TARGET).cpp `libpng-config --ldflags`

clean:
	$(RM) $(TARGET)