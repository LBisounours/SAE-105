import re
from datetime import datetime

def ics_to_csv(ics_file):
    event_data = {}
    with open(ics_file, 'r') as file:
        for line in file:
            if line.startswith('BEGIN:VEVENT'):
                continue
            if line.startswith('END:VEVENT'):
                break
            key, value = line.strip().split(':', 1)
            event_data[key] = value

    # Converti les dates et heures
    dtstart = datetime.strptime(event_data['DTSTART'], '%Y%m%dT%H%M%SZ')
    dtend = datetime.strptime(event_data['DTEND'], '%Y%m%dT%H%M%SZ')
    duration = dtend - dtstart

    # Formatage des données pour le CSV
    uid = event_data['UID']
    date = dtstart.strftime('%d-%m-%Y')
    heure = dtstart.strftime('%H:%M')
    duree = '{:02}:{:02}'.format(duration.seconds // 3600, (duration.seconds // 60) % 60)
    intitule = event_data.get('SUMMARY', '')
    salle = event_data.get('LOCATION', '')
    description_raw = event_data.get('DESCRIPTION', '')
    description_parts = re.split(r'\\n', description_raw)

    groupe = description_parts[2] if len(description_parts) > 2 else ''
    prof = description_parts[3] if len(description_parts) > 3 else ''

    # Créer la chaîne CSV
    csv_data = f'"UID = {uid}";\n"Date = {date}"; "Heure = {heure}"; "Durée = {duree}";\n"Ressource = {intitule};"\n"Salle = {salle}";\n"Professeur = {prof}";\n"Groupe = {groupe}";'
    return csv_data

ics_file = 'evenementSAE_15.ics'
csv_output = ics_to_csv(ics_file)
print(csv_output)

input("Appuyez sur Entrée pour quitter...")