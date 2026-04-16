// Reusable card container
export default function Card({ title, children }) {
  return (
    <section className="card">
      {/* Optional title */}
      {title && <h2 className="card-title">{title}</h2>}

      {/* Card content */}
      {children}
    </section>
  );
}