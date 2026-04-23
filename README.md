# network-routing-api


Create and manage **Nodes (Servers)**
Create and manage **Edges (Connections with latency)**
Compute **Shortest Path** between nodes
Store and fetch **Route History**


Tech Stack

 **Backend:** Django, Django REST Framework
 **Database:** SQLite 
 **Language:** Python 3



1️ Clone Repository


git clone <your-repo-url>
cd network-routing-api


2️ Create Virtual Environment

```
python3 -m venv venv
source venv/bin/activate
```


3️ Install Dependencies

```
pip install django djangorestframework psycopg2-binary
```



4️ Apply Migrations

```
python manage.py makemigrations
python manage.py migrate
```


 5️ Run Server

```
python manage.py runserver
```

Server will run at:

```
http://127.0.0.1:8000/
```



API Endpoints

Base URL

```
/api/
```



1️ Add Node

**POST** `/api/nodes`

```
{
  "name": "ServerA"
}
```



2️ List Nodes

**GET** `/api/nodes/list`


3️ Add Edge

**POST** `/api/edges`

```
{
  "source": 1,
  "destination": 2,
  "latency": 10
}
```



4️ List Edges

**GET** `/api/edges/list`



5️ Get Shortest Route

**POST** `/api/routes/shortest`

```
{
  "source_id": 1,
  "destination_id": 3
}
```

**Response:**

```
{
  "total_latency": 23.4,
  "path": ["ServerA", "ServerB", "ServerD"]
}
```



6️ Route History

**GET** `/api/routes/history`




Add Node

```
curl -X POST http://127.0.0.1:8000/api/nodes \
-H "Content-Type: application/json" \
-d '{"name": "ServerA"}'
```



Shortest Path

```
curl -X POST http://127.0.0.1:8000/api/routes/shortest \
-H "Content-Type: application/json" \
-d '{"source_id": 1, "destination_id": 3}'


