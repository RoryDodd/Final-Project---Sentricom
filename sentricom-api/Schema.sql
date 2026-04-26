-- SENTRICOM DATABASE

PRAGMA foreign_keys = ON;

-- 1. ZONES
CREATE TABLE zones (
    zone_id INTEGER PRIMARY KEY AUTOINCREMENT,
    zone_name TEXT NOT NULL
    capacity INTEGER DEFAULT 0,
    risk_status TEXT DEFAULT 'LOW RISK'
);

-- 2. OCCUPANCY READINGS
CREATE TABLE occupancy_readings (
    reading_id INTEGER PRIMARY KEY AUTOINCREMENT,
    zone_id INTEGER NOT NULL,
    site_id INTEGER DEFAULT 1,
    noisy_count REAL NOT NULL,
    confidence REAL,
    zone_state TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (zone_id) REFERENCES zones(zone_id)
);

-- 3. PRIVACY BUDGET TRACKING
CREATE TABLE privacy_budget (
    budget_id INTEGER PRIMARY KEY AUTOINCREMENT,
    zone_id INTEGER NOT NULL,
    reading_id INTEGER NOT NULL,
    noise_level REAL NOT NULL,
    cumulative_noise REAL NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (zone_id) REFERENCES zones(zone_id),
    FOREIGN KEY (reading_id) REFERENCES occupancy_readings(reading_id)
);

-- 4. EVENTS
CREATE TABLE events (
    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
    zone_id INTEGER,
    event_type TEXT NOT NULL,
    description TEXT,
    severity TEXT CHECK(severity IN ('info', 'warning', 'critical')) DEFAULT 'info',
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP,
    FOREIGN KEY (zone_id) REFERENCES zones(zone_id)
);

-- 5. WARNINGS
CREATE TABLE warnings (
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

-- 6. USERS
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    full_name TEXT,
    role TEXT CHECK(role IN ('admin', 'warden', 'viewer')) DEFAULT 'warden',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);

-- 7. REPORTS
CREATE TABLE reports (
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

-- 8. TIMELINE
CREATE TABLE timeline (
    timeline_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    event_type TEXT NOT NULL,
    message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);


-- 9. VULNERABLE TRACKING
CREATE TABLE vulnerable_tracking (
    tracking_id INTEGER PRIMARY KEY AUTOINCREMENT,
    zone_from INTEGER,
    zone_to INTEGER,
    vulnerable_type TEXT,
    estimated_count INTEGER,
    passed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 10. KEY MANAGEMENT
CREATE TABLE keys (
    key_id INTEGER PRIMARY KEY AUTOINCREMENT,
    key_hash TEXT NOT NULL,           
    client_name TEXT NOT NULL,         
    description TEXT,                  
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    revoked TINYINT DEFAULT 0,
    last_used TIMESTAMP
);

-- 11. SESSION MANAGEMENT
CREATE TABLE sessions (
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

-- INITIAL DATA

INSERT INTO zones (zone_name, capacity, risk_status) VALUES 
('Main Lobby', 100, 'LOW RISK'),
('Level 1 - North Wing', 75, 'LOW RISK'),
('Level 1 - South Wing', 75, 'LOW RISK'),
('Level 2 - Offices', 50, 'LOW RISK'),
('Emergency Stairwell A', 30, 'LOW RISK'),
('Emergency Stairwell B', 30, 'LOW RISK');

INSERT INTO users (username, email, password_hash, full_name, role) 
VALUES ('admin', 'admin@sentricom.com', 'admin123', 'System Administrator', 'admin');

-- VIEWS

-- Latest occupancy for dashboard
CREATE VIEW latest_occupancy AS
SELECT 
    z.zone_id,
    z.zone_name,
    o.noisy_count,
    o.timestamp AS last_updated
FROM zones z
LEFT JOIN occupancy_readings o ON z.zone_id = o.zone_id
WHERE o.timestamp = (
    SELECT MAX(timestamp) 
    FROM occupancy_readings 
    WHERE zone_id = z.zone_id
);

-- Active warnings for dashboard
CREATE VIEW active_warnings AS
SELECT * FROM warnings WHERE status = 'active';

-- Privacy budget remaining
CREATE VIEW privacy_budget_remaining AS
SELECT 
    zone_id,
    MAX(cumulative_noise) AS total_noise_spent,
    10.0 - MAX(cumulative_noise) AS noise_remaining
FROM privacy_budget
GROUP BY zone_id;