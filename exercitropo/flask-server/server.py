from flask import Flask, request, jsonify
from openai import OpenAI
import os
from dotenv import load_dotenv
import json

app = Flask(__name__, static_folder='../client/public', static_url_path='')

load_dotenv()

# Configura OpenAI
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

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

@app.route("/chatbot", methods=['POST'])
def chatbot():
    global count, index
    
    data = request.json
    user_input = data.get('message')
    index = data.get('index', index)

    try:
        index = int(index)
        count += 1
        print (count)
    except ValueError:
        return jsonify({"message": "Invalid index provided."})

    if count == 1:
        return jsonify({"message": 'Ora dimmi in cosa si somigliano. Trova uno o più concetti che li accomunano'})

    if count <= 4:
        primachiavematch = sentence_dict.get("img_" + str(index))
        if not primachiavematch:
            return jsonify({"message": "No data found for the provided index."})

        chiavesomiglianze = primachiavematch.get("somiglianze_" + str(index))
        chiaveallucinazioni = primachiavematch.get("allucinazioni_" + str(index))
        concetto = str(primachiavematch.get("concetto_" + str(index)))

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
            {"role": "user", "content": content_text}
        ]

        response = client.chat.completions.create(
            model="gpt-4",
            messages=chat_prompt,
            max_tokens=100
        )
        response = response.choices[0].message.content.strip()
        response_number = int(response)

        if response_number == 0:
            if count == 2:
                leading = "No, prova ancora, pensa ai dettagli per descrivere le immagini: c'è qualcosa in comune tra i due soggetti che hai scritto o che stai notando adesso?"
                return jsonify({"message": leading})
            if count == 3:
                messaggio = misleading()
                return jsonify({"message": "Non ci siamo ancora. " + messaggio})
            if count == 4:
                summarized_text = summarized()
                return jsonify({"message": summarized_text})

        elif response_number == 1:
            count = 5
            return jsonify({"message": "Ottimo, adesso riassumi tutto con una metafora.."})
    
    if count >= 5:
        metafora_text = metafora(user_input)
        return jsonify({"message": metafora_text})

    return jsonify({"message": "Error processing your request."})

def misleading():
    primachiavematch = sentence_dict.get("img_" + str(index))
    chiavesomiglianze = primachiavematch.get("somiglianze_" + str(index)) if primachiavematch else []
    concetto = str(primachiavematch.get("concetto_" + str(index))) if primachiavematch else ""
    identità_terzolivello = "You are a LLM that speaks Italian. You are able to help to focus on an aspect through a leading question; you are very concise, brief in your answering, and able to scaffold properly without revealing the answer."
    prompt_terzolivello = f"You have these two concepts: {concetto}. Generate an example of a leading question to guide and help a person focus on the right aspects to find the association among those concepts (which is requested by the user in the game). Be very concise and brief in your answer, and scaffold properly without revealing the answer. Pick only one concept among these examples: {', '.join(chiavesomiglianze)}"

    chat_prompt = [
        {"role": "system", "content": identità_terzolivello},
        {"role": "assistant", "content": prompt_terzolivello}
    ]

    response = client.chat.completions.create(
        model="gpt-4",
        messages=chat_prompt,
        max_tokens=100
    )
    misleading_text = response.choices[0].message.content.strip()
    return misleading_text

def summarized():
    primachiavematch = sentence_dict.get("img_" + str(index))
    chiavesomiglianze = primachiavematch.get("somiglianze_" + str(index)) if primachiavematch else []
    identità_quartolivello = "You are a LLM that speaks Italian. You are able to summarize many related sentences in a word or a circumlocution; do not mention the descriptions I give you to answer properly."
    prompt_quartolivello = f"Reply in the form of this example: La risposta che mi hai dato non è pertinente perché non è correlata al concetto che accomuna le immagini. Per esempio, un aspetto di somiglianza è il seguente: ... Consider only one concept, picking it from these descriptions: {', '.join(chiavesomiglianze)}. BUT DO NOT MENTION THE LIST OR DESCRIPTIONS. ANSWER SIMPLY in a syntactically correct and concluded sentence."

    chat_prompt = [
        {"role": "system", "content": identità_quartolivello},
        {"role": "assistant", "content": prompt_quartolivello}
    ]

    response = client.chat.completions.create(
        model="gpt-4",
        messages=chat_prompt,
        max_tokens=100
    )
    concept_text = response.choices[0].message.content.strip()
    return concept_text + " Adesso definisci la metafora finale: ma bada che abbia la forma corretta della metafora, similitudine o analogia. Prendi uno dei due soggetti rappresentati nelle figure e paragonalo, usando il 'come' o senza, all'altro, utilizzando la caratteristica in comune individuata, ad esempio... questa cosa è, è come, si somiglia a quell'altra perché condividono questa caratteristica. Per farlo puoi ispirarti a ciò che ti ho suggerito."

def metafora(user_input):
    primachiavematch = sentence_dict.get("img_" + str(index))
    chiavesomiglianze = primachiavematch.get("somiglianze_" + str(index)) if primachiavematch else []
    chiaveallucinazioni = primachiavematch.get("allucinazioni_" + str(index)) if primachiavematch else []
    metafora12 = str(primachiavematch.get("metafora_" + str(index)))
    content_identity_metafora = "You are a LLM that speaks Italian and calculates conceptual similarities between the actual answer and hypothetical ones, in given lists that exemplify right answers and wrong ones. Only answer 0 for no, 1 for yes, if the user answers as expected AND ARE IN THE FORM OF ANALOGIES, METAPHORS, SIMILES. ONLY answer with number values: 1 for yes or 0 for no. Answer 1 only if the percentage of semantic correlation calculated is high, over 90 percent, and if the user's answer is an explicit metaphor, analogy, or comparison."
    content_text_metafora = f"ONLY answer 0 for no or 1 for yes to these 2 questions: Is this answer '{user_input}' a comparison or a metaphor? And is it related to all these sentences in the list: {', '.join(chiavesomiglianze)}? If not, answer 0. Here are a few EXAMPLES FOR 0: If '{user_input}' is related to {', '.join(chiaveallucinazioni)}, answer 0, NO."

    chat_prompt = [
        {"role": "system", "content": content_identity_metafora},
        {"role": "user", "content": content_text_metafora}
    ]

    response = client.chat.completions.create(
        model="gpt-4",
        messages=chat_prompt,
        max_tokens=100
    )
    risposta = int(response.choices[0].message.content.strip())

    if risposta == 1:
        return 'Ok. Adesso puoi proseguire con il training.'
    else:
        return f"Questa è la risposta: {metafora12}. \nAdesso puoi proseguire con il training."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
