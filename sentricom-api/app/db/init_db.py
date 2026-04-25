# app/db/init_db.py
# Run this at startup to create the database if it doesn't exist

from app.db.connection import execute

def init_db():

    # Enable foreign key support
    execute("""PRAGMA foreign_keys = ON;""")

    # 1. ZONES
    execute("""
        CREATE TABLE IF NOT EXISTS zones (
            zone_id INTEGER PRIMARY KEY AUTOINCREMENT,
            zone_name TEXT NOT NULL
        );
    """)

    # 2. OCCUPANCY READINGS
    execute("""
        CREATE TABLE IF NOT EXISTS occupancy_readings (
            reading_id INTEGER PRIMARY KEY AUTOINCREMENT,
            zone_id INTEGER NOT NULL,
            site_id INTEGER DEFAULT 1,
            noisy_count REAL NOT NULL,
            confidence REAL,
            zone_state TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (zone_id) REFERENCES zones(zone_id)
        );
    """)

    # 3. PRIVACY BUDGET TRACKING
    execute("""
        CREATE TABLE IF NOT EXISTS privacy_budget (
            budget_id INTEGER PRIMARY KEY AUTOINCREMENT,
            zone_id INTEGER NOT NULL,
            reading_id INTEGER NOT NULL,
            noise_level REAL NOT NULL,
            cumulative_noise REAL NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (zone_id) REFERENCES zones(zone_id),
            FOREIGN KEY (reading_id) REFERENCES occupancy_readings(reading_id)    
        );
    """)

    # 4. EVENTS
    execute("""
        CREATE TABLE IF NOT EXISTS events (
            event_id INTEGER PRIMARY KEY AUTOINCREMENT,
            zone_id INTEGER,
            event_type TEXT NOT NULL,
            description TEXT,
            severity TEXT CHECK(severity IN ('info', 'warning', 'critical')) DEFAULT 'info',
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            resolved_at TIMESTAMP,
            FOREIGN KEY (zone_id) REFERENCES zones(zone_id)
        );
    """)

    # 5. WARNINGS
    execute("""
        CREATE TABLE IF NOT EXISTS warnings (
            warning_id INTEGER PRIMARY KEY AUTOINCREMENT,
            zone_id INTEGER,
            title TEXT NOT NULL,
            description TEXT,
            severity TEXT CHECK(severity IN ('low', 'medium', 'high', 'critical')) DEFAULT 'medium',
            status TEXT CHECK(status IN ('active', 'acknowledged', 'resolved')) DEFAULT 'active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            resolved_at TIMESTAMP,
            resolved_by INTEGER,
            FOREIGN KEY (zone_id) REFERENCES zones(zone_id)
        );
    """)

    # 6. USERS
    execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            full_name TEXT,
            role TEXT CHECK(role IN ('admin', 'warden', 'viewer')) DEFAULT 'warden',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP
        );
    """)

    # 7. REPORTS
    execute("""
        CREATE TABLE IF NOT EXISTS reports (
            report_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            summary TEXT,
            content TEXT,
            status TEXT CHECK(status IN ('draft', 'generated', 'exported')) DEFAULT 'draft',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            exported_at TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        );
    """)

    # 8. TIMELINE
    execute("""
        CREATE TABLE IF NOT EXISTS timeline (
            timeline_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            event_type TEXT NOT NULL,
            message TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        );
    """)

    # 9. VULNERABLE TRACKING
    execute("""
        CREATE TABLE IF NOT EXISTS vulnerable_tracking (
            tracking_id INTEGER PRIMARY KEY AUTOINCREMENT,
            zone_from INTEGER,
            zone_to INTEGER,
            vulnerable_type TEXT,
            estimated_count INTEGER,
            passed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    # 10. KEY MANAGEMENT
    execute("""
        CREATE TABLE IF NOT EXISTS keys (
            key_id INTEGER PRIMARY KEY AUTOINCREMENT,
            key_hash TEXT NOT NULL,           
            client_name TEXT NOT NULL,         
            description TEXT,                  
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            revoked TINYINT DEFAULT 0,
            last_used TIMESTAMP
        );
    """)

    # 11. SESSION MANAGEMENT
    execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            session_id INTEGER PRIMARY KEY AUTOINCREMENT,
            key_id INTEGER NOT NULL,
            session_token TEXT NOT NULL,
            ip_address TEXT,
            user_agent TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expires_at TIMESTAMP NOT NULL,
            active TINYINT DEFAULT 1,
            FOREIGN KEY (key_id) REFERENCES keys(key_id)
        );
    """)

    '''
    #
    execute("""
        CREATE TABLE IF NOT EXISTS xxx (
        
        );
    """)
    '''

    print("Database creation executed successfully.")

    if __name__ == "__main__":
        init_db()

