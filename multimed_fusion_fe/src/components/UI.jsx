export function SectionCard({ title, subtitle, actions, children, className = "" }) {
  return (
    <section className={`section-card ${className}`}>
      <div className="section-card__header">
        <div>
          <h2>{title}</h2>
          {subtitle ? <p>{subtitle}</p> : null}
        </div>
        {actions ? <div className="section-card__actions">{actions}</div> : null}
      </div>
      {children}
    </section>
  );
}

export function StatCard({ label, value, detail }) {
  return (
    <article className="stat-card">
      <span>{label}</span>
      <strong>{value}</strong>
      {detail ? <p>{detail}</p> : null}
    </article>
  );
}

export function StatusBadge({ tone = "neutral", children }) {
  return <span className={`status-badge status-badge--${tone}`}>{children}</span>;
}

export function EmptyState({ title, description }) {
  return (
    <div className="empty-state">
      <h3>{title}</h3>
      <p>{description}</p>
    </div>
  );
}

export function DataRow({ title, subtitle, actions, meta }) {
  return (
    <div className="data-row">
      <div className="data-row__content">
        <div className="data-row__title">{title}</div>
        {subtitle ? <div className="data-row__subtitle">{subtitle}</div> : null}
        {meta ? <div className="data-row__meta">{meta}</div> : null}
      </div>
      {actions ? <div className="data-row__actions">{actions}</div> : null}
    </div>
  );
}
