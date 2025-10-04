

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