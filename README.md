# deepsearch_server

### install this package:
pip install .

### Add these lines to /.jupyter/jupyter_notebook_config.py:
##### Make sure there is no assignment to NotebookApp.nbserver_extensions already. 
c.NotebookApp.nbserver_extensions = {
    'deepsearch.deepsearch': True,
}