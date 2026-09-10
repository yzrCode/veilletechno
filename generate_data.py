import feedparser
from datetime import datetime
import json

def extraire_image(article, nom_site):
    """Tente de trouver une image dans l'article, sinon renvoie une image par défaut."""
    # Récupération des balises média via feedparser (flux RSS)
    if 'media_content' in article and len(article.media_content) > 0:
        return article.media_content[0].get('url')
        
    # Fichiers joints (enclosures)
    if 'enclosures' in article and len(article.enclosures) > 0:
        for enc in article.enclosures:
            if enc.get('type', '').startswith('image/'):
                return enc.get('url')
                
    # Images de secours selon la source
    images_secours = {
        "CERT-FR": "https://images.unsplash.com/photo-1563986768609-322da13575f3?w=400", 
        "Sécurité Debian": "https://images.unsplash.com/photo-1629654297299-c8506221ca97?w=400", 
        "IT-Connect": "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=400",
    }
    return images_secours.get(nom_site, "https://images.unsplash.com/photo-1518770660439-4636190af475?w=400")

def generer_json_veille():
    sources_rss = {
        "IT-Connect": "https://www.it-connect.fr/feed/",
        "Journal du Hacker": "https://www.journalduhacker.net/rss",
        "Korben": "https://korben.info/feed/",
        "CERT-FR": "https://www.cert.ssi.gouv.fr/alerte/feed/",
        "ZDNET": "https://www.zdnet.fr/feeds/rss/actualites/",
        "Sécurité Debian": "https://www.debian.org/security/dsa-long.fr.rdf", 
        "Blog Officiel Zabbix": "https://blog.zabbix.com/feed/",
        "CVE Feed": "https://cvefeed.io/rssfeed/severity/high.xml",
        "Bleeping": "https://www.bleepingcomputer.com/feed/",
        "LeMagIT": "https://www.lemagit.fr/rss/ContentSyndication.xml",
        "L'informaticien": "https://www.linformaticien.com/?format=feed&type=rss",
        "ChannelNews": "https://www.channelnews.fr/feed/",
        "next.ink": "https://next.ink/feed/"
    }
    
    donnees_site_web = {}

    for nom_site, url_flux in sources_rss.items():
        try:
            flux = feedparser.parse(url_flux)
            if not flux.entries:
                continue

            donnees_site_web[nom_site] = []
            
            # Récupère les 10 derniers articles et formate la date (JJ/MM/AAAA)
            for article in flux.entries[:10]:
                date_brute = article.get('published_parsed') or article.get('updated_parsed')
                date_pub = datetime(*date_brute[:6]).strftime("%d/%m/%Y") if date_brute else "Date inconnue"
                
                image_url = extraire_image(article, nom_site)
                
                donnees_site_web[nom_site].append({
                    "titre": article.title,
                    "lien": article.link,
                    "date": date_pub,
                    "image": image_url
                })
        except Exception as e:
            print(f"[!] Erreur lors de la récupération de {nom_site}: {e}")

    # Écriture dans le fichier veille.json
    with open("veille.json", "w", encoding="utf-8") as fichier_json:
        json.dump(donnees_site_web, fichier_json, ensure_ascii=False, indent=4)
        
    print("[*] Fichier veille.json généré avec succès !")

if __name__ == "__main__":
    generer_json_veille()
