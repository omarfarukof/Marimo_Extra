import os
import shutil
import marimo_extra as me

def _fresh_web_build(output_dir):
    if os.path.exists(output_dir): 
        shutil.rmtree(output_dir)
        me.rich_print(f"Removed [blue]{output_dir}[end] folder")
    else:
        print("No Folder Found")

def build_website(fresh_build=False):
    output_dir = "_site"

    if fresh_build:
        _fresh_web_build(output_dir)

    # record_csv(["notebooks", "apps"])
    me.auto_export_notebooks_web(["notebooks", "apps"], output_dir=output_dir)
    me.export(notebook_path="index.py", output="_site/index.html", show_code=False)


if __name__ == "__main__":
    build_website(fresh_build=True)