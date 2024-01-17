import re
from collections import defaultdict
import markdown

# Expressions régulières pour identifier les adresses IP et les noms de domaine
IP_pattern = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
domain_pattern = re.compile(r'[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}')

# Initialisation des compteurs et des dictionnaires pour garder une trace des IPs et des domaines
compteur_ssh, compteur_icmp, compteur_http, compteur_https, compteur_domaine = 0, 0, 0, 0, 0
compteur_flags_connexion, compteur_flags_SynAcK, compteur_flags_deco, compteur_flags_push, compteur_flags_nokonnexion = 0, 0, 0, 0, 0
ip_counts = defaultdict(int)
domain_counts = defaultdict(int)
activity_ip_counts = defaultdict(lambda: defaultdict(int))
activity_domain_counts = defaultdict(lambda: defaultdict(int))

# Analyse du fichier
with open("DumpFile.txt", "r") as f:
    for line in f:
        ips = IP_pattern.findall(line)
        domains = domain_pattern.findall(line)

        for ip in ips:
            ip_counts[ip] += 1  # Compter toutes les occurrences d'IP

        for domain in domains:
            domain_counts[domain] += 1  # Compter toutes les occurrences de domaines

        if 'http' in line:
            compteur_http += 1
            for ip in ips: activity_ip_counts['http'][ip] += 1

        if 'https' in line:
            compteur_https += 1
            for ip in ips: activity_ip_counts['https'][ip] += 1

        if '.domain' in line:
            compteur_domaine += 1
            for ip in ips: activity_ip_counts['domain'][ip] += 1
            for domain in domains: activity_domain_counts['domain'][domain] += 1

        if 'ssh' in line:
            compteur_ssh += 1
            for ip in ips: activity_ip_counts['ssh'][ip] += 1

        if 'ICMP' in line:
            compteur_icmp += 1
            for ip in ips: activity_ip_counts['icmp'][ip] += 1

        # Ajoutez des conditions similaires pour d'autres protocoles si nécessaire

        if 'Flags [S]' in line:
            compteur_flags_connexion += 1
            for ip in ips: activity_ip_counts['flags_connexion'][ip] += 1

        if 'Flags [S.]' in line:
            compteur_flags_SynAcK += 1
            for ip in ips: activity_ip_counts['flags_SynAcK'][ip] += 1

        if 'Flags [F.]' in line:
            compteur_flags_deco += 1
            for ip in ips: activity_ip_counts['flags_deco'][ip] += 1

        if 'Flags [P.]' in line:
            compteur_flags_push += 1
            for ip in ips: activity_ip_counts['flags_push'][ip] += 1

        if 'Flags [.]' in line:
            compteur_flags_nokonnexion += 1
            for ip in ips: activity_ip_counts['flags_nokonnexion'][ip] += 1

        compteur_http_final = compteur_http - compteur_https

# Seuils pour définir ce qui est considéré comme une activité suspecte
SEUIL_SSH = 100
SEUIL_ICMP = 50
SEUIL_NO_CONNEXION = 1000
SEUIL_HTTP = 100
SEUIL_HTTPS = 100
SEUIL_PUSH = 100
SEUIL_DOMAINE = 100

# Détecter les activités suspectes et les adresses IP associées
activites_suspectes = []

if compteur_ssh > SEUIL_SSH:
    activites_suspectes.append("Trafic SSH élevé: {} connexions".format(compteur_ssh))
    for ip, count in activity_ip_counts['ssh'].items():
        if count > 10:
            activites_suspectes.append("    IP suspecte (SSH): {} - {} requêtes".format(ip, count))

if compteur_icmp > SEUIL_ICMP:
    activites_suspectes.append("\nTrafic ICMP élevé: {} requêtes".format(compteur_icmp))
    for ip, count in activity_ip_counts['icmp'].items():
        if count > 10:
            activites_suspectes.append("    IP suspecte (ICMP): {} - {} requêtes".format(ip, count))

if compteur_flags_nokonnexion > SEUIL_NO_CONNEXION:
    activites_suspectes.append("\nTrafic avec Flags No Connexion élevé: {} requêtes".format(compteur_flags_nokonnexion))
    for ip, count in activity_ip_counts['flags_nokonnexion'].items():
        if count > 20:
            activites_suspectes.append("    IP suspecte (No Connexion): {} - {} requêtes".format(ip, count))

if compteur_http_final > SEUIL_HTTP:
    activites_suspectes.append("\nTrafic HTTP élevé (hors HTTPS): {} requêtes".format(compteur_http_final))
    for ip, count in activity_ip_counts['http'].items():
        if count > 20:
            activites_suspectes.append("    IP suspecte (HTTP): {} - {} requêtes".format(ip, count))

if compteur_https > SEUIL_HTTPS:
    activites_suspectes.append("\nTrafic HTTPS élevé: {} requêtes".format(compteur_https))
    for ip, count in activity_ip_counts['https'].items():
        if count > 20:
            activites_suspectes.append("    IP suspecte (HTTPS): {} - {} requêtes".format(ip, count))

if compteur_flags_push > SEUIL_PUSH:
    activites_suspectes.append("\nTrafic avec Flags PUSH élevé: {} requêtes".format(compteur_flags_push))
    for ip, count in activity_ip_counts['https'].items():
        if count > 20:
            activites_suspectes.append("    IP suspecte (PUSH): {} - {} requêtes".format(ip, count))

activites_suspectes_domaines = []

for domain, count in domain_counts.items():
    if count > SEUIL_DOMAINE:
        activites_suspectes_domaines.append(f"    Domaine suspect: {domain} - {count} requêtes")

# Calcul de la moyenne des requêtes par domaine
total_domain_requests = sum(domain_counts.values())
nombre_domaines = len(domain_counts)
moyenne_domaines = total_domain_requests / nombre_domaines if nombre_domaines > 0 else 0

# Seuil pour considérer un domaine comme suspect (par exemple, 2 fois la moyenne)
SEUIL_DOMAINE = 3 * moyenne_domaines

# Détecter les activités suspectes pour les noms de domaine
activites_suspectes_domaines = []

for domain, count in domain_counts.items():
    if count > SEUIL_DOMAINE:
        activites_suspectes_domaines.append(f"    Domaine suspect: {domain} - {count} requêtes")


# Calcul de la moyenne des requêtes par IP
total_requetes = sum(ip_counts.values())
nombre_ips = len(ip_counts)
moyenne_requetes = total_requetes / nombre_ips if nombre_ips else 0

# Seuil pour définir ce qui est considéré comme une activité suspecte par rapport à la moyenne
SEUIL_SUSPECT = moyenne_requetes * 3

activites_suspectes.append("\nMoyenne des requêtes par IP: {:.2f}".format(moyenne_requetes))

# Détecter les IPs avec une activité suspectement élevée
for ip, count in ip_counts.items():
    if count > SEUIL_SUSPECT:
        activites_suspectes.append("    \nIP suspecte (au-dessus de la moyenne): {} - {} requêtes".format(ip, count))

# Génération du rapport en Markdown incluant les domaines
markdown_text = f'''
# Résultats d'Analyse de Trafic

Nombre total de trames : {sum(ip_counts.values())}

## Liste des adresses IP
''' + '\n'.join(f'- {ip}: {count} requêtes' for ip, count in ip_counts.items()) + f'''

## Liste des noms de domaine
''' + '\n'.join(f'- {domain}: {count} requêtes' for domain, count in domain_counts.items()) + f'''

## Statistiques de Protocole
- SSH: {compteur_ssh}
- HTTP: {compteur_http_final}
- HTTPS: {compteur_https}
- DNS: {compteur_domaine}
- ICMP: {compteur_icmp}
- Flags de Connexion: {compteur_flags_connexion}
- SynAcK: {compteur_flags_SynAcK}
- Déconnexion: {compteur_flags_deco}
- Push: {compteur_flags_push}
- No Connexion: {compteur_flags_nokonnexion}

## Activités Suspectes pour les Adresses IP
''' + '\n'.join(activites_suspectes) + f'''

## Activités Suspectes pour les Noms de Domaine
''' + f' Moyenne des requêtes par domaine : \n{moyenne_domaines:.2f}\n' + '''
''' + '\n\n'.join(activites_suspectes_domaines)

# Conversion en HTML et enregistrement du rapport
html_text = markdown.markdown(markdown_text)
with open("Rapport_Analyse_Trafic.html", "w") as file:
    file.write(html_text)

print("Rapport généré avec succès.")