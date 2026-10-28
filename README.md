# MediBook Clinic Appointments — Test III & IV
Student: Angel Erica L. Uanang | BSIT-4 | October 28, 2026

## Setup
1. `python -m venv .venv`
2. Activate the environment.
3. `pip install -r requirements.txt`
4. `python manage.py migrate`
5. `python manage.py loaddata sample_data`
6. `python manage.py runserver`
7. Open `http://127.0.0.1:8000/`.

## Main routes
- `/` — Doctor Directory
- `/doctors/<id>/` — Doctor Detail
- `/doctors/<id>/book/` — Appointment Booking
- `/appointments/<id>/confirmation/` — Appointment Confirmation
- `/manage/doctors/` — Doctor Management
- `/manage/doctors/new/` — Add Doctor / DoctorForm
- `/manage/appointments/` — Appointment Management

## Hosting choices
HTMX 2.0.4 and Alpine.js 3.14.9 are pinned CDN builds in `base.html`. This keeps the exam project build-free and reproducible because the project does not require Node, npm, or a bundler before it can run. For an offline deployment, both libraries can be copied into `static/js/` without changing the overall Django + HTMX + Alpine architecture.

## Sample data
`clinic/fixtures/sample_data.json` contains sample specialties, six doctors, and sample appointments. Sample doctor images are included under `media/doctors/`, so the fixture can be loaded immediately after migration.

## Alpine components and where each is used
| Alpine component / store | Page where it is used | Purpose |
| --- | --- | --- |
| Inline mobile menu state (`open`) | All pages through `base.html` | Opens/closes the responsive navigation and reacts to Escape/outside click. |
| `directory()` | Doctor Directory (`/`) | Search helper state, grid/list preference, and HTMX loading state. |
| `tabs()` | Doctor Detail (`/doctors/<id>/`) | Controls About, Fees, and Availability tabs. |
| `bookingWizard()` | Appointment Booking (`/doctors/<id>/book/`) | Controls the 3-step wizard, selected date/slot/visit, reason counter, and persisted step. |
| `management()` | Appointment Management (`/manage/appointments/`) | Controls client-side status tabs and selected appointment rows. |
| `theme` store | All pages through `base.html` | Shared light/dark presentation preference stored in `localStorage`. |
| `toasts` store | All pages through `base.html` | Shared temporary notifications triggered by client or HTMX events. |

## State map
| State | Owner | Scope | Persistence / reason |
| --- | --- | --- | --- |
| Mobile menu `open` | Alpine | Local | Temporary; belongs only to the navigation instance. |
| Directory `query`, `grid`, `loading` | Alpine | Local component | `grid` may persist in `localStorage`; loading/query are temporary UI state. |
| Doctor-detail `tab` | Alpine | Local component | Temporary selected tab only. |
| Booking `step`, `date`, `slot`, `visit`, `reason` | Alpine | Local component | Wizard step may persist in `sessionStorage`; these values are only the in-progress UI state. |
| Theme preference | Alpine store | Shared | Persisted in `localStorage` because it is a user presentation preference. |
| Toast items | Alpine store | Shared | Temporary; removed automatically after display. |
| Doctors, appointments, validation, slot conflicts | Django/server | Server-owned | Must remain authoritative on the server/database and must not be trusted to Alpine. |

## Alpine + HTMX integration points
1. The Doctor Directory listens to `htmx:before-request` and `htmx:after-request` while HTMX replaces `#doctor-grid`; Alpine controls the loading indicator and view preference only.
2. Appointment date selection uses HTMX to request refreshed slot HTML from Django, while Alpine only tracks the currently selected client-side slot state.
3. Appointment booking uses `hx-post`; failed Django validation re-renders the form, while successful booking returns `HX-Redirect` and `HX-Trigger` for navigation and toast feedback.
4. Appointment confirm/cancel actions use HTMX to replace only the affected table row, while Alpine keeps the management status filter and selected-row state outside the swapped row.
5. Django supplies CSRF protection through `{% csrf_token %}` in POST forms, so Alpine does not bypass server security or validation.

## Architecture note
Django owns saved doctors, appointments, validation, conflicts, and server-rendered lists. HTMX exchanges server-generated HTML fragments. Alpine owns temporary interface state only; it does not become a second database or source of truth.

## Repository
https://github.com/AngelEricaUanang/UANANG_SF_EXAM_TESTIIIandIV
