/* eslint-disable react-refresh/only-export-components */
import { createContext, useCallback, useContext, useEffect, useMemo, useState } from "react";

import { configureAuthBridge } from "../api/client";
import { authService } from "../api/services";
import { clearStoredAuth, readStoredAuth, writeStoredAuth } from "../lib/storage";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [session, setSession] = useState(() => readStoredAuth());
  const [booting, setBooting] = useState(true);

  useEffect(() => {
    if (!booting) {
      return undefined;
    }

    let active = true;

    async function boot() {
      if (!session?.access || !session?.refresh) {
        if (active) {
          setBooting(false);
        }
        return;
      }

      try {
        const user = await authService.me();
        const nextSession = { ...session, user };
        if (active) {
          setSession(nextSession);
          writeStoredAuth(nextSession);
        }
      } catch {
        if (active) {
          clearStoredAuth();
          setSession(null);
        }
      } finally {
        if (active) {
          setBooting(false);
        }
      }
    }

    void boot();
    return () => {
      active = false;
    };
  }, [booting, session]);

  async function login(credentials) {
    const authPayload = await authService.login(credentials);
    const nextSession = {
      access: authPayload.access,
      refresh: authPayload.refresh,
      user: authPayload.user,
    };
    setSession(nextSession);
    writeStoredAuth(nextSession);
    return nextSession.user;
  }

  async function register(payload) {
    return authService.register(payload);
  }

  const refreshSession = useCallback(async () => {
    if (!session?.refresh) {
      return null;
    }

    const refreshed = await authService.refresh(session.refresh);
    const nextSession = {
      ...session,
      access: refreshed.access,
    };
    setSession(nextSession);
    writeStoredAuth(nextSession);
    return refreshed.access;
  }, [session]);

  function logout() {
    clearStoredAuth();
    setSession(null);
  }

  useEffect(() => {
    configureAuthBridge({
      getAccessToken: () => session?.access ?? null,
      getRefreshToken: () => session?.refresh ?? null,
      refreshSession,
      clearSession: logout,
    });
  }, [session, refreshSession]);

  const value = useMemo(
    () => ({
      booting,
      session,
      user: session?.user ?? null,
      login,
      register,
      logout,
      refreshSession,
      setSession,
    }),
    [booting, session, refreshSession],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used inside AuthProvider");
  }
  return context;
}
