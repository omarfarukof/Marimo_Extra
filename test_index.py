import marimo

__generated_with = "0.11.5"
app = marimo.App(width="full", app_title="Index")


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# Hello""")
    return


@app.cell(hide_code=True)
def _(me, mo):
    mo.sidebar(
        [
            mo.md("# Marimo Extra"),
            mo.nav_menu(
                {
                    "/index.html": f"{mo.icon('lucide:home')} Home",
                    f"{mo.icon('lucide:book')} Notebooks": me.index_csv_to_nav_dict(),
                    "#about": f"{mo.icon('lucide:user')} About",
                },
                orientation="vertical",
            ),
        ]
    )
    return


@app.cell
def _(me):
    me.ui.Gallery(me.index_csv_to_dict())
    return


@app.cell
def _():
    # Imports
    return


@app.cell
async def _(mo, running_in_server):
    _marimo_extra_version = '1.0.2'
    if running_in_server():
        try:
            import micropip
            pkg = mo.notebook_location() / 'public' / f"marimo_extra-{_marimo_extra_version}-py3-none-any.whl"
            await micropip.install(str(pkg))
            import marimo_extra as me
        except Exception as e:
            print('failed to install marimo_extra')
            print(e)
    else:
        import marimo_extra as me
    return me, micropip, pkg


@app.cell
def _(mo):
    def running_in_server():
        return str(mo.notebook_location())[:4] == "http"
    return (running_in_server,)


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import os
    return mo, os, pd


if __name__ == "__main__":
    app.run()
