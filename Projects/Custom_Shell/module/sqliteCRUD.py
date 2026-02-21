import sqlite3
from datetime import datetime
from prettytable import PrettyTable
from concurrent.futures import ThreadPoolExecutor, as_completed

CURRENT_TIMESTAMP = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


class SqliteCRUD:
    """
    A class for handling SQLite database operations using CRUD methods.
    """

    def __init__(self, db_path):
        """
        Initialize the database connection and cursor.
        """
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def __buildResponse(self, query: str, success: bool, message: str, affected: int, data: dict) -> dict:
        """
        Build a response object for SQL operations.
        Args:
            query (str): SQL query executed.
            success (bool): Status of the operation.
            message (str): Message to return.
            affected (int): Number of affected rows.
            data (list): Query results.
        Returns:
            dict: Response object.
        """
        return {
            "query": query,
            "success": success,
            "message": message,
            "affected": affected,
            "data": data,
        }

    def __runQuery(self, query, qtype="all", params=()):
        """
        Execute a SQL query and return the results.
        Args:
            query (str): SQL query to execute.
            qtype (str): Type of query to run (one, many, all). Defaults to 'all'.
            params (tuple): Parameters for the SQL query.
        Returns:
            dict: Response object with query details.
        """
        affected_keys = ["UPDATE", "INSERT", "DELETE"]
        affected_rows = None
        try:
            self.cursor.execute(query, params)  # Bind parameters here

            # Get the column names from the cursor
            column_names = [desc[0] for desc in self.cursor.description] if self.cursor.description else []

            if qtype == "one":
                rows = self.cursor.fetchone()
                rows = [dict(zip(column_names, rows))] if rows else []
            elif qtype == "many":
                rows = self.cursor.fetchmany()
                rows = [dict(zip(column_names, row)) for row in rows]
            else:
                rows = self.cursor.fetchall()
                rows = [dict(zip(column_names, row)) for row in rows]

            for key in affected_keys:
                if key in query:
                    affected_rows = self.conn.total_changes

            if not affected_rows:
                affected_rows = len(rows)

            # Commit the transaction after modifying queries
            if any(key in query for key in affected_keys):
                self.conn.commit()

            return self.__buildResponse(query, True, "None", int(affected_rows), rows)
        except sqlite3.Error as e:
            return self.__buildResponse(query, False, f"Error executing query: {e}", None, [])


    def __rawResults(self, results):
        """
            Convert raw results to a list of table names.
        Args:
            results (list): List of tuples containing query results.
        Returns:
            list: List of table names.
        """
        table = [row[0] for row in results]
        return table

    def __formattedResults(self, results):
        """
        Format results as a PrettyTable.
        Args:
            results (list): List of tuples containing query results.
        Returns:
            PrettyTable: Table object containing the formatted data.
        """
        table = PrettyTable()
        table.field_names = [desc[0] for desc in self.cursor.description]
        table.add_rows(results)
        return table

    def closeConnection(self):
        """Close the database connection."""
        self.conn.close()

    def createTable(self, table_name, columns):
        """
        Create a new table with the specified columns.
        Args:
            table_name (str): Name of the table.
            columns (list): List of column definitions.
        Returns:
            dict: Response object.
        """
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(columns)});"
        return self.__runQuery(query)

    def dropTable(self, table_name):
        """
        Drop a table by its name.
        Args:
            table_name (str): Name of the table to drop.
        Returns:
            dict: Response object.
        """
        query = f"DROP TABLE IF EXISTS {table_name};"
        return self.__runQuery(query)

    def showTables(self, raw=True):
        """
        Show all tables in the database.
        Args:
            raw (bool): Whether to return raw results or a formatted table.
        Returns:
            list: List of table names or a formatted table.
        """
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        results = self.cursor.fetchall()
        return self.__rawResults(results) if raw else self.__formattedResults(results)

    def describeTable(self, table_name, raw=False):
        """
        Describe the structure of a table.
        Args:
            table_name (str): Name of the table.
            raw (bool): Whether to return raw data or a PrettyTable.
        Returns:
            list: List of dictionaries containing column information.
        """
        self.cursor.execute(f"PRAGMA table_info({table_name});")
        results = self.cursor.fetchall()
        if raw:
            return [{"column_name": r[1], "data_type": r[2], "isnull": "NULL" if r[3] == 0 else "NOT NULL"} for r in results]
        else:
            return self.__formattedResults(results)

    def insertData(self, table_name, data):
        """
        Insert data into a table.
        Args:
                table_name (str): Name of the table.
                data (tuple): Data to insert.
        Returns:
                dict: Response object.
        """
        placeholders = ", ".join(["?"] * len(data))
        query = f"INSERT INTO {table_name} VALUES ({placeholders});"

        print(f"Executing Query: {query} with Data: {data}")  # Debugging line

        return self.__runQuery(query, "one", data)  # Make sure to pass data


    def readData(self, table_name):
        """
        Read data from a table.
        Args:
            table_name (str): Name of the table.
        Returns:
            dict: Response object.
        """
        query = f'SELECT * FROM "{table_name}";'
        return self.__runQuery(query)

    def updateData(self, table_name, target, new_value, where_column, where_value):
        """
        Update data in a table based on a condition.
        Args:
            table_name (str): Name of the table.
            target (str): Column to update.
            new_value (str): New value to set.
            where_column (str): Column to filter on.
            where_value (str): Filter value.
        Returns:
            dict: Response object.
        """
        query = f'UPDATE "{table_name}" SET {target} = "{new_value}" WHERE "{where_column}" = "{where_value}";'
        return self.__runQuery(query)

    def deleteData(self, table_name, condition_column, condition_value):
        """
        Delete data from a table based on a condition.
        Args:
            table_name (str): Name of the table.
            condition_column (str): Column to filter on.
            condition_value (str): Filter value.
        Returns:
            dict: Response object.
        """
        query = f'DELETE FROM "{table_name}" WHERE "{condition_column}" = "{condition_value}";'
        return self.__runQuery(query)

    def formattedPrint(self, table_name):
        """
        Print the contents of a table in a formatted manner.
        Args:
            table_name (str): Name of the table.
        Returns:
            PrettyTable: Table object containing the formatted data.
        """
        self.cursor.execute(f"SELECT * FROM {table_name};")
        table_info = self.cursor.fetchall()
        table = PrettyTable()
        table.field_names = [desc[0] for desc in self.cursor.description]
        table.add_rows(table_info)
        return table

    def readFileData(self, table_name, file_id):
        """
        Read file contents from a file contents table.
        Args:
            table_name (str): Name of the table.
            file_id (str): ID of the file.
        Returns:
            dict: Response object.
        """
        query = f"SELECT chunk FROM {table_name} WHERE file_id = '{file_id}' ORDER BY chunk_index;"
        return self.__runQuery(query)

    def tableExists(self, table_name):
        """
        Check if a table exists in the database.
        Args:
            table_name (str): Name of the table.
        Returns:
            dict: Response object.
        """
        query = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';"
        return self.__runQuery(query, "one")

    def runQuery(self, query, params=(), qtype="all"):
        """
        Execute a raw SQL query safely with parameters.
        Args:
                query (str): SQL query to execute.
                params (tuple): Parameters to safely bind to the SQL query.
                qtype (str): Type of query to run (one, many, all). Defaults to 'all'.
        Returns:
                dict: Response object.
        """
        affected_keys = ["UPDATE", "INSERT", "DELETE"]
        try:
                self.cursor.execute(query, params)
                if qtype == "one":
                        rows = self.cursor.fetchone()
                elif qtype == "many":
                        rows = self.cursor.fetchmany()
                else:
                        rows = self.cursor.fetchall()
                
                # Determine affected rows
                affected_rows = self.conn.total_changes if any(key in query for key in affected_keys) else len(rows)
                self.conn.commit() if any(key in query for key in affected_keys) else None

                return self.__buildResponse(query, True, "Operation Successful", affected_rows, rows)
        except sqlite3.Error as e:
                return self.__buildResponse(query, False, f"Error: {e}", 0, [])


# Example usage:
if __name__ == "__main__":

    db_name = "../data/filesystem.db"
    conn = SqliteCRUD(db_name)

    # res = conn.readFileData("file_contents", "13")

    # data = res["data"]
    # del res["data"]

    # print(res)

    # res = conn.readData("files")
    # print(res)

    # res = conn.updateData("files", "modified_at", CURRENT_TIMESTAMP, "file_id", "13")
    # print(res)

    res = conn.runQuery(
        'UPDATE "files" SET "created_at" = CURRENT_TIMESTAMP WHERE "file_id" = "16";'
    )
    print(res)

    # # Define table schema
    # table_name = "students"
    # columns = ["id TEXT", "name TEXT", "age INTEGER"]

    # # # Create table
    # conn.create_table(table_name, columns)

    # # Insert data
    # data = ("1", "Alice", 25)
    # conn.insert_data(table_name, data)

    # data = ("2", "Bob", 23)
    # conn.insert_data(table_name, data)

    # data = ("3", "Charlie", 11)
    # conn.insert_data(table_name, data)

    # # Read data
    # conn.read_data(table_name)

    # # Update data
    # conn.update_data(table_name, "age", 26, "name", "Alice")

    # # Delete data
    # conn.delete_data(table_name, "name", "Alice")

    # Close the database connection
    conn.closeConnection()
