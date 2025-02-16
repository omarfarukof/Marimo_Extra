import os
import shutil
from pathlib import Path
import pandas as pd

from marimo_extra.marimo_export import export, export_app, export_editable, export_executable, export_html
from marimo_extra.utils import rich_print

def collect_notebooks_info(directories: list[str]):
    """
    Collects information about Python notebook files in the specified directories.

    This function searches through the given list of directories, recursively 
    finding all Python files (files with a '.py' extension) and compiles a list 
    of dictionaries containing the directory name and file path for each notebook.

    Args:
        directories (list[str]): A list of directory paths to search for notebooks.

    Returns:
        list[dict]: A list of dictionaries where each dictionary contains:
            - 'dir': The directory name where the notebook was found.
            - 'path': The full file path to the notebook.
    """
    all_notebooks = []
    for directory in directories:
        dir_path = Path(directory)
        if not dir_path.exists():
            print(f"Warning: Directory not found: {dir_path}")
        else:
            notebooks = [{"dir":directory, "path":str(path)} for path in dir_path.rglob("*.py")]
            all_notebooks.extend(notebooks)
    return all_notebooks

def export_notebook(notebook_path: str, notebook_type: str, html_output_path: str=None, output_dir: str="_site") -> bool:
    """
    Exports a notebook based on the given notebook type.

    Args:
        notebook_path (str): The path to the notebook file.
        notebook_type (str): The type of notebook to export. Can be one of:
            - 'app': Export an executable notebook.
            - 'edit': Export an editable notebook.
            - 'exe': Export a statically linked executable notebook.
            - 'html': Export an HTML notebook.
            - 'html-save': Export an HTML notebook from `__marimo__` save the generated HTML 
                to a file.
        html_output_path (str, optional): The path to the HTML output file.
        output_dir (str): The directory where the exported notebook will be
            saved. Defaults to "_site".

    Returns:
        bool: True if the notebook was exported successfully, False otherwise.
    """
    if notebook_type == "app":
        if html_output_path is not None:
            return export_app(notebook_path=notebook_path, output=os.path.join(output_dir, html_output_path))
        return export_app(notebook_path=notebook_path, output=os.path.join(output_dir, notebook_path.replace(".py", ".html")))
    elif notebook_type == "edit":
        if html_output_path is not None:
            return export_editable(notebook_path=notebook_path, output=os.path.join(output_dir, html_output_path))
        return export_editable(notebook_path=notebook_path, output=os.path.join(output_dir, notebook_path.replace(".py", ".html")))
    elif notebook_type == "exe":
        if html_output_path is not None:
            return export_executable(notebook_path=notebook_path, output=os.path.join(output_dir, html_output_path))
        return export_executable(notebook_path=notebook_path, output=os.path.join(output_dir, notebook_path.replace(".py", ".html")))
    elif notebook_type == "html":
        if html_output_path is not None:
            return export_html(notebook_path=notebook_path, output=os.path.join(output_dir, html_output_path))
        return export_html(notebook_path=notebook_path, output=os.path.join(output_dir, notebook_path.replace(".py", ".html")))
    elif notebook_type == "html-save":
        if html_output_path is not None:
            return export_html(notebook_path=notebook_path, output=os.path.join(output_dir, html_output_path), from_saved=True)
        return export_html(notebook_path=notebook_path, output=os.path.join(output_dir, notebook_path.replace(".py", ".html")), from_saved=True)
    elif notebook_type == "html-nocode":
        if html_output_path is not None:
            return export_html(notebook_path=notebook_path, output=os.path.join(output_dir, html_output_path), show_code=False)
        return export_html(notebook_path=notebook_path, output=os.path.join(output_dir, notebook_path.replace(".py", ".html")), show_code=False)
    else:
        rich_print(f"[red]Error:[end] Unknown notebook type: {notebook_type}")
    return False

def _nb_path_html2py(notebook_path: list[str]) -> str:
    """
    Replace the ".html" extension with ".py" for a given list of notebook paths.

    Args:
        notebook_path (list[str]): A list of notebook paths.

    Returns:
        list[str]: A list of notebook paths with ".html" replaced with ".py".
    """
    return [path.replace(".html", ".py") for path in notebook_path]
def _search_dict_of_lists(dict_of_lists, value):
    """
    Searches for a value in a dictionary of lists and returns the key associated with
    the first list that contains the value.

    Args:
        dict_of_lists (dict): A dictionary where the values are lists.
        value (any): The value to search for.

    Returns:
        str: The key associated with the first list that contains the value, or "html" if
            the value is not found.
    """
    for key, lst in dict_of_lists.items():
        if value in lst:
            return key
    return "html"
def _nb_type_encoder(notebook_type: list[str]) -> str:
    """
    Encodes a list of notebook types into a list of strings.

    Given a list of notebook types, this function will convert each type into a string
    based on the following mapping:

        - "app" to "app"
        - "exe" to "exe"
        - "edit" to "edit"
        - "html" to "html"
        - "html-save" to "html-save"
        - "html-nocode" to "html-nocode"

    Returns:
        list[str]: A list of strings corresponding to the input notebook types.
    """
    type_web = {
        "app": ["app", "apps", "application", "applications"],
        "exe": ["run", "exe", "executable", "executables"],
        "edit": ["edit", "editable", "editor", "editors"],
        "html": ["html", "htmls", "website", "websites", "web", "webs"],
        "html-save": ["html-save", "htmls-save", "website-save", "websites-save", "web-save", "webs-save", "save", "__marimo__"],
        "html-nocode": ["html-nocode", "htmls-nocode", "html-app"]
    }
    
    out_type = []
    for nb_type in notebook_type:
        out_type.append(_search_dict_of_lists(type_web, nb_type))
    return out_type

def auto_export_notebooks_web(index_csv_path: str="public/index.csv") -> bool:
    """
    Automatically exports notebooks from the specified directories.

    This function checks for the existence of an "index.csv" file to determine the
    notebooks and their types to export. If the file exists, it reads the notebook
    paths and types from the CSV; otherwise, it collects this information by scanning
    the provided directories.

    Args:
        notebook_dir (list[str]): A list of directories to search for notebook files.
        output_dir (str): The directory where the exported notebook files will be
            saved. Defaults to "_site".
        index_csv_path (str): The path to the "index.csv" file. Defaults to "index.csv".

    Returns:
        bool: True if the notebooks were exported successfully, False otherwise.
    """

    if os.path.exists(index_csv_path):
        notebook_df = pd.read_csv(index_csv_path)
        notebook_path = notebook_df["NB_Path"].values
        notebook_html_path = notebook_df["HTML_Path"].values
        notebook_type = notebook_df["Type"].values
    else:
        print(f"No index.csv file found at {index_csv_path}. Export will be skipped.")
        return False

    notebook_type = _nb_type_encoder(notebook_type)
    for nb_path, html_path, nb_type in zip(notebook_path, notebook_html_path, notebook_type):
        export_notebook(notebook_path = nb_path, html_output_path=html_path, notebook_type = nb_type)
    return True


def generate_index(output_dir: str="_site") -> bool:
    pass

def _add_row_csv(out, out_dict):
    """
    Adds rows to the given dataframe based on the notebook dictionaries.

    Args:
        out (pd.DataFrame): The dataframe to add rows to.
        out_dict (list[dict]): A list of dictionaries containing the notebook's
            information. Each dictionary should contain the following keys:
            - path (str): The path to the notebook file.
            - dir (str): The directory where the notebook is located.

    Returns:
        pd.DataFrame: The dataframe with the added rows.
    """
    for notebook in out_dict:
        nb_path = notebook["path"]
        html_path = os.path.join(notebook["path"].replace(".py", ".html"))
        name = os.path.basename(nb_path).replace(".py", "").replace(".html", "").capitalize()
        np_type = notebook["dir"]
        thumbnail = os.path.join(os.path.dirname(nb_path), "public", "thumbnail", os.path.basename(nb_path).replace(".py", "").replace(".html", "")+".png")
        tags = ""
        out.loc[len(out)] = [name, nb_path, html_path, np_type, thumbnail, tags]
    return out

def _save_record_csv(out, output_csv):
    """
    Saves the given dataframe to a CSV file.

    Args:
        out (pd.DataFrame): The dataframe to save.
        output_csv (str): The path to the CSV file to save to.

    Returns:
        bool: True if the save was successful, False otherwise.
    """
    try:
        out.to_csv(output_csv, index=False)
        rich_print(f"[green]Successfully Recoded[end] Index to {output_csv}")
        return True
    except Exception as e:
        rich_print(f"[red]Unexpected error Recording[end] Index: {e}")
        return False
def record_csv(dirs: list[str] , output_csv = os.path.join("public" , "index.csv"), replace: bool=False, output=False):
    """
    Records information about notebooks in specified directories to a CSV file.

    This function scans the specified directories for notebook files, collects
    their information, and records it into a CSV file with specified columns.
    If the CSV file already exists, it can either replace it or skip the
    recording based on the `replace` argument.

    Args:
        dirs (list[str]): A list of directories to search for notebook files.
        output_csv (str): The path to the CSV file to save to. Defaults to "public/index.csv".
        replace (bool): If True, replaces the existing CSV file. Defaults to False.
        output (bool): If True, returns the DataFrame instead of saving it to a CSV file. Defaults to False.

    Returns:
        bool or pd.DataFrame: True if the CSV was successfully saved, or the
        DataFrame if `output` is True. If the CSV file already exists and
        `replace` is False, returns True without saving.
    """

    if os.path.exists(output_csv) and not replace:
        rich_print(f"[red]Warning:[end] File already exists: {output_csv}")
        return True

    os.makedirs(os.path.dirname(output_csv), exist_ok=True)

    columns = ["Name", "NB_Path", "HTML_Path" , "Type", "Thumbnail", "Tags"]
    out_dict = collect_notebooks_info(dirs)
    out = pd.DataFrame(columns=columns)
    out = _add_row_csv(out, out_dict)
    if output:
        return out
    return _save_record_csv(out, output_csv)
