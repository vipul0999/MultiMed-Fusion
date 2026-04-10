const AUTH_KEY = "ehr_portal_auth";

export function readStoredAuth() {
  const raw = sessionStorage.getItem(AUTH_KEY);
  if (!raw) {
    return null;
  }

  try {
    return JSON.parse(raw);
  } catch {
    sessionStorage.removeItem(AUTH_KEY);
    return null;
  }
}

export function writeStoredAuth(payload) {
  sessionStorage.setItem(AUTH_KEY, JSON.stringify(payload));
}

export function clearStoredAuth() {
  sessionStorage.removeItem(AUTH_KEY);
}
