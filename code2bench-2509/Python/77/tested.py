from typing import List

def get_security_advice(vulns: List[str]) -> List[str]:
    # Dictionary to map vulnerability types to their respective advice
    vulnerability_advice = {
        "FTP": ["Disabling FTP service or prohibiting anonymous login, and setting strong passwords"],
        "Telnet": ["Disabling Telnet service and using SSH or other secure protocols as an alternative"],
        "SMB": ["Disabling unnecessary SMB services and applying timely patches"],
        "远程桌面": ["Enabling two-factor authentication and restricting access sources for remote desktop services"]
    }

    # Filter the vulnerabilities that are present in the input list
    filtered_vulns = [vuln for vuln in vulns if vuln in vulnerability_advice]

    # Extract unique advice strings
    unique_advice = list(set([advice for vulnerability in filtered_vulns for advice in vulnerability_advice[vulnerability]]))

    return unique_advice