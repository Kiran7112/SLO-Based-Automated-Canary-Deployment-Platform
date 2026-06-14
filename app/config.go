package main

import (
	"os"
	"strconv"
)

// config holds the runtime knobs. The two interesting ones — errorRate and
// extraLatency — let a deployment deliberately behave like a "bad" canary so
// the SLO gates can be demonstrated end-to-end without changing code.
type config struct {
	addr         string
	version      string
	errorRate    float64 // probability [0,1] that /checkout returns 5xx
	extraLatency int     // extra milliseconds injected into /checkout
}

func loadConfig() config {
	return config{
		addr:         getEnv("LISTEN_ADDR", ":8080"),
		version:      getEnv("VERSION", "stable"),
		errorRate:    getEnvFloat("ERROR_RATE", 0.0),
		extraLatency: getEnvInt("EXTRA_LATENCY_MS", 0),
	}
}

func getEnv(key, def string) string {
	if v, ok := os.LookupEnv(key); ok && v != "" {
		return v
	}
	return def
}

func getEnvFloat(key string, def float64) float64 {
	if v, ok := os.LookupEnv(key); ok {
		if f, err := strconv.ParseFloat(v, 64); err == nil {
			return f
		}
	}
	return def
}

func getEnvInt(key string, def int) int {
	if v, ok := os.LookupEnv(key); ok {
		if n, err := strconv.Atoi(v); err == nil {
			return n
		}
	}
	return def
}
