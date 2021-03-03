from flask_script import Manager, Server, Shell

from app import create_app

app = create_app('development')

manager = Manager(app)

manager.add_command('runserver', Server(host='localhost', port=4000))

def make_shell_context():
    return dict(app=app)

manager.add_command("shell", Shell(make_context=make_shell_context))

if __name__ == '__main__':
    manager.run()