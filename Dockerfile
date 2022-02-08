FROM jupyter/tensorflow-notebook

USER $NB_UID

RUN pip install spotipy pymongo python-dotenv
