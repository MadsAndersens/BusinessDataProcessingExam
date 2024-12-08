import psycopg2
from psycopg2.extras import RealDictCursor
import os 

class PostgresDB:
    def __init__(self,
                 db_name: str,
                 user: str,
                 password:str,
                 host: str = "localhost",
                 port: int = 5432):
        """
        Initialize the PostgresDB class with connection parameters.

        :param db_name: Name of the database
        :param user: Username for the database
        :param password: Password for the database
        :param host: Host address (default is localhost)
        :param port: Port number (default is 5432)
        """
        self.db_name = db_name
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.connection = None
        self.error_log_path = "error_logs/db_log.txt"

    def connect(self):
        """Establish a connection to the database."""
        try:
            self.connection = psycopg2.connect(
                dbname=self.db_name,
                password=self.password,
                host=self.host,
                port=self.port,
            )
            print("Database connection established.")
        except Exception as e:
            print(f"Error connecting to database: {e}")
            raise

    def close(self):
        """Close the database connection."""
        if self.connection:
            self.connection.close()
            print("Database connection closed.")

    def execute_query(self, query: str, params=None) -> None:
        """
        Execute a query that modifies the database (e.g., INSERT, UPDATE, DELETE).

        :param query: SQL query to execute
        :param params: Parameters for the SQL query
        """
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params)
                self.connection.commit()
        except Exception as e:
            print(f"Error executing query: {e}")
            self.connection.rollback()
            raise

    def fetch_data(self, query: str, params=None) -> list:
        """
        Fetch data from the database.

        :param query: SQL query to fetch data
        :param params: Parameters for the SQL query
        :return: List of dictionaries containing the query results
        """
        try:
            with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query, params)
                results = cursor.fetchall()
                return results
        except Exception as e:
            print(f"Error fetching data: {e}")
            raise
    
    def write_error_log(self, error_message: str)-> None:
        """
        Write an error message to the error log file.

        :param error_message: Error message to write to the log file
        """
        with open(self.error_log_path, "a") as file:
            file.write(error_message + "\n")

def init_db() -> None:
    """
    Initialize the database by creating the necessary tables.
    """
    # Initialize the database connection
    db = PostgresDB("BuildingData","Mads",os.environ['DB_PASSWORD'])
    try:
        # Connect to the database
        db.connect()

        # Execute the sql file to create the tables
        with open("utils/Create_DB.sql", "r") as file:
            create_tables_query = file.read()
            db.execute_query(create_tables_query)

    finally:
        db.close()