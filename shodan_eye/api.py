"""Shodan API client wrapper — key resolution, client creation, account info."""

import os
import shodan

# Dev plan limits — used for credit-aware defaults and budget warnings.
PLAN_LIMITS = {
    "query_credits": 100,
    "scan_credits": 100,
    "monitored_ips": 16,
    "unlocked_results": 100,
    "has_https_filter": False,
    "has_telnet_filter": False,
}

# Credit thresholds for warnings
CREDIT_WARNING_THRESHOLD = 10
CREDIT_CRITICAL_THRESHOLD = 3


def resolve_api_key(filepath="api.txt"):
    """Resolve API key: env var > file > None."""
    key = os.environ.get("SHODAN_API_KEY")
    if key:
        return key

    if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
        with open(filepath, "r") as f:
            return f.readline().rstrip("\n")

    return None


def save_api_key(key, filepath="api.txt"):
    """Write API key to file."""
    with open(filepath, "w") as f:
        f.write(key)


def create_client(api_key):
    """Create and return a shodan.Shodan client instance."""
    return shodan.Shodan(api_key)


def get_account_info(client):
    """Validate key and return account info using the free api.info() endpoint.

    Returns dict with plan, query_credits, scan_credits, budget status, etc.
    Raises shodan.APIError if key is invalid.
    """
    info = client.info()
    query_credits = info.get("query_credits", 0)
    scan_credits = info.get("scan_credits", 0)

    return {
        "plan": info.get("plan", "unknown"),
        "query_credits": query_credits,
        "scan_credits": scan_credits,
        "monitored_ips": info.get("monitored_ips", 0),
        "telnet": info.get("telnet", False),
        "https": info.get("https", False),
        "unlocked": info.get("unlocked", False),
        "unlocked_left": info.get("unlocked_left", 0),
        "usage_limits": info.get("usage_limits", PLAN_LIMITS),
        "budget": _assess_budget(query_credits, scan_credits),
    }


def _assess_budget(query_credits, scan_credits):
    """Return budget status based on remaining credits."""
    if query_credits <= CREDIT_CRITICAL_THRESHOLD:
        return {"status": "critical", "message": f"Only {query_credits} query credits left — avoid searches until next month"}
    if query_credits <= CREDIT_WARNING_THRESHOLD:
        return {"status": "low", "message": f"{query_credits} query credits remaining — use targeted queries"}
    return {"status": "ok", "message": f"{query_credits} query credits remaining"}
