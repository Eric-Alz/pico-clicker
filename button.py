class ButtonHandler:
    def __init__(self):
        with open('click_count.txt', 'r') as file:
            click_count = int(file.read().strip())
            self.click_count = click_count

    # Increments click count
    def click(self):
        with open('click_count.txt', 'w') as file:
            self.click_count += 1
            file.write(str(self.click_count))

    # Resets click count
    def reset_click_count(self):
        with open('click_count.txt', 'w') as file:
            self.click_count = 0
            file.write(str(self.click_count))

    # Determines whether button is pressed from pin input
    @staticmethod
    def is_button_pressed(button_input):
        v = button_input.value()
        if v == 0:
            return True
        else:
            return False