import os
import pandas as pd
import marimo as mo

color = {
    "[red]": "\033[31m",
    "[green]": "\033[32m",
    "[yellow]": "\033[33m",
    "[blue]": "\033[34m",
    "[magenta]": "\033[35m",
    "[cyan]": "\033[36m",
    "[white]": "\033[37m",
    "[end]": "\033[0m",
    "[bold]": "\033[1m",
    "[underline]": "\033[4m",
    "[italic]": "\033[3m",

}

def rich_print(message):
    """
    Prints a message with color and style formatting.

    This function replaces color and style tags in the provided message
    with terminal escape codes to print formatted text to the console.

    Available color and style tags:
    - [red]: Red text
    - [green]: Green text
    - [yellow]: Yellow text
    - [blue]: Blue text
    - [magenta]: Magenta text
    - [cyan]: Cyan text
    - [white]: White text
    - [end]: Reset to default text color and style
    - [bold]: Bold text
    - [underline]: Underlined text
    - [italic]: Italic text

    Args:
        message (str): The message containing color and style tags.
    """

    for old, new in color.items():
        message = message.replace(old, new)
    print(message)


def add_row_csv(out, new_row):
    """
    Adds a row to the given dataframe.

    Args:
        out (pd.DataFrame): The dataframe to add a row to.
        new_row (list): A list containing the values to add as a new row.

    Returns:
        pd.DataFrame: The dataframe with the added row.
    """
    out.loc[len(out)] = new_row
    return out

def _filter_out_data(notebooks: pd.DataFrame, filter_out_data: dict[list[str]]) -> pd.DataFrame:
    filter_index = notebooks.index
    for key, value in filter_out_data.items():
        filter_index = filter_index[~notebooks[key].isin(value)]
    return notebooks.loc[filter_index]
def index_csv_to_dict(
    index_csv_path: str=os.path.join(str(mo.notebook_location()), 'public', 'index.csv'),
    index_to_dict_names = {
        'Name': 'name',
        'HTML_Path': 'link',
        'Thumbnail': 'thumbnail',
        'Tags': 'content'
    },
    filter_out_data= {
        "Name": ['Home']
        },
    search: str = "",
    ) -> dict:
    """
    Reads a CSV file at the given path and returns a dictionary of dictionaries.

    The resulting dictionary will have the following structure:
    {
        'name': str,
        'link': str,
        'thumbnail': str,
        'content': str
    }

    The dictionary keys are specified by the `index_to_dict_names` argument, and the
    values are the corresponding columns in the CSV file.

    The `filter_out_data` argument is a dictionary of filter criteria, where the keys
    are column names and the values are lists of values to exclude from the resulting
    dictionary.

    Args:
        index_csv_path (str): The path to the CSV file to read. Defaults to
            `os.path.join('public', 'index.csv')`.
        index_to_dict_names (dict): A dictionary of column names to dictionary keys.
            Defaults to `{'Name': 'name', 'HTML_Path': 'link', 'Thumbnail': 'thumbnail', 'Tags': 'content'}`.
        filter_out_data (dict): A dictionary of filter criteria. Defaults to
            `{'Name': ['Home']}`.

    Returns:
        dict: A dictionary of dictionaries, where each inner dictionary represents a
            row in the CSV file.
    """
    notebooks = pd.read_csv(index_csv_path)
    notebooks = _filter_out_data(notebooks, filter_out_data)
    if search != "":
        notebooks = notebooks[notebooks["Name"].str.contains(search, case=False)]
    notebooks = notebooks[index_to_dict_names.keys()].rename( columns = index_to_dict_names )
    return notebooks.fillna("").to_dict('records')

def index_csv_to_nav_dict(
    home_dir: str = os.path.basename(str(mo.notebook_location())),
    index_csv_path: str=os.path.join('public', 'index.csv'),
    index_names = {
        'name': 'Name',
        'link': 'HTML_Path'
    },
    filter_out_data= {
        "Name": ['Home']
        } ) -> dict:
    _nb = pd.read_csv(index_csv_path)
    _nb = _filter_out_data(_nb, filter_out_data)[index_names.values()]
    _nb[index_names['link']] = _nb[index_names['link']].apply(lambda x: os.path.join(" ", home_dir, x).replace(" ",""))

    return dict( zip( _nb[index_names['link']], _nb[index_names['name']] ) )


    


def alter_dict_key_value(dic: dict[str]):
    return {value:key for key,value in dic.items()}