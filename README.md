## 📘 API Documentation

### Base URL
```
http://localhost:8000/api/v1/
```

---


Running the Application with Docker Compose

To quickly set up and run the application locally using Docker, Docker Compose is used to manage the services.
🚀 Steps to Spin Up the App:

    Clone the repository: If you haven’t already cloned the repository, use the following command:

git clone <repository-url>
cd <repository-folder>

Build and start the services: Use Docker Compose to build and start the services (backend, database, etc.):

    docker-compose up --build

    This will:

        Build the application image.

        Start the backend (Django app) and the PostgreSQL database.

        Make the app available at http://localhost:8000/.

    Access the app:

        The app will be running on http://localhost:8000/.

        To access the Django admin panel, visit http://localhost:8000/admin/ (you’ll need to create a superuser, see below).

📝 Create a Superuser:

If you want to access the Django admin panel, you'll need to create a superuser. You can do this by running the following command inside the container:

docker-compose exec web python manage.py createsuperuser

Follow the prompts to create the superuser.

    Access the Postgres database (optional): If you want to access the Postgres database, you can run:

    docker-compose exec db psql -U postgres

    This will open a psql prompt, and you can interact with the database directly.

🧹 Stop and Clean Up:

When you’re done, you can stop the running services with:

docker-compose down

This will stop the containers and remove them. If you want to remove the volumes (to clear out the database, etc.), run:

docker-compose down -v

---

### 🔹 GET `/levels/`

**Description**: Retrieve a list of glucose readings for a specific user. Supports filtering by start/stop datetime, pagination, and ordering.

**Query Parameters**:

| Parameter     | Type   | Required | Description                                               |
|---------------|--------|----------|-----------------------------------------------------------|
| `user_id`     | int    | ✅ yes    | The ID of the user whose readings you want to retrieve.  |
| `start`       | string | ❌ no     | ISO 8601 datetime to filter readings from (inclusive).   |
| `stop`        | string | ❌ no     | ISO 8601 datetime to filter readings to (inclusive).     |
| `ordering`    | string | ❌ no     | Field to order by. E.g. `glucose_level`, `-reading_datetime`. |
| `page`        | int    | ❌ no     | The page number for paginated results.                   |
| `page_size`   | int    | ❌ no     | The number of items per page.                            |

**Response** (200 OK):

```json
{
  "count": 3,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "user": 1,
      "glucose_level": 100,
      "reading_datetime": "2021-10-10T09:00:00Z"
    },
    ...
  ]
}
```

**Example**:
```
GET /api/v1/levels/?user_id=1&start=2021-02-10T00:00:00&stop=2021-02-12T00:00:00&ordering=-glucose_level&page=1&page_size=30
```

---

### 🔹 GET `/levels/<id>/`

**Description**: Retrieve a single glucose reading by its unique ID.

**Path Parameters**:

| Parameter | Type | Required | Description              |
|-----------|------|----------|--------------------------|
| `id`      | int  | ✅ yes    | The ID of the reading.   |

**Response** (200 OK):

```json
{
  "id": 2,
  "user": 1,
  "glucose_level": 150,
  "reading_datetime": "2021-10-11T09:00:00Z"
}
```

**Error Responses**:
- `404 Not Found` if the reading with the given ID does not exist.

**Example**:
```
GET /api/v1/levels/2/
```

---
Import Glucose Readings Command

This command imports glucose readings from CSV files into the database. The CSV files should be placed in a directory and follow a specific format.
📂 Directory Format:

    The files should be named user_<user_id>.csv (e.g., user_1.csv, user_2.csv).

    Each file contains glucose readings for the specified user, with the following columns:

        Glukosewert-Verlauf mg/dL (Glucose Level)

        Gerätezeitstempel (Date and Time)

📝 Sample CSV Format:

(download)

🚀 Command Usage

    Prepare your CSV files:

        Place the user_<user_id>.csv files in the sample_data directory.

    Run the command:

        Run the following Django management command to import the glucose readings:

    python manage.py import_glucose_readings sample_data/


⚙️ What happens when you run this command?

    The command reads all CSV files in the provided directory.

    It imports the glucose readings for each user in the file, creating GlucoseReading objects in the database associated with the correct user.
---

### Authentication
Currently, no authentication is enforced on these endpoints. If you plan to restrict access later, consider using DRF's authentication classes.

---

