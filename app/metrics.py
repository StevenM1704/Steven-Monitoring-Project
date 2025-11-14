import time
import requests
from prometheus_client import Gauge, Counter

URLS_TO_MONITOR = [
    "https://www.google.com",
    "https://www.github.com"
]

url_up = Gauge("url_up", "Whether the URL is up (1) or down (0)", ["url"])
url_latency = Gauge("url_latency_seconds", "Latency of the URL check", ["url"])
url_failures = Counter("url_failures_total", "Total failures for the URL", ["url"])
url_checks = Counter("url_checks_total", "Total checks for the URL", ["url"])

def collect_metrics():
    for url in URLS_TO_MONITOR:
        start = time.time()
        try:
            response = requests.get(url, timeout=5)
            latency = time.time() - start

            url_checks.labels(url=url).inc()
            url_latency.labels(url=url).set(latency)

            if response.status_code == 200:
                url_up.labels(url=url).set(1)
            else:
                url_up.labels(url=url).set(0)
                url_failures.labels(url=url).inc()

        except Exception:
            url_up.labels(url=url).set(0)
            url_failures.labels(url=url).inc()