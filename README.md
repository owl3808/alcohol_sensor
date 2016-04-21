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
![MCP3008 pins](https://raw.githubusercontent.com/owl3808/alcohol_sensor/master/doc/mcp2008_pin.gif)
![Raspberry Pi B+ Pins](https://raw.githubusercontent.com/owl3808/alcohol_sensor/master/doc/rpi_GPIO.png)

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
execute ui.py
<code>$ python ui.py</code>

### Config
to calibration, accurate the result, please edit file MQ3Data.json.
this file is write in JSON formate, include some parameters.
* RsroConcentration_Mapping: a mapping list convert from MQ-3 document figure.
* Ro: resistance when alcohol concentration 0.4 mg/L, currently not confirmed, just a temporaray value.
* Rl: resistance of variable resistor, also currently not confirmed just a temporaray value.


## Calibration
I'm try to figure out a method to calibrate,
with our simple equipment, I have no any ideal for that.
If any ideal, please inform me.

There's what I had try to do.
At first I want to use a 2L plastic bottle with some ethanol in it,
but 0.0057 "mg" is such a slight unit, that we are not able to measure.
