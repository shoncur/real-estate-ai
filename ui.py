from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from functools import partial
from kivy.uix.label import Label
from kivy.core.window import Window
from ai import process_user_message

class ChatInterface(BoxLayout):
    def __init__(self, **kwargs):
        super(ChatInterface, self).__init__(**kwargs)
        self.orientation = 'vertical'

        self.messages = []
        self.ai_response = "Hello Dave... I am HAL. How can I assist you today?"

        self.chat_layout = BoxLayout(orientation='vertical', size_hint_y=None)

        self.user_input = TextInput(hint_text='Type your message here...', size_hint_y=None, height=50)
        self.send_button = Button(text='Send', size_hint_y=None, height=60)
        self.send_button.bind(on_press=self.send_user_message)

        self.add_widget(self.chat_layout)
        self.add_widget(self.user_input)
        self.add_widget(self.send_button)

    def send_user_message(self, instance):
        user_message = self.user_input.text.strip()
        if user_message:
            # Call the function from the AI file to process the user's message and get AI response
            ai_response = process_user_message(user_message)
            if (len(ai_response) > 30):
                textArray = ai_response.split(" ")
                counter = 0
                message = ""
                for i in textArray:
                    if counter == 0:
                        message = "[color=FF0000]HAL:[/color] " + i + " "
                    if counter > 1 and counter > 15:
                        message += i + "\n"
                        counter = 1
                    if counter > 1:
                        message += i + " "
                    counter += 1
                self.add_message("[color=00FF00]You:[/color] " + user_message + "\n")
                self.add_message(message + "\n")
            else:
                self.add_message("[color=00FF00]You:[/color] " + user_message)
                self.add_message("[color=FF0000]HAL:[/color] " + ai_response)
            self.user_input.text = ""

    def add_message(self, message):
        message_label = Label(text=message, markup=True, size_hint_y=None, halign='center')
        message_label.bind(texture_size=message_label.setter('size'))
        self.chat_layout.add_widget(message_label)

class ChatApp(App):
    def build(self):
        return ChatInterface()

if __name__ == '__main__':
    ChatApp().run()

