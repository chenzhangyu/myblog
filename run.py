from blog import app

_mode = 'debug'

if _mode == 'debug':
    print app.url_map
    app.run(debug=True)
else:
    app.run()

