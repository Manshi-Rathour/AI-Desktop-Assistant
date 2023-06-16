import speech_recognition as sr
import os
import win32com.client
import webbrowser
import openai
from config import apikey
import datetime


chatStr = ""
def chat(text):
    global chatStr
    print(chatStr)
    openai.api_key = apikey
    chatStr += f"Manshi: {text}\n Jarvis: "

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=chatStr,
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    # todo: wrap this inside of a try catch block
    say(response["choices"][0]["text"])
    chatStr += f"{response['choices'][0]['text']}\n"
    return response["choices"][0]["text"]



def ai(prompt):
    openai.api_key = apikey
    text_ = f"OpenAI response for Prompt: {prompt} \n **************************\n\n"


    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    # todo: wrap this inside of a try catch block
    print(response["choices"][0]["text"])
    text_ += response["choices"][0]["text"]
    if not os.path.exists("Openai"):
        os.mkdir("Openai")

    with open(f"Openai/{''.join(prompt.split('intelligence')[1:]).strip()}.txt", "w") as f:
        f.write(text_)







speaker = win32com.client.Dispatch("SAPI.SpVoice")
def say(text):
    # os.system(f"say{text}")
    speaker.Speak(text)
# say("Hello I am Jarvis AI")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 0.8
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except Exception as e:
            return "Some Error Occurred. Sorry from Jarvis."
say("Jarvis AI")
while True:
    print("Listening...")
    text = takeCommand()

    # todo: Opening Sites
    sites = [["youtube", "https://www.youtube.com"],["google", "https://www.google.com"],
             ["linkedin", "https://www.linkedin.com/feed/"],["github", "https://github.com/Manshi-Rathour"]]
    for site in sites:
        if f"Open {site[0]}".lower() in text.lower():
            say(f"Opening {site[0]} Ma'am")
            webbrowser.open(site[1])


    # todo: Opening Files and Folders
    folders = [["user", "C:Users\mansh"],["movies", "D:"], ["downloads", "C:Users\mansh\Downloads"],
               ["e", "E:"]]
    for folder in folders:
        if f"open {folder[0]}".lower() in text.lower():
            say(f"Opening {folder[0]} Ma'am")
            os.startfile(folder[1])


    # todo: Date & Time
    if "the time" in text:
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        say(f"Ma'am the time is {strTime}")


    # todo: using openai
    elif "Using artificial intelligence".lower() in text.lower():
        ai(prompt=text)


    elif "Jarvis Quit".lower() in text.lower():
        exit()

    elif "reset chat".lower() in text.lower():
        chatStr = ""

    else:
        print("Chatting...")
        chat(text)
