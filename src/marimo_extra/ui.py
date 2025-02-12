import marimo as mo
import numpy as np
import pandas as pd

color = {
    "light_gray": "#CCCCCC",
    "light_gray_2": "#E5E5E5",
    "light_gray_3": "#F5F5F5",
    "light_green": "#CCFFCC"
}

def card(name: str|list, thumbnail=None, content=None , link=""):
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
    # thumbnail = mo.md(f"<img src=\"{thumbnail}\" width=\"100%\"/ alt=\" {name} \">")
    thumbnail = mo.image(src=thumbnail, alt=f"{name}", rounded=True)
    open_link = frame(content=mo.md(f"<a href=\"{link}\">&nbsp; Open &nbsp;</a>\n"), padding=0 , border_color="#CCFFCC", border_width=1, border_redius=7, bg_color="#CCFFCC")
    title_link = mo.md(f"<h3>{name}</h3>")
    title = mo.hstack([title_link, open_link])
    view = mo.md(f"{mo.center(thumbnail)}<br>{content}<br>{title}")

    # out = mo.accordion({"#"+name: view} , multiple=True)

    return frame(view, box_min_width=270, box_min_height=80)

def gallery(data: list[str] , style="vartical" ,max_column=2 , ):
    search_box = mo.ui.text(placeholder="Search", label=f"{mo.icon('lucide:search')}")
    mo.output.append(search_box)

    if isinstance(data, pd.DataFrame):
        cards = []
        for inx, notebook in data.iterrows():
            cards.append(
                card(
                    name=notebook["Name"], 
                    link=notebook["Path"], 
                    thumbnail=notebook["Thumbnail"] , 
                    content=notebook["Tags"]))
    elif isinstance(data[0], np.ndarray) or isinstance(data[0], list):
        cards = []
        for notebook in data:
            # print("Notebook: ", notebook)
            cards.append(card(name=notebook[0], link=notebook[1], thumbnail=notebook[3] , content=notebook[4]))
    else:
        cards = [card(name=data) , ]
        # print("Not List")
    if style == "vartical":
        mo.output.append( mo.vstack(cards) )
    elif style == "horizontal":
        for i in range(0, len(cards), max_column):
            mo.output.append(mo.hstack(cards[i:i+max_column], justify="center", align="stretch"))



def frame(content, box_min_width=10, box_min_height=10, padding=5, border_width=2, border_redius=10 , border_type="solid", border_color="#CCCCCC", bg_color="", margin_size=10):
    return mo.Html( f"<div style='min-width: {box_min_width}px; min-height: {box_min_height}px; background-color: {bg_color}; border: {border_width}px {border_type} {border_color}; border-radius: {border_redius}px; padding: {padding}px;'> {content} </div>" )
    # content_html = f"<div style='line-height: {line_height}px'>{content}</div>"
    # return mo.Html(border(content))
    # return mo.Html(
    #     # f"<div style='min-width: {box_size}px; min-height: {box_size}px; background-color: orange; text-align: center; line-height: {box_size}px'>{content}</div>"
    #     f"<div style='min-width: {box_min_width}px; min-height: {box_min_height}px;  line-height: {line_height}px; margin: {margin_size}px; border: {border_width}px solid #00FF00;'>{content}</div>"
    # )