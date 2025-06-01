import requests
from lxml import html
from feedgen.feed import FeedGenerator
from urllib.parse import urljoin
import hashlib

URL = 'https://axelera.ai/careers'

response = requests.get(URL)
tree = html.fromstring(response.content)

fg = FeedGenerator()
fg.title('Axelera AI Careers')
fg.link(href=URL)
fg.description('Latest job offers at Axelera AI')

# Get all h5 titles inside the "openings" section
titles = tree.xpath('//div[contains(@id, "openings")]//h5')

for h5 in titles:
    title_text = h5.text_content().strip()

    # Try to find the nearest <a> tag to get a link
    link_el = h5.xpath('.//ancestor::a[1]/@href')
    link = urljoin(URL, link_el[0]) if link_el else URL

    # Optional: look for nearby <p> elements for description
    description_parts = h5.xpath('./following-sibling::p[1]/text()')
    description = description_parts[0].strip() if description_parts else ''

    # Use job title as part of GUID (or hash for safety)
    unique_id = hashlib.md5(title_text.encode('utf-8')).hexdigest()

    fe = fg.add_entry()
    fe.title(title_text)
    fe.link(href=link)
    fe.description(description)
    fe.guid(unique_id, permalink=False)

# Output RSS
rss_feed = fg.rss_str(pretty=True)
print(rss_feed.decode())

import subprocess
from pathlib import Path

def get_git_root() -> Path:
    return Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"]).decode("utf-8").strip())

git_root = get_git_root()
rss_path = git_root / "docs" / "axelera.xml"

with open(rss_path, "wb") as f:
    f.write(rss_feed)