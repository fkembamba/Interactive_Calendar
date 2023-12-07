from bottle import Bottle, request, template
from peewee import MySQLDatabase, Model, PrimaryKeyField, CharField, DateTimeField, ForeignKeyField

# Replace these values with your database connection details
db = MySQLDatabase('interactive_calendar', user='root', password='@p@55ionFruit#', host='localhost', port=3306)

class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    user_id = PrimaryKeyField()
    username = CharField(unique=True)
    password_hash = CharField()
    color_code = CharField(max_length=7)

class Event(BaseModel):
    event_id = PrimaryKeyField()
    title = CharField()
    description = CharField()
    start_datetime = DateTimeField()
    end_datetime = DateTimeField()
    location = CharField()
    created_by = ForeignKeyField(User, backref='events')

class UserEvent(BaseModel):
    user_event_id = PrimaryKeyField()
    user_id = ForeignKeyField(User, backref='user_events')
    event_id = ForeignKeyField(Event, backref='event_users')

app = Bottle()

# Routes for CRUD operations
@app.route('/user/<user_id>', method='GET')
def get_user(user_id):
    user = User.get(User.user_id == user_id)
    return template('user_template', user=user)

@app.route('/user', method='POST')
def create_user():
    username = request.forms.get('username')
    password_hash = request.forms.get('password_hash')
    color_code = request.forms.get('color_code')
    user = User.create(username=username, password_hash=password_hash, color_code=color_code)
    return template('user_template', user=user)

# Similar routes for updating and deleting users

@app.route('/event/<event_id>', method='GET')
def get_event(event_id):
    event = Event.get(Event.event_id == event_id)
    return template('event_template', event=event)

@app.route('/event', method='POST')
def create_event():
    title = request.forms.get('title')
    description = request.forms.get('description')
    # ... (other event fields)
    created_by_id = request.forms.get('created_by')
    created_by = User.get(User.user_id == created_by_id)
    event = Event.create(title=title, description=description, created_by=created_by)
    return template('event_template', event=event)

# Similar routes for updating and deleting events

if __name__ == '__main__':
    #app.run(host='localhost', port=8080, debug=True)
    test_setup_database()
    test_get_items()
    test_add_item()
    test_delete_item()
    test_update_item()
    print("done.")
