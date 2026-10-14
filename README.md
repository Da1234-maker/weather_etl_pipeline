# Weather ETL Pipeline

A small data pipeline that fetches live weather data for Chennai from a public API, structures it, and stores it in a PostgreSQL database. It is scheduled to run automatically every hour.

## What it does

1. **Extract:** calls the [Open-Meteo API](https://open-meteo.com/) (free, no API key) and gets the current weather for Chennai.
2. **Transform:** picks out the useful fields (temperature, windspeed) and adds a `fetched_at` timestamp, producing a clean record.
3. **Load:** inserts the record into a PostgreSQL table.
4. **Schedule:** Windows Task Scheduler runs the script every hour, so the table builds up a history of readings.

```
Open-Meteo API  ->  Python (requests)  ->  clean record  ->  PostgreSQL
                                                  ^
                                   Windows Task Scheduler (hourly)
```

## Tech stack

- Python 3
- `requests` (API calls)
- `psycopg2` (PostgreSQL connection)
- PostgreSQL
- Windows Task Scheduler
- Git / GitHub

## Database table

```sql
CREATE TABLE weather (
    id SERIAL PRIMARY KEY,
    city VARCHAR(50),
    temperature FLOAT,
    windspeed FLOAT,
    fetched_at TIMESTAMP
);
```

## How to run it

1. Install Python and PostgreSQL.
2. Install the libraries:
   ```bash
   pip install requests psycopg2-binary
   ```
3. In PostgreSQL, create a database named `weather_db` and run the `CREATE TABLE` statement above.
4. Create a file named `config.py` in the project folder with your database password (this file is ignored by Git so the password is never uploaded):
   ```python
   DB_PASSWORD = "your_postgres_password"
   ```
5. Run the pipeline:
   ```bash
   python weather.py
   ```
   You should see `Saved to database!`.
6. Check the data:
   ```sql
   SELECT * FROM weather;
   ```

## Scheduling (Windows)

In Task Scheduler, create a task that runs hourly with:

- **Program/script:** path to `python.exe`
- **Add arguments:** `weather.py`
- **Start in:** the project folder

## Example record

```python
{'city': 'Chennai', 'temperature': 29.3, 'windspeed': 9.0, 'fetched_at': '2026-09-01 23:32:41'}
```

## What I learned

- Calling a REST API and reading nested JSON
- Writing reusable Python functions
- Connecting Python to PostgreSQL and inserting rows safely with parameterized queries
- Keeping secrets out of Git using a config file and `.gitignore`
- Scheduling a script and debugging a failed scheduled task

## Possible improvements

- Support multiple cities
- Add error handling and logging
- Move scheduling to Apache Airflow
- Build a dashboard on top of the collected data

## Author

Praveen David A, BSc Data Science student, Chennai, India
