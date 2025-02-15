import os

def run_gen_index_csv():
    if os.path.exists(os.path.join("scripts", "gen_index_csv.py")):
        os.system("uv run scripts/gen_index_csv.py")
    else:
        print("No scripts/gen_index_csv.py found")


def run_website_build():
    if os.path.exists(os.path.join("scripts", "website_build.py")):
        os.system("uv run scripts/website_build.py")
    else:
        print("No scripts/website_build.py found")