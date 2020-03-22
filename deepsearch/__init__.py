from notebook.utils import url_path_join
from .handler import DeepsearchHandler


def load_jupyter_server_extension(nb_app):
    """Registers the deepsearch API handler to receive HTTP requests from the frontend extension.
    Parameters
    ----------
    nb_app: notebook.notebookapp.NotebookApp
        Notebook application instance
    """

    web_app = nb_app.web_app
    host_pattern = '.*$'
    route_pattern = url_path_join(web_app.settings['base_url'], '/api/deepsearch')
    web_app.add_handlers(host_pattern, [
        (route_pattern, DeepsearchHandler)
    ])
    nb_app.log.info(f'Registered DeepsearchHandler extension at URL path {route_pattern} '
                    f'to serve results of finding in files under local path {nb_app.notebook_dir}')