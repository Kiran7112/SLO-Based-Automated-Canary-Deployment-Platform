// k6 load generator that drives steady checkout traffic so Argo Rollouts has
// live signals to analyse during a canary. Run while a rollout is in progress:
//
//   k6 run -e BASE_URL=http://checkout.local load/k6-canary-test.js
//
// The SLO thresholds below mirror the AnalysisTemplate, so k6 fails locally
// under the same conditions the canary gate would roll back in-cluster.
import http from "k6/http";
import { check, sleep } from "k6";

const BASE_URL = __ENV.BASE_URL || "http://checkout.local";

export const options = {
  scenarios: {
    steady_traffic: {
      executor: "constant-arrival-rate",
      rate: 50, // 50 checkouts/sec
      timeUnit: "1s",
      duration: "10m",
      preAllocatedVUs: 50,
      maxVUs: 100,
    },
  },
  thresholds: {
    http_req_failed: ["rate<0.01"], // < 1% errors  (matches error-rate SLO)
    http_req_duration: ["p(99)<500"], // p99 < 500ms (matches latency SLO)
  },
};

export default function () {
  const res = http.post(`${BASE_URL}/checkout`, JSON.stringify({ amount: 49.99 }), {
    headers: { "Content-Type": "application/json" },
  });
  check(res, {
    "status is 200": (r) => r.status === 200,
  });
  sleep(0.1);
}
