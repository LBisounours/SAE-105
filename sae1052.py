import re
import markdown

IP_pattern = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')

with open("DumpFile.txt", "r") as f:
    compteur_http = 0
    compteur_https = 0
    compteur_http_final = 0
    compteur_domaine = 0
    compteur_ssh = 0
    compteur_icmp = 0
    compteur_icmp_req = 0
    compteur_icmp_rep = 0
    compteur_ip = 0
    compteur_flags_connexion = 0
    compteur_flags_SynAcK = 0
    compteur_flags_deco = 0
    compteur_flags_push = 0
    compteur_flags_nokonnexion = 0
    compteur = 0
    listeIp = []

    for line in f:
        if 'http' in line:
            compteur_http += 1
        if '.domain' in line:
            compteur_domaine += 1
        if 'ssh' in line:
            compteur_ssh += 1
        if 'https' in line:
            compteur_https += 1
        if 'ICMP' in line:
            compteur_icmp += 1
        if 'ICMP echo request' in line:
            compteur_icmp_req += 1
        if 'ICMP echo reply' in line:
            compteur_icmp_rep += 1
        if '192.168' in line:
            compteur_ip += 1
        if 'Flags [S]' in line:
            compteur_flags_connexion += 1
        if 'Flags [S.]' in line:
            compteur_flags_SynAcK += 1
        if 'Flags [F.]' in line:
            compteur_flags_deco += 1
        if 'Flags [P.]' in line:
            compteur_flags_push += 1
        if 'Flags [.]' in line:
            compteur_flags_nokonnexion += 1
        for ip in IP_pattern.findall(line):
            if ip not in listeIp:
                listeIp.append(ip)
            compteur += 1

    compteur_http_final = compteur_http - compteur_https

markdown_text = f'''
# Résultats d'Analyse de Trafic

Nombre total de trames : {compteur}

## Liste des adresses IP
''' + '\n'.join(f'- {ip}' for ip in listeIp) + f'''

## Statistiques de Protocole
- SSH: {compteur_ssh}
- HTTP: {compteur_http_final}
- HTTPS: {compteur_https}
- DNS: {compteur_domaine}
- ICMP: {compteur_icmp}
- ICMP Requests: {compteur_icmp_req}
- ICMP Replies: {compteur_icmp_rep}
- Adresses IP 192.168.x.x: {compteur_ip}

## Flags de Connexion
- Connexion Demande: {compteur_flags_connexion}
- SynAcK: {compteur_flags_SynAcK}
- Déconnexion: {compteur_flags_deco}
- Push: {compteur_flags_push}
- No Connexion: {compteur_flags_nokonnexion}
'''

html_output = markdown.markdown(markdown_text)

with open("rapport.html", "w") as file:
    file.write(html_output)

print("Rapport généré.")