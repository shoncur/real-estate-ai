from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from ai import process_user_message

class ChatUI(BoxLayout):
    def __init__(self, **kwargs):
        super(ChatUI, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.user_input = TextInput(hint_text='Type your message here...')
        self.submit_button = Button(text='Submit', on_press=self.send_user_message)
        self.ai_response_label = Label(text='', size_hint_y=None, height=50)

        self.add_widget(self.user_input)
        self.add_widget(self.submit_button)
        self.add_widget(self.ai_response_label)

    def send_user_message(self, instance):
        user_message = self.user_input.text.strip()
        if user_message:
            # Call the function from the AI file to process the user's message and get AI response
            ai_response = process_user_message(user_message)
            self.ai_response_label.text = ai_response

if __name__ == '__main__':
    class ChatApp(App):
        def build(self):
            return ChatUI()

    ChatApp().run()
