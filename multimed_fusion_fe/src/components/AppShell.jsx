import { LogOut, Shield } from "lucide-react";

export function AppShell({ user, title, subtitle, navItems, activeTab, onTabChange, actions, children, onLogout }) {
  return (
    <div className="workspace-shell">
      <header className="workspace-topbar">
        <div className="workspace-sidebar__brand">
          <div className="workspace-logo">
            <Shield size={18} />
          </div>
          <div>
            <div className="workspace-sidebar__title">Aurelia EHR</div>
            <div className="workspace-sidebar__subtitle">Protected care environment</div>
          </div>
        </div>

        <div className="workspace-topbar__right">
          <div className="workspace-user workspace-user--compact">
            <div className="workspace-user__avatar">{user?.username?.slice(0, 1)?.toUpperCase() || "U"}</div>
            <div>
              <div className="workspace-user__name">{user?.username}</div>
              <div className="workspace-user__meta">{user?.role}</div>
            </div>
          </div>

          <button type="button" className="workspace-logout" onClick={onLogout}>
            <LogOut size={16} />
            <span>Sign out</span>
          </button>
        </div>
      </header>

      <div className="workspace-main">
        <header className="workspace-header">
          <div>
            <h1>{title}</h1>
            <p>{subtitle}</p>
          </div>
          <div className="workspace-header__actions">
            {actions}
          </div>
        </header>

        <nav className="workspace-nav workspace-nav--top">
          {navItems.map((item) => (
            <button
              key={item.id}
              type="button"
              className={`workspace-nav__button ${activeTab === item.id ? "is-active" : ""}`}
              onClick={() => onTabChange(item.id)}
            >
              <span className="workspace-nav__label">{item.label}</span>
              {item.badge ? <span className="workspace-nav__badge">{item.badge}</span> : null}
            </button>
          ))}
        </nav>

        <main className="workspace-content">
          {children}
        </main>
      </div>
    </div>
  );
}
