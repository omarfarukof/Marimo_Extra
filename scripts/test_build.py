import os
import shutil
import pandas as pd

def _run_gen_index_csv():
    """
    Runs the gen_index_csv.py script in the scripts directory if it exists.
    
    The script is expected to generate an index.csv file. 
    Which specifies the Marimo Notebooks' names, paths, export paths and types, etc . 
    By default, the index.csv file is generated in the public directory, 
    and exported notebooks are saving them to the _site directory.
    """
    if os.path.exists(os.path.join("scripts", "gen_index_csv.py")):
        os.system("uv run scripts/gen_index_csv.py")
    else:
        print("No scripts/gen_index_csv.py found")


def _run_website_build():
    """
    Runs the website_build.py script in the scripts directory if it exists.
    
    The script is expected to generate the website by exporting the notebooks
    specified in the index.csv file. By default, the index.csv file is generated 
    in the public directory, and exported notebooks are saving them
    to the _site directory.
    """
    if os.path.exists(os.path.join("scripts", "website_build.py")):
        os.system("uv run scripts/website_build.py")
    else:
        print("No scripts/website_build.py found")

def _run_web_server():
    """
    Runs the web server for the website by running the uv command
    "uv run -m http.server -d _site".
    
    This command starts a web server serving the files in the _site directory.
    """
    os.system("uv run -m http.server -d _site")

def _add_test_csv():
    """
    Modifies the index.csv file in the public directory to include a special
    test notebook entry. The entry is for the test_index.py notebook, which
    is used for testing purposes. The entry is added by modifying the
    'NB_Path' column of the index.csv file to point to the test_index.py
    notebook for the row where 'HTML_Path' is 'index.html'.
    """
    csv = pd.read_csv( os.path.join('public' , 'index.csv'))
    csv.loc[csv['HTML_Path'] == 'index.html', 'NB_Path'] = 'test_index.py'
    csv.to_csv( os.path.join('public' , 'index.csv'), index=False)

def _run_uv_build():
    """
    Executes the UV build command to build the project.

    This function invokes the "uv build" command using the operating system's
    shell. It is expected to be used in scenarios where building the project
    is necessary, such as preparing for deployment or testing.
    """
    os.system("uv build")

def _set_wheel_for_test(dist_path='dist', test_dist_path='public'):
    """
    Copies the wheel built by uv to the test directory, to prepare it for testing.
    
    This function is used to set up the wheel built by uv for testing purposes.
    It takes two optional parameters, dist_path and test_dist_path. The default
    values are 'dist' and 'public' respectively.
    
    The function creates the test_dist_path directory if it does not exist,
    and then copies the entire directory tree from dist_path to test_dist_path.
    The .gitignore file is ignored during the copy process.
    """
    _ignore_file = ['.gitignore']
    os.makedirs(test_dist_path, exist_ok=True)
    shutil.copytree(dist_path, test_dist_path, ignore=lambda path, names: _ignore_file, dirs_exist_ok=True)



def test_build():
    """
    Runs the test build process for Marimo Extra.

    This function runs the following steps to prepare the Marimo Extra project for testing:
    1. Builds the project using the "uv build" command.
    2. Copies the built wheel to the test directory.
    3. Generates the index.csv file containing the notebook metadata.
    4. Modifies the index.csv file to include the test notebook entry.
    5. Builds the website using the website_build.py script.
    6. Runs the web server to serve the generated website.
    """
    _run_uv_build()
    _set_wheel_for_test()
    _run_gen_index_csv()
    _add_test_csv()
    _run_website_build()
    _run_web_server()

if __name__ == "__main__":
    test_build()