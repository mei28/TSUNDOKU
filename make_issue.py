import glob
import markdown
import re
import subprocess
import shutil
from pathlib import Path
import pathlib

root_path = Path(__file__).resolve().parent
issued_path = Path(__file__).resolve().parent / "issued"

files = root_path.glob("*.md")

for file in files:
    if file.name == "README.md":
        continue
    else:
        md = markdown.Markdown()
        with open(file, "r") as f:
            text = f.read()
            html = md.convert(text)
            pattern = re.compile(r"<h1>(.*?)<\/h1>")
            match = pattern.search(html)
            if match:
                title = match.group(1)
                try:
                    # add to issue
                    subprocess.run(
                        f"gh issue create -t {title} -F {file}",
                        shell=True,
                    )
                    file.rename(issued_path / file.name)
                    print(f"DONE: {file.name}")

                except:
                    print("Error Occur")
                    pass
            else:
                print(f"ERROR at {file.name}")
                raise ValueError
