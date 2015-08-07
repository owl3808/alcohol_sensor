# alcohol_sensor
This is a alcohol_sensor implementation for NCKU TCM drunk-driving research.

## Hardware
this implementation include few hardware stuff.
* Raspberry pi B+ (Rpi)
* MCP3008 chip for ADC
* FC-22 MQ3 alcohol sensor

### Hardware setup
* FC-22 analog-pin ---> MCP3008 CH0
* MCP3008 CLK ---> Rpi SPI_CLK
* MCP3008 D-out ---> Rpi SPI_MISO
* MCP3008 D-in ---> Rpi SPI_MOSI
* MCP3008 CS/SHDN ---> SPI_CE0_N

## Software
### Pre-work
**Enable SPI Model**  
edit file: /etc/modprobe.d/raspi-blacklist.conf
```
#blacklist spi-bcm2708
```

### run Test
This module follow Test-driven development(TDD) to ensure reliability.
To run the test, please unmark unittest.main() and mark usage_example() in alcohol_sensor.py
```
unittest.main()
#usage_example()
```

### Execute
run alcohol_sensor.py

### Config
to adjust accuracy, please edit file MQ3Data.json.
this file is write in JSON formate, include some parameters.
* RsroConcentration_Mapping: a mapping list convert from MQ-3 document figure.
* Ro: resistance when alcohol concentration 0.4 mg/L, currently not confirmed, just a temporaray value.
* Rl: resistance of variable resistor, also currently not confirmed just a temporaray value.
