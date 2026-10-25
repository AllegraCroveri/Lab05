import flet as ft
from alert import AlertManager
from deposito_strumenti import DepositoStrumenti

FILE_STRUMENTI = "strumenti.csv"

def main(page: ft.Page):
    page.title = "Lab05"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK

    # --- ALERT ---
    alert = AlertManager(page)

    # --- LA LOGICA DELL'APPLICAZIONE E' PRESA DAL DEPOSITO DI STRUMENTI DEL LAB03 ---
    deposito = DepositoStrumenti("Deposito Strumenti Musicali", "Alessandro Visconti")
    try:
        deposito.carica_file_strumenti(FILE_STRUMENTI)  # Carica il file
    except FileNotFoundError as e:
        alert.show_alert(f"❌ {e}")  # Fa apparire una finestra che mostra l'errore

    # --- UI ELEMENTI ---

    # Text per mostrare il nome e il responsabile del deposito
    txt_titolo = ft.Text(value=deposito.nome, size=38, weight=ft.FontWeight.BOLD)
    txt_responsabile = ft.Text(
        value=f"Responsabile: {deposito.get_responsabile()}",
        size=16,
        weight=ft.FontWeight.BOLD
    )

    # TextField per responsabile
    input_responsabile = ft.TextField(value=deposito.get_responsabile(), label="Responsabile")

    # ListView per mostrare la lista di strumenti aggiornata
    lista_strumenti = ft.ListView(expand=True, spacing=5, padding=10, auto_scroll=True)

    # Tutti i TextField per le info necessarie per aggiungere un nuovo strumento (tipo, marca, anno, contatore posti)
    # devo creare 3 caselle di testo che l'utente potrà riempire per inserire i dati di un nuovon studente
    input_tipo= ft.TextField(label='Tipo', hint_text='Es. Chitarra', expand=True)
    input_marca= ft.TextField(label='Marca', hint_text='Es. Fender', expand=True)
    input_anno= ft.TextField(label='Anno', hint_text='Es. 2021', expand=True)

    #ft.TextField permette all'utente di inserire del testo da tastiera all'interno dell'applicazione
    # label è l'etichetta descrittiva del campo per indicare all'utente cosa deve inserire in quel campo
    # hint_text è un testo di suggerimento (appare in grigio chiaro) e scompare appena si inizia a scrivere nella casella
    # expand indica che questo campo di testo deve espandersi orizzontalmente per occupare lo spazio disponibile
    #in modo flessibile


    # --- FUNZIONI APP ---
    def aggiorna_lista_strumenti():
        lista_strumenti.controls.clear()
        for strumento in deposito.strumenti_ordinati_per_marca():
            stato = "✅" if strumento.disponibile else "⛔"
            lista_strumenti.controls.append(ft.Text(f"{stato} {strumento}"))

    # --- HANDLERS APP ---
    def cambia_tema(e):
        page.theme_mode = ft.ThemeMode.DARK if toggle_cambia_tema.value else ft.ThemeMode.LIGHT
        toggle_cambia_tema.label = "Tema scuro" if toggle_cambia_tema.value else "Tema chiaro"

    def conferma_responsabile(e):
        deposito.set_responsabile(input_responsabile.value)
        txt_responsabile.value = f"Responsabile: {deposito.get_responsabile()}"
        page.update()

    # Handlers per la gestione dei pulsanti utili all'inserimento di un nuovo strumento
    # ogni volta che schiaccia sul pulsante viene eseguito questo codice
    def aggiungi_strumento(e):
        try:
            # prende il testo inserito dell'utente e lo pulisce da eventuali spazi vuoti
            tipo = input_tipo.value.strip()
            marca= input_marca.value.strip()

            if not tipo or not marca:
                #se manca o la marca o il tipo fa apparire il messaggio di errore
                alert.show_alert("❌ I campi 'Tipo' e 'Marca' sono obbligatori.")
                # con return interrompe l'esecuzione della funzione, in modo da evitare
                # di aggiungere uno strumento incompleto
                return

            anno_str= input_anno.value.strip()
            anno= int(anno_str) if anno_str else 0

            # Chiamata al metodo del deposito per aggiungere lo strumento
            deposito.aggiungi_strumento(tipo,marca,anno)

            # Aggiorna la vista e pulisce i campi di input
            aggiorna_lista_strumenti()
            # svuotamento delle caselle di testo azzerandole, pronte per i nuovi inserimenti
            input_tipo.value = ""
            input_marca.value = ""
            input_anno.value = ""
            # dice alla pagina di aggiornarsi per mostrare le modifiche appena fatte
            page.update()

        except ValueError:
            # se l'utente inserisce nella casella dell'anno una stringa con lettere
            alert.show_alert("❌ L'anno deve essere un valore numerico valido.")
        except Exception as ex:
            # cattura tutti gli altri errori possibili
            alert.show_alert(f"❌ Errore durante l'inserimento: {ex}")

    # --- EVENTI ---
    toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=cambia_tema)
    pulsante_conferma_responsabile = ft.Button("Conferma", on_click=conferma_responsabile)

    # Pulsanti per la gestione dell'inserimento di un nuovo strumento
    pulsante_aggiungi = ft.Button("Aggiungi Strumento", on_click=aggiungi_strumento)

    # --- LAYOUT ---
    page.add(
        toggle_cambia_tema,

        # Sezione 1
        txt_titolo,
        txt_responsabile,
        ft.Divider(),

        # Sezione 2
        ft.Text("Modifica Informazioni", size=20),
        ft.Row(spacing=200,
               controls=[input_responsabile, pulsante_conferma_responsabile],
               alignment=ft.MainAxisAlignment.CENTER),

        # Sezione 3
        # ft.Divider(): crea una linea orizzontale di separazione sullo schermo.
        ft.Divider(),
        # creazione di un'intestazione di testo di dimensione 20
        ft.Text("Aggiungi Nuovo Strumento", size=20),

        # lista dei componenti che vengono inseriti: controls=[input_tipo, input_marca, input_anno, pulsante_aggiungi]
        ft.Row(spacing=15,
               controls=[input_tipo, input_marca, input_anno, pulsante_aggiungi],
               # allinea tutto il blocco al centro della pagina orizzontalmente
               alignment=ft.MainAxisAlignment.CENTER),

        # Sezione 4
        ft.Divider(),
        ft.Text("Strumenti", size=20),
        lista_strumenti,
    )
    aggiorna_lista_strumenti()

ft.run(main)
