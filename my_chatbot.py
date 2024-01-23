# importing the required modules
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer

# creating a chatbot
myBot = ChatBot(
    name='Sakura',
    read_only=True,
    logic_adapters=[
        'chatterbot.logic.MathematicalEvaluation',
        'chatterbot.logic.BestMatch'
    ]
)

# training the chatbot
small_convo = [
    'Hi there!',
    'Hi',
    'How do you do?',
    'How are you?',
    'I\'m cool.',
    'Always cool.',
    'I\'m Okay',
    'Glad to hear that.',
    'I\'m fine',
    'I feel awesome',
    'Excellent, glad to hear that.',
    'Not so good',
    'Sorry to hear that.',
    'What\'s your name?',
    ' I\'m Sakura. Ask me a math question, please.'
]

math_convo_1 = [
    'Pythagorean theorem',
    'a squared plus b squared equals c squared.'
]

math_convo_2 = [
    'Law of Cosines',
    'c**2 = a**2 + b**2 - 2*a*b*cos(gamma)'
]

# using the ListTrainer class
list_trainee = ListTrainer(myBot)
for i in (small_convo, math_convo_1, math_convo_2):
    list_trainee.train(i)

# using the ChatterBotCorpusTrainer class
corpus_trainee = ChatterBotCorpusTrainer(myBot)
corpus_trainee.train('chatterbot.corpus.english')
