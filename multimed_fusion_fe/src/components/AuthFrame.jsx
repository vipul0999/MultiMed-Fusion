import { Activity, ShieldCheck, Stethoscope } from "lucide-react";
import { Link } from "react-router-dom";

export function AuthFrame({ eyebrow, title, subtitle, children, footerText, footerLink, footerLabel }) {
  return (
    <div className="auth-shell">
      <section className="auth-panel auth-panel--brand">
        <div className="brand-mark">
          <div className="brand-mark__icon">
            <Stethoscope size={20} />
          </div>
          <div>
            <div className="brand-mark__title">Aurelia EHR</div>
            <div className="brand-mark__subtitle">Clinical intelligence and patient records</div>
          </div>
        </div>

        <div className="auth-hero">
          <span className="eyebrow">{eyebrow}</span>
          <h1>{title}</h1>
          <p>{subtitle}</p>
        </div>
        <div className="auth-notes">
          <div className="auth-note"><ShieldCheck size={16} /><span>Secure sign-in with role-based routing</span></div>
          <div className="auth-note"><Activity size={16} /><span>Doctor, patient, and admin workflows</span></div>
        </div>
      </section>

      <section className="auth-panel auth-panel--form">
        {children}

        <div className="auth-footer">
          <span>{footerText}</span>
          <Link to={footerLink}>{footerLabel}</Link>
        </div>
      </section>
    </div>
  );
}
