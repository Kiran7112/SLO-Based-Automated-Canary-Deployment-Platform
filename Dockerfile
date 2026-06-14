# syntax=docker/dockerfile:1
# ---- build stage ---------------------------------------------------------
FROM golang:1.22-alpine AS build
WORKDIR /src

# Cache dependencies first for faster rebuilds. go.sum is resolved on the fly
# (-mod=mod) so the repo stays buildable even before a go.sum is committed.
COPY app/go.mod ./
RUN go mod download || true

COPY app/ ./
# Static, stripped binary so it runs in a distroless/scratch image.
RUN CGO_ENABLED=0 GOOS=linux go build -mod=mod -trimpath -ldflags="-s -w" -o /out/checkout .

# ---- runtime stage -------------------------------------------------------
FROM gcr.io/distroless/static-debian12:nonroot
WORKDIR /
COPY --from=build /out/checkout /checkout

# Run as the built-in non-root user from distroless.
USER nonroot:nonroot
EXPOSE 8080
ENV LISTEN_ADDR=":8080" VERSION="stable"
ENTRYPOINT ["/checkout"]
