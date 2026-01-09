# Audit Log

Chronological record of significant work sessions.

---

## 2026-01-08 — Jebidiah Framework Setup

**Projects touched:** jebidiah
**Duration:** ~30 min

### What was done
- Cloned agentic_DrH from GitHub
- Renamed all "agentic" references to "jebidiah"
- Renamed folder from agentic_DrH to jebidiah
- Rewrote CLAUDE.md to define Chief of Staff identity
- Created _REGISTRY.md for project tracking
- Created _AUDIT.md (this file)

### Files changed
- CLAUDE.md (complete rewrite)
- _REGISTRY.md (new)
- _AUDIT.md (new)
- All .md files (agentic → jebidiah replacement)

### Next steps
- Review home-infrastructure project state
- Decide on GitHub repo rename (agentic_DrH → jebidiah)

---

## 2026-01-08 — CAPCOM v1.1 Deployment

**Projects touched:** capcom
**Duration:** ~2 hours

### What was done
- Imported real data from Excel consolidated report
  - 22 facilities, 85 sectors, 1472 TSCIFs, 21507 cabinets, 1201 customers
- Created enhanced dashboard with campus-level aggregation
- Added KPI stat cards with icons
- Added utilization gauge charts (GaugeChart.jsx)
- Added TSCIF status distribution pie chart
- Enhanced Facilities page with filtering/sorting
- Added health indicator components (HealthIndicator.jsx)
- Created dashboard API endpoint (/api/dashboard/summary)
- Deployed to Unraid at 10.69.2.45:5173
- Published to GitHub (joshewing02/capcom)

### Files changed
- backend/src/routes/dashboard.js (new)
- backend/src/utils/healthStatus.js (new)
- backend/prisma/importRealData.js (new)
- frontend/src/components/GaugeChart.jsx (new)
- frontend/src/components/HealthIndicator.jsx (new)
- frontend/src/pages/Dashboard.jsx (redesigned)
- frontend/src/pages/Facilities.jsx (enhanced)
- frontend/src/services/api.js (added dashboard call)
- frontend/src/components/Layout.jsx (v1.1)
- +12 other modified files

### Deployment details
- Backend: docker @ 10.69.2.45:3002
- Frontend: docker @ 10.69.2.45:5173
- Database: PostgreSQL @ 172.17.0.9:5432

### Next steps
- None specified — shipped and working

---

## 2026-01-08 — Home Infrastructure Documentation Update

**Projects touched:** home-infrastructure
**Duration:** ~30 min

### What was done
- Ran infrastructure collection scripts (update-docs.sh)
  - Unifi: Firmware 4.4.6, 116 DHCP leases
  - Unraid: v7.2.3, 14/17 docker containers, 2/5 VMs
  - Home Assistant: 2026.1.0, 12/13 add-ons, 59 automations
- Added CAPCOM stack to Unraid Docker documentation
  - capcom-frontend (5173)
  - capcom-backend (3002)
  - capcom-db (PostgreSQL 5432)
- Created detailed CAPCOM Stack section with properties and access info
- Committed and pushed changes to GitHub

### Files changed
- unraid/docker.md (added CAPCOM containers)
- scripts/update.log (collection run logs)

### Next steps
- Consider automating CAPCOM container detection in collection scripts
- Fill in empty VLAN and IP addressing documentation

---

## 2026-01-09 — CAPCOM v1.2 Data Quality & Customer Dashboard

**Projects touched:** capcom
**Duration:** ~3 hours

### What was done
- Fixed mobile web access (removed .env with hardcoded internal IP)
- Changed frontend from Vite dev server to nginx production build
- Changed "Committed" label to "Contracted" throughout Dashboard
- Created enhanced CustomerDetail page with drill-down to TSCIF level
  - Summary stat cards (Contracted, Committed, Installed, Peak, Cabinets, TSCIFs)
  - Expandable facilities list with sector breakdown
  - Full TSCIF table with navigation links
- Enhanced /api/customers/:id/summary endpoint
- Fixed importContractKw.js parsing issues:
  - Handle numeric facility prefixes (08.04.01A format)
  - Look for "Sold" labels in addition to "Contract"
  - Better fallback row detection
- Imported contract kW values from CAPCOM Excel files (338 TSCIFs updated)
- Updated SWAG proxy config from port 5173 to 3003

### Data Quality Investigation
**Root cause of "0 contract but installed > 0" issue:**
- 628 TSCIFs (42%) are "Shared" multi-tenant infrastructure
- These don't have individual contracts - contract is at cabinet/customer level
- CAPCOM files only contain contract data for primary/single-tenant TSCIFs
- This is correct business logic, not a bug

**Resolution:** Implemented "effectiveContract" calculation
- For shared TSCIFs with contract=0, aggregate whipKw from cabinet positions matching customer name
- Customer dashboard now shows "Allocated" (effectiveContract) instead of "Contracted"
- Example: 24 Hour Fitness went from "0 contract, 105 kW installed" to "89.9 kW allocated, 105 kW installed"

### Files changed
- backend/src/routes/customers.js (effectiveContract calculation + enhanced summary)
- backend/prisma/importContractKw.js (fixed parsing)
- frontend/src/pages/CustomerDetail.jsx (complete rewrite with Allocated display)
- frontend/src/pages/Dashboard.jsx (Committed → Contracted)
- frontend/Dockerfile (nginx production build)

### Deployment details
- Backend: docker @ 10.69.2.45:3002
- Frontend: docker @ 10.69.2.45:3003 (changed from 5173)
- External: https://capcom.ewingfam.net (via SWAG)

### Lessons learned
1. **Two-stage data import:** CAPCOM uses two import phases - importRealData.js (utilization) + importContractKw.js (contracts)
2. **Shared TSCIFs:** Multi-tenant TSCIFs have customerName="Shared" and no individual contract values
3. **CAPCOM file formats vary:** Different facilities use different ID formats (08.04.01A vs GRR01.01.01A)
4. **Production builds matter:** Vite dev server blocks external hosts; nginx production build works for mobile
5. **effectiveContract pattern:** For shared infrastructure, aggregate cabinet-level allocations to show meaningful customer totals

### Next steps
- Consider adding "Shared" indicator in UI for multi-tenant TSCIFs
- Document CAPCOM data model in project README

---

## Template

```markdown
## YYYY-MM-DD — Title

**Projects touched:** project1, project2
**Duration:** ~X hours

### What was done
- Item 1
- Item 2

### Files changed
- path/to/file.js (new/modified/deleted)

### Next steps
- What remains to be done
```
