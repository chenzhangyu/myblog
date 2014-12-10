from blog.app import app

_mode = 'debug'

if _mode == 'debug':
    app.run(debug=True)
else:
    app.run()

