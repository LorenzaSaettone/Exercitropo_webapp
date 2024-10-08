# Exercitropo_webapp


## Descrizione

ExerciTropo è un'applicazione web per training metaforico che combina un'interfaccia utente React con un backend Flask. L'applicazione serve come strumento di training per la comprensione metaforica attraverso un gioco interattivo che utilizza immagini e domande. Il training è un training validato. Lorenza Saettone l'ha automatizzato e ha particolareggiato le metafore coinvolte nel test.
L'utente interagisce con un bot che fornisce istruzioni e feedback basati su input dell'utente e immagini.

## Struttura del Progetto

- `flask-server/` - Contiene il backend in Flask.
- `client/` - Contiene il frontend in React.

## Installazione

### Backend (Flask)

1. **Clona il repository:**

   ```bash
   git clone https://github.com/tuo_username/tuo_repository.git
   cd tuo_repository
   ```

2. **Naviga nella cartella del server Flask:**

   ```bash
   cd flask-server
   ```

3. **Crea e attiva un ambiente virtuale:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # Su Windows usa `venv\Scripts\activate`
   ```

4. **Installa le dipendenze:**

   ```bash
   pip install -r requirements.txt
   ```

5. **Configura le variabili d'ambiente:**

   Crea un file `.env` nella cartella `flask-server` e aggiungi le seguenti variabili:

   ```env
   OPENAI_API_KEY=la_tua_chiave_api_openai
   DIZIONARI_PATH=dizionari.json
   IMAGES_DIRECTORY=client/src/images
   ```

6. **Avvia il server Flask:**

   ```bash
   python server.py
   ```

   Il server sarà accessibile su `http://localhost:5000`.

### Frontend (React)

1. **Naviga nella cartella del client React:**

   ```bash
   cd client
   ```

2. **Installa le dipendenze:**

   ```bash
   npm install
   ```

3. **Avvia il server di sviluppo:**

   ```bash
   npm start
   ```

   L'app sarà accessibile su `http://localhost:3000`.

## Uso

- **Interfaccia Utente:** L'utente può navigare tra le pagine, visualizzare immagini e interagire con il bot per ricevere feedback e istruzioni.
- **Bot:** Fornisce risposte e guida basata su input dell'utente e immagini selezionate.

## Contributi

Se desideri contribuire a questo progetto, segui questi passaggi:

1. **Forka il repository**
2. **Crea un branch per la tua feature:**

   ```bash
   git checkout -b nome-feature
   ```

3. **Fai le tue modifiche e commit:**

   ```bash
   git commit -am 'Aggiungi una nuova feature'
   ```

4. **Pusha il tuo branch:**

   ```bash
   git push origin nome-feature
   ```

5. **Crea una pull request**

## Licenza

Distribuito sotto la Licenza MIT. Vedi `LICENSE` per maggiori dettagli.

## Contatti

Per ulteriori informazioni o domande, contatta [Lorenza Saettone] a [lorenzasaettone@gmail.com].
```

### Note:
1. **Sostituisci** i segnaposto come `tuo_username`, `tuo_repository`, `la_tua_chiave_api_openai`, `tuo_nome`, e `tuo_email` con le informazioni specifiche del tuo progetto e del tuo contatto.
2. **Salva** il file con il nome `README.md` nella root del tuo progetto.

Questo file `README.md` fornisce una panoramica completa su come installare e usare il tuo progetto, ed è utile sia per te che per altri sviluppatori che potrebbero voler contribuire o utilizzare il tuo progetto.