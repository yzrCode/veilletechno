import json
from datetime import datetime
import feedparser


def extraire_image(article, nom_site):
    """Tente de trouver une image dans l'article, sinon renvoie une image par défaut."""
    if 'media_content' in article and len(article.media_content) > 0:
        return article.media_content[0].get('url')

    if 'enclosures' in article and len(article.enclosures) > 0:
        for enc in article.enclosures:
            if enc.get('type', '').startswith('image/'):
                return enc.get('url')

    images_secours = {
        'CERT-FR': (
            'https://images.unsplash.com/photo-1614064641938-3bbee52942c7?w=500'
        ),
        'CVE Feed': (
            'https://images.unsplash.com/photo-1550751827-4bd374c3f58b?w=500'
        ),
        'Bleeping': (
            'https://images.unsplash.com/photo-1563986768609-322da13575f3?w=500'
        ),
        'Sécurité Debian': (
            'https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=500'
        ),
        'IT-Connect': (
            'https://images.unsplash.com/photo-1544197150-b99a580bb7a8?w=500'
        ),
        'Blog Officiel Zabbix': (
            'https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=500'
        ),
        'LeMagIT': (
            'https://images.unsplash.com/photo-1518770660439-4636190af475?w=500'
        ),
        'Journal du Hacker': (
            'https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=500'
        ),
        'Korben': (
            'https://images.unsplash.com/photo-1526379095098-d400fd0bf935?w=500'
        ),
        'ZDNET': (
            'https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=500'
        ),
        "L'informaticien": (
            'https://images.unsplash.com/photo-1498050108023-c5249f4df085?w=500'
        ),
        'ChannelNews': (
            'https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=500'
        ),
        'next.ink': (
            'https://images.unsplash.com/photo-1504384308090-c894fdcc538d?w=500'
        ),
    }

    return images_secours.get(
        nom_site,
        'https://images.unsplash.com/photo-1518770660439-4636190af475?w=500',
    )


def generer_json_veille():
    sources_rss = {
        'IT-Connect': 'https://www.it-connect.fr/feed/',
        'Journal du Hacker': 'https://www.journalduhacker.net/rss',
        'Korben': 'https://korben.info/feed/',
        'CERT-FR': 'https://www.cert.ssi.gouv.fr/alerte/feed/',
        'ZDNET': 'https://www.zdnet.fr/feeds/rss/actualites/',
        'Sécurité Debian': (
            'https://www.debian.org/security/dsa-long.fr.rdf'
        ),
        'Blog Officiel Zabbix': 'https://blog.zabbix.com/feed/',
        'CVE Feed': 'https://cvefeed.io/rssfeed/severity/high.xml',
        'Bleeping': 'https://www.bleepingcomputer.com/feed/',
        'LeMagIT': (
            'https://www.lemagit.fr/rss/ContentSyndication.xml'
        ),
        "L'informaticien": (
            'https://www.linformaticien.com/?format=feed&type=rss'
        ),
        'ChannelNews': 'https://www.channelnews.fr/feed/',
        'next.ink': 'https://next.ink/feed/',
    }

    donnees_site_web = {}

    for nom_site, url_flux in sources_rss.items():
        try:
            flux = feedparser.parse(url_flux)
            if not flux.entries:
                continue

            donnees_site_web[nom_site] = []

            for article in flux.entries[:10]:
                date_brute = article.get('published_parsed') or article.get(
                    'updated_parsed'
                )
                date_pub = (
                    datetime(*date_brute[:6]).strftime('%d/%m/%Y')
                    if date_brute
                    else 'Date inconnue'
                )

                image_url = extraire_image(article, nom_site)

                donnees_site_web[nom_site].append({
                    'titre': article.title,
                    'lien': article.link,
                    'date': date_pub,
                    'image': image_url,
                })
        except Exception as e:
            print(f'[!] Erreur lors de la récupération de {nom_site}: {e}')

    with open('data.json', 'w', encoding='utf-8') as fichier_json:
        json.dump(donnees_site_web, fichier_json, ensure_ascii=False, indent=4)

    print('[*] Fichier data.json généré avec succès !')


if __name__ == '__main__':
    generer_json_veille()
