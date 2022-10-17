# ERSS-project-lam147-sj346

Before Running:
- open docker-deploy/ups_server/server.py
- edit the WORLD_HOST value on line 33 to be the hostname where the world server is running (i.e. "vcm-25947.vm.duke.edu")

To Run with Docker:
(Comes up, but currently bugged after multithreading implementation, so DO NOT USE)
- cd into docker-deploy
- run: sudo docker-compose up


To Run without Docker:

- FRONT_END:
  - cd into docker-deploy/mini_ups
  - run: python3 manage.py python3 manage.py runserver 0.0.0.0:8000

- BACK_END:
  - cd into docker-deploy/ups_server
  - run: python3 server.py

