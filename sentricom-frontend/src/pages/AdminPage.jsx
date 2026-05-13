// React state hook
import { useState } from "react";

// Shared layout components
import PageContainer from "../components/PageContainer";
import Card from "../components/Card";

// Simple admin settings page
export default function AdminPage() {

  // Store currently selected privacy method
  const [privacyMethod, setPrivacyMethod] = useState("laplace");

  // Temporary user list until backend integration
  const users = [
    {
      id: 1,
      username: "Admin",
      role: "admin",
    },
    {
      id: 2,
      username: "Warden",
      role: "warden",
    },
  ];

  return (
    <PageContainer
      title="Admin Panel"
      subtitle="System configuration and user management"
    >

      <div className="dashboard-grid-2">

        {/* Privacy configuration */}
        <Card title="Privacy Settings">

          <div className="form-group">
            <label htmlFor="privacyMethod">
              Privacy Engine Method
            </label>

            <select
              id="privacyMethod"
              value={privacyMethod}
              onChange={(event) =>
                setPrivacyMethod(event.target.value)
              }
            >
              <option value="laplace">Laplace</option>
              <option value="gaussian">Gaussian</option>
            </select>
          </div>

          <div
            style={{
              marginTop: "15px",
              padding: "10px",
              background: "#f5f5f5",
              borderRadius: "8px",
            }}
          >
            Current Method: <strong>{privacyMethod}</strong>
          </div>

        </Card>

        {/* User management */}
        <Card title="User Management">

          <table className="summary-table">
            <thead>
              <tr>
                <th>User</th>
                <th>Role</th>
              </tr>
            </thead>

            <tbody>
              {users.map((user) => (
                <tr key={user.id}>
                  <td>{user.username}</td>
                  <td>{user.role}</td>
                </tr>
              ))}
            </tbody>
          </table>

        </Card>

      </div>

    </PageContainer>
  );
}