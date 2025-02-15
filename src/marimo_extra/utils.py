import os
import pandas as pd
import marimo as mo
import requests

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
    home_dir: str = str(mo.notebook_location()),
    index_csv_path: str=os.path.join('public', 'index.csv'),
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
    ) -> list[dict]:

    """
    Converts the contents of an index CSV file to a list of dictionaries.

    This function reads the specified index CSV file, filters out specified
    data, and converts the remaining data to a list of dictionaries with
    specified key mappings. It also supports searching for specific entries
    in the 'Name' column.

    Args:
        home_dir (str): The base directory of the Marimo notebook.
            Defaults to the directory of the current Marimo notebook.
        index_csv_path (str): The path to the index CSV file relative to 
            the home directory. Defaults to 'public/index.csv'.
        index_to_dict_names (dict): A dictionary mapping CSV column names to
            dictionary keys. Defaults to mapping 'Name' to 'name', 'HTML_Path'
            to 'link', 'Thumbnail' to 'thumbnail', and 'Tags' to 'content'.
        filter_out_data (dict): A dictionary specifying the data to filter out
            from the CSV. Defaults to filtering out rows with 'Name' equal to 'Home'.
        search (str): A string to search for in the 'Name' column. If specified,
            only rows containing this string in the 'Name' column will be included.

    Returns:
        list[dict]: A list of dictionaries containing the filtered and mapped data
        from the index CSV file. If the file is not available, returns a list with
        a single dictionary indicating that no index CSV was found.
        Example: [{'name': 'Name', 'link': 'HTML_Path', 'thumbnail': 'Thumbnail', 'content': 'Tags'}, .. .. ]
    """

    _index_csv_fullpath = os.path.join(home_dir, index_csv_path)

    if not is_available(_index_csv_fullpath):
        return [dict(zip(index_to_dict_names.values() , ["No index.csv found","","",""]))]

    notebooks = pd.read_csv(_index_csv_fullpath)
    notebooks = _filter_out_data(notebooks, filter_out_data)
    if search != "":
        notebooks = notebooks[notebooks["Name"].str.contains(search, case=False)]
    notebooks = notebooks[index_to_dict_names.keys()].rename( columns = index_to_dict_names )
    return notebooks.fillna("").to_dict('records')

def index_csv_to_nav_dict(
    home_dir: str = str(mo.notebook_location()),
    index_csv_path: str=os.path.join('public', 'index.csv'),
    index_names = {
        'name': 'Name',
        'link': 'HTML_Path'
    },
    filter_out_data= {
        "Name": ['Home']
        } ) -> dict[str, str]:


    """
    Converts an index CSV file into a navigation dictionary.

    This function reads the specified CSV file and filters out specified
    entries. It maps the CSV columns to dictionary keys as specified by
    `index_names` and creates a dictionary where keys are links to the
    HTML files and values are the corresponding names.

    Args:
        home_dir (str): The base directory of the Marimo notebook.
            Defaults to the directory of the current Marimo notebook.
        index_csv_path (str): The path to the index CSV file relative to 
            the home directory. Defaults to 'public/index.csv'.
        index_names (dict): A dictionary mapping dictionary keys to CSV
            column names. Defaults to mapping 'name' to 'Name' and 'link'
            to 'HTML_Path'.
        filter_out_data (dict): A dictionary specifying the data to filter 
            out from the CSV. Defaults to filtering out rows with 'Name'
            equal to 'Home'.

    Returns:
        dict[str, str]: A dictionary where the keys are the full paths to
        HTML files and the values are the corresponding names. If the file
        is not available, returns a dictionary with a placeholder indicating
        that no index CSV was found. 
        Example: {'index.html': 'Home', .. ..}
    """

    _index_csv_fullpath = os.path.join(home_dir, index_csv_path)

    if not is_available(path = _index_csv_fullpath):
        return {"#": "No index.csv found"}

    _nb = pd.read_csv(_index_csv_fullpath)
    _nb = _filter_out_data(_nb, filter_out_data)[index_names.values()]
    _nb[index_names['link']] = _nb[index_names['link']].apply(lambda x: os.path.join(home_dir, x))#.replace(" ",""))

    return dict( zip( _nb[index_names['link']], _nb[index_names['name']] ) )


def running_in_server():
    return str(mo.notebook_location())[:4] == "http"

def is_available(path: str):
    if running_in_server():
        try:
            response = requests.head(path)
            if response.status_code != 200:
                print(f"No index.csv found at {path}")
                return False
            else:
                return True
        except requests.exceptions.RequestException as err:
            print("Error:", err)
            return False
    else:
        return os.path.exists(path)



def alter_dict_key_value(dic: dict[str]):
    return {value:key for key,value in dic.items()}