import subprocess
import re

def get_network_devicess():
    try:
        # arp-scan orqali tarmoqni skanerlash
        result = subprocess.run(['sudo', 'arp-scan', '-l'], capture_output=True, text=True, check=True)

        devices = []
        lines = result.stdout.strip().split('\n')
        for line in lines:
            match = re.search(r'(\d+\.\d+\.\d+\.\d+)\s+([0-9a-f:]{17})\s+(.+)', line)
            if match:
                ip_address = match.group(1)
                mac_address = match.group(2)
                manufacturer = match.group(3).strip()

                # Qo'shimcha ma'lumotlar qo'shish
                device = {
                    'ip_address': ip_address,
                    'mac_address': mac_address,
                    'manufacturer': manufacturer,
                    'status': 'active'  # Masalan, qurilma faol holatda
                }
                devices.append(device)

        return devices

    except subprocess.CalledProcessError as e:
        print(f"Error running arp-scan: {e}")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []
