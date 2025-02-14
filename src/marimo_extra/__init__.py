import marimo_extra.ui as ui

from marimo_extra.marimo_web import _add_row_csv, _save_record_csv
from marimo_extra.marimo_web import auto_export_notebooks_web
from marimo_extra.marimo_web import export_notebook
from marimo_extra.marimo_web import generate_index
from marimo_extra.marimo_web import record_csv
from marimo_extra.marimo_web import collect_notebooks_info

from marimo_extra.marimo_export import export
from marimo_extra.marimo_export import export_app
from marimo_extra.marimo_export import export_editable
from marimo_extra.marimo_export import export_executable
from marimo_extra.marimo_export import export_html

from marimo_extra.utils import rich_print
from marimo_extra.utils import add_row_csv
from marimo_extra.utils import index_csv_to_dict
from marimo_extra.utils import alter_dict_key_value
from marimo_extra.utils import index_csv_to_nav_dict





def hello() -> str:
    return "Hello from marimo-gh-pages-template!"
