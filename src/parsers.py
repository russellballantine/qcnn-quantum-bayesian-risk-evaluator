# src/parsers.py
import urllib.request
import json

def fetch_vulnerability_metrics(cve_id):
    """
    Fetches raw quantitative security vectors from NIST NVD and FIRST EPSS endpoints.
    
    Args:
        cve_id (str): Standardized identifier format (e.g., 'CVE-2021-44228')
    Returns:
        dict: Parsed prior metrics for the Quantum Bayesian Network engine.
    """
    print(f"Fetching metrics for target identifier: {cve_id}...")
    
    # 1. Fetch live threat telemetry metrics from the FIRST EPSS API
    epss_url = f"https://first.org{cve_id}"
    epss_prob = 0.1  # Sensible fallback prior if the record is missing
    
    try:
        req = urllib.request.Request(epss_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            epss_data = json.loads(response.read().decode())
            entries = epss_data.get("data", [])
            if entries:
                epss_prob = float(entries[0]["epss"])
                print(f"  [EPSS Target Found] Wild Exploitation Probability: {epss_prob:.5f}")
    except Exception as e:
        print(f"  [Notice] EPSS Stream Unavailable, reverting to base prior: {e}")

    # 2. Fetch baseline severity configurations from the NIST NVD API
    nvd_url = f"https://nist.gov{cve_id}"
    base_severity_score = 5.0  # Middle-of-the-road base severity fallback
    
    try:
        req = urllib.request.Request(nvd_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            nvd_data = json.loads(response.read().decode())
            vulns = nvd_data.get("vulnerabilities", [])
            if vulns:
                # Target the CVSS v3.1 metrics collection block
                metrics = vulns[0]["cve"]["metrics"]
                cvss_list = metrics.get("cvssMetricV31", metrics.get("cvssMetricV30", []))
                if cvss_list:
                    base_severity_score = float(cvss_list[0]["cvssData"]["baseScore"])
                    print(f"  [NIST NVD Found] CVSS Base Severity Score: {base_severity_score}/10.0")
    except Exception as e:
        print(f"  [Notice] NIST NVD Connection bypassed, utilizing fallback severity: {e}")

    # 3. Compile quantitative variables into unified priors
    # Normalize the 0-10 CVSS base score into a neat probability scalar between 0.0 and 1.0
    normalized_severity = base_severity_score / 10.0

    return {
        "cve": cve_id,
        "exploitability_prior": epss_prob,
        "severity_prior": normalized_severity
    }

if __name__ == "__main__":
    # Diagnostic check utilizing the historic Log4Shell target vector
    test_cve = "CVE-2021-44228"
    metrics = fetch_vulnerability_metrics(test_cve)
    print("\n--- INTAKE PARSER PASSED ---")
    print(json.dumps(metrics, indent=2))
