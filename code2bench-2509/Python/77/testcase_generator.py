from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import json
import os
import atexit
import copy

# Configuration
TEST_CASE_DIR = os.path.abspath("test_cases")
os.makedirs(TEST_CASE_DIR, exist_ok=True)
TEST_CASE_FILE = os.path.join(TEST_CASE_DIR, "test_cases.json")
generated_cases = []
stop_collecting = False  # Global flag to control case collection

# Ground truth function
def get_security_advice(vulns):
    advice = []
    for v in vulns:
        if "FTP" in v:
            advice.append("建议：关闭FTP服务或禁止匿名登录，设置强密码。")
        if "Telnet" in v:
            advice.append("建议：关闭Telnet服务，使用SSH等安全协议替代。")
        if "SMB" in v:
            advice.append("建议：关闭不必要的SMB服务，及时打补丁。")
        if "远程桌面" in v:
            advice.append("建议：开启远程桌面双因素认证，限制访问来源。")
    return list(set(advice))  # 去重

# Strategy for generating vulnerability strings
def vuln_strategy():
    return st.one_of([
        st.just("FTP漏洞"),
        st.just("Telnet漏洞"),
        st.just("SMB漏洞"),
        st.just("远程桌面漏洞"),
        st.text(
            st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')),
            min_size=1,
            max_size=50
        ).filter(lambda x: any(keyword in x for keyword in ["FTP", "Telnet", "SMB", "远程桌面"]))
    ])

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(vulns=st.lists(vuln_strategy(), min_size=1, max_size=10))
@example(vulns=["FTP漏洞"])
@example(vulns=["Telnet漏洞"])
@example(vulns=["SMB漏洞"])
@example(vulns=["远程桌面漏洞"])
@example(vulns=["FTP漏洞", "Telnet漏洞"])
@example(vulns=["FTP漏洞", "SMB漏洞", "远程桌面漏洞"])
@example(vulns=["FTP漏洞", "FTP漏洞"])  # Test deduplication
def test_get_security_advice(vulns):
    global stop_collecting
    if stop_collecting:
        return
    
    vulns_copy = copy.deepcopy(vulns)
    try:
        expected = get_security_advice(vulns_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    if any(keyword in v for v in vulns for keyword in ["FTP", "Telnet", "SMB", "远程桌面"]):
        generated_cases.append({
            "Inputs": {"vulns": vulns},
            "Expected": expected
        })
        if len(generated_cases) >= 500:
            stop_collecting = True

# Save test cases
def save_test_cases():
    with open(TEST_CASE_FILE, "w") as f:
        json.dump(generated_cases, f, indent=2, ensure_ascii=False)
    print(f"✅ Saved {len(generated_cases)} test cases to {TEST_CASE_FILE}")

atexit.register(save_test_cases)