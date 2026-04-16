// Layout wrapper with header and content
import Header from "./Header";

export default function MainLayout({ children }) {
  return (
    <div className="app-shell">
      {/* Top navigation */}
      <Header />

      {/* Page content */}
      <main className="app-main">
        {children}
      </main>
    </div>
  );
}