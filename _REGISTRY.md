# Project Registry

Central index of all projects under management.

---

## Active Projects

### capcom
| Field | Value |
|-------|-------|
| **Path** | `D:\github repositories\capcom` |
| **GitHub** | https://github.com/joshewing02/capcom (private) |
| **Purpose** | Switch data center capacity planning & commitment management |
| **Tech** | React + Vite + Tailwind, Node/Express, PostgreSQL, Prisma |
| **Deployed** | Unraid @ http://10.69.2.45:3003 (external: https://capcom.ewingfam.net) |
| **Version** | v1.2 |
| **Status** | Deployed, operational |
| **Last Touched** | 2026-01-09 |

**Quick Context:**
- 22 facilities, 85 sectors, 1495 TSCIFs, 338 with contract data
- Dashboard with campus views, "Contracted" KPI (84.6 MW total)
- Customer detail page with facility drill-down to TSCIF level
- Production nginx build (was Vite dev server)
- Backend API at port 3002, frontend at port 3003

**Data model notes:**
- 42% of TSCIFs are "Shared" (multi-tenant) with no individual contract
- Two import phases: importRealData.js (utilization) + importContractKw.js (contracts)

---

### home-infrastructure
| Field | Value |
|-------|-------|
| **Path** | `D:\github repositories\home-infrastructure` |
| **GitHub** | TBD |
| **Purpose** | Home lab infrastructure documentation — single source of truth |
| **Tech** | Markdown documentation, shell scripts |
| **Deployed** | N/A (documentation repo) |
| **Status** | Active |
| **Last Touched** | 2026-01-08 |

**Quick Context:**
- Documents Unifi (UDM-Pro @ 10.69.1.1), Unraid (10.69.2.45), Home Assistant (10.69.2.40)
- Contains: networking/, unraid/, unifi/, home-assistant/, swag/, scripts/
- SSH key: `~/.ssh/id_ed25519` (ed25519, on all systems)
- Security: Uses `[REDACTED]` placeholders for secrets

---

### jebidiah
| Field | Value |
|-------|-------|
| **Path** | `D:\github repositories\jebidiah` |
| **GitHub** | https://github.com/joshewing02/agentic_DrH (to be renamed) |
| **Purpose** | Chief of Staff framework — orchestration identity |
| **Tech** | Markdown documentation |
| **Status** | Active, being configured |
| **Last Touched** | 2026-01-08 |

**Quick Context:**
- Defines Claude's identity as Chief of Staff
- Tracks all projects, maintains audit log
- Renamed from "agentic" to "jebidiah"

---

## Project Status Legend

| Status | Meaning |
|--------|---------|
| **Deployed** | Live and operational |
| **Active** | Under development |
| **Paused** | On hold, has context saved |
| **Archived** | Complete, no active work |

---

## Adding New Projects

When a new project is created:
1. Add entry to this registry
2. Create `CLAUDE.md` in project root with context
3. Log creation in `_AUDIT.md`
4. Update main `CLAUDE.md` projects table
