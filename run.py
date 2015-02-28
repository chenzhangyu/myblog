from blog.app import app
from blog.app import info

app.debug = True

if not app.debug:
    import logging
    from logging import Formatter, FileHandler
    file_handler = FileHandler(info['site']['log_path'], encoding='utf-8')
    file_handler.setLevel(logging.WARNING)
    file_handler.setFormatter(Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]'
    ))
    app.logger.addHandler(file_handler)

if __name__ == '__main__':
    app.run(port=info['site']['port'])
