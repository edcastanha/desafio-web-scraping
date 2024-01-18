import imaplib
import email
from email.header import decode_header

# Configurações do e-mail
email_user = "edson.lourenco@outlook.com.br"
email_pass = "sua_senha" 
mail = imaplib.IMAP4_SSL("outlook.office365.com")  # Servidor IMAP do Outlook

# Faça login no e-mail
mail.login(email_user, email_pass)

# Seleciona a caixa de entrada
mail.select("inbox")

# Procura por e-mails com o assunto "Teste Web Scrapping"
status, messages = mail.search(None, '(SUBJECT "Teste Web Scrapping")')

# Lista de e-mails encontrados
email_list = messages[0].split()

for num in email_list:
    # Obtém o e-mail completo
    _, msg_data = mail.fetch(num, "(RFC822)")
    raw_email = msg_data[0][1]
    msg = email.message_from_bytes(raw_email)

    # Verifica o conteúdo do e-mail
    if "Received: from PR3PR03MB6457.eurprd03.prod.outlook.com" in str(msg):
        # Aqui você pode realizar ações com o e-mail, como extrair informações específicas.
        # Neste exemplo, apenas exibirei o assunto e o remetente.
        subject, encoding = decode_header(msg["Subject"])[0]
        if isinstance(subject, bytes):
            subject = subject.decode(encoding or "utf-8")
        print(f"Assunto: {subject}")
        print(f"Remetente: {msg['From']}")
        print("Conteúdo:")
        print(msg.get_payload(decode=True).decode("utf-8"))
        print("\n")

# Logout
mail.logout()
