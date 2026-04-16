// Page layout with title and content
export default function PageContainer({ title, subtitle, children }) {
  return (
    <div className="page-container">

      {/* Header */}
      <div className="page-header">
        <div>
          <h1 className="page-title">{title}</h1>

          {/* Optional subtitle */}
          {subtitle && (
            <p className="page-subtitle">{subtitle}</p>
          )}
        </div>
      </div>

      {/* Page content */}
      <div className="page-content">
        {children}
      </div>
    </div>
  );
}