// Card component that serves as a reusable container for displaying content with an optional title
export default function Card({ title, children }) {
  return (
    <section className="card">
      {title && <h2 className="card-title">{title}</h2>}
      {children}
    </section>
  );
}