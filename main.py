from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup

class NumberConverterApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical', spacing=10)

        self.label = Label(text="Choose the input format:\n1. Decimal\n2. Hexadecimal\n3. Octal\n4. Binary")
        self.layout.add_widget(self.label)

        self.text_input = TextInput()
        self.layout.add_widget(self.text_input)

        self.convert_button = Button(text="Convert", on_press=self.show_conversion_popup)
        self.layout.add_widget(self.convert_button)

        self.result_label = Label(text="")
        self.layout.add_widget(self.result_label)

        return self.layout

    def show_conversion_popup(self, instance):
        try:
            choice = int(self.text_input.text)
        except ValueError:
            self.result_label.text = "Invalid choice. Please choose a valid option."
            return

        if choice < 1 or choice > 4:
            self.result_label.text = "Invalid choice. Please choose a valid option."
            return

        popup_layout = self.create_conversion_popup_layout(choice)
        self.popup = Popup(content=popup_layout, title=f"Enter {self.get_format_label(choice)}")
        self.popup.open()

    def create_conversion_popup_layout(self, choice):
        popup_layout = BoxLayout(orientation='vertical', spacing=10)

        popup_label = Label(text=f"Enter the {self.get_format_label(choice)} number:")
        popup_input = TextInput()
        popup_layout.add_widget(popup_label)
        popup_layout.add_widget(popup_input)

        popup_button = Button(text="Submit", on_press=lambda x: self.display_conversion_result(popup_input.text, choice))
        popup_layout.add_widget(popup_button)

        popup_dismiss_button = Button(text="Dismiss", on_release=self.dismiss_conversion_popup)
        popup_layout.add_widget(popup_dismiss_button)

        return popup_layout

    def display_conversion_result(self, input_text, choice):
        try:
            number_input = self.process_conversion_input(input_text, choice)
        except ValueError:
            self.result_label.text = "Invalid input. Please enter a valid number."
            return

        self.result_label.text = self.format_conversion_result(choice, number_input)
        self.dismiss_conversion_popup()

    def process_conversion_input(self, input_text, choice):
        if choice == 2:
            # Hexadecimal input
            return int(input_text, 16)
        elif choice == 4:
            # Binary input
            return int(input_text, 2)
        else:
            # Decimal or Octal input
            return int(input_text)

    def format_conversion_result(self, choice, number_input):
        formats = {
            1: {"label": "Decimal", "format": "{:d}", "base": 10},
            2: {"label": "Hexadecimal", "format": "{:X}", "base": 16},
            3: {"label": "Octal", "format": "{:o}", "base": 8},
            4: {"label": "Binary", "format": "{:b}", "base": 2}
        }

        results = []

        for i in range(1, 4 + 1):
            if i != choice:
                try:
                    result = formats[i]['format'].format(number_input)
                    if isinstance(number_input, float):
                        result = f"{formats[i]['label']}: {float(result)}"
                    else:
                        result = f"{formats[i]['label']}: {result}"
                except (ValueError, TypeError):
                    result = f"{formats[i]['label']}: Invalid input for this format"

                results.append(result)

        return "Result:\n" + "\n".join(results)

    def dismiss_conversion_popup(self, instance=None):
        self.popup.dismiss()

    def get_format_label(self, choice):
        formats = {
            1: "Decimal",
            2: "Hexadecimal",
            3: "Octal",
            4: "Binary"
        }
        return formats[choice]

if __name__ == '__main__':
    NumberConverterApp().run()