import os
from pymobiledevice3.lockdown import create_using_usbmux
from pymobiledevice3.services.installation_proxy import InstallationProxyService

def get_installed_apps():
    try:
        # Crea una connessione al dispositivo iOS tramite USB
        lockdown = create_using_usbmux()
        app_service = InstallationProxyService(lockdown=lockdown)

        # Estrai l'elenco delle applicazioni installate
        apps = app_service.get_apps()
        print("Dati grezzi restituiti da get_apps():", apps)  # Debug: mostra i dati grezzi

        # Crea una lista per salvare i nomi delle app
        app_list = []
        if not apps:
            print("Nessuna app trovata.")
            return app_list

        # Controlla il tipo di dati restituito
        for app in apps:
            if isinstance(app, dict):  # Se è un dizionario
                bundle_id = app.get("CFBundleIdentifier", "Sconosciuto")
                app_name = app.get("CFBundleName", bundle_id)
                app_list.append(f"Nome: {app_name} | Bundle ID: {bundle_id}")
            elif isinstance(app, str):  # Se è una stringa (solo Bundle ID)
                app_list.append(f"Nome: Sconosciuto | Bundle ID: {app}")
            else:
                app_list.append(f"Dato non riconosciuto: {app}")

        return app_list

    except Exception as e:
        print(f"Errore durante l'estrazione delle app: {e}")
        return []

def save_to_file(app_list, filename="installed_apps.txt"):
    try:
        with open(filename, "w", encoding="utf-8") as file:
            if not app_list:
                file.write("Nessuna applicazione trovata o errore di connessione.\n")
            else:
                file.write("Elenco delle applicazioni installate:\n")
                file.write("-" * 50 + "\n")
                for app in app_list:
                    file.write(app + "\n")
        print(f"Elenco salvato con successo in {filename}")
    except Exception as e:
        print(f"Errore durante il salvataggio del file: {e}")

def main():
    print("Collega il tuo iPhone tramite USB e assicurati che sia sbloccato...")
    apps = get_installed_apps()
    save_to_file(apps)

if __name__ == "__main__":
    main()