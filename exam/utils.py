import psutil

def get_network_devices():
    devices = []
    interfaces = psutil.net_if_addrs()
    for iface, addrs in interfaces.items():
        for addr in addrs:
            if addr.family == psutil.AF_INET:
                device = {
                    'interface': iface,
                    'ip_address': addr.address,
                    'netmask': addr.netmask,
                    'broadcast': addr.broadcast
                }
                devices.append(device)
    return devices