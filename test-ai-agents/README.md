# Invoice Generating Application

Full-stack app with Golang (Gin), MongoDB, and React (Vite + Tailwind).

## Features
- JWT auth (register/login)
- Invoice CRUD, date-range search
- PDF export (server-side)
- WhatsApp share stub (extend with provider)

## Quick Start

1) Prereqs: Docker + Docker Compose.

2) Start stack:
```
docker compose up -d --build
```

3) Open frontend: http://localhost:5173

4) Register then Login. Create invoices and export PDFs.

## Services
- Backend: http://localhost:8080
- Frontend: http://localhost:5173
- MongoDB: mongodb://localhost:27017 (container `mongo`)

## Env Vars
- Backend
  - `APP_ENV` (default: development)
  - `PORT` (default: 8080)
  - `MONGO_URI` (default: mongodb://mongo:27017)
  - `MONGO_DB` (default: invoice_app)
  - `JWT_SECRET` (default: dev-secret)
- Frontend
  - `VITE_API_BASE` (default: http://localhost:8080)

## Development (optional)

Backend:
```
cd backend
go run ./cmd/server
```

Frontend:
```
cd frontend
npm install
npm run dev
```


