from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from functools import partial
from kivy.uix.label import Label
from kivy.core.window import Window
from ai import process_user_message
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput

class ChatInterface(BoxLayout):
    def __init__(self, **kwargs):
        super(ChatInterface, self).__init__(**kwargs)
        self.orientation = 'vertical'

        self.messages = []
        self.ai_response = "Hello! I am the AI. How can I assist you today?"

        self.chat_label = Label(text="", markup=True)
        self.user_input = TextInput(hint_text='Type your message here...', size_hint_y=None, height=50)
        self.send_button = Button(text='Send', size_hint_y=None, height=50)
        self.send_button.bind(on_press=self.send_user_message)

        self.add_widget(self.chat_label)
        self.add_widget(self.user_input)
        self.add_widget(self.send_button)

    def send_user_message(self, instance):
        user_message = self.user_input.text.strip()
        if user_message:
            # Call the function from the AI file to process the user's message and get AI response
            ai_response = process_user_message(user_message)
            self.messages.append("[color=00FF00]You:[/color] " + user_message)
            self.messages.append(ai_response)
            self.update_chat_label()
            self.user_input.text = ""

    def update_chat_label(self):
        self.chat_label.text = "\n\n".join(self.messages)


class ChatApp(App):
    def build(self):
        return ChatInterface()

if __name__ == '__main__':
    ChatApp().run()


