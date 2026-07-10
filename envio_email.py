# endereço:3143
import csv
import smtplib
from email.message import EmailMessage

# ---- Configuração ----
DESTINATARIO = "inbox@teste.local"  # GreenMail aceita qualquer destinatário; só precisa ser um endereço válido
SERVIDOR = "Definir endereço"       # Direcionar o Endereço do servidor SMTP do GreenMail (ex: localhost)
PORTA = 0000                        # Porta do servidor SMTP do GreenMail
# Caminho do dataset (colunas: id, from, subject, body, label)
DATASET_PATH = "emails_manual_phishing.csv"

# IDs dos e-mails do dataset que quero enviar. Defina aqui os que desejar.
IDS_PARA_ENVIAR = [0,1,2,3,4,5]


def carregar_emails(caminho=DATASET_PATH, ids=IDS_PARA_ENVIAR):
    """Lê o dataset CSV e retorna os e-mails cujos ids estão em `ids`.

    Preserva a ordem definida em `ids` e avisa sobre ids não encontrados.
    """
    ids_desejados = [str(i) for i in ids]
    encontrados = {}
    with open(caminho, encoding="utf-8") as f:
        for linha in csv.DictReader(f):
            if linha["id"] in ids_desejados:
                encontrados[linha["id"]] = linha

    faltando = [i for i in ids_desejados if i not in encontrados]
    if faltando:
        print(f"Aviso: ids não encontrados no dataset: {', '.join(faltando)}")

    return [encontrados[i] for i in ids_desejados if i in encontrados]


def montar_mensagem(dados, destinatario=DESTINATARIO):
    msg = EmailMessage()
    msg["From"] = dados["from"]
    msg["To"] = destinatario
    msg["Subject"] = dados["subject"]
    msg.set_content(dados["body"])
    return msg


def enviar(msg, servidor=SERVIDOR, porta=PORTA):
    with smtplib.SMTP(servidor, porta) as smtp:
        smtp.send_message(msg)


def main():
    emails = carregar_emails()
    if not emails:
        print("Nenhum e-mail para enviar. Confira IDS_PARA_ENVIAR e o dataset.")
        return

    for dados in emails:
        msg = montar_mensagem(dados)
        enviar(msg)
        print(f"E-mail id={dados['id']} enviado para {DESTINATARIO} via {SERVIDOR}:{PORTA}. Label do e-mail: {dados['label']}")
        input("Pressione Enter para continuar...")

    print(f"Total: {len(emails)} e-mail(s) enviado(s).")


if __name__ == "__main__":
    main()
