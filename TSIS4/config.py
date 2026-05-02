W, H = 600, 640
GRID = 20
COLS = W // GRID
ROWS = (H - 80) // GRID
 
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "snake_db",
    "user": "postgres",
    "password": "your_password",
}
 