#!/usr/bin/env python3

import time
from enviroplus import gas
import ST7735
from PIL import Image, ImageDraw, ImageFont

# Initialize the LCD screen
disp = ST7735.ST7735(
    port=0,
    cs=1,
    dc=9,
    backlight=12,
    rotation=270,
    spi_speed_hz=10000000
)

# Initialize the fonts
font = ImageFont.load_default()

# Set up the canvas
image = Image.new("RGB", (disp.width, disp.height), (0, 0, 0))
draw = ImageDraw.Draw(image)

# Set the positions for the text
x_pos = 10
y_pos = 10

# Display the gas readings
try:
    while True:
        # Get the gas readings
        readings = gas.read_all()
        
        # Convert the readings to parts per million
        oxidising = "{:.2f}".format(readings.oxidising / 1000)
        reducing = "{:.2f}".format(readings.reducing / 1000)
        nh3 = "{:.2f}".format(readings.nh3 / 1000)
        
        # Clear the canvas
        draw.rectangle((0, 0, disp.width, disp.height), (0, 0, 0))
        
        # Draw the gas readings on the canvas
        draw.text((x_pos, y_pos), "Oxidizing Gas: {} ppm".format(oxidising), font=font, fill=(255, 255, 255))
        draw.text((x_pos, y_pos+20), "Reducing Gas: {} ppm".format(reducing), font=font, fill=(255, 255, 255))
        draw.text((x_pos, y_pos+40), "Ammonia Gas: {} ppm".format(nh3), font=font, fill=(255, 255, 255))
        
        # Display the canvas on the LCD screen
        disp.display(image)
        
        # Wait for one second before taking the next reading
        time.sleep(1)

# Turn off the backlight and exit the program when Ctrl-C is pressed
except KeyboardInterrupt:
    disp.set_backlight(0)
