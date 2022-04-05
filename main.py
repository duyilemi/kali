import nltk
from neuralintents import GenericAssistant
import speech_recognition
import pyttsx3 as tts
import sys

nltk.download('omw-1.4')

# init recognizer
recognizer = speech_recognition.Recognizer()

# init text tospeech
speaker = tts.init()
speaker.setProperty('rate', 150)

todo_list = ['Go Shopping','Play Football', 'Record Video']

def create_note():
    global recognizer

    speaker.say('What do you want to write on your note?')
    speaker.runAndWait()

    done = False

    while not done:
        try:
            with speech_recognition.Microphone as mic:
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)

                note = recognizer.recognize_google(audio)
                note = note.lower()

                speaker.say('Choose a filename')
                speaker.runAndWait()

                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)

                filename = recognizer.recognize_google(audio)
                filename = filename.lower()
            with open(filename, "w") as f:
                f.write(note)

                done = True
                speaker.say(f'I successfully created the note {filename}')
                speaker.runAndWait()

        except speech_recognition.UnknownValueError:
            recognizer = speech_recognition.Recognizer()
            speaker.say("I did not understand you! Please try again !")
            speaker.runAndWait()


def add_todo():
    global recognizer

    speaker.say('What to do do you want to add?')
    speaker.runAndWait()

    done = False

    while not done:
        try:
            with speech_recognition.Microphone as mic:
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)

                item = recognizer.recognize_google(audio)
                item = item.lower()

                

                todo_list.append(item)
                done = True

                
                speaker.say(f'I added {item} to the to do list')
                speaker.runAndWait()

        except speech_recognition.UnknownValueError:
            recognizer = speech_recognition.Recognizer()
            speaker.say("I did not understand you! Please try again !")
            speaker.runAndWait()

def show_todos():
    speaker.say("The item on your to do list are the following")

    for item in todo_list:
        speaker.say(item)
        speaker.runAndWait()

def hello():
    speaker.say("Hello, what can i do for you")
    speaker.runAndWait()

def quit():
    speaker.say("Bye")
    speaker.runAndWait()
    sys.exit()

mappings = {
    "greetings":hello,
    "create_note": create_note,
    "add_todo": add_todo,
    "show_todos":show_todos,
    "exit": quit
}
#  train a model that recognize the intent and map them to a function
assistant = GenericAssistant('intents.json',intent_methods=mappings)
assistant.train_model()

while True:
    try:
        with speech_recognition.Microphone() as mic:

            recognizer.adjust_for_ambient_noise(mic, duration=0.2)
            audio = recognizer.listen(mic)

            message = recognizer.recognize_google(audio)
            mssage = message.lower()

        assistant.request(message)
    except speech_recognition.UnknownValueError:
        recognizer = speech_recognition.Recognizer()