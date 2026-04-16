// PageContainer component that provides a consistent layout for different pages in the app
export default function PageContainer({ title, subtitle, children }) {
  return (
    <div className="page-container">
      <div className="page-header">
        <div>
          <h1 className="page-title">{title}</h1>
          {subtitle && (
            <p className="page-subtitle">{subtitle}</p>
          )}
        </div>
      </div>

      <div className="page-content">
        {children}
      </div>
    </div>
  );
}