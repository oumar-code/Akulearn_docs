---
template: home.html
---

# Akulearn Documentation Portal

This is the central portal for Akulearn architecture, platform operations, and product delivery across web, mobile, and classroom edge devices.

<div class="portal-grid">
  <section class="portal-card">
    <h3>Platform & Architecture</h3>
    <p>Read the full system map, deployment model, and service boundaries.</p>
    <div class="portal-links">
      <a class="md-button md-button--primary" href="ecosystem-map/">Ecosystem Map</a>
      <a class="md-button" href="01-architecture/">Architecture Docs</a>
    </div>
  </section>
  <section class="portal-card">
    <h3>Dashboard & Authentication</h3>
    <p>Access login flow, role mapping, and troubleshooting for Supabase auth.</p>
    <div class="portal-links">
      <a class="md-button md-button--primary" href="02-backend/platform_login/">Login Guide</a>
      <a class="md-button" href="02-backend/dashboard-login-troubleshooting/">Troubleshooting</a>
    </div>
  </section>
  <section class="portal-card">
    <h3>Mobile (Aku-Mobile)</h3>
    <p>Canonical Kotlin Multiplatform repo for Android + iOS delivery.</p>
    <div class="portal-links">
      <a class="md-button md-button--primary" href="https://github.com/oumar-code/Aku-Mobile" target="_blank" rel="noopener">Open Aku-Mobile</a>
      <a class="md-button" href="03-mobile/">Mobile Docs</a>
    </div>
  </section>
  <section class="portal-card">
    <h3>Classroom Smartboard</h3>
    <p>Desktop client migration target for smart TV/board deployments.</p>
    <div class="portal-links">
      <a class="md-button md-button--primary" href="https://github.com/oumar-code/Aku-Smartboard" target="_blank" rel="noopener">Open Aku-Smartboard</a>
      <a class="md-button" href="04-iot-projector/">IoT & Projector Docs</a>
    </div>
  </section>
</div>

## Current Ecosystem Reality

- **Frontend/Dashboard canonical source**: `akulearn-dashboard/` in this repository.
- **Mobile canonical source**: [Aku-Mobile](https://github.com/oumar-code/Aku-Mobile).
- **Smartboard canonical source**: [Aku-Smartboard](https://github.com/oumar-code/Aku-Smartboard) (migration in progress).

## Quick Start

1. Review [Ecosystem Map](ecosystem-map.md) for service ownership and status.
2. Use [Login & Dashboard Access](02-backend/platform_login.md) for auth routing and team dashboard mapping.
3. If login fails after magic link, follow [Dashboard Login Troubleshooting](02-backend/dashboard-login-troubleshooting.md).

<div class="portal-note">
  <strong>Need to debug login errors quickly?</strong> Check Supabase environment variables, redirect URLs, and callback behavior in the troubleshooting guide before changing app code.
</div>
