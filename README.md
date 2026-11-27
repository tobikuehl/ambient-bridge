# ambient-bridge
**A privacy-preserving ("Local-First"), zero-config bridge between local AI documentation pipelines (such as [`local-ambient-scribe`](https://github.com/tobikuehl/local-ambient-scribe)) and closed, browser-based Electronic Health Records (EHRs) without open write APIs (e.g., Lemniscus).**

---

## 1. Problem Statement & Civic Tech Value
Small practices, therapists, and social care providers face a structural interoperability bottleneck:

+ **Privacy vs. Automation:** Sensitive patient and client records must not be sent to external cloud AI services under GDPR and medical confidentiality laws (§ 203 StGB). While local open-source AI pipelines solve data sovereignty, practitioners still hit a workflow wall when transferring notes into their practice software.
+ **Closed Web EHRs (Vendor Lock-in):** Many widely used web-based practice management systems (such as *Lemniscus*) do not provide an open REST API for writing clinical progress notes.
+ **Cross-Platform Friction:** Workarounds like browser extensions or cloud clipboards are insecure, fragile, or fail across mixed practice hardware (Linux/Windows/macOS at the front desk, iPads/Android tablets in treatment rooms).

**Solution:** `ambient-bridge` closes this gap with a **maintenance-free, local Progressive Web App (PWA)** featuring **mDNS auto-discovery**, **automated local TLS**, and explicit **Human-in-the-Loop** verification—without cloud dependencies, browser plugins, or manual client configuration files.

---

## 2. System Architecture (Zero-Config & Multi-Platform)

```text
+-----------------------------------------------------------------------+

|  Local Practice Mini-PC (Docker Host, 100% Offline-Capable)           |
|                                                                       |
|  [ local-ambient-scribe ]  (Local ASR + Diarization + LLM)            |
|            |                                                          |
|            v  POST /api/drafts (Local Webhook)                        |
|  [ FastAPI Backend ]  <--->  [ mDNS / Zeroconf Announcer ]            |
|            |                   ("https://ambient-bridge.local")       |
|            v                                                          |
|  [ Caddy Reverse Proxy ] (Automated Local TLS for Mobile Clipboard)   |
+------------|----------------------------------------------------------+
             |
             |  Local Practice LAN / Wi-Fi (HTTPS)
             +-----------------------------+

             |                             |
             v                             v
+-------------------------+   +-----------------------------------------+

|  Tablets (iPad/Android) |   |  Desktops (Linux KDE/GNOME, Win, macOS) |
|                         |   |                                         |
|  PWA in Split-Screen    |   |  PWA + Optional Desktop Auto-Paste      |
|  1. Review AI draft     |   |  1. Click "Review & Copy"               |
|  2. 1-Tap Copy          |   |  2. Focus switch -> Browser (Web EHR)   |
|  3. Paste into Web EHR  |   |  3. Auto-paste (Wayland/X11/Win/macOS)  |
+-------------------------+   +-----------------------------------------+
```

### Core Components
1. **Local-First Backend (`backend/main.py`):** Receives structured Markdown drafts from local AI pipelines via a local webhook and manages the practitioner review queue.
2. **Zero-Config Discovery (`backend/mdns.py`):** Announces the service automatically via Zeroconf/mDNS (`ambient-bridge.local`) on the local network so client devices require zero IP configuration.
3. **Local TLS (`Caddyfile`):** Provides an internal HTTPS endpoint—required by mobile browsers (Safari on iPadOS, Chrome/Firefox on Android) to unlock the Web Clipboard API (`navigator.clipboard.writeText`).
4. **Cross-Platform PWA (`backend/static/`):** Installable web interface designed for tablet split-screen workflows with mandatory human review before transfer.
5. **Optional Desktop Helper (`desktop-helper/auto_paste.py`):** Lightweight background helper for desktop workstations that switches focus back to the active browser window and triggers paste upon approval (designed to support Linux Wayland via `ydotool`/`wtype` as well as X11, Windows, and macOS).

---

## 3. Quick Start (Prototype Stub)

Prerequisites: Docker and Docker Compose on the local host.

```bash
git clone https://github.com
cd ambient-bridge
docker compose up --build
```

Open in your browser (on desktop or tablet within the same local network):
* `https://ambient-bridge.local` (or `https://localhost` on the host machine)

### Simulate Incoming Draft from `local-ambient-scribe`
```bash
chmod +x demo_push.sh
./demo_push.sh
```

---

## 4. Prototype Fund Roadmap
+ **Milestone 1 – Zero-Friction Device Pairing:** One-time QR-code onboarding flow for practice tablets, including guided local root-CA trust setup for seamless HTTPS without certificate warnings.
+ **Milestone 2 – Cross-Platform Desktop Daemon:** Packaging the optional auto-paste helper as a standalone binary (Linux AppImage/Flatpak with native Wayland `ext-data-control` / `ydotool` support, Windows, macOS).
+ **Milestone 3 – Multi-Field Mapping & Clipboard Auto-Wipe:** Sequential clipboard staging for multi-field web forms (e.g., history, diagnosis, billing codes) with automatic clipboard clearing after paste (*Auto-Wipe*).
+ **Milestone 4 – Clinical Pilot & Documentation:** Real-world evaluation in independent therapeutic practices and release as a reusable open-source reference architecture.

---

## Related Project
+ **[`local-ambient-scribe`](https://github.com/tobikuehl/local-ambient-scribe):** Modular, local-first ambient documentation pipeline generating the structured drafts consumed by `ambient-bridge`.

## License
AGPL-3.0 (aligned with `local-ambient-scribe`).
