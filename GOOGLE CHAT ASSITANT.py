#ACTUAL CODEEEEEEEE FOORRRRRR CHAT ASSSITANT
import textwrap
from gtts import gTTS
import google.generativeai as genai
from IPython.display import display, Markdown, Audio
from google.colab import userdata

genai.configure(api_key=userdata.get('GOOGLE_API_KEY'))
model = genai.GenerativeModel('gemini-pro')

def to_markdown(text):
    text = text.replace('•', '  *')
    return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

def ask_question(name):
    ques = f"Hey {name}, what do you want? "
    return input(ques)

def classify_questions(ques):
    go_ahead_with_web_search = False
    device_lst = ['alarm', 'reminder', 'message', 'call']
    personal_lst = ['who are you?', 'who created you']

    device = any(i in ques for i in device_lst)
    personal_question = any(i in ques.lower() for i in personal_lst)

    if device:
        print("This question is related to Device things, which doesn't support our Google Assistant.")
    elif personal_question:
        print("Hey, I am a personal assistant created by your names.")
    else:
        go_ahead_with_web_search = True

    return go_ahead_with_web_search

def ask_gemini(ques):
    modified_prompt = f"Hey, give me an answer to this question: {ques}, in a maximum of 40 words."
    response = model.generate_content(modified_prompt)
    return response.text

def speak(answer):
    tts = gTTS(answer)
    tts.save('audio.mp3')
    display(Audio('audio.mp3', autoplay=True))

have_any_other_ques = 'y'
name = ''

while have_any_other_ques.lower() == 'y':
    if name == '':
        name = input("Hey, what is your name? - ")
    q = ask_question(name)
    go_ahead = classify_questions(q)
    answer = ''

    if go_ahead:
        answer = ask_gemini(q)
        print(answer)
        speak(answer)

    have_any_other_ques = input("Do you have any other questions? (y/n) ")

print("Goodbye!")
