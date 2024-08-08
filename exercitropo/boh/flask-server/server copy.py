'''prompt migliorato sulla base  delle mie conoscenze linguistiche, tiè'''

from flask import Flask, request, jsonify
from openai import OpenAI
import os
from dotenv import load_dotenv
import json
import logging

app = Flask(__name__, static_folder='../client/public', static_url_path='')

load_dotenv()

# Configura OpenAI
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Percorso al file dizionari.json
dizionari_path = os.getenv('DIZIONARI_PATH', 'dizionari.json')

if not os.path.isfile(dizionari_path):
    raise FileNotFoundError(f"Il file '{dizionari_path}' non è stato trovato.")

try:
    with open(dizionari_path, encoding='utf-8') as f:
        sentence_dict = json.load(f)
except json.JSONDecodeError as e:
    raise RuntimeError(f"Errore nel decodificare il file JSON: {e}")
except Exception as e:
    raise RuntimeError(f"Errore imprevisto durante la lettura del file JSON: {e}")

# Percorso per le immagini
images_directory = os.getenv('IMAGES_DIRECTORY', 'client/src/images')

# Variabili globali
index = 0
count = 0

# Configura il logging
logging.basicConfig(level=logging.DEBUG)

# Endpoint di login (se necessario)
@app.route('/login', methods=['POST'])
def login():
    global index, count
    data = request.get_json()
    input_string = data.get('inputString', '').strip()
    input_index = data.get('inputIndex', '').strip()

    try:
        index = int(input_index)
        count = 0
    except ValueError:
        return jsonify({"authenticated": False, "error": "Invalid index, please enter a number"})

    # Verifica la password (esempio, personalizzabile)
    passwords = ["merda", "culo", "culo123", "user_123"]
    if input_string in passwords:
        return jsonify({"authenticated": True})
    else:
        return jsonify({"authenticated": False, "error": "Invalid credentials"})

# Endpoint delle istruzioni
@app.route('/instructions', methods=['GET'])
def instructions():
    return jsonify({
        "title": "Instructions",
        "instructions": "These are the instructions for using the application."
    })


@app.route("/set_image", methods=['GET'])
def set_image():
    global index, count
    try:
        index = int(request.args.get("msg"))
        count = 0  # Reset count when setting a new image
        update_globals()
        logging.debug(f"Image set to {index}, count reset to {count}")
        return jsonify({"message": "Image set", "index": index})
    except ValueError:
        return jsonify({"message": "Invalid index."})

@app.route("/set_again_image", methods=['GET'])
def set_again_image():
    global index, count
    try:
        index = int(request.args.get("msg"))
        count = 0  # Reset count when setting the image again
        update_globals()
        logging.debug(f"Image reset to {index}, count reset to {count}")
        return jsonify({"message": "Image set again", "index": index})
    except ValueError:
        return jsonify({"message": "Invalid index."})

# Funzione di aggiornamento delle variabili globali
def update_globals():
    global primachiavematch, chiavesomiglianze, chiaveallucinazioni, concetto
    primachiavematch = sentence_dict.get("img_" + str(index))
    chiavesomiglianze = primachiavematch.get("somiglianze_" + str(index)) if primachiavematch else []
    chiaveallucinazioni = primachiavematch.get("allucinazioni_" + str(index)) if primachiavematch else []
    concetto = str(primachiavematch.get("concetto_" + str(index))) if primachiavematch else ""

    logging.debug(f"Primachiavematch: {primachiavematch}")
    logging.debug(f"Chiavesomiglianze: {chiavesomiglianze}")
    logging.debug(f"Chiaveallucinazioni: {chiaveallucinazioni}")
    logging.debug(f"Concetto: {concetto}")

@app.route("/chatbot", methods=['POST'])
def chatbot():
    global count, index
    
    data = request.json
    user_input = data.get('message')
    index = data.get('index', index)

    try:
        index = int(index)
        count += 1
    except ValueError:
        return jsonify({"message": "Invalid index provided."})

    logging.debug(f"Index: {index}, Count: {count}")

    if count == 1:
        return jsonify({"message": 'Ora dimmi in cosa si somigliano. Trova uno o più concetti che li accomunano'})

    if count <= 4:
        primachiavematch = sentence_dict.get("img_" + str(index))
        if not primachiavematch:
            return jsonify({"message": "No data found for the provided index."})

        chiavesomiglianze = primachiavematch.get("somiglianze_" + str(index))
        chiaveallucinazioni = primachiavematch.get("allucinazioni_" + str(index))
        concetto = str(primachiavematch.get("concetto_" + str(index)))

        logging.debug(f"Chiave Somiglianze: {chiavesomiglianze}")
        logging.debug(f"Chiave Allucinazioni: {chiaveallucinazioni}")
        logging.debug(f"Concetto: {concetto}")

        content_identity = (
            f"You are a language model that speaks Italian and helps users train with metaphorical comprehension. "
            f"The user is asked to find meaningful concepts or properties that associate these subjects: {concetto}. "
            "I provide you with some examples of correct answers in a given list. "
            "I also give you another list with incorrect answers. "
            "Your task is to determine if the user's answer matches any correct answers or incorrect answers. "
            "Respond only with 0 for no and 1 for yes, and answer 1 only if the percentage of semantic correlation is over 90 percent with the list of correct answers."
        )

        content_text = (
            "TASK: Determine if the user's answer matches any correct answers or incorrect answers. "
            "Respond only with 0 for no and 1 for yes, and answer 1 only if the percentage of semantic correlation is over 90 percent with the list of correct answers I provide you and among the concepts through which the metaphor is built. "
            f"OUTPUT: You must evaluate the user answer '{user_input}'. Return 0 if the user responded incorrectly, or doesn't know the answer; answer 1 if they respond correctly in identifying the correct characteristics to explain the metaphor in the training. "
            f"CONTEXT: This metaphorical training is a test where the user is asked which properties are common to the concepts '{concetto}' used to construct the metaphor. "
            f"Examples of correct answers: {', '.join(chiavesomiglianze)}. "
            f"Examples of incorrect answers: {', '.join(chiaveallucinazioni)}. "
            "LONG-TERM EFFECT: Through this test, the user must learn to find the characteristics to understand the metaphor without interpreting it literally or responding off-topic."
        )



        chat_prompt = [
            {"role": "system", "content": content_identity},
        ] + [{"role": "user", "content": content_text }] 

        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

        response = client.chat.completions.create(
            model="gpt-4",
            messages=chat_prompt,
            max_tokens=100,  
        )
        response = (response.choices[0].message.content)
        response_number = int(response)

        

        if response_number == 0:
            if count == 2:
                return jsonify({"message": "NO, prova ancora, pensa ai dettagli che hai enumerato all'inizio descrivendo le immagini: c'è qualcosa in comune tra i due soggetti?"})
            if count == 3:
                return jsonify({"message": "Non ci siamo ancora... osserva bene l'immagine a destra e a sinistra. Cosa ti suscita? C'è qualcosa che si può dire a riguardo del concetto?"})
            if count == 4:
                return jsonify({"message": "Per esempio.... "})

        elif response_number == 1:
            return jsonify({"message": "Ottimo, adesso riassumi tutto con una metafora.."})

    

    return jsonify({"message": "Error processing your request."})







if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
