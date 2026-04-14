import sqlite3
import json
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).with_name("pigilan.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def _column_names(cursor, table_name):
    rows = cursor.execute(f"PRAGMA table_info({table_name})").fetchall()
    return {row["name"] for row in rows}


def init_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            role TEXT DEFAULT 'farmer',
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            barangay TEXT NOT NULL,
            municipality TEXT NOT NULL,
            province TEXT NOT NULL,
            address TEXT,
            latitude REAL,
            longitude REAL
        )
    """)

    user_columns = _column_names(cursor, "users")
    if "username" not in user_columns:
        cursor.execute("ALTER TABLE users ADD COLUMN username TEXT")
    if "password" not in user_columns:
        cursor.execute("ALTER TABLE users ADD COLUMN password TEXT")
    if "role" not in user_columns:
        cursor.execute("ALTER TABLE users ADD COLUMN role TEXT DEFAULT 'farmer'")
    if "address" not in user_columns:
        cursor.execute("ALTER TABLE users ADD COLUMN address TEXT")
    if "latitude" not in user_columns:
        cursor.execute("ALTER TABLE users ADD COLUMN latitude REAL")
    if "longitude" not in user_columns:
        cursor.execute("ALTER TABLE users ADD COLUMN longitude REAL")
    if "client_record_id" not in user_columns:
        cursor.execute("ALTER TABLE users ADD COLUMN client_record_id TEXT")
    if "sync_status" not in user_columns:
        cursor.execute("ALTER TABLE users ADD COLUMN sync_status TEXT DEFAULT 'pending'")
    if "updated_at" not in user_columns:
        cursor.execute("ALTER TABLE users ADD COLUMN updated_at TEXT")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS risk_assessments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            pig_count INTEGER NOT NULL,
            symptoms TEXT NOT NULL,
            checklist_score INTEGER NOT NULL,
            ml_percentage REAL NOT NULL,
            total_percentage REAL NOT NULL,
            risk_level TEXT NOT NULL,
            recommendation TEXT NOT NULL,
            created_at TEXT NOT NULL,
            client_record_id TEXT,
            sync_status TEXT DEFAULT 'pending',
            updated_at TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    assessment_columns = _column_names(cursor, "risk_assessments")
    if "client_record_id" not in assessment_columns:
        cursor.execute("ALTER TABLE risk_assessments ADD COLUMN client_record_id TEXT")
    if "sync_status" not in assessment_columns:
        cursor.execute("ALTER TABLE risk_assessments ADD COLUMN sync_status TEXT DEFAULT 'pending'")
    if "updated_at" not in assessment_columns:
        cursor.execute("ALTER TABLE risk_assessments ADD COLUMN updated_at TEXT")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            assessment_id INTEGER NOT NULL,
            case_name TEXT,
            remarks TEXT,
            case_status TEXT NOT NULL,
            latitude REAL,
            longitude REAL,
            created_at TEXT NOT NULL,
            client_record_id TEXT,
            sync_status TEXT DEFAULT 'pending',
            updated_at TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (assessment_id) REFERENCES risk_assessments(id)
        )
    """)

    case_columns = _column_names(cursor, "cases")
    if "case_name" not in case_columns:
        cursor.execute("ALTER TABLE cases ADD COLUMN case_name TEXT")
    if "remarks" not in case_columns:
        cursor.execute("ALTER TABLE cases ADD COLUMN remarks TEXT")
    if "latitude" not in case_columns:
        cursor.execute("ALTER TABLE cases ADD COLUMN latitude REAL")
    if "longitude" not in case_columns:
        cursor.execute("ALTER TABLE cases ADD COLUMN longitude REAL")
    if "client_record_id" not in case_columns:
        cursor.execute("ALTER TABLE cases ADD COLUMN client_record_id TEXT")
    if "sync_status" not in case_columns:
        cursor.execute("ALTER TABLE cases ADD COLUMN sync_status TEXT DEFAULT 'pending'")
    if "updated_at" not in case_columns:
        cursor.execute("ALTER TABLE cases ADD COLUMN updated_at TEXT")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS biosecurity_checks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            checklist_json TEXT,
            checked_count INTEGER DEFAULT 0,
            unchecked_count INTEGER DEFAULT 0,
            checklist_score INTEGER NOT NULL,
            remarks TEXT NOT NULL,
            created_at TEXT NOT NULL,
            client_record_id TEXT,
            sync_status TEXT DEFAULT 'pending',
            updated_at TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    bio_columns = _column_names(cursor, "biosecurity_checks")
    if "checklist_json" not in bio_columns:
        cursor.execute("ALTER TABLE biosecurity_checks ADD COLUMN checklist_json TEXT")
    if "checked_count" not in bio_columns:
        cursor.execute("ALTER TABLE biosecurity_checks ADD COLUMN checked_count INTEGER DEFAULT 0")
    if "unchecked_count" not in bio_columns:
        cursor.execute("ALTER TABLE biosecurity_checks ADD COLUMN unchecked_count INTEGER DEFAULT 0")
    if "client_record_id" not in bio_columns:
        cursor.execute("ALTER TABLE biosecurity_checks ADD COLUMN client_record_id TEXT")
    if "sync_status" not in bio_columns:
        cursor.execute("ALTER TABLE biosecurity_checks ADD COLUMN sync_status TEXT DEFAULT 'pending'")
    if "updated_at" not in bio_columns:
        cursor.execute("ALTER TABLE biosecurity_checks ADD COLUMN updated_at TEXT")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS case_shares (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            case_id INTEGER NOT NULL,
            pdf_file_path TEXT NOT NULL,
            image_file_path TEXT,
            shared_to TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (case_id) REFERENCES cases(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS case_images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            case_id INTEGER NOT NULL,
            image_path TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (case_id) REFERENCES cases(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            case_id INTEGER NOT NULL,
            barangay TEXT NOT NULL,
            municipality TEXT NOT NULL,
            province TEXT NOT NULL,
            alert_message TEXT NOT NULL,
            alert_level TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (case_id) REFERENCES cases(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            alert_id INTEGER NOT NULL,
            is_read INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (alert_id) REFERENCES alerts(id)
        )
    """)

    conn.commit()
    conn.close()


def create_user(
    username,
    password,
    first_name,
    last_name,
    barangay,
    municipality,
    province,
    address=None,
    role="farmer",
    client_record_id=None,
    sync_status="pending",
):
    conn = get_connection()
    cursor = conn.cursor()
    timestamp = datetime.now().isoformat()

    cursor.execute(
        """
        INSERT INTO users (
            username, password, role, first_name, last_name, barangay, municipality, province,
            address, client_record_id, sync_status, updated_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            username,
            password,
            role,
            first_name,
            last_name,
            barangay,
            municipality,
            province,
            address,
            client_record_id,
            sync_status,
            timestamp,
        ),
    )
    user_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return user_id


def get_user_by_username(username):
    conn = get_connection()
    cursor = conn.cursor()
    row = cursor.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    conn.close()
    return dict(row) if row else None


def get_user_by_id(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    row = cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def get_user_by_client_record_id(client_record_id):
    conn = get_connection()
    cursor = conn.cursor()
    row = cursor.execute(
        "SELECT * FROM users WHERE client_record_id = ?",
        (client_record_id,),
    ).fetchone()
    conn.close()
    return dict(row) if row else None


def create_risk_assessment(
    user_id,
    pig_count,
    symptoms,
    checklist_score,
    ml_percentage,
    total_percentage,
    risk_level,
    recommendation,
    client_record_id=None,
    sync_status="pending",
):
    conn = get_connection()
    cursor = conn.cursor()
    timestamp = datetime.now().isoformat()

    cursor.execute(
        """
        INSERT INTO risk_assessments (
            user_id, pig_count, symptoms, checklist_score,
            ml_percentage, total_percentage, risk_level,
            recommendation, created_at, client_record_id, sync_status, updated_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            user_id,
            pig_count,
            symptoms,
            checklist_score,
            ml_percentage,
            total_percentage,
            risk_level,
            recommendation,
            timestamp,
            client_record_id,
            sync_status,
            timestamp,
        ),
    )
    assessment_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return assessment_id


def update_user_coordinates(user_id, latitude, longitude):
    conn = get_connection()
    cursor = conn.cursor()
    timestamp = datetime.now().isoformat()
    cursor.execute(
        """
        UPDATE users
        SET latitude = ?, longitude = ?, sync_status = 'pending', updated_at = ?
        WHERE id = ?
        """,
        (latitude, longitude, timestamp, user_id),
    )
    conn.commit()
    conn.close()


def update_user_profile(
    user_id,
    first_name,
    last_name,
    barangay,
    municipality,
    province,
    address=None,
    latitude=None,
    longitude=None,
):
    conn = get_connection()
    cursor = conn.cursor()
    timestamp = datetime.now().isoformat()
    cursor.execute(
        """
        UPDATE users
        SET first_name = ?, last_name = ?, barangay = ?, municipality = ?, province = ?, address = ?,
            latitude = ?, longitude = ?, sync_status = 'pending', updated_at = ?
        WHERE id = ?
        """,
        (
            first_name,
            last_name,
            barangay,
            municipality,
            province,
            address,
            latitude,
            longitude,
            timestamp,
            user_id,
        ),
    )
    conn.commit()
    conn.close()


def update_user_password(user_id, password):
    conn = get_connection()
    cursor = conn.cursor()
    timestamp = datetime.now().isoformat()
    cursor.execute(
        "UPDATE users SET password = ?, sync_status = 'pending', updated_at = ? WHERE id = ?",
        (password, timestamp, user_id),
    )
    conn.commit()
    conn.close()


def update_imported_user_profile(
    user_id,
    first_name,
    last_name,
    barangay,
    municipality,
    province,
    address=None,
    latitude=None,
    longitude=None,
    client_record_id=None,
    updated_at=None,
):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE users
        SET first_name = ?, last_name = ?, barangay = ?, municipality = ?, province = ?, address = ?,
            latitude = ?, longitude = ?, client_record_id = ?, sync_status = 'synced', updated_at = ?
        WHERE id = ?
        """,
        (
            first_name,
            last_name,
            barangay,
            municipality,
            province,
            address,
            latitude,
            longitude,
            client_record_id,
            updated_at or datetime.now().isoformat(),
            user_id,
        ),
    )
    conn.commit()
    conn.close()


def create_case(
    user_id,
    assessment_id,
    case_status,
    case_name=None,
    remarks=None,
    latitude=None,
    longitude=None,
    client_record_id=None,
    sync_status="pending",
):
    conn = get_connection()
    cursor = conn.cursor()
    timestamp = datetime.now().isoformat()

    cursor.execute(
        """
        INSERT INTO cases (
            user_id, assessment_id, case_name, remarks, case_status, latitude, longitude,
            created_at, client_record_id, sync_status, updated_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            user_id,
            assessment_id,
            case_name,
            remarks,
            case_status,
            latitude,
            longitude,
            timestamp,
            client_record_id,
            sync_status,
            timestamp,
        ),
    )
    case_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return case_id


def create_biosecurity_check(
    user_id,
    checklist,
    checked_count,
    unchecked_count,
    checklist_score,
    remarks,
    client_record_id=None,
    sync_status="pending",
):
    conn = get_connection()
    cursor = conn.cursor()
    timestamp = datetime.now().isoformat()

    cursor.execute(
        """
        INSERT INTO biosecurity_checks (
            user_id, checklist_json, checked_count, unchecked_count, checklist_score, remarks,
            created_at, client_record_id, sync_status, updated_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            user_id,
            json.dumps(checklist),
            checked_count,
            unchecked_count,
            checklist_score,
            remarks,
            timestamp,
            client_record_id,
            sync_status,
            timestamp,
        ),
    )
    record_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return record_id


def create_case_share(case_id, pdf_file_path, image_file_path, shared_to):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO case_shares (case_id, pdf_file_path, image_file_path, shared_to, created_at)
        VALUES (?, ?, ?, ?, ?)
        """,
        (case_id, pdf_file_path, image_file_path, shared_to, datetime.now().isoformat()),
    )
    share_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return share_id


def create_case_image(case_id, image_path):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO case_images (case_id, image_path, created_at)
        VALUES (?, ?, ?)
        """,
        (case_id, image_path, datetime.now().isoformat()),
    )
    image_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return image_id


def create_alert(case_id, barangay, municipality, province, alert_message, alert_level):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO alerts (
            case_id, barangay, municipality, province,
            alert_message, alert_level, created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            case_id,
            barangay,
            municipality,
            province,
            alert_message,
            alert_level,
            datetime.now().isoformat(),
        ),
    )
    alert_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return alert_id


def create_notification(user_id, alert_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO notifications (user_id, alert_id, is_read, created_at)
        VALUES (?, ?, ?, ?)
        """,
        (user_id, alert_id, 0, datetime.now().isoformat()),
    )
    notification_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return notification_id


def mark_notification_read(notification_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE notifications SET is_read = 1 WHERE id = ?", (notification_id,))
    conn.commit()
    conn.close()


def get_users():
    conn = get_connection()
    cursor = conn.cursor()
    rows = cursor.execute("SELECT * FROM users ORDER BY id DESC").fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_cases():
    conn = get_connection()
    cursor = conn.cursor()
    rows = cursor.execute("SELECT * FROM cases ORDER BY id DESC").fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_case_by_client_record_id(client_record_id):
    conn = get_connection()
    cursor = conn.cursor()
    row = cursor.execute(
        "SELECT * FROM cases WHERE client_record_id = ?",
        (client_record_id,),
    ).fetchone()
    conn.close()
    return dict(row) if row else None


def get_cases_for_user(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    rows = cursor.execute(
        """
        SELECT
            cases.id,
            cases.case_name,
            cases.remarks,
            cases.case_status,
            cases.sync_status,
            cases.updated_at,
            cases.latitude,
            cases.longitude,
            cases.created_at,
            risk_assessments.pig_count,
            risk_assessments.symptoms,
            risk_assessments.checklist_score,
            risk_assessments.ml_percentage,
            risk_assessments.total_percentage,
            risk_assessments.risk_level,
            risk_assessments.recommendation,
            (
                SELECT image_path
                FROM case_images
                WHERE case_images.case_id = cases.id
                ORDER BY case_images.id DESC
                LIMIT 1
            ) AS image_path
        FROM cases
        JOIN risk_assessments ON risk_assessments.id = cases.assessment_id
        WHERE cases.user_id = ?
        ORDER BY cases.id DESC
        """,
        (user_id,),
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def update_case_details(case_id, case_name, remarks, case_status):
    conn = get_connection()
    cursor = conn.cursor()
    timestamp = datetime.now().isoformat()
    cursor.execute(
        """
        UPDATE cases
        SET case_name = ?, remarks = ?, case_status = ?, sync_status = 'pending', updated_at = ?
        WHERE id = ?
        """,
        (case_name, remarks, case_status, timestamp, case_id),
    )
    conn.commit()
    conn.close()


def get_all_cases_with_coordinates():
    conn = get_connection()
    cursor = conn.cursor()
    rows = cursor.execute(
        """
        SELECT
            cases.id,
            cases.user_id,
            cases.case_status,
            cases.latitude,
            cases.longitude,
            cases.created_at,
            risk_assessments.risk_level,
            risk_assessments.total_percentage,
            users.first_name,
            users.last_name
        FROM cases
        JOIN risk_assessments ON risk_assessments.id = cases.assessment_id
        JOIN users ON users.id = cases.user_id
        WHERE cases.latitude IS NOT NULL AND cases.longitude IS NOT NULL
        ORDER BY cases.id DESC
        """
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_notifications_for_user(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    rows = cursor.execute(
        """
        SELECT
            notifications.id,
            notifications.is_read,
            notifications.created_at,
            alerts.alert_message,
            alerts.alert_level
        FROM notifications
        JOIN alerts ON alerts.id = notifications.alert_id
        WHERE notifications.user_id = ?
        ORDER BY notifications.id DESC
        """,
        (user_id,),
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_admin_case_overview(limit=20):
    conn = get_connection()
    cursor = conn.cursor()
    rows = cursor.execute(
        """
        SELECT
            cases.id,
            cases.case_name,
            cases.case_status,
            cases.created_at,
            users.username,
            users.first_name,
            users.last_name,
            users.barangay,
            users.municipality,
            users.province,
            users.address,
            risk_assessments.risk_level,
            risk_assessments.total_percentage,
            risk_assessments.ml_percentage,
            risk_assessments.pig_count
        FROM cases
        JOIN users ON users.id = cases.user_id
        JOIN risk_assessments ON risk_assessments.id = cases.assessment_id
        ORDER BY cases.id DESC
        LIMIT ?
        """,
        (limit,),
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_alerts(limit=20):
    conn = get_connection()
    cursor = conn.cursor()
    rows = cursor.execute(
        """
        SELECT *
        FROM alerts
        ORDER BY id DESC
        LIMIT ?
        """,
        (limit,),
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_biosecurity_checks_for_user(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    rows = cursor.execute(
        """
        SELECT *
        FROM biosecurity_checks
        WHERE user_id = ?
        ORDER BY id DESC
        """,
        (user_id,),
    ).fetchall()
    conn.close()
    records = []
    for row in rows:
        item = dict(row)
        if item.get("checklist_json"):
            item["checklist"] = json.loads(item["checklist_json"])
        else:
            item["checklist"] = {}
        records.append(item)
    return records


def get_biosecurity_check_by_client_record_id(client_record_id):
    conn = get_connection()
    cursor = conn.cursor()
    row = cursor.execute(
        "SELECT * FROM biosecurity_checks WHERE client_record_id = ?",
        (client_record_id,),
    ).fetchone()
    conn.close()
    if not row:
        return None
    item = dict(row)
    if item.get("checklist_json"):
        item["checklist"] = json.loads(item["checklist_json"])
    else:
        item["checklist"] = {}
    return item


def get_pending_sync_counts(user_id=None):
    conn = get_connection()
    cursor = conn.cursor()

    if user_id is None:
        user_count = cursor.execute(
            "SELECT COUNT(*) AS count FROM users WHERE COALESCE(sync_status, 'pending') != 'synced'"
        ).fetchone()["count"]
        case_count = cursor.execute(
            "SELECT COUNT(*) AS count FROM cases WHERE COALESCE(sync_status, 'pending') != 'synced'"
        ).fetchone()["count"]
        bio_count = cursor.execute(
            """
            SELECT COUNT(*) AS count
            FROM biosecurity_checks
            WHERE COALESCE(sync_status, 'pending') != 'synced'
            """
        ).fetchone()["count"]
    else:
        user_count = cursor.execute(
            """
            SELECT COUNT(*) AS count
            FROM users
            WHERE id = ? AND COALESCE(sync_status, 'pending') != 'synced'
            """,
            (user_id,),
        ).fetchone()["count"]
        case_count = cursor.execute(
            """
            SELECT COUNT(*) AS count
            FROM cases
            WHERE user_id = ? AND COALESCE(sync_status, 'pending') != 'synced'
            """,
            (user_id,),
        ).fetchone()["count"]
        bio_count = cursor.execute(
            """
            SELECT COUNT(*) AS count
            FROM biosecurity_checks
            WHERE user_id = ? AND COALESCE(sync_status, 'pending') != 'synced'
            """,
            (user_id,),
        ).fetchone()["count"]

    conn.close()
    return {
        "users": user_count,
        "cases": case_count,
        "biosecurity_checks": bio_count,
    }


def mark_user_synced(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET sync_status = 'synced', updated_at = ? WHERE id = ?",
        (datetime.now().isoformat(), user_id),
    )
    conn.commit()
    conn.close()


def mark_cases_synced_for_user(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE cases SET sync_status = 'synced', updated_at = ? WHERE user_id = ?",
        (datetime.now().isoformat(), user_id),
    )
    conn.commit()
    conn.close()


def mark_biosecurity_checks_synced_for_user(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE biosecurity_checks
        SET sync_status = 'synced', updated_at = ?
        WHERE user_id = ?
        """,
        (datetime.now().isoformat(), user_id),
    )
    conn.commit()
    conn.close()


init_database()
