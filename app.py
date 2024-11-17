from flask import Flask,render_template
from flask_restful import Resource,reqparse,Api,marshal_with,abort,fields
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///database.db'
db = SQLAlchemy(app)
api = Api(app)

class task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=False, nullable=False)
    description = db.Column(db.String(200), unique=False, nullable=False)
    priority = db.Column(db.Integer,unique=False,nullable=False)
    status = db.Column(db.Boolean,nullable=False)

user_args = reqparse.RequestParser()

user_args.add_argument('title', type=str, required=True, help='Title of the task is required')

user_args.add_argument('description', type=str, required=True, help='Description of the task is required')

user_args.add_argument('priority', type=int, required=True, help='Priority of the task is required')

user_args.add_argument('status', type=bool, required=True, help='Status of the task is required')

task_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'description': fields.String,
    'priority': fields.Integer,
    'status': fields.Boolean
    }

class Users(Resource):
    @marshal_with(task_fields)
    def get(self):
        tasks = task.query.all()
        return tasks

    @marshal_with(task_fields)
    def post(self):
        args = user_args.parse_args()
        tas = task(title=args['title'], description=args['description'], 
                    priority=args['priority'], status=args['status'])
        db.session.add(tas)
        db.session.commit()
        user = task.query.all()
        return user, 201

class UserById(Resource):
    @marshal_with(task_fields)
    def get(self, id):
        user = task.query.get_or_404(id)
        return user

    @marshal_with(task_fields)
    def patch(self, id):
        args = user_args.parse_args()
        user = task.query.get_or_404(id)
        user.title = args['title']
        user.description = args['description']
        user.priority = args['priority']
        user.status = args['status']
        db.session.commit()
        return user
    
    def delete(self, id):
        user = task.query.get_or_404(id)
        db.session.delete(user)
        db.session.commit()
        return {"message":"deteled"}, 204



api.add_resource(Users,'/task')
api.add_resource(UserById,'/task/<int:id>')



@app.route('/')
def hello_world():
    return render_template('index.html')