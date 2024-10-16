import os

from flask import Flask, render_template, request, redirect, url_for
import json
app = Flask(__name__)
from bot import  *

# Default language
default_language = "English"


@app.route('/')
def index():
    return render_template('index.html', selected_language=default_language)


@app.route('/set_language', methods=['POST'])
def set_language():
    global default_language
    selected_language = request.form['language']
    default_language = selected_language
    return redirect(url_for('greeting', language=selected_language))

@app.route('/bot/<language>')
def greeting(language):
    return render_template('bot.html', selected_language=language)

@app.route("/get", methods=["POST"])
def chatbot_response():
    msg = request.form["msg"]

    # Load and process the intents JSON file
    data_file = open(r"intents.json").read()
    intents = json.loads(data_file)

    # Rest of your existing code
    if msg.startswith('my name is'):
        name = msg[11:]
        ints = predict_class(msg, model)
        res1 = getResponse(ints, intents,None)
        res = res1.replace("{n}", name)
    elif msg.startswith('hi my name is'):
        name = msg[14:]
        ints = predict_class(msg, model)
        res1 = getResponse(ints, intents,None)
        res = res1.replace("{n}", name)
    else:
        ints = predict_class(msg, model)
        amount = extract_numbers(msg)
        if amount:
            res = getResponse(ints, intents,amount[0])
        else:
            res = getResponse(ints, intents, None)
        # word_to_translate = "Hello"
        # target_language = "English"
        audio_file = 'output.mp3'
        if default_language == "English":
            text_to_audio(res, lang='en')
            if text_to_audio(res, lang='en'):
                if os.path.exists(audio_file):
                    play_audio(audio_file)
                    os.remove(audio_file)
                else:
                    print("Error: Audio file not found.")
            return res
        elif default_language == "Hindi":
            target_language = 'hi'
            translated_word = translate_word(res, target_language)
            text_to_audio(translated_word, lang='hi')  # 'hindi'
            # Check if the file exists
            if text_to_audio(translated_word, lang='hi'):
                if os.path.exists(audio_file):
                    play_audio(audio_file)
                    os.remove(audio_file)
                else:
                    print("Error: Audio file not found.")

            print(f"{res} in {target_language} is: {translated_word}")
            return translated_word
        elif default_language == "Tamil":
            target_language = 'ta'
            translated_word = translate_word(res, target_language)
            # text_to_audio(translated_word, lang='ta')
            # text_to_audio(translated_word, lang='hi')  # 'hindi'
            # Check if the file exists
            if text_to_audio(translated_word, lang='hi'):
                if os.path.exists(audio_file):
                    play_audio(audio_file)
                    os.remove(audio_file)
                else:
                    print("Error: Audio file not found.")
            print(f"{res} in {target_language} is: {translated_word}")
            return translated_word


    # return res

if __name__ == '__main__':
    app.run(debug=True,port=7854,use_reloader = True)
