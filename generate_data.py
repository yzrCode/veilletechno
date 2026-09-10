import feedparser
import json
from datetime import datetime
import time

# Liste des flux RSS (Sites IT + liens RSS-Bridge pour réseaux sociaux)
SOURCES = [
    {"nom": "Le Monde Informatique", "url": "https://www.lemondeinformatique.fr/flux-rss/thematique/toutes-les-actualites/rss.xml"},
    {"nom": "ZDNet France", "url": "https://www.zdnet.fr/feeds/rss/actualites/"},
    {"nom": "Les Numériques - Informatique", "url": "https://www.lesnumeriques.com/informatique/rss.xml"},
    {"nom": "Developpez.com", "url": "https://www.developpez.com/index/rss"}
]

def recuperer_articles():
    articles = []
    
    for source in SOURCES:
        try:
            print(f"Récupération : {source['nom']}...")
            flux = feedparser.parse(source['url'])
            
            for item in flux.entries[:10]:  # Top 10 des derniers articles par source
                date_struct = item.get('published_parsed') or item.get('updated_parsed')
                if date_struct:
                    timestamp = time.mktime(date_struct)
                    date_affichee = time.strftime('%d/%m/%Y à %H:%M', date_struct)
                else:
                    timestamp = time.time()
                    date_affichee = "Date inconnue"

                articles.append({
                    "titre": item.title,
                    "lien": item.link,
                    "source": source['nom'],
                    "date": date_affichee,
                    "timestamp": timestamp
                })
        except Exception as e:
            print(f"Erreur pour {source['nom']}: {e}")

    # Tri chronologique inverse (du plus récent au plus ancien)
    articles.sort(key=lambda x: x['timestamp'], reverse=True)

    donnees = {
        "derniere_mise_a_jour": datetime.now().strftime('%d/%m/%Y à %H:%M'),
        "nb_articles": len(articles),
        "articles": articles
    }

    # Sauvegarde au format JSON
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(donnees, f, ensure_ascii=False, indent=4)
        
    print(f"✅ data.json généré avec {len(articles)} articles.")

if __name__ == "__main__":
    recuperer_articles()