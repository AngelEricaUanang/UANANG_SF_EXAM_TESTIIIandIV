# MediBook Clinic Appointments — Test III & IV
Student: Angel Erica L. Uanang | BSIT-4 | October 28, 2026

## Setup
1. `python -m venv .venv`
2. Activate the environment.
3. `pip install -r requirements.txt`
4. `python manage.py makemigrations && python manage.py migrate`
5. Add sample specialties/doctors in the Django shell or admin.
6. `python manage.py runserver`

## Hosting choices
HTMX 2.0.4 and Alpine.js 3.14.9 are pinned CDN builds in `base.html` to keep the exam project build-free and reproducible. For an offline deployment they can be copied into `static/js/` without changing the architecture.

## Alpine components
- `directory()` — doctor directory search helper, loading state, view preference.
- `tabs()` — doctor detail tabs.
- `bookingWizard()` — 3-step booking flow, counter, summary, persisted step.
- `management()` — appointment status UI and bulk selection.
- `theme` store — shared persisted theme.
- `toasts` store — shared notifications.

## Alpine + HTMX integration points
1. Directory listens to `htmx:before-request` / `htmx:after-request` while HTMX swaps `#doctor-grid`.
2. Appointment date uses HTMX to replace slot HTML; Alpine owns only the selected client-side slot state.
3. Booking uses `hx-post`; validation errors replace the form while successful responses use `HX-Redirect` and `HX-Trigger` for a toast.
4. Appointment row actions use HTMX to swap only the changed `<tr>` while Alpine keeps management filters outside the swap.
5. CSRF is supplied by Django's `{% csrf_token %}` in POST forms.

## Architecture note
Django owns saved doctors, appointments, validation, conflicts, and server-rendered lists. HTMX exchanges server HTML. Alpine owns temporary interface state only.
