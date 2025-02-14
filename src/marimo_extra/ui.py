import marimo as mo
import numpy as np
import pandas as pd
from marimo_extra.utils import index_csv_to_dict

color = {
    "light_gray": "#CCCCCC",
    "light_gray_2": "#E5E5E5",
    "light_gray_3": "#F5F5F5",
    "light_green": "#CCFFCC"
}

def card(name: str|list, thumbnail=None, content=None , link="", thum_width=200, thum_height=150):
    if isinstance(name, list):
        thumbnail = name[1]
        content = name[2]
        link = name[3]
        name = name[0]
    else:
        if thumbnail is None:
            thumbnail = mo.md(f"<i> {name} </i>")
        if content is None:
            content = mo.md(f"Details for {name}")
    thumbnail = mo.image(src=thumbnail, alt=f"{name}", rounded=True, width=thum_width, height=thum_height)
    open_link = frame(content=mo.md(f"<a href=\"{link}\">&nbsp; Open &nbsp;</a>\n"), padding=0 , border_color="#CCFFCC", border_width=1, border_redius=7, bg_color="#CCFFCC")
    title_link = mo.md(f"<h3>{name}</h3>")
    title = mo.hstack([title_link, open_link])
    view = mo.md(f"{mo.center(thumbnail)}<br>{content}<br>{title}")


    return frame(view, box_min_width=270, box_min_height=80)


def Gallery(data: list[dict] , max_column=2 , v_gap=2, h_gap=2, orientation = "vertical"):
    search_box = mo.ui.text(
        placeholder="Search", 
        label=f"{mo.icon('lucide:search')}",
        on_change=lambda x: _gallary_view()
        )
    orientation_box = mo.ui.dropdown( 
        label="Orientation" , 
        options=["vertical" , "horizontal", "mixed"] , 
        value=orientation,
        on_change=lambda x: _gallary_view()
        ) 
    controller = mo.hstack([search_box, orientation_box])

    def _gallary_view():
        orientation = orientation_box.value
        search = search_box.value

        mo.output.append(controller)

        if search != "":
            mo.output.append( mo.md(f"Search: {search}") )

        cards = _get_cards(search=search)

        if len(cards) == 0:
            mo.output.append( mo.md("<div style=\"text-align: center;\">No results</div>"))

        _card_view(cards, orientation)

    def _card_view(cards, orientation):
        if orientation == "vertical":
            mo.output.append( mo.vstack(cards, gap=v_gap) )
        elif orientation == "horizontal":
            mo.output.append( mo.hstack(cards, gap=h_gap) )
        elif orientation == "mixed":
            _view = []
            for i in range(0, len(cards), max_column):
                _view.append(mo.hstack(cards[i:i+max_column], justify="start", align="stretch", gap=h_gap) )
            mo.output.append( mo.vstack(_view, gap=v_gap) )

    mo.output.append(controller)
    _card_view(_get_cards(), orientation)



def _get_cards(search=""):
    """
    Get a list of marimo cards based on the current index.csv file.

    Returns:
        list: A list of marimo cards.
    """
    cards = []
    for item in index_csv_to_dict(search=search):
        cards.append(
            card(
                name=item["name"],
                thumbnail=item["thumbnail"],
                content=item["content"],
                link=item["link"]
            )
            )
    return cards


def frame(content, box_min_width=10, box_min_height=10, padding=5, border_width=2, border_redius=10 , border_type="solid", border_color="#CCCCCC", bg_color="", margin_size=10):
    return mo.Html( f"<div style='min-width: {box_min_width}px; min-height: {box_min_height}px; background-color: {bg_color}; border: {border_width}px {border_type} {border_color}; border-radius: {border_redius}px; padding: {padding}px;'> {content} </div>" )
