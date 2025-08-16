# Chhabra Billing (Go + React + Mongo + MinIO)

## Run
1. Copy repo files.
2. `docker compose up --build`
3. Frontend: http://localhost:5173  
   Backend:  http://localhost:8080/api/v1

Login with:
- **Email:** admin@chhabrafurniture.com
- **Password:** Admin@123

## Typical Flow
- Login → Create a bill → Open the bill → Generate PDF → Share public link or WhatsApp.

## Notes
- MinIO Console: http://localhost:9001 (cf_minio / cf_minio_secret)
- PDFs stored in bucket `invoices`.
- Change `.env` secrets for production.


```
chhabra-billing/
├─ docker-compose.yml
├─ README.md
├─ backend/
│  ├─ Dockerfile
│  ├─ go.mod
│  ├─ go.sum
│  ├─ cmd/server/main.go
│  ├─ internal/
│  │  ├─ config/config.go
│  │  ├─ db/mongo.go
│  │  ├─ models/bill.go
│  │  ├─ models/user.go
│  │  ├─ middleware/auth.go
│  │  ├─ repository/bill_repo.go
│  │  ├─ repository/user_repo.go
│  │  ├─ services/jwt.go
│  │  ├─ services/pdf.go
│  │  ├─ services/storage.go
│  │  ├─ handlers/auth_handler.go
│  │  ├─ handlers/bill_handler.go
│  │  ├─ routes/routes.go
│  │  └─ util/util.go
│  └─ assets/
│     ├─ fonts/NotoSans-Regular.ttf
│     └─ images/vishwakarma.png
└─ frontend/
   ├─ Dockerfile
   ├─ index.html
   ├─ package.json
   ├─ tsconfig.json
   ├─ vite.config.ts
   └─ src/
      ├─ main.tsx
      ├─ App.tsx
      ├─ api/client.ts
      ├─ auth/auth.ts
      ├─ components/BillForm.tsx
      ├─ components/ShareButtons.tsx
      ├─ pages/Login.tsx
      ├─ pages/BillsList.tsx
      ├─ pages/BillEditor.tsx
      ├─ pages/PublicShare.tsx
      ├─ i18n/index.ts
      ├─ i18n/locales/en/invoice.json
      ├─ i18n/locales/hi/invoice.json
      └─ styles.css
```
