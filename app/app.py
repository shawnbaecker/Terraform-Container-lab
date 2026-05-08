"""
Platform Inspector
A small Flask app that reports back where it's running.
The same image runs on Docker, ACI, ACA, and AKS — and tells you which.
"""

import os
import socket
import time
from datetime import datetime, timezone
from flask import Flask, render_template, jsonify

app = Flask(__name__)

# Track app start time and request count in memory.
# These reset on container restart — that's a feature, not a bug:
# it teaches you that containers are ephemeral.
START_TIME = time.time()
REQUEST_COUNT = 0


def detect_platform():
    """
    Figure out which Azure container service we're running on
    by checking environment variables each platform sets.
    Order matters — check most specific first.
    """
    if os.environ.get("KUBERNETES_SERVICE_HOST"):
        return {
            "name": "Azure Kubernetes Service (AKS)",
            "color": "#f97316",  # orange
            "icon": "⎈",
        }
    if os.environ.get("CONTAINER_APP_NAME"):
        return {
            "name": "Azure Container Apps (ACA)",
            "color": "#a855f7",  # purple
            "icon": "▲",
        }
    if os.environ.get("ACI_RESOURCE_GROUP") or os.environ.get("WEBSITE_INSTANCE_ID"):
        return {
            "name": "Azure Container Instances (ACI)",
            "color": "#22c55e",  # green
            "icon": "◆",
        }
    # No Azure markers found — must be local Docker or bare Python
    if os.path.exists("/.dockerenv"):
        return {
            "name": "Local Docker",
            "color": "#3b82f6",  # blue
            "icon": "⬢",
        }
    return {
        "name": "Local Python (no container)",
        "color": "#64748b",  # slate
        "icon": "○",
    }


def get_info():
    """Build the info payload returned by the dashboard and the API."""
    global REQUEST_COUNT
    REQUEST_COUNT += 1
    platform = detect_platform()
    uptime_seconds = int(time.time() - START_TIME)
    return {
        "hostname": socket.gethostname(),
        "platform": platform["name"],
        "platform_color": platform["color"],
        "platform_icon": platform["icon"],
        "uptime_seconds": uptime_seconds,
        "uptime_human": format_uptime(uptime_seconds),
        "request_count": REQUEST_COUNT,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "region": os.environ.get("REGION", "unknown"),
        # A few raw env hints for the curious — not the whole environment
        "container_app_revision": os.environ.get("CONTAINER_APP_REVISION", ""),
        "kubernetes_pod_namespace": os.environ.get("POD_NAMESPACE", ""),
    }


def format_uptime(seconds):
    """Turn seconds into something readable like '2m 14s' or '1h 3m'."""
    if seconds < 60:
        return f"{seconds}s"
    minutes, secs = divmod(seconds, 60)
    if minutes < 60:
        return f"{minutes}m {secs}s"
    hours, mins = divmod(minutes, 60)
    return f"{hours}h {mins}m"


@app.route("/")
def dashboard():
    """The HTML dashboard — what you see in a browser."""
    return render_template("index.html", info=get_info())


@app.route("/api/info")
def api_info():
    """JSON endpoint — what the dashboard polls every 2 seconds, also good for curl."""
    return jsonify(get_info())


@app.route("/healthz")
def healthz():
    """Health check endpoint — used by ACA, AKS, and load balancers."""
    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    # Bind to 0.0.0.0 so the container's port is reachable from outside.
    # Port 8000 is a sensible default for non-root containers.
    app.run(host="0.0.0.0", port=8000, debug=False)