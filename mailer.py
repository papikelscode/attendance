from flask_mail import Mail, Message


mail = Mail()

def init_mailer(app):
    mail.init_app(app)

class EmailSender:
    def _init_(self,subject=None,recipient=None,msgbody=None):
        self.subject = subject
        self.recipient = recipient
        self.msgbody = msgbody


    def send(self):
        try:
            msg = Message(self.subject,
                            sender='itfneca@hiosoft.com.ng',
                            recipients=[self.recipient])
            msg.body = self.msgbody
            mail.send(msg)
            return True
        except Exception as e:
            print(e)
            return False