import re
import requests
from urllib.parse import urlparse
import cloudscraper
from os import environ


crypt = "eldBQXpCaDJ0ZE05TnVxeWtlU3VuMGozNmxwYlZQbFVuR0N4UjRUMW5pND0%3D"

def parse_info(res, url):
    info_parsed = {}
    
    info_chunks = re.findall(">(.*?)<\/td>", res.text)
    for i in range(0, len(info_chunks), 2):
        info_parsed[info_chunks[i]] = info_chunks[i + 1]
    return info_parsed

def kolop(url: str) -> str:
    
    client = cloudscraper.create_scraper(delay=10, browser='chrome')
    
    client.cookies.update({"crypt": crypt})
    res = client.get(url)
    info_parsed = parse_info(res, url)
    info_parsed["error"] = False

    up = urlparse(url)
    req_url = f"{up.scheme}://{up.netloc}/ajax.php?ajax=download"

    file_id = url.split("/")[-1]

    data = {"id": file_id}

    headers = {"x-requested-with": "XMLHttpRequest"}

    res = client.post(req_url, headers=headers, data=data).json()['file']
    gd_id = re.findall('gd=(.*)', res, re.DOTALL)[0]

    info_parsed["gdrive_url"] = f"https://drive.google.com/open?id={gd_id}"
    info_parsed["src_url"] = url
    flink = info_parsed['gdrive_url']

    return flink
