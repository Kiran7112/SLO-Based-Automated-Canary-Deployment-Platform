package main

import (
	"github.com/prometheus/client_golang/prometheus"
	"github.com/prometheus/client_golang/prometheus/promauto"
)

// Metric names are the single source of truth for the whole platform.
// The Prometheus SLO rules (observability/prometheus/slo-rules.yaml), the
// Argo Rollouts AnalysisTemplate (deploy/k8s/analysistemplate.yaml) and the
// Grafana dashboard all query exactly these names — keep them in sync.
const (
	metricRequestsTotal   = "http_requests_total"
	metricRequestDuration = "http_request_duration_seconds"
	metricPaymentAttempts = "payment_attempts_total"
	metricPaymentSuccess  = "payment_success_total"
)

var (
	// httpRequestsTotal counts every HTTP response, labelled by route, method
	// and status code. The canary's 5xx error-rate SLO is derived from this.
	httpRequestsTotal = promauto.NewCounterVec(prometheus.CounterOpts{
		Name: metricRequestsTotal,
		Help: "Total HTTP requests processed, partitioned by route, method and status code.",
	}, []string{"route", "method", "status"})

	// httpRequestDuration is the latency histogram backing the p99 latency SLO.
	httpRequestDuration = promauto.NewHistogramVec(prometheus.HistogramOpts{
		Name:    metricRequestDuration,
		Help:    "HTTP request latency in seconds.",
		Buckets: []float64{0.01, 0.025, 0.05, 0.1, 0.2, 0.3, 0.5, 0.75, 1, 2.5},
	}, []string{"route", "method"})

	// paymentAttempts / paymentSuccess back the business SLO: successful
	// payment rate must stay >= 99% of the stable baseline.
	paymentAttempts = promauto.NewCounter(prometheus.CounterOpts{
		Name: metricPaymentAttempts,
		Help: "Total checkout payment attempts.",
	})
	paymentSuccess = promauto.NewCounter(prometheus.CounterOpts{
		Name: metricPaymentSuccess,
		Help: "Total successful checkout payments.",
	})

	// appInfo exposes the running version so dashboards can tell canary from stable.
	appInfo = promauto.NewGaugeVec(prometheus.GaugeOpts{
		Name: "app_info",
		Help: "Static application info; the version label distinguishes stable vs canary.",
	}, []string{"version"})
)
