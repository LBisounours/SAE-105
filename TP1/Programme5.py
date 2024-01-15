import re
from datetime import datetime
import matplotlib.pyplot as plt

def ics_events(ics_file):
    events = []
    with open(ics_file, 'r') as file:
        lines = [line.strip() for line in file]
    content = "\n".join(lines)
    events_raw = content.split("BEGIN:VEVENT")[1:]
    for event_raw in events_raw:
        lines = event_raw.strip().split("\n")
        event_data = {}
        key = ""
        for line in lines:
            if line.startswith("END:VEVENT"):
                break
            if ':' in line:
                key, value = line.split(':', 1)
                event_data[key] = value
            else:
                event_data[key] += line
        events.append(event_data)
    return events

def count_tp_sessions(events, groupe):
    monthly_counts = {'09': 0, '10': 0, '11': 0, '12': 0}
    for event in events:
        if 'DESCRIPTION' in event and groupe in event['DESCRIPTION']:
            dtstart = datetime.strptime(event['DTSTART'], '%Y%m%dT%H%M%SZ')
            month = dtstart.strftime('%m')
            if month in monthly_counts:
                monthly_counts[month] += 1
    return monthly_counts

def export_graph(counts):
    months = ['Septembre', 'Octobre', 'Novembre', 'Décembre']
    sessions = [counts[month] for month in ['09', '10', '11', '12']]

    plt.bar(months, sessions, color='blue')
    plt.xlabel('Mois')
    plt.ylabel('Nombre de séances de TP')
    plt.title('Nombre de séances de TP pour le groupe A1 par mois')

    plt.savefig('tp_sessions_graph.png')
    plt.close()

def export_html(counts):
    graph_file = 'tp_sessions_graph.png'
    export_graph(counts)

    html_content = f"""
    <html>
    <head><title>Rapport de Sessions TP</title></head>
    <body>
    <h1>Nombre de séances de TP pour le groupe A1 par mois</h1>
    <img src="{graph_file}" alt="Graphique des séances de TP">
    </body>
    </html>
    """

    with open("report.html", "w") as file:
        file.write(html_content)

ics_file = 'ADE_RT1_Septembre2023_Decembre2023.ics'
events = ics_events(ics_file)
tp_counts = count_tp_sessions(events, 'RT1-TP A1')

export_html(tp_counts)

print("Rapport généré avec succès.")
