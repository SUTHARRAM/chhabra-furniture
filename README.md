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
