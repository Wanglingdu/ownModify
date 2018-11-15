#!/usr/bin/env python
# encoding: utf-8

#author:PYsaber
#date:2016/9/14

from app import app, db
'''
manager = Manager(app)
manager.add_command("server", Server())

@manager.shell
def make_shell_context():
    return dict(app=app, db=db, User=User, Rop_info=Rop_info)

if __name__ == '__main__':
    manager.run()
'''

app.run(debug=True, port=5000, host='0.0.0.0',threaded=True)
