import os

def run_gen_index_csv():
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


def run_website_build():
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

def run_web_server():
    """
    Runs the web server for the website by running the uv command
    "uv run -m http.server -d _site".
    
    This command starts a web server serving the files in the _site directory.
    """
    os.system("uv run -m http.server -d _site")

def _run_uv_build():
    """
    Executes the UV build command to build the project.

    This function invokes the "uv build" command using the operating system's
    shell. It is expected to be used in scenarios where building the project
    is necessary, such as preparing for deployment or testing.
    """

    os.system("uv build")

def run_web():
    """
    Executes the sequence of scripts to build and run the web server.

    This function first generates the index CSV file by running the 
    gen_index_csv.py script. It then builds the website using the 
    website_build.py script, and finally, starts the web server to 
    serve the generated website.
    """

    run_gen_index_csv()
    run_website_build()
    run_web_server()

def run_build_web():
    """
    Builds the project and runs the web server.

    This function first builds the project using the UV build command,
    and then runs the web server to serve the generated website.
    """
    _run_uv_build()
    run_web()

def run_test_build():
    """
    Runs the test_build.py script in the scripts directory if it exists.

    The test_build.py script is expected to test the build process of the
    project. It should check that the project is built correctly and that
    the generated website can be served by the web server.
    """
    if os.path.exists(os.path.join("scripts", "test_build.py")):
        os.system("uv run scripts/test_build.py")
    else:
        print("No scripts/test_build.py found")