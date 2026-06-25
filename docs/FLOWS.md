# Major User Flows

This document outlines the primary user journeys in ProcurePro.

## 1) Signup & Onboarding

- User visits `/signup/`.
- User submits: email, password, confirm_password, company_name, license_number, phone, address, specialization, experience.
- Server validates password via Django validators and `procurement.validators.PasswordComplexityValidator`.
- If valid and email is unique, `User` is created with `role=CONTRACTOR` and a `ContractorProfile` is created.
- User is automatically logged in and redirected to `/dashboard/`.

## 2) Authentication (Signin / Logout)

- User visits `/signin/` and posts `email` + `password`.
- Rate-limited login endpoint (`django_ratelimit`) enforces `5/h` on POSTs.
- On success, `login()` is called and user is redirected depending on role (admin -> `/admin-dashboard/`, contractor -> `/dashboard/`).
- Logout uses `/logout/` and redirects to home.

## 3) Tender Discovery & Details

- Public users and authenticated users can view `/tenders/` which lists active tenders from the `Tender` model.
- Each tender detail page is `/tenders/<id>/details/` showing the tender description, budget, deadline, and attachments.

## 4) Request Tender (Contractors)

- Authenticated contractors can submit a formal tender request via `/request-tender/`.
- Submission includes metadata and an optional document upload which is validated by `validate_document_file()` in `views.py`.
- On submission, a `TenderRequest` entry is created and admins receive `Notification` entries linking to a review page.

## 5) Bidding Workflow

- On a tender detail page, contractors can submit a bid via `/tenders/<id>/submit/`.
- `Bid` records the amount, duration, proposal text and status (e.g., SUBMITTED, UNDER_REVIEW).
- Contractors can view their bids at `/my-bids/`.

## 6) Admin Review & Publishing

- Admins access `/admin-dashboard/` and related admin pages for posting and managing tenders.
- Admin actions create `Notification` instances for affected users.
- Admins can download tender documents and review `TenderRequest` entries.

## 7) Notifications

- Notifications are created in the `Notification` model and shown in the header dropdown.
- Users can mark individual notifications read at `/notifications/mark-read/<pk>/` or all read at `/notifications/mark-all-read/`.

## 8) File Uploads & Media

- Uploaded files go to `media/` and are kept in date-based folders for documents.
- Upload validation checks file size, extension, and content type. Ensure `media/` exists and is writable.

## Notes & Best Practices

- Password complexity and length policy is enforced; adjust `AUTH_PASSWORD_VALIDATORS` if needed.
- Rate-limiting protects login and request endpoints from brute force.
- Static assets are centralized under `static/` and should be collected for production with `collectstatic`.

