**Parts list**
Pico:         https://www.waveshare.com/raspberry-pi-pico-2.htm
Power Supply: https://www.waveshare.com/pico-ups-b.htm
Display:      https://www.waveshare.com/0.49inch-oled-module.htm
Button/Input: https://www.amazon.com/dp/B0FKB78HLX?ref=ppx_yo2ov_dt_b_fed_asin_title&th=1

**Other necessary tools**
 - Soldering iron
 - Solder
 - Flux (if not included in solder)
 - Jumper wire
 - Dupont wire (with female connectors)
 - Wire stripper
 - Micro USB cable with data capabilities (for connecting Pico to pc)
 - Thonny software (for connecting, setting up, and coding Pico)
 - Brass or regular sponge (for cleaning the soldering iron tip, somewhat optional)
 - Fan (for ventilation, optional)

**Setup Guide**
Part 1 - Hardware
This was my first hardware project. Please take my instructions with caution.
The first step is soldering the pico board to the UPS module. You want to solder all the necessary pins for the UPS to work, as well as all the pins for the other peripherals. I put the Pico board onto the female connectors
and used stripped jumper wire as the header pins. I soldered pins 3, 8, 9, 10, 13, 15, 18, 23, 25, 26, 28, 33, 36, 38, 39, 40. Follow soldering guides online; there are a ton of them. The joints do not need to be pretty,
just make sure solder fills the hole that the pin sits in, does not bridge with other pins, surrounds the pin itself, and that there is enough pin above the solder for a female connector to attach to (~1/2 inch). Also,
cut and strip two dupont wires with female connectors and solder them directly to the pins on the button.
Once the soldering is done, you can connect the lithium battery that comes with the UPS module to the UPS board and slide it into place between the Pico board and UPS board.
Attach the female connectors of the button to pins 16 and 18. Order does not matter.
Attach the female connectors of the screen as such:
 - Black wire (GND) to pin 23
 - Green wire (SDA) to pin 25
 - Yellow wire (SCL) to pin 26
 - Red wire (VCC) to pin 36
Note: Certain pins on Raspberry Pis can be shared and connected to different components, for example, the 3v3 and ground pins. In this setup, both the screen and the UPS will make use of the 3v3 pin (pin 36).
This should be all you need for the hardware side. It's probably wise to set this all up on a breadboard first and test it to make sure everything works before committing to soldering.

Part 2 - Firmware/Software
This guide is very helpful for initial setup, getting Thonny and Pico configured: https://www.youtube.com/watch?v=_ouzuI_ZPLs
The one piece of that tutorial that didn't quite work for me was the updating the firmware portion. I had to manually download the micropython firmware from here: https://micropython.org/download/RPI_PICO2/ and drag that
into the Pico in the file explorer. Once you do that, the pico should disappear from the file explorer, and then you should be able to connect and interact with it in Thonny.
After that setup, add the code in this repo to the Pico, and everything should work.

Part 3 - Casing
TODO
