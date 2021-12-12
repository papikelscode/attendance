from flask import Flask
from flask_login import LoginManager, login_manager, login_url
from models import *
import os
import sqlite3
from mailer import init_mailer
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


from flask_mail import Mail



app = Flask(__name__)
basedir= os.path.abspath(os.path.dirname((__file__)))
database = 'app.db'
# con = sqlite3.connect(os.path.join(basedir,database))


login_manager = LoginManager()

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,database)
app.config['SECRET_KEY'] = 'JDFSHVJHVUSVFHVBFHVDFVBH'
app.config['MAIL_SERVER'] = 'mail.hiosoft.com.ng'
app.config['MAIL_PORT'] = 26
app.config['MAIL_SSL'] = True
app.config['MAIL_USERNAME'] = 'itfneca@hiosoft.com.ng'
app.config['MAIL_PASSWORD'] = 'ITF123@..'
# Set Admin theme
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
admin = Admin(app,name ="ITF Control Panel", template_mode='bootstrap3')
admin.add_view(ModelView(users, db.session))
admin.add_view(ModelView(programme, db.session))
admin.add_view(ModelView(attendance, db.session))
admin.add_view(ModelView(visitor, db.session))
admin.add_view(ModelView(luggage, db.session))


db.init_app(app)
login_manager.init_app(app)
init_mailer(app)

login_manager.login_view = 'endpoint.login'

@login_manager.user_loader
def load_user(user_id):
      return users.query.filter_by(id=user_id).first()



from views import main


app.register_blueprint(main)
if __name__ == '__main__':
  app.run(host='127.0.0.1', port=8000, debug=True)
 