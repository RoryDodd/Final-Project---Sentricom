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
        CREATE UNIQUE INDEX IF NOT EXISTS idx_occupancy_readings_zone_timestamp
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

    # 10. VULNERABLE ZONE STATE
    execute("""
    CREATE TABLE IF NOT EXISTS vulnerable_zone_state (
        zone_id INTEGER PRIMARY KEY,
        vuln_flag TINYINT NOT NULL DEFAULT 0,
        last_seen_at TIMESTAMP,
        FOREIGN KEY (zone_id) REFERENCES zones(zone_id)
    );
    """)

    # 11. KEY MANAGEMENT
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

    # 12. SESSION MANAGEMENT
    execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            session_id INTEGER PRIMARY KEY AUTOINCREMENT,
            key_id INTEGER NOT NULL,
            user_id INTEGER,
            session_token TEXT NOT NULL,
            ip_address TEXT,
            user_agent TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expires_at TIMESTAMP NOT NULL,
            active TINYINT DEFAULT 1,
            FOREIGN KEY (key_id) REFERENCES keys(key_id),
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        );
    """)

    # 13. ZONE DATA CALL LOG
    execute("""
        CREATE TABLE IF NOT EXISTS zone_call_log (
            log_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            key_id INTEGER,
            zone_id INTEGER,
            endpoint TEXT,
            request_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            ip_address TEXT,
            user_agent TEXT,
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            FOREIGN KEY (key_id) REFERENCES keys(key_id),
            FOREIGN KEY (zone_id) REFERENCES zones(zone_id)
        );
    """)

    # 14. LOGGING DATA - changed from master schema
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

    # zone readings
    execute("""
        INSERT INTO occupancy_readings (zone_id, site_id, noisy_count, confidence, zone_state, timestamp) VALUES 
            (1, 1, 27, 0.95, 'MONITOR', datetime('now', '-5 minutes')),
            (2, 1, 42, 0.92, 'MONITOR', datetime('now', '-5 minutes')),
            (3, 1, 18, 0.88, 'LOW RISK', datetime('now', '-5 minutes')),
            (4, 1, 35, 0.91, 'MONITOR', datetime('now', '-5 minutes')),
            (5, 1, 5, 0.75, 'LOW RISK', datetime('now', '-5 minutes')),
            (6, 1, 3, 0.70, 'LOW RISK', datetime('now', '-5 minutes'));
    """)

    # sample warnings
    execute("""
        INSERT INTO warnings (zone_id, title, description, severity, status) VALUES 
            (2, 'High Occupancy', 'Level 1 North Wing is at 56% capacity', 'medium', 'active'),
            (1, 'Evacuation Alert', 'Fire reported in Main Lobby area', 'critical', 'active');  
    """)

    # sample events
    execute("""
        INSERT INTO events (zone_id, event_type, description, severity) VALUES 
            (1, 'alarm_triggered', 'Smoke detector activated', 'critical'),
            (2, 'evacuation_started', 'Evacuation initiated for Level 1', 'warning');
    """)

    # sample privacy budget
    execute("""
        -- Sample privacy budget records (links to the sample readings above)
        INSERT INTO privacy_budget (zone_id, reading_id, noise_level, cumulative_noise) 
        SELECT zone_id, reading_id, 0.5, 0.5 FROM occupancy_readings WHERE reading_id <= 6; 
    """)

    # Sample vulnerable tracking data
    execute("""
        INSERT INTO vulnerable_tracking (zone_from, zone_to, vulnerable_type, estimated_count) VALUES 
            (1, 2, 'elderly', 3),
            (2, 5, 'mobility_aid', 1),
            (3, 2, 'child', 2);
    """)

    # admin, warden, viewer
    execute("""
        INSERT INTO users (username, email, password_hash, full_name, role) VALUES 
            ('Admin', 'admin@sentricom.com', '$2b$12$fgq3oXjO9UrxVkyZlSqvZuhCzikiizQ4hHifWct94H4yUMzo9NtFO', 'System Administrator', 'admin'),
            ('Warden', 'warden@sentricom.com', '$2b$12$9ZOEGomya7Y4gFw1WHgXjOFtK3I8GuKhlSvMeKO7eLZmttaznXp9W', 'System Warden', 'warden'),
            ('Roryadm', 'rory_adm@sentricom.com', '$2b$12$fgq3oXjO9UrxVkyZlSqvZuhCzikiizQ4hHifWct94H4yUMzo9NtFO', 'System Administrator', 'admin'),
            ('Rorywar', 'rory_war@sentricom.com', '$2b$12$9ZOEGomya7Y4gFw1WHgXjOFtK3I8GuKhlSvMeKO7eLZmttaznXp9W', 'System Warden', 'warden'),
            ('Richadm', 'rich_adm@sentricom.com', '$2b$12$fgq3oXjO9UrxVkyZlSqvZuhCzikiizQ4hHifWct94H4yUMzo9NtFO', 'System Administrator', 'admin'),
            ('Richwar', 'rich_war@sentricom.com', '$2b$12$9ZOEGomya7Y4gFw1WHgXjOFtK3I8GuKhlSvMeKO7eLZmttaznXp9W', 'System Warden', 'warden'),
            ('Zenaadm', 'zena_adm@sentricom.com', '$2b$12$fgq3oXjO9UrxVkyZlSqvZuhCzikiizQ4hHifWct94H4yUMzo9NtFO', 'System Administrator', 'admin'),
            ('Zenawar', 'zena_war@sentricom.com', '$2b$12$9ZOEGomya7Y4gFw1WHgXjOFtK3I8GuKhlSvMeKO7eLZmttaznXp9W', 'System Warden', 'warden'),
            ('Benadm', 'ben_adm@sentricom.com', '$2b$12$fgq3oXjO9UrxVkyZlSqvZuhCzikiizQ4hHifWct94H4yUMzo9NtFO', 'System Administrator', 'admin'),
            ('Benwar', 'ben_war@sentricom.com', '$2b$12$9ZOEGomya7Y4gFw1WHgXjOFtK3I8GuKhlSvMeKO7eLZmttaznXp9W', 'System Warden', 'warden'),
            ('Lukeadm', 'luke_adm@sentricom.com', '$2b$12$fgq3oXjO9UrxVkyZlSqvZuhCzikiizQ4hHifWct94H4yUMzo9NtFO', 'System Administrator', 'admin'),
            ('Lukewar', 'luke_war@sentricom.com', '$2b$12$9ZOEGomya7Y4gFw1WHgXjOFtK3I8GuKhlSvMeKO7eLZmttaznXp9W', 'System Warden', 'warden');
    """)

    # api key for testing
    execute("""
        INSERT INTO keys (key_hash, client_name, description, created_at, revoked, last_used) VALUES 
            ('$2b$12$AgZNTBMNqFcmQ8SVqMLp6e7DopVbIDj9lcYa73xvudC055WeTggym', 'sentricom-client/1.0', 'Sentricom Client API Key', CURRENT_TIMESTAMP, 0, NULL);
    """)


    print("Database creation executed successfully.")

    if __name__ == "__main__":
        init_db()

