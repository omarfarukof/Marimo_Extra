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
    if sandbox:
        cmd.append("--sandbox")

    if show_code:
        cmd.append("--include-code")
    else:
        cmd.append("--no-include-code")
    return cmd

def _get_xcmd_ipynb(cmd, sandbox, show_code, sort):
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


    if output is None:
        output = notebook_path.replace(".py", format_ext[export_format])
    os.makedirs(os.path.dirname(output), exist_ok=True)

    if from_saved:
        return _html_copy_process(notebook_path, output, saved_html_path)

    
    else:
        cmd = get_export_cmd(notebook_path, output, export_format, mode, show_code, watch, sandbox, sort)
        return _export_with_cmd(cmd, notebook_path, output)


def export_executable(notebook_path: str, output: str=None, watch=False, sandbox=False) -> bool:
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
    rich_print(f"\n[yellow]Exporting[end] to [blue]App[end]: {notebook_path}")
    return export(
        notebook_path=notebook_path,
        output=output,
        export_format="html-wasm",
        mode="run",
        show_code=False
    )

def export_html(notebook_path: str, output: str=None, output_dir: str="_site", show_code:bool=True, from_saved:bool=False, saved_html_path=None) -> bool:
    rich_print(f"\n[yellow]Exporting[end] to [blue]HTML{"-save" if from_saved else ""}[end]: {notebook_path}")
    return export(
        notebook_path=notebook_path,
        output=output,
        export_format="html",
        show_code=show_code,
        from_saved=from_saved,
        saved_html_path=saved_html_path
    )


def test(file_name):
    output_dir = "_site"
    if os.path.exists(output_dir): 
        shutil.rmtree(output_dir)
        rich_print(f"Removed [blue]{output_dir}[end] folder")
    output = f"_site/{file_name.replace('.py', '')}"

    export(notebook_path=file_name, output=f"{output}.html")
    export_executable(notebook_path=file_name, output=f"{output}_exe.html")
    export_editable(notebook_path=file_name, output=f"{output}_edit.html")
    export_app(notebook_path=file_name, output=f"{output}_app.html")
    export_html(notebook_path=file_name, output=f"{output}_html.html")
    export_html(notebook_path=file_name, output=f"{output}_saved_html.html", from_saved=True)

    # # Run Server
    # python -m http.server -d _site
    # or
    # uv run python -m http.server -d _site

# # For Testing
if __name__ == "__main__":
    # test("notebooks/fibonacci.py")
    pass