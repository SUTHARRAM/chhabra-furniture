FROM golang:1.22 AS build
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 go build -o server ./cmd/server

FROM gcr.io/distroless/base-debian12
WORKDIR /app
COPY --from=build /app/server /app/server
COPY assets /app/assets
COPY .env /app/.env
EXPOSE 8080
USER 65532:65532
ENTRYPOINT ["/app/server"]
