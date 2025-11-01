import React from 'react';
import ZamfaraNetworkMap from './components/ZamfaraNetworkMap';

export default function App() {
  return (
    <div className="app-root">
      <header className="app-header">
        <h1 className="brand">Aku Workspace</h1>
        <nav className="topnav">
          <button className="icon-btn">☰</button>
        </nav>
      </header>

      <main className="content">
        <section className="panel">
          <h2>Workspace Dashboard</h2>
          <p className="muted">Mobile-first, responsive PWA shell — demo components below.</p>
        </section>

        <section className="panel map-panel">
          <h3>Network Map</h3>
          <ZamfaraNetworkMap />
        </section>

      </main>

      <footer className="app-footer">
        <small>© Aku Platform</small>
      </footer>
    </div>
  );
}
