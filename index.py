import marimo

__generated_with = "0.11.0"
app = marimo.App(width="full", app_title="Index")


@app.cell
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
    import marimo_extra as me
    return (me,)


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import os
    return mo, os, pd


if __name__ == "__main__":
    app.run()
