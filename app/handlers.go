package main

import (
	"encoding/json"
	"math/rand"
	"net/http"
	"strconv"
	"time"
)

// server wires the config and the HTTP routes together.
type server struct {
	cfg   config
	ready bool
}

func newServer(cfg config) *server {
	appInfo.WithLabelValues(cfg.version).Set(1)
	return &server{cfg: cfg, ready: true}
}

func (s *server) routes() http.Handler {
	mux := http.NewServeMux()
	mux.HandleFunc("/checkout", s.instrument("/checkout", s.handleCheckout))
	mux.HandleFunc("/healthz", s.handleHealthz)
	mux.HandleFunc("/readyz", s.handleReadyz)
	return mux
}

// instrument wraps a handler so every response feeds the latency histogram and
// the request counter — the raw signals the SLO gates are computed from.
func (s *server) instrument(route string, next http.HandlerFunc) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		start := time.Now()
		rec := &statusRecorder{ResponseWriter: w, status: http.StatusOK}
		next(rec, r)
		httpRequestDuration.WithLabelValues(route, r.Method).Observe(time.Since(start).Seconds())
		httpRequestsTotal.WithLabelValues(route, r.Method, strconv.Itoa(rec.status)).Inc()
	}
}

// handleCheckout simulates processing a payment. ERROR_RATE and EXTRA_LATENCY_MS
// let a release misbehave on demand so the canary analysis can react.
func (s *server) handleCheckout(w http.ResponseWriter, r *http.Request) {
	if s.cfg.extraLatency > 0 {
		time.Sleep(time.Duration(s.cfg.extraLatency) * time.Millisecond)
	}

	paymentAttempts.Inc()

	if rand.Float64() < s.cfg.errorRate {
		http.Error(w, `{"status":"error","reason":"payment_failed"}`, http.StatusInternalServerError)
		return
	}

	paymentSuccess.Inc()
	writeJSON(w, http.StatusOK, map[string]string{
		"status":  "ok",
		"version": s.cfg.version,
		"order":   "ORD-" + time.Now().Format("150405.000"),
	})
}

func (s *server) handleHealthz(w http.ResponseWriter, _ *http.Request) {
	writeJSON(w, http.StatusOK, map[string]string{"status": "alive"})
}

func (s *server) handleReadyz(w http.ResponseWriter, _ *http.Request) {
	if !s.ready {
		writeJSON(w, http.StatusServiceUnavailable, map[string]string{"status": "not_ready"})
		return
	}
	writeJSON(w, http.StatusOK, map[string]string{"status": "ready"})
}

func writeJSON(w http.ResponseWriter, status int, body any) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	_ = json.NewEncoder(w).Encode(body)
}

// statusRecorder captures the response status code for instrumentation.
type statusRecorder struct {
	http.ResponseWriter
	status int
}

func (r *statusRecorder) WriteHeader(code int) {
	r.status = code
	r.ResponseWriter.WriteHeader(code)
}
