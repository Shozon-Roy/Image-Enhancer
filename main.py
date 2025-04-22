from io import BytesIO
import time
import re

image_url = 'img_link'

img_response = requests.get(image_url)
img_response.raise_for_status()
image_data = BytesIO(img_response.content)

upload_url = "https://photoai.imglarger.com/api/PhoAi/Upload"
data = {
    "type": "2",
    "scaleRadio": "1"
}
files = {
    "file": ("image.jpg", image_data, "image/jpeg")
}
headers = {
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9",
    "priority": "u=1, i",
    "sec-ch-ua": "\"Google Chrome\";v=\"135\", \"Not-A.Brand\";v=\"8\", \"Chromium\";v=\"135\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site",
    "referer": "https://image-enhancer-snowy.vercel.app/",
    "referrerPolicy": "strict-origin-when-cross-origin"
}

upload_response = requests.post(upload_url, data=data, files=files, headers=headers)
upload_json = upload_response.json()
code = upload_json["data"]["code"]
print(f"Upload successful. Code: {code}")

time.sleep(0.2)

status_url = "https://photoai.imglarger.com/api/PhoAi/CheckStatus"
status_headers = {
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9",
    "content-type": "application/json",
    "priority": "u=1, i",
    "sec-ch-ua": "\"Google Chrome\";v=\"135\", \"Not-A.Brand\";v=\"8\", \"Chromium\";v=\"135\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site",
    "referer": "https://image-enhancer-snowy.vercel.app/",
    "referrerPolicy": "strict-origin-when-cross-origin"
}

while True:
    status_payload = {
        "type": "2",
        "code": code
    }
    status_response = requests.post(status_url, json=status_payload, headers=status_headers)
    status_json = status_response.json()

    if "data" in status_json and "downloadUrls" in status_json["data"]:
        download_url = status_json["data"]["downloadUrls"][0]
        if download_url.startswith(f"https://photoai.imglarger.com/color-enhancer/{code}.jpg"):
            print("\n✅ Image is ready!")
            print("Matched Link:", download_url)
            break

    time.sleep(3)
