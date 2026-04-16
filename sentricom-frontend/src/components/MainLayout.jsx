// MainLayout component that defines the overall structure of the app, including the header and main content area
import Header from "./Header";

export default function MainLayout({ children }) {
  return (
    <div className="app-shell">
      <Header />

      <main className="app-main">
        {children}
      </main>
    </div>
  );
}