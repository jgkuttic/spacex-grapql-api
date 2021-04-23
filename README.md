#  SpaceX Graphql API using Django, Python and Graphene

## How to run the server

1. Clone the project
```bash
$ git clone https://github.com/jgkuttic/spacex-grapql-api.git
```

2. Create a virtual environment using venv or pipenv
```bash
$ pipenv shell
```

3. Install required python packages
```bash
$ pipenv install -r requirements.txt
```

4. Run the server
```bash
$ python manage.py runserver
```

5. Open your web browser to http://localhost:8000/graphql to access the graphql endpoint where you can make the queries/mutations listed in the *.gql files.