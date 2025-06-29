# Utilise une image Python légère
FROM python:3.9-slim

# Définit le répertoire de travail
WORKDIR /app

# Copie les fichiers requirements et installe les dépendances
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copie le code source dans /app/src
COPY src/ ./src

# Expose le port Flask
EXPOSE 5000

# Configure le PYTHONPATH pour l'application
ENV PYTHONPATH=/app/src
# Définit le module Flask à lancer
ENV FLASK_APP=interfaces.http.app

# Démarrage de l'application
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]