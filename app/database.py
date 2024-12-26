import sqlite3

DB_NAME = "data.db"


def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Crear tablas
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS scrape_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT,
            scraped_text TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS process_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            input_text TEXT,
            result TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS combined_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT,
            scraped_text TEXT,
            analysis TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """
    )
    conn.commit()
    conn.close()


def save_scrape_result(url, scraped_text):
    conn = get_db_connection()

    # Convertir listas a cadenas separadas por comas
    if isinstance(scraped_text, list):
        scraped_text = ", ".join(scraped_text)  # Convertir a string separado por comas

    conn.execute(
        """
        INSERT INTO scrape_results (url, scraped_text, created_at)
        VALUES (?, ?, datetime('now'))
    """,
        (url, scraped_text),
    )
    conn.commit()
    conn.close()


def save_process_result(input_text, result):
    conn = get_db_connection()
    conn.execute(
        """
        INSERT INTO process_results (input_text, result)
        VALUES (?, ?)
    """,
        (input_text, str(result)),
    )
    conn.commit()
    conn.close()


def save_combined_result(url, scraped_text, analysis):
    conn = get_db_connection()

    # Convertir listas a cadenas separadas por comas
    if isinstance(scraped_text, list):
        scraped_text = ", ".join(scraped_text)  # Convertir a string separado por comas
    if isinstance(analysis, list):
        analysis = ", ".join(analysis)

    conn.execute(
        """
        INSERT INTO combined_results (url, scraped_text, analysis, created_at)
        VALUES (?, ?, ?, datetime('now'))
    """,
        (url, scraped_text, analysis),
    )
    conn.commit()
    conn.close()

init_db()
