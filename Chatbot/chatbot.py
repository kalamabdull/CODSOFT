import re
import datetime

class RuleBasedChatbot:
    def __init__(self):
        # Define rules as a dictionary where keys are regex patterns and values are responses or functions
        self.rules = {
            r'\b(hi|hello|hey|greetings)\b': self.greet,
            r'\bhow are you\b': "I'm just a computer program, but I'm doing well! How are you?",
            r'\b(what is your name|who are you)\b': "I am a simple rule-based chatbot.",
            r'\bwhat time is it\b': self.get_time,
            r'\b(bye|goodbye|exit|quit)\b': "Goodbye! Have a great day!",
            r'\bhelp\b': "I can respond to greetings, tell you my name, and tell you the current time. Try saying 'Hi' or 'What time is it'.",
            r'.*weather.*': "I don't have access to live weather data yet.",
        }
        self.default_response = "I'm sorry, I don't understand that. Could you please rephrase?"

    def greet(self, match):
        return "Hello there! How can I help you today?"

    def get_time(self, match):
        now = datetime.datetime.now()
        return f"The current time is {now.strftime('%H:%M')}."

    def get_response(self, user_input):
        # Normalize the input to lowercase for easier pattern matching
        user_input = user_input.lower().strip()
        
        # Check against all predefined rules
        for pattern, response_action in self.rules.items():
            match = re.search(pattern, user_input)
            if match:
                # If the mapped action is a function, call it
                if callable(response_action):
                    return response_action(match)
                # Otherwise, it's a fixed string response
                else:
                    return response_action
        
        # If no patterns match, return the default response
        return self.default_response

    def chat(self):
        print("Chatbot: Hello! I'm a simple rule-based chatbot. Type 'quit' to exit.")
        while True:
            try:
                user_input = input("You: ")
                if not user_input.strip():
                    continue
                    
                response = self.get_response(user_input)
                print(f"Chatbot: {response}")
                
                # Exit condition
                if re.search(r'\b(bye|goodbye|exit|quit)\b', user_input.lower()):
                    break
            except (KeyboardInterrupt, EOFError):
                print("\nChatbot: Goodbye!")
                break

if __name__ == "__main__":
    bot = RuleBasedChatbot()
    bot.chat()
