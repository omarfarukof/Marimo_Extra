# Marimo Extra

# Usage

1. Create `index.py` with `marimo` notebook
2. Create `scripts/website_build.py` which will be run to generate `HTML` files
3. Push to `master` branch
4. Go to repository **Settings > Pages** and change the "Source" dropdown to "GitHub Actions"
5. GitHub Actions will automatically build and deploy to Pages

# Feature

* [X] Marimo Exporter
  * [X] Generate Export CMD
  * [X] Export function (Defult: Static HTML)
  * [X] Spesial Function
    * [X] Export Executable Notebook (Run HTML-WASM)
    * [X] Export Editable Notebook (Edit HTML-WASM)
    * [X] Export App Notebook (with out code Run HTML-WASM)
* [X] Autometed Website Build
  * [ ] Generate Index Notebook
    * [X] Collect available Notebooks
      * [X] Convert Notebook with Exporter (Besed on Dir Structure)
      * [X] Link them with Marimo Navigator
