import socket
import time
from zeroconf import IPVersion, ServiceInfo, Zeroconf


def get_local_ip() -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("10.255.255.255", 1))
        return s.getsockname()[0]
    except Exception:
        return "127.0.0.1"
    finally:
        s.close()


if __name__ == "__main__":
    ip = get_local_ip()
    info = ServiceInfo(
        "_https._tcp.local.",
        "Ambient Bridge._https._tcp.local.",
        addresses=[socket.inet_aton(ip)],
        port=443,
        properties={"path": "/"},
        server="ambient-bridge.local.",
    )
    zc = Zeroconf(ip_version=IPVersion.V4Only)
    zc.register_service(info)
    print(f"mDNS active: https://ambient-bridge.local -> {ip}")
    try:
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        pass
    finally:
        zc.unregister_service(info)
        zc.close()
