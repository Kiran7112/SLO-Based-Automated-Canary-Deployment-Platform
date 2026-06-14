package main

import (
	"net/http"
	"net/http/httptest"
	"testing"
)

func TestCheckoutHealthy(t *testing.T) {
	srv := newServer(config{version: "test", errorRate: 0})
	rec := httptest.NewRecorder()
	req := httptest.NewRequest(http.MethodPost, "/checkout", nil)

	srv.routes().ServeHTTP(rec, req)

	if rec.Code != http.StatusOK {
		t.Fatalf("expected 200, got %d", rec.Code)
	}
}

func TestCheckoutAlwaysFails(t *testing.T) {
	srv := newServer(config{version: "canary", errorRate: 1.0})
	rec := httptest.NewRecorder()
	req := httptest.NewRequest(http.MethodPost, "/checkout", nil)

	srv.routes().ServeHTTP(rec, req)

	if rec.Code != http.StatusInternalServerError {
		t.Fatalf("expected 500 with error_rate=1.0, got %d", rec.Code)
	}
}

func TestReadyz(t *testing.T) {
	srv := newServer(config{version: "test"})
	rec := httptest.NewRecorder()
	req := httptest.NewRequest(http.MethodGet, "/readyz", nil)

	srv.routes().ServeHTTP(rec, req)

	if rec.Code != http.StatusOK {
		t.Fatalf("expected ready 200, got %d", rec.Code)
	}
}
