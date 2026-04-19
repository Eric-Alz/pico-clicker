import time
import machine

import screen
import battery
import button

# Charging, don't do anything, comment this out when coding in Thonny
#vbus = machine.Pin(24, machine.Pin.IN)
#if vbus():
#    while True:
#        pass

POLLING_RATE = 100 # Per second
MAX_TIME_DISPLAYED = 599 # In seconds
ONE_SECOND_IN_TICKS = 1_000_000
THREE_SECONDS_IN_TICKS = 3_000_000
TEN_SECONDS_IN_TICKS = 10_000_000

# SETUP SCREEN
i2c = machine.SoftI2C(scl=machine.Pin(20), sda=machine.Pin(19))
pin = machine.Pin(16, machine.Pin.OUT)
pin.value(0)
pin.value(1)
oled_width = 64
oled_height = 32
oled = screen.SSD1306_I2C(oled_width, oled_height, i2c)
oled.fill(0)


# SETUP BATTERY
ina219 = battery.INA219(addr=0x43)
stored_battery_percentage = ina219.calculate_battery_percent()
current_battery_percentage = stored_battery_percentage
battery_changing_time = 0

# Update offset of displayed text to compensate for number of characters
battery_display_offset = oled.calculate_battery_display_offset(stored_battery_percentage)


# SETUP BUTTON
button_handler = button.ButtonHandler()
button_input = machine.Pin(11, machine.Pin.IN, machine.Pin.PULL_UP)
is_pressed = button_handler.is_button_pressed(button_input)

# Reset count dialog appears after holding button for 3 seconds, once dialog appears, hold for a another 3 seconds to
# confirm reset
is_pressed_time = 0

# Whether reset click count dialog is open
resetting_click_count = False 

# When the button is held down to enter a new state, we dont want the release of the button to count as a click. Ignore
# "click" action while waiting for release
waiting_for_release = False


# SETUP TIME TRACKING
current_frame_tick = time.ticks_us()
ticks = 0
time_seconds = 0


while True:
    # KEEP TIME
    previous_frame_tick = current_frame_tick
    current_frame_tick = time.ticks_us()
    delta = time.ticks_diff(current_frame_tick, previous_frame_tick)
    ticks += delta
    time_seconds += delta / ONE_SECOND_IN_TICKS

    # Keep track of one second at a time
    if ticks >= ONE_SECOND_IN_TICKS:
        ticks -= ONE_SECOND_IN_TICKS

    if time_seconds > MAX_TIME_DISPLAYED:
        time_seconds = MAX_TIME_DISPLAYED


    # CHECK BATTERY
    old_battery_percentage = current_battery_percentage
    current_battery_percentage = ina219.calculate_battery_percent()
    if (current_battery_percentage < 0):
        current_battery_percentage = 0
    elif (current_battery_percentage > 100):
        current_battery_percentage = 100

    # Don't want the battery percentage flickering on screen between two different values
    if old_battery_percentage == current_battery_percentage and current_battery_percentage != stored_battery_percentage:
        battery_changing_time += ticks
    else:
        battery_changing_time = 0

    if battery_changing_time >= TEN_SECONDS_IN_TICKS:
        stored_battery_percentage = current_battery_percentage
        battery_display_offset = oled.calculate_battery_display_offset(stored_battery_percentage)


    # CHECK BUTTON
    was_pressed = is_pressed
    is_pressed = button_handler.is_button_pressed(button_input)

    if waiting_for_release:
        if not is_pressed:
            waiting_for_release = False
    else:
        if is_pressed:
            is_pressed_time += delta
        else:
            is_pressed_time = 0
            if was_pressed:
                # If button was pressed down and released (clicked)
                if resetting_click_count:
                    # If on reset click count menu, cancel operation
                    resetting_click_count = False
                else:
                    # Otherwise, execute standard click operation and increment counter
                    button_handler.click()
                    time_seconds = 0
        if is_pressed_time >= THREE_SECONDS_IN_TICKS:
            # Watching for button hold of 3 seconds to signify reset operation from user
            if resetting_click_count:
                # If already in reset dialog, reset count
                button_handler.reset_click_count()
                resetting_click_count = False
                time_seconds = 0
            else:
                # Otherwise, go to reset dialog
                resetting_click_count = True
            waiting_for_release = True
            is_pressed_time = 0

    # UPDATE SCREEN
    oled.fill(0)
    if resetting_click_count:
        oled.text('Reset?', 0, 0)
        oled.text('Hold...', 0, 10)
    else:
        minutes, seconds = divmod(time_seconds, 60)
        oled.text(str(button_handler.click_count), 0, 0)
        oled.text('{}:{:02d}'.format(int(minutes), int(seconds)), 0, 10)
        oled.text('{:6.0f}%'.format(stored_battery_percentage), battery_display_offset, 20)
    oled.show()

    # Polling rate
    time.sleep(1 / POLLING_RATE)