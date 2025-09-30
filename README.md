# csv-crud-fastapi-docker

Questo è il progetto esempio per Social Thingum, utilizzo Anaconda, Docker e PostMan 

CURL PER POST:
C:\Users\PC\OneDrive\Documenti\GitHub\csv-crud-fastapi-docker>curl -X POST "http://localhost:8000/items/" -H "Content-Type: application/json" -d "{\"ID\":98, \"Nome\": \"Mario\", \"Cognome\": \"Rossi\", \"Codice_Fiscale\": \"RSSMRA01A01H501A\"}"

uvicorn main:app --reload   

pip install --no-cache-dir -r requirements.txt

docker load -i csv-crud-api-finalespero.tar
docker run -it --rm -p 8000:8000 csv-crud-api-finalespero
