# To Do List Application

## 📋 Project Overview
This is a *To Do List Application* built using FastAPI as the backend and React with Vite as the frontend. The app supports multiple roles: *Admin, **Manager, and **User*, with distinct permissions and capabilities. The primary goal is to manage tasks and activities, assign them to users, and monitor the performance and progress of those tasks. 

chat me on (mailto:mr.rifqi2000@gmail.com) for any information or discussion

### 🔑 User Roles
- *Admin*: Has full control over tasks and user profiles.
- *Manager*: Can create and delegate tasks to users, update profiles, and monitor user performance.
- *User*: Can view tasks assigned to them, update task status, and comment on tasks.

### Manager User Flow
 ```css
 [Login/Sign Up] --> [Dashboard] --> [Create Activity] --> [Create Task] --> [Delegate Task to User]
                                           |                          |
                                           |                          |
                                    [View Activity]            [Manage Task (CRUD)]  --> [View Analytics]
 ```

### User Flow
 ```css
 [Login/Sign Up] --> [Dashboard] --> [View Tasks] --> [Update Task Status] --> [Add Comments]
                                   |                                 |
                                   |                                 |
                              [Search/Filter Tasks]          [Receive Notifications]

 ```

## 🌟 Features
### Core Features
- *Manager* can create "Activity" and delegate tasks to users.
- Individual dashboards for viewing activities and user performance.
- *User Dashboard* to see tasks assigned specifically to them.
- *Email Notifications* when tasks are assigned or updated.
- Secure authentication using *JWT tokens*.
- *Sharding* data with MongoDB database.

### Additional Features
- Commenting on tasks.
- Task prioritization (High, Medium, Low).
- Task search and filter options.
- Task status updates (Pending, In Progress, Completed).
- Analytics Dashboard for viewing performance metrics.

## 🛠️ Tech Stack
### Backend
- *FastAPI* (latest version)
- *Pydantic V2* for data validation
- *MongoDB* as the database
- *JWT* for secure authentication

### Frontend
- *React* with *Vite*
- UI components using a UI Library (e.g., *Material-UI* or *Ant Design*)

### DevOps
- *Docker* for containerization
- *Git* for version control

## 📂 Project Structure
### Backend Structure
   ```
backend/
│
├── app/
│   ├── __init__.py
│   ├── main.py               # File utama untuk menjalankan aplikasi FastAPI
│   │
│   ├── core/                 # Konfigurasi inti dan pengaturan
│   │   ├── __init__.py
│   │   ├── config.py         # Konfigurasi aplikasi (pengaturan, database URL, dll)
│   │   ├── security.py       # Pengaturan keamanan (JWT, OAuth)
│   │   └── utils.py          # Fungsi utilitas umum
│   │
│   ├── db/                   # Pengaturan dan model database
│   │   ├── __init__.py
│   │   ├── connection.py     # Koneksi database MongoDB dan pengaturan pool
│   │   └── repository/       # Repositori untuk operasi database
│   │       ├── __init__.py
│   │       ├── user_repo.py  # Operasi CRUD untuk User
│   │       ├── task_repo.py  # Operasi CRUD untuk Task
│   │       └── activity_repo.py  # Operasi CRUD untuk Activity
│   │
│   ├── models/               # Deklarasi model Pydantic (schemas)
│   │   ├── __init__.py
│   │   ├── user.py           # Schema untuk User
│   │   ├── task.py           # Schema untuk Task
│   │   └── activity.py       # Schema untuk Activity
│   │
│   ├── routers/              # Routing endpoint API
│   │   ├── __init__.py
│   │   ├── auth.py           # Endpoint untuk autentikasi dan otorisasi
│   │   ├── user.py           # Endpoint untuk operasi User
│   │   ├── task.py           # Endpoint untuk operasi Task
│   │   └── activity.py       # Endpoint untuk operasi Activity
│   │
│   ├── services/             # Logika bisnis aplikasi
│   │   ├── __init__.py
│   │   ├── user_service.py   # Logika bisnis terkait User
│   │   ├── task_service.py   # Logika bisnis terkait Task
│   │   └── activity_service.py # Logika bisnis terkait Activity
│   │
│   └── tests/                # Pengujian untuk setiap komponen
│       ├── __init__.py
│       ├── test_auth.py      # Pengujian untuk autentikasi
│       ├── test_user.py      # Pengujian untuk operasi User
│       ├── test_task.py      # Pengujian untuk operasi Task
│       └── test_activity.py  # Pengujian untuk operasi Activity
│
├── .env                      # File environment untuk konfigurasi variabel (DB URL, JWT_SECRET, dll)
├── requirements.txt          # Daftar dependensi Python
└── Dockerfile                # Konfigurasi Docker untuk aplikasi
   ```

### Frontend Structure

   ```
    frontend/
    ├── public/                    # Public assets (images, icons, etc.)
    ├── src/                       # Source code for React
    │   ├── components/            # Reusable UI components
    │   ├── pages/                 # Page components for different views
    │   ├── services/              # API service calls
    │   ├── store/                 # State management (Redux or Context API)
    │   └── App.js                 # Main React App component
    ├── .env                       # Environment variables
    ├── package.json               # Node.js dependencies
    └── vite.config.js             # Vite configuration file
   ```

## 🗂️ MongoDB Data Structure

### Users Collection

```
{
  "_id": "ObjectId",
  "email": "string",
  "password_hash": "string",
  "roles": ["admin", "manager", "user"], 
  <!-- "profile": {
    "name": "string",
    "position": "string",
    "department": "string"
  } -->
}
```

### Tasks Collection

```
{
  "_id": "ObjectId",
  "title": "string",
  "description": "string",
  "priority": "enum: ['High', 'Medium', 'Low']",
  "status": "enum: ['Pending', 'In Progress', 'Completed']",
  "created_by": "ObjectId (User ID)",
  "assigned_to": "ObjectId (User ID)",
  "comments": [
    {
      "user_id": "ObjectId",
      "content": "string",
      "timestamp": "Date"
    }
  ],
  "created_at": "Date",
  "updated_at": "Date"
}
```

### Activities Collection

```
{
  "_id": "ObjectId",
  "activity_name": "string",
  "description": "string",
  "tasks": ["ObjectId (Task ID)"],
  "manager_id": "ObjectId (Manager ID)",
  "created_at": "Date",
  "updated_at": "Date"
}
```

### 📊 ERD (Entity Relationship Diagram)

Diagram ERD untuk menjelaskan hubungan antar entitas dalam aplikasi ini.

Entities:

1. *User* - Menyimpan informasi pengguna dan peran yang dimiliki.


2. *Task* - Menyimpan tugas yang dapat dibuat oleh Manager dan dapat didelegasikan ke User.


3. *Activity* - Kumpulan tugas yang dikelola oleh Manager.



Relationships:

1. User dapat memiliki beberapa peran (roles).

2. Manager dapat membuat banyak Tasks dan Activities.

3. Task dapat memiliki beberapa Comments.

4. Activity dapat memiliki beberapa Tasks.


Berikut adalah deskripsi tekstual ERD:

```
+----------------+       1..*        +---------------+       *..1     +---------------+
|     User       |-------------------|     Task      |----------------|    Activity   |
+----------------+                   +---------------+                +---------------+
| _id (ObjectId) |                   | _id (ObjectId)|                | _id (ObjectId)|
| username       |                   | title         |                | activity_name |
| email          |                   | description   |                | description   |
| password_hash  |                   | priority      |                | manager_id    |
| roles          |                   | status        |                | tasks         |
+----------------+                   | created_by    |                +---------------+
                                     | assigned_to   |
                                     | comments      |
                                     +---------------+
```


## 🚀 Getting Started

### Prerequisites
Ensure you have the following installed:
- *Ubuntu* (version 24.04 or higer)
- *Python* (version 3.9 or higher)
- *Node.js* (version 14 or higher)
- *Docker* (optional, for containerization)

### Installation
#### 1. Database MongoDB Instalation

1. Docker dan Docker Compose:
   ```bash
   sudo apt update
   sudo apt install docker.io -y
   ```
2. Instal Docker Compose:

   ```bash
   sudo apt install docker-compose -y
   ```

3. Verifikasi instalasi:
   ```bash
   docker --version
   docker-compose --version
   ```

4. jalankan semua container:
   ```bash
   docker-compose up -d
   ```

5. Inisialisasi konfigurasi shard:
   - Config Server
   ```bash
   docker exec -it configsvr mongosh --port 27019
   ```
   
   jalankan: 
   ```javascript
   rs.initiate({
   _id: "configReplSet",
   configsvr: true,
   members: [{ _id: 0, host: "configsvr:27019" }]
   });
   ```

   - Shard 1:
   ```bash
   docker exec -it shard1 mongosh --port 27018
   ```

   ```javascript
   rs.initiate({
   _id: "shard1ReplSet",
   members: [{ _id: 0, host: "shard1:27018" }]
   });
   ```

   - Shard 2:
   ```bash
   docker exec -it shard2 mongosh --port 27017
   ```

   ```javascript
   rs.initiate({
     _id: "shard2ReplSet",
     members: [{ _id: 0, host: "shard2:27017" }]
   });
   ```

   - Tambahkan Shard ke MongoS:
   ```bash
   docker exec -it mongos mongosh --port 27020
   ```

   ```javascript
   sh.addShard("shard1ReplSet/shard1:27018");
   sh.addShard("shard2ReplSet/shard2:27017");
   ```

6. Aktifkan sharding untuk database:

   ```
   use projectDB;
   sh.enableSharding("projectDB");
   ```

7. Tambahkan skema koleksi dan shard key:
   ```
   db.createCollection("users");
   db.createCollection("tasks");
   db.createCollection("activities");

   sh.shardCollection("projectDB.users", { _id: "hashed" });
   sh.shardCollection("projectDB.tasks", { _id: "hashed" });
   sh.shardCollection("projectDB.activities", { _id: "hashed" });
   ```

8. Verivikasi
   - pastikan semua container berjalan:
   ```bash
   docker ps
   ```

   - cek status shard:
   ```
   docker exec -it mongos mongosh --port 27020
   sh.status();
   ```


#### 2. Backend Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/todolist-app.git
   cd todolist-app/backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a .env file in the backend/ directory and add the following environment variables:
   ```bash
   DATABASE_URL="mongodb://localhost:27017/todolist"
   JWT_SECRET_KEY="your_default_secret_key"
   EMAIL_SENDER="your_email@example.com"
   EMAIL_PASSWORD="your_email_password"
   PRIVATE_KEY_PATH="./keys/private.pem"
   PUBLIC_KEY_PATH="./keys/public.pem"
   AUTH_LOG_PATH="./log/usr.log"
   ```

5. Run the FastAPI server:
   ```bash
   uvicorn app.main:app --reload
   ```

6. Access the API documentation at:
   ```bash
   Swagger UI: http://localhost:8000/docs
   ReDoc: http://localhost:8000/redoc
   ```


## 📄 Contributing

1. Fork the repository.


2. Create a feature branch: git checkout -b feature-name


3. Commit your changes: git commit -m 'Add new feature'


4. Push to the branch: git push origin feature-name


5. Create a Pull Request.



## 📝 License

This project is licensed under the [GPL](https://github.com/muhrifqi17/to_do_list_project/blob/main/LICENSE) License. See the LICENSE file for more details.

## 🙏 Acknowledgements

Chat GPT+

FastAPI

MongoDB

React

Vite

