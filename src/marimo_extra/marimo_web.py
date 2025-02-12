import os

from pathlib import Path
import pandas as pd

from marimo_extra.marimo_export import export, export_app, export_editable, export_executable
from marimo_extra.utils import rich_print

def collect_notebooks_info(directorys: list[str]):
    all_notebooks = []
    for directory in directorys:
        dir_path = Path(directory)
        if not dir_path.exists():
            print(f"Warning: Directory not found: {dir_path}")
            continue
        notebooks = [{"dir":directory, "path":str(path)} for path in dir_path.rglob("*.py")]
        all_notebooks.extend(notebooks)
    return all_notebooks

def export_notebook(notebook_path: str, notebook_type: str , output_dir: str="_site") -> bool:
    if notebook_type.lower() in ["apps", "app"]:
        return export_app(notebook_path=notebook_path, output=os.path.join(output_dir, notebook_path.replace(".py", ".html")))
    elif notebook_type.lower() in ["edit", "editable", "editables"]:
        return export_editable(notebook_path=notebook_path, output=os.path.join(output_dir, notebook_path.replace(".py", ".html")))
    elif notebook_type.lower() in ["run", "exe", "executable", "executables"]:
        return export_executable(notebook_path=notebook_path, output=os.path.join(output_dir, notebook_path.replace(".py", ".html")))
    return export(notebook_path=notebook_path, output=os.path.join(output_dir, notebook_path.replace(".py", ".html")))

def export_all_notebooks(notebooks: list[str], output_dir: str="_site") -> bool:
    output_csv = os.path.join("public" , "index.csv")
    if os.path.exists(output_csv):
        rich_print(f"[yellow]Collecting Index[end] from: {output_csv}")
        notebooks = pd.read_csv(output_csv).values
        for notebook in notebooks:
            rich_print(f"[yellow]Info::[end] Name: {notebook[0]} | Path: {notebook[1]} | Type: {notebook[2]} | Thumbnail: {notebook[3]} | Tags: {notebook[4]}")
            if not export_notebook(notebook_path =notebook[1].replace(".html", ".py"), notebook_type = notebook[2], output_dir=output_dir):
                return False
        return True

    notebooks = collect_notebooks_info(notebooks)
    for notebook in notebooks:
        if not export_notebook(notebook_path = notebook["path"], notebook_type = notebook["dir"], output_dir=output_dir):
            return False
    return True

def generate_index(output_dir: str="_site") -> bool:
    pass

def test():
    for notebook in (collect_notebooks_info(["notebooks", "apps"])):
        print(f"{notebook["dir"]} : {notebook['path']}")

def record_csv(dirs: list[str] , replace: bool=False):
    output_csv = os.path.join("public" , "index.csv")
    if os.path.exists(output_csv) and not replace:
        print(f"Warning: File already exists: {output_csv}")
        return True

    os.makedirs(os.path.dirname(output_csv), exist_ok=True)

    columns = ["Name", "Path", "Type", "Thumbnail", "Tags"]
    out = pd.DataFrame(columns=columns)
    out_dict = collect_notebooks_info(dirs)

    for notebook in out_dict:
        path = notebook["path"].replace(".py", ".html")
        name = os.path.basename(path).replace(".py", "").replace(".html", "").capitalize()
        np_type = notebook["dir"]
        thumbnail = os.path.join(os.path.dirname(path), "public", "thumbnail", os.path.basename(path).replace(".py", "").replace(".html", "")+".png")
        tags = ""
        out.loc[len(out)] = [name, path, np_type, thumbnail, tags]
    
    # Save the DataFrame to a CSV file
    try:
        out.to_csv(output_csv, index=False)
        rich_print(f"[green]Successfully Recoded[end] Index to {output_csv}")
    except Exception as e:
        rich_print(f"[red]Unexpected error Recording[end] Index: {e}")
        return False

    return True



if __name__ == "__main__":
    # test()
    record_csv(["notebooks", "apps"], replace=True)
    export_all_notebooks(["notebooks", "apps"], output_dir="_site")
    export(notebook_path="index.py", output="_site/index.html", show_code=False)

    # # Run Server
    # python -m http.server -d _site
    # or
    # uv run python -m http.server -d _site