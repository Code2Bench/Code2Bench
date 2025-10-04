import json
import urllib.parse

def parse_rtc_config(data: str) -> tuple[list, list, str]:
    config = json.loads(data)
    stun_uris = []
    turn_uris = []
    
    for server in config.get("iceServers", []):
        urls = server.get("urls", [])
        for url in urls:
            if url.startswith("stun:"):
                # Format STUN URI
                parsed_url = urllib.parse.urlparse(url)
                stun_uris.append(f"stun://{parsed_url.netloc}")
            elif url.startswith("turn:") or url.startswith("turns:"):
                # Format TURN URI with username and credential
                parsed_url = urllib.parse.urlparse(url)
                user_pass = parsed_url.username
                if user_pass:
                    user_pass = f"{user_pass}@"
                stun_uris.append(f"{url.split(':')[0]}://{user_pass}{parsed_url.netloc}")
    
    return stun_uris, turn_uris, data