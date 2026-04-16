import { useState } from "react";
import PageContainer from "../components/PageContainer";
import Card from "../components/Card";

export default function ProfilePage() {
  const [profile, setProfile] = useState({
    fullName: "John Doe",
    email: "john.doe@sentricom.com",
    role: "Security Operator",
    department: "Emergency Monitoring",
    phone: "+61 412 345 678",
    location: "Control Room A",
    emailAlerts: true,
    smsAlerts: false,
    systemNotifications: true,
  });

  const handleChange = (event) => {
    const { name, value, type, checked } = event.target;

    setProfile((prev) => ({
      ...prev,
      [name]: type === "checkbox" ? checked : value,
    }));
  };

  const handleSave = (event) => {
    event.preventDefault();
    alert("Profile changes saved locally. Backend connection can be added later.");
  };

  return (
    <PageContainer
      title="Profile"
      subtitle="Manage your account details and notification preferences"
    >
      <div className="profile-grid">
        <Card title="User Overview">
          <div className="profile-summary">
            <div className="profile-avatar">AM</div>

            <div className="profile-summary-text">
              <h3>{profile.fullName}</h3>
              <p>{profile.role}</p>
              <span>{profile.email}</span>
            </div>
          </div>

          <div className="profile-meta">
            <div className="profile-meta-item">
              <span className="meta-label">Department</span>
              <span className="meta-value">{profile.department}</span>
            </div>

            <div className="profile-meta-item">
              <span className="meta-label">Location</span>
              <span className="meta-value">{profile.location}</span>
            </div>
          </div>
        </Card>

        <Card title="System Info">
          <div className="report-preview">
            <div className="preview-item">
              <span className="preview-label">Access Level</span>
              <span className="preview-value">Operator</span>
            </div>

            <div className="preview-item">
              <span className="preview-label">Last Login</span>
              <span className="preview-value">Today, 8:42 AM</span>
            </div>

            <div className="preview-item">
              <span className="preview-label">Assigned Region</span>
              <span className="preview-value">Main Campus</span>
            </div>

            <div className="report-note">
              Security settings, password reset, and role permissions can be added later when authentication is connected.
            </div>
          </div>
        </Card>
      </div>

      <div className="profile-form-layout">
        <Card title="Edit Profile">
          <form className="report-form" onSubmit={handleSave}>
            <div className="form-row">
              <div className="form-group">
                <label htmlFor="fullName">Full Name</label>
                <input
                  id="fullName"
                  name="fullName"
                  type="text"
                  value={profile.fullName}
                  onChange={handleChange}
                />
              </div>

              <div className="form-group">
                <label htmlFor="role">Role</label>
                <input
                  id="role"
                  name="role"
                  type="text"
                  value={profile.role}
                  onChange={handleChange}
                />
              </div>
            </div>

            <div className="form-row">
              <div className="form-group">
                <label htmlFor="email">Email</label>
                <input
                  id="email"
                  name="email"
                  type="email"
                  value={profile.email}
                  onChange={handleChange}
                />
              </div>

              <div className="form-group">
                <label htmlFor="phone">Phone</label>
                <input
                  id="phone"
                  name="phone"
                  type="text"
                  value={profile.phone}
                  onChange={handleChange}
                />
              </div>
            </div>

            <div className="form-row">
              <div className="form-group">
                <label htmlFor="department">Department</label>
                <input
                  id="department"
                  name="department"
                  type="text"
                  value={profile.department}
                  onChange={handleChange}
                />
              </div>

              <div className="form-group">
                <label htmlFor="location">Location</label>
                <input
                  id="location"
                  name="location"
                  type="text"
                  value={profile.location}
                  onChange={handleChange}
                />
              </div>
            </div>

            <button type="submit" className="primary-button">
              Save Changes
            </button>
          </form>
        </Card>

        <Card title="Notification Preferences">
          <div className="settings-list">
            <label className="settings-item">
              <div>
                <span className="settings-title">Email Alerts</span>
                <p className="settings-description">
                  Receive crowd and incident alerts by email
                </p>
              </div>
              <input
                type="checkbox"
                name="emailAlerts"
                checked={profile.emailAlerts}
                onChange={handleChange}
              />
            </label>

            <label className="settings-item">
              <div>
                <span className="settings-title">SMS Alerts</span>
                <p className="settings-description">
                  Receive urgent notifications by SMS
                </p>
              </div>
              <input
                type="checkbox"
                name="smsAlerts"
                checked={profile.smsAlerts}
                onChange={handleChange}
              />
            </label>

            <label className="settings-item">
              <div>
                <span className="settings-title">System Notifications</span>
                <p className="settings-description">
                  Show in-app alerts and operational reminders
                </p>
              </div>
              <input
                type="checkbox"
                name="systemNotifications"
                checked={profile.systemNotifications}
                onChange={handleChange}
              />
            </label>
          </div>
        </Card>
      </div>
    </PageContainer>
  );
}