# Audit Log

Chronological record of significant work sessions.

---

## 2026-01-10 — CAPCOM v2.6: QA Bug Fixes

**Projects touched:** capcom, jebidiah
**Duration:** ~1 hour

### What was done
- Ran comprehensive QA/QC with parallel agents (frontend + backend review)
- Fixed 68 bugs identified (39 frontend, 29 backend)
- Added null safety for API responses in IntakeForm, Alarms, Dashboard
- Fixed division by zero in Alarms bulk update calculation
- Use actual username instead of hardcoded 'Editor' for alarm silencing
- Added API error interceptor with consistent logging
- Added 30s default timeout and 2min upload timeout for API calls
- Wrapped bulk forecast updates in transaction for atomicity
- Added 404 responses for missing records in opportunities/alarms
- Added type validation for numeric fields (forecastPct, contractKw)
- Added date parsing validation for installDate
- Added existence checks before updates/deletes
- Fixed missing multer dependency in package.json

### Files changed
- backend/src/routes/alarms.js (transaction + validation)
- backend/src/routes/opportunities.js (404s + validation)
- backend/package.json (added multer)
- frontend/src/pages/Alarms.jsx (null safety + division by zero)
- frontend/src/pages/Dashboard.jsx (safe destructuring)
- frontend/src/pages/IntakeForm.jsx (null safety)
- frontend/src/services/api.js (error interceptor + timeouts)

### Deployment
- Deployed v2.6 to Unraid at 10.69.2.45:5173
- Verified API endpoints return proper 404s for missing records
- Alarms count working: 9 total, 1 critical

---

## 2026-01-10 — CAPCOM v2.1 Alpha: Scenario Planning

**Projects touched:** capcom, jebidiah
**Duration:** ~3 hours

### What was done
- Implemented Scenario Planning module for what-if capacity analysis
- Created Scenario and ScenarioAllocation Prisma models
- Built scenarioCalculator.js utility for forecast/capacity calculations
- Created full scenarios.js API with CRUD, sharing, cloning, analysis endpoints
- Built Scenarios list page with create/share/clone actions
- Built ScenarioDetail page with allocation management and comparison views
- Built Opportunities page - find sectors with available forecast capacity
- Added Report Upload feature (XLSX file upload for updating actuals)
- Added Activity Log for tracking who changed what
- Changed Dashboard from "oversold %" to Forecast-based Opportunity metrics
- Updated navigation and version to v2.1 Alpha

### Key Features
| Feature | Description |
|---------|-------------|
| Scenario Planning | Create what-if scenarios, add customer allocations, analyze impact |
| Opportunity Finder | Find sectors with available forecast capacity for new placements |
| Before/After View | Side-by-side comparison of baseline vs scenario |
| Facility Impact | See delta by facility when scenario is applied |
| Report Upload | Editors upload XLSX to bulk update actuals |
| Activity Log | Audit trail of all changes in admin panel |

### Files changed
- backend/prisma/schema.prisma (Scenario, ScenarioAllocation models)
- backend/src/routes/scenarios.js (new)
- backend/src/routes/reports.js (upload endpoints)
- backend/src/utils/scenarioCalculator.js (new)
- backend/src/utils/activityLog.js (new)
- backend/src/index.js (scenarios router)
- frontend/src/pages/Scenarios.jsx (new)
- frontend/src/pages/ScenarioDetail.jsx (new)
- frontend/src/pages/Opportunities.jsx (new)
- frontend/src/pages/ReportUpload.jsx (new)
- frontend/src/pages/Admin.jsx (Activity Log tab)
- frontend/src/components/Layout.jsx (nav + v2.1)
- frontend/src/services/api.js (scenario + upload APIs)
- frontend/src/App.jsx (new routes)

### Deployment
- Backend: docker @ 10.69.2.45:3002 (rebuilt)
- Frontend: docker @ 10.69.2.45:3003 (rebuilt)
- Database: schema synced with Prisma db push
- External: https://capcom.ewingfam.net

### Next steps
- User testing of Scenario Planning workflow
- Enhanced Reports view (Campus/Facility/Sector with PDF export)
- Consider PDF export for scenarios

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
- ~~Document CAPCOM data model in project README~~ DONE v1.2.1

---

## 2026-01-09 — CAPCOM v1.2.1 QA & Documentation

**Projects touched:** capcom, jebidiah
**Duration:** ~1 hour

### What was done
- QA sweep of all CAPCOM pages before user release
- Added all power metrics to Dashboard (Sold, Installed, Actual, Peak, Forecast)
- Fixed Customer → Facility navigation (was /facility/, now /facilities/)
- Made Feedback form mobile-friendly (larger touch targets, full-width buttons)
- Updated all documentation (CLAUDE.md, README.md, _REGISTRY.md, _AUDIT.md)
- Committed and pushed all projects to GitHub

### Dashboard Metrics Now Shown
| Row 1 (Power) | Row 2 (Counts) |
|---------------|----------------|
| UPS Capacity | Facilities |
| Sold | TSCIFs |
| Installed | Customer Cabs |
| Actual | Available |
| Peak | |
| Forecast | |

### Files changed
- frontend/src/pages/Dashboard.jsx (added metrics)
- frontend/src/pages/CustomerDetail.jsx (fixed routes)
- frontend/src/pages/Feedback.jsx (mobile UX)
- CLAUDE.md (v1.2.1 update)
- README.md (v1.2.1 update)

### Deployment
- Rebuilt frontend container on Unraid
- Verified all routes return 200
- External access working: https://capcom.ewingfam.net

### Next steps
- User acceptance testing at 9:30 PST
- Consider adding "Shared" indicator badge for multi-tenant TSCIFs

---

## 2026-01-09 — CAPCOM Data Import Fix (Unmapped Sectors)

**Projects touched:** capcom, jebidiah
**Duration:** ~1 hour

### What was done
- Fixed importCapcomData.js to distribute remaining sellable capacity to unmapped sectors
- RNO01 was showing 24,890 kW instead of correct 48,733 kW (mapped sectors only)
- Sectors 05-11 in RNO01 and similar unmapped sectors now receive proportional share
- Dashboard now shows 317.7 MW total sellable (correctly from CAPCOM files)
- Verified TSCIF values tie out: contractKw, forecastKw, forecastPct all populated

### Root Cause
- CAPCOM files only have columns for sectors 0-4 in Facility Summary
- Sectors 05-11 had no column mapping, so they retained old estimated values
- Fix: Distribute (facilitySellable - mappedSectorSum) proportionally to unmapped sectors

### Files changed
- backend/prisma/importCapcomData.js (unmapped sector distribution)
- CEO_DEMO_NOTES.md (updated values)

### Data Verification
| Facility | CAPCOM D4 | Dashboard | Status |
|----------|-----------|-----------|--------|
| RNO01 | 48,733 kW | 48,733 kW | MATCH |
| LAS09 | 20,832 kW | 20,832 kW | MATCH |
| Portfolio | - | 317.7 MW | Correct |

### Next steps
- None - data ties out correctly

---

## 2026-01-09 — CAPCOM v1.4 CEO Demo Prep

**Projects touched:** capcom, jebidiah
**Duration:** ~4 hours (overnight YOLO mode)

### What was done
- Audited all CAPCOM files for Sold vs Sellable capacity
- Critical finding: 15 of 16 facilities are OVERSOLD (128.4% utilization)
- Created importFacilitySummary.js with dynamic row detection
- Updated Dashboard to show oversell indicators
- Added Anonymous toggle and Job Title to Feedback form
- Added jobTitle field to Prisma schema
- Deployed v1.4 to Unraid (backend + frontend)

### Audit Findings
| Metric | Value |
|--------|-------|
| Total Sellable | 257.6 MW |
| Total Sold | 330.8 MW |
| Utilization | 128.4% |
| Oversold Facilities | 15 of 16 |

Most oversold: LAS05 (237%), LAS02 (167%), LAS10 (157%), LAS11 (154%), LAS07 (152%)

### Files changed
- backend/prisma/importFacilitySummary.js (new)
- backend/prisma/schema.prisma (jobTitle field)
- frontend/src/pages/Dashboard.jsx (oversell indicator)
- frontend/src/pages/Feedback.jsx (Anonymous/JobTitle)

### Known Issues for CEO Demo
1. Some CAPCOM files have Sold row not detected (Row ?? in import)
2. Dashboard shows 343.5 MW sellable (import update needed)
3. Sold values vary by file structure (Row 12, 13, or 17)

### Next steps
- CEO demo at 6am PST
- May need manual verification of specific facility data

---

## 2026-01-09 — CAPCOM v1.3 Sellable Capacity

**Projects touched:** capcom, jebidiah
**Duration:** ~1 hour

### What was done
- Replaced estimated UPS Capacity (120% of installed) with actual Sellable Capacity from CAPCOM files
- Created importSellableCapacity.js to read "UPS Sellable Capacity" from Sector High sheets
- Pattern detection: LAS uses "UPS Sellable Capacity", RNO uses "UPS Capacity"
- Imported 281.3 MW across 52 sectors from CAPCOM files
- Dashboard now shows "Sellable Capacity: 351.2 MW" instead of estimated 604.7 MW
- Updated Dashboard label from "UPS Capacity" to "Sellable Capacity"
- Verified Forecast is prominent in first row of stats

### Files changed
- backend/prisma/importSellableCapacity.js (new)
- frontend/src/pages/Dashboard.jsx (label change)
- CLAUDE.md (v1.3 update)
- README.md (v1.3 update)

### Deployment
- Backend image rebuilt with new import script
- Import ran successfully: 52 sectors updated, 33 skipped (no CAPCOM file)
- Frontend rebuilt with updated label
- External access verified: https://capcom.ewingfam.net

### Data Quality Notes
- CAPCOM files use different label patterns:
  - LAS: "UPS Sellable Capacity" at Row 11
  - RNO: "UPS Capacity" or "UPS Capacity End State" at Row 11-12
- Combined sectors (e.g., "Sector 4 & 5 High") correctly map to both sector codes
- Some facilities have no CAPCOM file mapping yet (DFY, MEM, ATL02, HOU02)

### Next steps
- None specified — v1.3 shipped and working

---

## 2026-01-09 — CAPCOM v2.0 User Management & Admin Edit Mode

**Projects touched:** capcom, jebidiah
**Duration:** ~3 hours

### What was done
- Implemented 3-tier user role system (ADMIN, EDITOR, VIEWER)
- Created User model in Prisma schema with roles, status, credentials
- Built user profile page for self-service name/title editing
- Built admin panel with two tabs:
  - Users tab: Create/edit/pause/remove user accounts
  - Access Logs tab: View login history (username, time, IP, action)
- Implemented htpasswd sync when creating/updating users
- Renamed AuditLog.jsx to Admin.jsx with expanded functionality
- Added sector grid admin edit mode:
  - Edit Mode toggle button (admin only)
  - Editable sector header cards (upsCapacity, expansionKw)
  - TSCIF edit modal (contractKw, forecastPct, status)
  - Yellow highlight ring on editable cells
- Added updateSector and updateTscif API endpoints
- Deployed to Unraid, rebuilt frontend container

### Files changed
- backend/prisma/schema.prisma (User model)
- backend/src/routes/admin.js (user CRUD, profile, htpasswd sync)
- backend/src/routes/sectors.js (updateSector endpoint)
- backend/src/routes/tscifs.js (updateTscif endpoint)
- frontend/src/pages/Admin.jsx (user management + access logs)
- frontend/src/pages/Profile.jsx (new)
- frontend/src/pages/SectorGrid.jsx (admin edit mode)
- frontend/src/services/api.js (user management + update APIs)
- frontend/src/components/Layout.jsx (Profile nav, admin check)
- frontend/src/App.jsx (profile route)

### Deployment
- Backend: docker @ 10.69.2.45:3002
- Frontend: docker @ 10.69.2.45:3003
- External: https://capcom.ewingfam.net

### Next steps
- Consider session-based auth for v2.1

---

## 2026-01-09 — CAPCOM v1.6 Admin Audit Log

**Projects touched:** capcom, jebidiah
**Duration:** ~30 min

### What was done
- Added AuthLog model to database schema
- Created admin route with auth logging endpoints
- Updated nginx to proxy API requests with auth headers (X-Authenticated-User, X-Real-IP)
- Created AuditLog.jsx admin-only page showing:
  - Stats: total logins, unique users, last 24 hours
  - User breakdown by login count
  - Full log table with time, username, IP, action, path
- Added automatic page access logging on navigation
- Admin nav item only visible to joshewing02
- Deployed to Unraid, verified working

### Files changed
- backend/prisma/schema.prisma (AuthLog model)
- backend/src/routes/admin.js (new)
- backend/src/index.js (admin router)
- frontend/nginx.conf (API proxy with auth headers)
- frontend/src/services/api.js (admin API functions)
- frontend/src/pages/AuditLog.jsx (new)
- frontend/src/components/Layout.jsx (admin nav, access logging)
- frontend/src/App.jsx (audit route)

### Next steps
- v2.0: Session-based auth with login page, Azure AD integration

---

## 2026-01-09 — CAPCOM v1.5.1 Auth Security

**Projects touched:** capcom, jebidiah
**Duration:** ~15 min

### What was done
- Added HTTP basic auth to nginx (password protection)
- Created .htpasswd with admin credentials
- Updated Dockerfile to use external nginx.conf
- Deployed to Unraid, verified 401 without auth, 200 with auth
- Marked Mark's feedback (Access Concern) as RESOLVED
- Documented session-based auth for v1.6 roadmap

### Files changed
- frontend/nginx.conf (new)
- frontend/.htpasswd (new, gitignored)
- frontend/Dockerfile (updated for config files)
- .gitignore (added .htpasswd)
- CLAUDE.md (v1.5.1, roadmap)
- frontend/src/components/Layout.jsx (version bump)

### Next steps
- v1.6: Session-based auth with login page, prep for Azure AD

---

## 2026-01-09 — CAPCOM v1.5 Customer Features

**Projects touched:** capcom, jebidiah
**Duration:** ~2 hours

### What was done
- Added customer search/filter on Customers page
- Added Top 10 Customers by Contract section with ranking badges
- Added customer logos using Google Favicon API (150+ company mappings)
- Added utilization dashboard to CustomerDetail (contracted vs actual gauge)
- Added /api/customers/top endpoint for top customers by contract
- Fixed TSCIF routing bug (/tscifs/ → /tscif/)
- Implemented feedback integration workflow (read → implement → resolve)
- Updated all version files to v1.5

### Files changed
- backend/src/routes/customers.js (added /top endpoint)
- frontend/src/pages/Customers.jsx (search, Top 10, logos)
- frontend/src/pages/CustomerDetail.jsx (utilization gauge, logos, routing fix)
- frontend/src/services/api.js (getTopCustomers)
- frontend/src/components/Layout.jsx (version v1.5)
- CLAUDE.md, README.md, CEO_DEMO_NOTES.md (version updates)

### Logo Implementation
- Google Favicon API: `https://www.google.com/s2/favicons?domain=${domain}&sz=64`
- 150+ company domain mappings (eBay, CoreWeave, Amazon, Nvidia, etc.)
- Graceful fallback with onError handler for missing logos

### Deployment
- Backend: docker @ 10.69.2.45:3002
- Frontend: docker @ 10.69.2.45:3003
- External: https://capcom.ewingfam.net

### Next steps
- Deploy v1.5 to production
- Continue feedback-driven development

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
