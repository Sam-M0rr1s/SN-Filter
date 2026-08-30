import requests
import json



def get_warranty_info(serial_number, country="gb", language="en"):
    url = "https://pcsupport.lenovo.com/gb/en/api/v4/upsell/redport/getIbaseInfo"

    payload = {
        "country": country,
        "language": language,
        "serialNumber": serial_number
    }

    headers = {
        "Content-Type": "application/json",
        "Referer": f"https://pcsupport.lenovo.com/{country}/{language}/products/laptops-and-netbooks/thinkpad-t-series-laptops/{serial_number[:2]}0w100/{serial_number.lower()}/warranty",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()







