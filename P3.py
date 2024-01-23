from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

chatbot = ChatBot('MyChatBot')
bot_trainer = ChatterBotCorpusTrainer(chatbot)
bot_trainer.train("chatterbot.corpus.english")

response = chatbot.get_response("Hello, how are you?")
print(response)

print("enter 'quit' to stop")
while True:
    user_input = input("You: ")
    if user_input == 'quit':
        break
    print("Bot:", chatbot.get_response(user_input))