from flask import Flask, request, jsonify, send_from_directory
from openai import OpenAI
import os
from dotenv import load_dotenv
import json

app = Flask(__name__, static_folder='client/public', static_url_path='')

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
passwords = [
    "merda",
    "culo",
    "culo123",
    "user_123",
]

index = None  # Initialize the global variable

@app.route('/login', methods=['POST'])
def login():
    global index  # Declare index as a global variable
    data = request.get_json()
    input_string = data.get('inputString')
    input_index = data.get('inputIndex')

    # Check if the index is valid
    try:
        index = int(input_index)
    except ValueError:
        return jsonify({"authenticated": False, "error": "Invalid index, please enter a number"})

    # Check if the password is in the list of passwords
    if input_string in passwords:
        return jsonify({"authenticated": True})
    else:
        return jsonify({"authenticated": False, "error": "Invalid credentials"})

@app.route('/instructions', methods=['GET'])
def instructions():
    return jsonify({
        "title": "Instructions",
        "instructions": "These are the instructions for using the application."
    })




# Ottieni il percorso della directory corrente dello script
base_dir = os.path.dirname(os.path.abspath(__file__))

file_path = os.path.join(base_dir, '..', 'client', 'src', 'pages', 'dizionari.json')

# Normalizza il percorso per gestire correttamente i separatori di directory
file_path = os.path.normpath(file_path)

# Stampa il percorso completo al file JSON per il debug
print("Percorso completo al file JSON: " + file_path)

if not os.path.isfile(file_path):
    print("Il file '" + file_path + "' non è stato trovato.")
    exit(1)

try:
    with open(file_path, encoding='utf-8') as f:
        sentence_dict = json.load(f)
except json.JSONDecodeError as e:
    print("Errore nel decodificare il file JSON: " + str(e))
    exit(1)
except Exception as e:
    print("Errore imprevisto durante la lettura del file JSON: " + str(e))
    exit(1)


@app.route('/chatbot', methods=['POST'])
def chatbot():
    global index
    if index is None:
        return jsonify({"error": "Index not set. Please log in first."})
    
    data = request.get_json()
    user_message = data.get('message').lower()

    # Retrieve the correct data from the JSON based on the current index
    training_key = f"training_{index}"
    training = sentence_dict.get(training_key, {})
    metafora_key = f"metafora_{index}"
    enciclopedia_key = f"enciclopedia_{index}"
    storia_key = f"storia_{index}"
    

    metafora = training.get(metafora_key, [""])[0]
    enciclopedia = training.get(enciclopedia_key, [""])[0]
    storia = training.get(storia_key, [""])[0]
    

    # Identity and prompt setup for OpenAI GPT-4
    # Construct the prompt for OpenAI
    identity = "You are a LLM that speaks Italian and answers with '0' for NO and '1' for YES."
    prompt = f"Questa è la storia {storia}\n"
    prompt += f" Questa la Metafora: {metafora}\n"
    prompt += "Leggi bene la storia. Dopodiché dimmi per la metafora quali sono le proprietà che accomunano entrambi i concetti e li rendono simili.\n"
    prompt += f"Proprietà fornite dall'utente: {user_message}\n"
    prompt += f"Proprietà enciclopediche che rendono simili i concetti della metafora: {', '.join(enciclopedia)}\n"
    prompt += "Rispondi '1' se l'utente ha identificato correttamente le proprietà, altrimenti rispondi '0'."

    # Create the chat prompt for OpenAI
    chat_prompt = [
        {"role": "system", "content": identity},
        {"role": "user", "content": prompt}
    ]
    try:
        # Generate response from OpenAI GPT-4
        response = client.chat.completions.create(
            model="gpt-4",
            messages=chat_prompt,
            max_tokens=100
        )
        response = int(response.choices[0].message.content)
        if response == 1:
            bot_response = "Perfetto. Adesso contestualizza la frase, spiegami il senso di quella metafora nella storia"
            
        else:
            bot_response = "Prova ancora, pensa bene ai dettagli, alle qualità, al significato culturale di qntrambi i concetti della metafora e trova ciò che li accomuna"
            
    except Exception as e:
        # Handle any errors from OpenAI
        print(f"Error generating response from OpenAI: {e}")
        bot_response = "Sorry, I couldn't process that request right now."

    return jsonify({"message": bot_response})



@app.route('/images/<path:filename>', methods=['GET'])
def serve_image(filename):
    print(f"Attempting to serve image: {filename}")
    try:
        return send_from_directory(os.path.join('client', 'public', 'images'), filename)
    except Exception as e:
        print(f"Error serving image: {e}")
        return jsonify({"error": "Image not found"}), 404

@app.route('/task2', methods=['GET'])
def task2():
    global index
    if index is None:
        return jsonify({"error": "Index not set. Please log in first."})

    giusta_image_path = f"/images/{index}/giusta_{index}.png"
    sbagliata_image_path = f"/images/{index}/sbagliata_{index}.png"

    print(f"Image paths: giusta={giusta_image_path}, sbagliata={sbagliata_image_path}")

    return jsonify({
        "giustaImagePath": giusta_image_path,
        "sbagliataImagePath": sbagliata_image_path
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)