import re
from datetime import datetime

def ics_to_csv(ics_file):
    events = []
    event_data = {}

    with open(ics_file, 'r') as file:
        for line in file:
            if line.startswith('BEGIN:VEVENT'):
                event_data = {}
                continue
            if line.startswith('END:VEVENT'):
                events.append(event_data)
                continue
            if ':' in line:
                key, value = line.strip().split(':', 1)
                event_data[key] = value

    csv_data_list = []

    for event in events:
        # Convertir les dates et heures
        dtstart = datetime.strptime(event['DTSTART'], '%Y%m%dT%H%M%SZ')
        dtend = datetime.strptime(event['DTEND'], '%Y%m%dT%H%M%SZ')
        duration = dtend - dtstart

        # Formatage des données pour le CSV
        uid = event['UID']
        date = dtstart.strftime('%d-%m-%Y')
        heure = dtstart.strftime('%H:%M')
        duree = '{:02}:{:02}'.format(duration.seconds // 3600, (duration.seconds // 60) % 60)
        intitule = event.get('SUMMARY', '')
        salle = event.get('LOCATION', '') or "vide"

        # Traitement de la description avec des expressions régulières
        description_raw = event.get('DESCRIPTION', '')
        description_parts = re.split(r'\\n', description_raw)
        groupe = description_parts[2] if len(description_parts) > 2 else "vide"
        prof = description_parts[3] if len(description_parts) > 3 else "vide"
        salles = salle.split(',') if salle != "vide" else ["vide"]
        professeurs = prof.split(',') if prof != "vide" else ["vide"]

        # Créer la chaîne CSV pour chaque événement
        csv_data = f'"UID = {uid}";\n"Date = {date}"; "Heure = {heure}"; "Durée = {duree}";\n"Ressource = {intitule}";\n"Salle = {", ".join(salles)}";\n"Professeur = {", ".join(professeurs)}";\n"Groupe = {groupe}";'
        csv_data_list.append(csv_data)

    return '\n\n'.join(csv_data_list)

ics_file = 'ADE_RT1_Septembre2023_Decembre2023.ics'
csv_output = ics_to_csv(ics_file)
print(csv_output)

input("Appuyez sur Entrée pour quitter...")
