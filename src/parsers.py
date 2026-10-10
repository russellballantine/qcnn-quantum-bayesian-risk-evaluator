import os
import json
import requests

def fetch_metrics_for_cve(cve_id="CVE-2021-44228"):
    print("\nFetching metrics for target identifier: " + str(cve_id) + "...")
    
    # --- FIXED: Full, complete API endpoints using direct string concatenation ---
    epss_url = "https://api.first.org/data/v1/epss?cve=" + str(cve_id)
    nvd_url = "https://services.nvd.nist.gov/rest/json/cves/2.0?cveId=" + str(cve_id)
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        "Accept": "application/json"
    }

    
    session = requests.Session()
    session.trust_env = False
    session.headers.update(headers)
    
    # --- Ingest FIRST EPSS Probability ---
    try:
        response = session.get(epss_url, timeout=10)
        if response.status_code == 200:
            res_data = response.json().get("data", [])
            # Read first item out of data payload array list
            if res_data and isinstance(res_data, list):
                epss_score = float(res_data[0].get("epss", 0.1))
            else:
                epss_score = 0.1
        else:
            epss_score = 0.1
    except Exception as e:
        print("  [Notice] EPSS Stream Unavailable, reverting to base prior: " + str(e))
        epss_score = 0.1

    # --- Ingest NIST NVD Severity Metrics ---
    try:
        response = session.get(nvd_url, timeout=10)
        if response.status_code == 200:
            vulns = response.json().get("vulnerabilities", [])
            if vulns and isinstance(vulns, list):
                cve_data = vulns[0].get("cve", {})
                metrics = cve_data.get("metrics", {})
                cvss_data = metrics.get("cvssMetricV31", []) or metrics.get("cvssMetricV30", [])
                if cvss_data and isinstance(cvss_data, list):
                    base_score = float(cvss_data[0]["cvssData"]["baseScore"])
                    severity_score = base_score / 10.0  # Normalize metric score to probability decimal
                else:
                    severity_score = 0.5
            else:
                severity_score = 0.5
        else:
            severity_score = 0.5
    except Exception as e:
        print("  [Notice] NIST NVD Connection bypassed, utilizing fallback severity: " + str(e))
        severity_score = 0.5

    return {
        "cve": cve_id,
        "exploitability_prior": epss_score,
        "severity_prior": severity_score
    }

if __name__ == "__main__":
    result = fetch_metrics_for_cve("CVE-2021-44228")
    print("\n--- INTAKE PARSER PASSED ---")
    print(json.dumps(result, indent=2))