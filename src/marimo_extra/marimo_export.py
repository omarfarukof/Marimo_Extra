import os
import subprocess
import shutil
from marimo_extra.utils import rich_print

try:
    import marimo
except ImportError:
    rich_print("[red]Error:[end] Python [green][italic]Marimo[end] Library is not installed!")
    rich_print("Please install it with \"[italic][yellow] uv add marimo [end]\" or \"[italic] pip install marimo [end]\" command.")
    exit(1)

format_ext = {
    "html": ".html",
    "html-wasm": ".html",
    "script": ".py",
    "ipynb": ".ipynb",
    "md": ".md",
}

def _get_xcmd_html(cmd, sandbox, show_code):
    """
    Modify the export command to generate an HTML file.

    Args:
        cmd (list): The base export command.
        sandbox (bool): If True, add the --sandbox flag.
        show_code (bool): If True, add the --include-code flag.

    Returns:
        list: The modified command.
    """
    if sandbox:
        cmd.append("--sandbox")

    if show_code:
        cmd.append("--include-code")
    else:
        cmd.append("--no-include-code")
    return cmd

def _get_xcmd_ipynb(cmd, sandbox, show_code, sort):
    """
    Modify the export command to generate an IPYNB file.

    Args:
        cmd (list): The base export command.
        sandbox (bool): If True, add the --sandbox flag.
        show_code (bool): If True, add the --include-code flag.
        sort (str): The sorting method, either 'topological' or 'top-down'.

    Returns:
        list: The modified command.
    """

    if sandbox:
        cmd.append("--sandbox")

    if show_code:
        cmd.append("--include-code")
    else:
        cmd.append("--no-include-code")

    if sort not in ["topological", "top-down"]:
        raise ValueError("sort must be either 'topological' or 'top-down'")
    cmd += ["--sort", sort]
    return cmd

def _get_xcmd_wasm(cmd, mode, show_code):
    """
    Modify the export command to generate an HTML-WASM file.

    Args:
        cmd (list): The base export command.
        mode (str): The export mode, either 'run' or 'edit'.
        show_code (bool): If True, add the --show-code flag; otherwise, add the --no-show-code flag.

    Returns:
        list: The modified command.
    """
    if mode not in ["run", "edit"]:
        raise ValueError("mode must be either 'run' or 'edit'")

    # Export Mode
    cmd += ["--mode", mode]
    if show_code:
        cmd.append(f"--show-code")
    else:
        cmd.append(f"--no-show-code")
    return cmd

def get_export_cmd(
    notebook_path: str, output: str=None, 
    export_format:str="html",   # html, html-wasm, ipynb, md, script
    mode:str="run",             # run, edit
    show_code:bool=True, watch:bool=False, sandbox:bool=False, 
    sort:str="topological"      # topological, top-down
    ) -> list[str]:

    """
    Generate the command to export a notebook using Marimo.

    Args:
        notebook_path (str): The path to the notebook file.
        output (str, optional): The path to the output file. Defaults to None.
        export_format (str, optional): The format to export the notebook to. Defaults to "html".
            Choices:
                - "html": Export to a static HTML file.
                - "html-wasm": Export to an HTML file with WebAssembly support.
                - "ipynb": Export to an IPython notebook file.
                - "md": Export to a Markdown file.
                - "script": Export to a Python script file.
        mode (str, optional): The export mode. Defaults to "run".
            Choices:
                - "run": Export the notebook in a form that can be run.
                - "edit": Export the notebook in a form that can be edited.
        show_code (bool, optional): If True, include the code in the exported notebook. Defaults to True.
        watch (bool, optional): If True, watch the notebook for changes and automatically export. Defaults to False.
        sandbox (bool, optional): If True, export the notebook in a sandboxed environment. Defaults to False.
        sort (str, optional): The sorting method for the exported notebook. Defaults to "topological".
            Choices:
                - "topological": Sort the notebook cells topologically.
                - "top-down": Sort the notebook cells top-down.

    Returns:
        list[str]: The command to export the notebook.
    """
    if output is None:
        output = notebook_path.replace(".py", format_ext[export_format])
        
    cmd = ["marimo", "export", export_format, notebook_path, "-o", output]

    # Watch the notebook for changes and automatically export
    if watch:
        cmd.append("--watch")
    else:
        cmd.append("--no-watch")

    # Export to HTML
    if export_format == "html":
        return _get_xcmd_html(cmd, sandbox, show_code)

    # Export to IPYNB
    if export_format == "ipynb":
        return _get_xcmd_ipynb(cmd, sandbox, show_code, sort)

    # Export to HTML WebAssembly
    if export_format == "html-wasm":
        return _get_xcmd_wasm(cmd, mode, show_code)

    return cmd

def _html_copy_process(notebook_path, output, saved_html_path=None):
    """
    Copies a saved HTML file to the specified output path.

    Args:
        notebook_path (str): The path to the notebook file.
        output (str): The path to the output file.
        saved_html_path (str, optional): The path to the saved HTML file to copy. Defaults to None.

    Returns:
        bool: True if the copy was successful, False otherwise.
    """
    
    if saved_html_path is None:
        saved_html_path = os.path.join(os.path.dirname(notebook_path),"__marimo__",os.path.basename(notebook_path).replace(".py", ".html"))
    
    if os.path.exists(saved_html_path):
        try:
            shutil.copy(saved_html_path, output)
            rich_print(f"[green]Successfully Copied[end] {saved_html_path} to {output}")
            return True
        except Exception as e:
            rich_print(f"[red]Unexpected error exporting[end] {notebook_path}: {e}")
            return False
    else:
        rich_print(f"[red]Error:[end] File not found: {saved_html_path}")
        return False

def _export_with_cmd(cmd, notebook_path, output):
    """
    Runs a command to export a notebook.

    Args:
        cmd (list[str]): The command to run.
        notebook_path (str): The path to the notebook file.
        output (str): The path to the output file.

    Returns:
        bool: True if the export was successful, False otherwise.
    """
    try:
        subprocess.run(cmd, capture_output=True, text=True, check=True)
        rich_print(f"[green]Successfully Exported[end] {notebook_path} to {output}")
        return True
    except subprocess.CalledProcessError as e:
        rich_print(f"[red]Error exporting {notebook_path}[end]:")
        print(e.stderr)
        return False
    except Exception as e:
        rich_print(f"[red]Unexpected error exporting[end] {notebook_path}: {e}")
        return False

def export(
    notebook_path: str, output: str=None,
    export_format:str="html",   # html, html-wasm, ipynb, md, script
    mode:str="run",             # run, edit
    show_code:bool=True, watch:bool=False, sandbox:bool=False, 
    sort:str="topological",      # topological, top-down
    from_saved:bool=False,
    saved_html_path:str=None
    ) -> bool:


    """
    Exports a notebook to a specified format and output location.

    Args:
        notebook_path (str): The path to the notebook file to be exported.
        output (str, optional): The path to the output file. If not provided, 
            it defaults to the notebook path with an appropriate extension.
        export_format (str, optional): The format to export the notebook to.
            Defaults to "html". Options include:
                - "html": Static HTML file.
                - "html-wasm": HTML file with WebAssembly support.
                - "ipynb": IPython notebook file.
                - "md": Markdown file.
                - "script": Python script file.
        mode (str, optional): The export mode. Defaults to "run".
            Options include:
                - "run": Export the notebook in a runnable form.
                - "edit": Export the notebook in an editable form.
        show_code (bool, optional): Whether to include the code in the exported 
            notebook. Defaults to True.
        watch (bool, optional): Whether to watch the notebook for changes and 
            automatically export. Defaults to False.
        sandbox (bool, optional): Whether to export the notebook in a sandboxed 
            environment. Defaults to False.
        sort (str, optional): The method to sort the exported notebook cells.
            Defaults to "topological". Options include:
                - "topological": Sort cells topologically.
                - "top-down": Sort cells top-down.
        from_saved (bool, optional): Whether to export from a saved HTML file. 
            Defaults to False.
        saved_html_path (str, optional): The path to the saved HTML file to copy 
            if `from_saved` is True. Defaults to None.

    Returns:
        bool: True if the export was successful, False otherwise.
    """

    if output is None:
        output = notebook_path.replace(".py", format_ext[export_format])
    os.makedirs(os.path.dirname(output), exist_ok=True)

    if from_saved:
        return _html_copy_process(notebook_path, output, saved_html_path)

    
    else:
        cmd = get_export_cmd(notebook_path, output, export_format, mode, show_code, watch, sandbox, sort)
        return _export_with_cmd(cmd, notebook_path, output)


def export_executable(notebook_path: str, output: str=None, watch=False, sandbox=False) -> bool:
    """
    Exports a notebook as an executable notebook.

    Args:
        notebook_path (str): The path to the notebook file.
        output (str, optional): The path to the output file. Defaults to None.
        watch (bool, optional): Whether to watch the notebook for changes and 
            automatically export. Defaults to False.
        sandbox (bool, optional): Whether to export the notebook in a sandboxed 
            environment. Defaults to False.

    Returns:
        bool: True if the export was successful, False otherwise.
    """
    rich_print(f"\n[yellow]Exporting[end] to [blue]Executable[end]: {notebook_path}")
    return export(
        notebook_path=notebook_path,
        output=output,
        export_format="html-wasm",
        mode="run",
        show_code=True,
        watch=watch,
        sandbox=sandbox,
        sort="topological"
    )

def export_editable(notebook_path: str, output: str=None, watch=False) -> bool:
    """
    Exports a notebook as an editable notebook.

    Args:
        notebook_path (str): The path to the notebook file.
        output (str, optional): The path to the output file. Defaults to None.
        watch (bool, optional): Whether to watch the notebook for changes and 
            automatically export. Defaults to False.

    Returns:
        bool: True if the export was successful, False otherwise.
    """
    rich_print(f"\n[yellow]Exporting[end] to [blue]Editable[end]: {notebook_path}")
    return export(
        notebook_path=notebook_path,
        output=output,
        export_format="html-wasm",
        mode="edit",
        show_code=True,
        watch=watch
    )

def export_app(notebook_path: str, output: str=None) -> bool:
    """
    Exports a notebook as a standalone app.

    Args:
        notebook_path (str): The path to the notebook file.
        output (str, optional): The path to the output file. Defaults to None.

    Returns:
        bool: True if the export was successful, False otherwise.
    """
    rich_print(f"\n[yellow]Exporting[end] to [blue]App[end]: {notebook_path}")
    return export(
        notebook_path=notebook_path,
        output=output,
        export_format="html-wasm",
        mode="run",
        show_code=False
    )

def export_html(notebook_path: str, output: str=None, output_dir: str="_site", show_code:bool=True, from_saved:bool=False, saved_html_path=None) -> bool:
    """
    Exports a notebook to HTML format.

    Args:
        notebook_path (str): The path to the notebook file.
        output (str, optional): The path to the output file. Defaults to None.
        output_dir (str, optional): The directory where the exported HTML file will
            be saved. Defaults to "_site".
        show_code (bool, optional): Whether to include the code in the exported 
            notebook. Defaults to True.
        from_saved (bool, optional): Whether to export from a saved HTML file. 
            Defaults to False.
        saved_html_path (str, optional): The path to the saved HTML file to copy 
            if `from_saved` is True. Defaults to None.

    Returns:
        bool: True if the export was successful, False otherwise.
    """
    rich_print(f"\n[yellow]Exporting[end] to [blue]HTML{"-save" if from_saved else ""}[end]: {notebook_path}")
    return export(
        notebook_path=notebook_path,
        output=output,
        export_format="html",
        show_code=show_code,
        from_saved=from_saved,
        saved_html_path=saved_html_path
    )
