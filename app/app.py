from flask import Flask, request, render_template, jsonify
import requests 
#from .config import Config

app = Flask(__name__, template_folder='templates')
#app.config.from_object(Config)

@app.route("/")
def index(personne):
    return "écrire /retrieve_wikidata/(id)"

@app.route("/retrieve_wikidata/<id>")
def retrieve_wikidata(id):
    url = 'https://www.wikidata.org/w/api.php'
    
    # Paramètres de la requête
    params = {
        'action': 'wbgetentities',
        'ids': id,
        'format': 'json'
    }

    try: 
        # Effectuer la requête à l'API Wikidata
        response = requests.get(url, params=params)

        http_status = response.status_code
        content_type = response.headers.get("Content-Type", "unknown")
    
        data = response.json()  # Décoder la réponse JSON
        # Vérifier si les données sont présentes
        if 'entities' in data and id in data['entities']:
            entity_data = data['entities'][id]
            return render_template('wikidata.html', 
                                   status_code = http_status,
                                   content_type = content_type,
                                   entity_data = entity_data,
                                   id = id,
                                    error_message = None, )
            
        else:
            entity_data = None
            error_message = f"Aucune donnée trouvée pour l'identifiant {id}"
            return render_template('wikidata.html', 
                                   error_message = error_message,
                                    status_code = http_status,
                                   content_type = content_type,
                                   entity_data = entity_data,
                                   id = id, )
        
        
    
    except requests.RequestException as e:
        # Gestion des erreurs de connexion
        return render_template(
            "wikidata.html",
            status_code=None,
            content_type=None,
            entity_data=None,
            error_message=f"Erreur lors de la requête : {str(e)}"
        )

if __name__ == "__main__":
    app.run(debug=app.config["DEBUG"])

