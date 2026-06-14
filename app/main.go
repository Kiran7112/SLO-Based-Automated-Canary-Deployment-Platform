// Command slo-canary-checkout is a small checkout microservice used to
// demonstrate SLO-gated progressive delivery. It exposes a /checkout business
// endpoint, Kubernetes health probes, and a Prometheus /metrics endpoint.
package main

import (
	"context"
	"errors"
	"log"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"

	"github.com/prometheus/client_golang/prometheus/promhttp"
)

func main() {
	cfg := loadConfig()
	srv := newServer(cfg)

	mux := http.NewServeMux()
	mux.Handle("/", srv.routes())
	mux.Handle("/metrics", promhttp.Handler())

	httpServer := &http.Server{
		Addr:              cfg.addr,
		Handler:           mux,
		ReadHeaderTimeout: 5 * time.Second,
	}

	go func() {
		log.Printf("slo-canary-checkout version=%s listening on %s (error_rate=%.3f extra_latency_ms=%d)",
			cfg.version, cfg.addr, cfg.errorRate, cfg.extraLatency)
		if err := httpServer.ListenAndServe(); err != nil && !errors.Is(err, http.ErrServerClosed) {
			log.Fatalf("server error: %v", err)
		}
	}()

	// Graceful shutdown so in-flight checkouts are not dropped during a rollout.
	stop := make(chan os.Signal, 1)
	signal.Notify(stop, syscall.SIGINT, syscall.SIGTERM)
	<-stop

	srv.ready = false
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()
	if err := httpServer.Shutdown(ctx); err != nil {
		log.Printf("graceful shutdown failed: %v", err)
	}
	log.Println("shutdown complete")
}
