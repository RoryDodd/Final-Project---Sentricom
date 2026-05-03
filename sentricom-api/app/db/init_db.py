# app/db/init_db.py
# Run this at startup to create the database if it doesn't exist

from app.db.connection import execute

def init_db():

    # Enable foreign key support
    execute("""PRAGMA foreign_keys = ON;""")

    # 1. ZONES - changed from master schema
    execute("""
        CREATE TABLE IF NOT EXISTS zones (
            zone_id INTEGER PRIMARY KEY,
            zone_name TEXT NOT NULL,
            capacity INTEGER DEFAULT 0,
            risk_status TEXT DEFAULT 'LOW RISK'
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

    # dulplicate protection for occupancy_readings ** check date in timestamp
    execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS idx_occupancy_readings_zone_timesamp
        ON occupancy_readings(zone_id, timestamp);
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

    # 12. LOGGING DATA - changed from master schema
    # originally for viewing pipeline events in UI but will be extended.
    execute("""
        CREATE TABLE IF NOT EXISTS pipeline_event_log (
            log_id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_type TEXT NOT NULL,
            severity TEXT DEFAULT 'info',
            reason TEXT,
            batch_id TEXT,
            zone_count INTEGER,
            age_seconds REAL,
            queue_depth INTEGER,
            validation_error TEXT,
            problem_record TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)


    '''
    #
    execute("""
        CREATE TABLE IF NOT EXISTS xxx (
        
        );
    """)
    '''

    # INITIAL DATA - changed from master schema
    execute("""
        INSERT OR IGNORE INTO zones (zone_id,zone_name, capacity, risk_status) VALUES 
        (1, 'Main Lobby', 100, 'LOW RISK'),
        (2, 'Level 1 - North Wing', 75, 'LOW RISK'),
        (3, 'Level 1 - South Wing', 75, 'LOW RISK'),
        (4, 'Level 2 - Offices', 50, 'LOW RISK'),
        (5, 'Emergency Stairwell A', 30, 'LOW RISK'),
        (6, 'Emergency Stairwell B', 30, 'LOW RISK');  
    """)

    # admin, warden, viewer
    execute("""
        INSERT INTO users (username, email, password_hash, full_name, role) VALUES 
            ('Admin', 'admin@sentricom.com', '$2b$12$fgq3oXjO9UrxVkyZlSqvZuhCzikiizQ4hHifWct94H4yUMzo9NtFO', 'System Administrator', 'admin'),
            ('Warden', 'warden@sentricom.com', '$2b$12$9ZOEGomya7Y4gFw1WHgXjOFtK3I8GuKhlSvMeKO7eLZmttaznXp9W', 'System Warden', 'warden');
    """)

    execute("""
        INSERT INTO keys (key_hash, client_name, description, created_at, revoked, last_used) VALUES 
            ('$2b$12$AgZNTBMNqFcmQ8SVqMLp6e7DopVbIDj9lcYa73xvudC055WeTggym', 'sentricom-client/1.0', 'Sentricom Client API Key', CURRENT_TIMESTAMP, 0, NULL);
    """)


    print("Database creation executed successfully.")

    if __name__ == "__main__":
        init_db()

