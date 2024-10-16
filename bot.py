# libraries
import random
import numpy as np
import pickle
import json
from flask import Flask, render_template, request
from flask_ngrok import run_with_ngrok
import nltk
from keras.models import load_model
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()


# chat initialization
model = load_model("my_model.keras")
# intents = json.loads(open("intents.json").read())
data_file = open(r"intents.json").read()
words = pickle.load(open("words.pkl", "rb"))
classes = pickle.load(open("classes.pkl", "rb"))


# chat functionalities
def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words


# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence
def bow(sentence, words, show_details=True):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words - matrix of N words, vocabulary matrix
    bag = [0] * len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print("found in bag: %s" % w)
    return np.array(bag)


def predict_class(sentence, model):
    # filter out predictions below a threshold
    p = bow(sentence, words, show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

import re
def extract_numbers(input_string):
    numbers = re.findall(r'\d+', input_string)
    return [int(num) for num in numbers]
def check_for_dollar(input_string):
    return "$" in input_string
def replace_dollar_one(input_string,amount):
    return input_string.replace("$1", str(amount))
def getResponse(ints, intents_json,amount):
    tag = ints[0]["intent"]
    list_of_intents = intents_json["intents"]
    for i in list_of_intents:
        if i["tag"] == tag:
            result = random.choice(i["responses"])
            if check_for_dollar(result):
                result =replace_dollar_one(result,amount)
            break
    return result

from googletrans import Translator

def translate_word(word, target_language='en'):
    translator = Translator()
    translation = translator.translate(word, dest=target_language)
    return translation.text

# word_to_translate = "Hello"
# target_language = "ta"  # Change this to the language code you want, e.g., 'es' for Spanish
#
# translated_word = translate_word(word_to_translate, target_language)
# print(f"{word_to_translate} in {target_language} is: {translated_word}")


from gtts import gTTS
import os


def text_to_audio(text, lang='en'):
    tts = gTTS(text=text, lang=lang, slow=False)
    try:
        os.remove("output.mp3")
    except:
        pass
    tts.save("output.mp3")
    # os.system("mpg321 output.mp3")  # For Linux
    # os.system("start output.mp3")  # For Windows

    return True

import pygame
import pygame

def play_audio(audio_file):
    pygame.init()
    pygame.mixer.init()
    try:
        pygame.mixer.music.load(audio_file)
        print("Playing audio...")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    except Exception as e:
        print("Error playing audio:", e)
    finally:
        pygame.mixer.music.stop()
        pygame.quit()

# if __name__ == "__main__":
#     # audio_file = "path_to_your_audio_file.mp3"  # Replace with the path to your audio file
#     # play_audio(audio_file)
#
