import marimo

__generated_with = "0.11.0"
app = marimo.App(width="full", app_title="Index")


@app.cell
def _(mo):
    mo.md(r"""# Hello""")
    return


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    return mo, pd


@app.cell(hide_code=True)
def _(mo):
    mo.sidebar(
        [
            mo.md("# marimo"),
            mo.nav_menu(
                {
                    "#home": f"{mo.icon('lucide:home')} Home",
                    "#about": f"{mo.icon('lucide:user')} About",
                    "#contact": f"{mo.icon('lucide:phone')} Contact",
                    "Links": {
                        "https://twitter.com/marimo_io": "Twitter",
                        "https://github.com/marimo-team/marimo": "GitHub",
                    },
                },
                orientation="vertical",
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _():
    import marimo_extra as me
    return (me,)


@app.cell(hide_code=True)
def _():
    # card = [
    #     me.ui.card(name="Gallary" , thumbnail=None, content="Tag: ML, Python", link="/notebooks/fibonacci.py"),
    #     me.ui.card(name="Gallary" , thumbnail=None, content="Tag: ML, Python", link="/notebooks/fibonacci.py"),

    #     me.ui.card(name="Gallary" , thumbnail=None, content="Tag: ML, Python", link="/notebooks/fibonacci.py"),
    #     me.ui.card(name="Gallary" , thumbnail=None, content="Tag: ML, Python", link="/notebooks/fibonacci.py")]
    # for c in card:
    #     mo.output.append(c)
    return


@app.cell
def _():
    return


@app.cell
def _(me, pd):
    import os
    notebooks = pd.read_csv(os.path.join('public', 'index.csv'))
    notebooks
    me.ui.gallery(data = notebooks)
    return notebooks, os


@app.cell
def _():
    # for notebook in notebooks:
    #     print("Name: " , notebook[0], "Link: ", notebook[1], "Types: ", notebook[2], "Thumbnail: ", notebook[3], "Tags: ", notebook[4])
    return


if __name__ == "__main__":
    app.run()
