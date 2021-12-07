To Run Webpage Backend:
    1. pip install -r requirements.txt
    2. Install Data:
        python -m spacy download en_core_web_sm
        python -m nltk.downloader stopwords
        python -m nltk.downloader punkt
        python -m nltk.downloader wordnet
    3. Setup Flask environment:
        Bash:
            export FLASK_ENV=development
            export FLASK_APP=backend.py
        CMD:
            set FLASK_ENV=development
            set FLASK_APP=backend.py
        Powershell:
            $env:FLASK_ENV = "development"
            $env:FLASK_APP = "backend.py"
    4. flask run