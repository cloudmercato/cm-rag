Jean-Cloud
==========

RAG system on top of Ollama and `Cloud Mercato <https://www.cloud-mercato.com>`_'s data.

Jean-Cloud is an AI assistant helping user getting a better understanding of Cloud Mercato's knowledge.
You can use it online (soon) or install and run it by yourself.

Installation
------------

::
  docker compose build
  docker compose up
  docker compose exec ollama ollama pull mistral
  docker compose exec jc ./manage.py migrate
  docker compose exec jc ./manage.py update_index
  docker compose exec jc ./manage.py refresh_db


Usage
-----

From here, you can access to the rudimentary web UI at http://yourhost:8000.

License
-------

Jean-Cloud is under MIT license. It's data comes directly from Cloud Mercato platform.
If you would like to benefit from our entire dataset please `contact us <mailto:contact@cloud-mercato.com>`_.


Cheers
------

Jean-Cloud is made with  ❤️  by `Cloud Mercato <https://www.cloud-mercato.com>`_.
