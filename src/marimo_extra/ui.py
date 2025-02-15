import marimo as mo
from marimo_extra.utils import index_csv_to_dict

color = {
    "light_gray": "#CCCCCC",
    "light_gray_2": "#E5E5E5",
    "light_gray_3": "#F5F5F5",
    "light_green": "#CCFFCC"
}

def card(
    name: str|list, 
    thumbnail=None, 
    content=None , 
    link="", 
    thumbnail_width=200, 
    thumbnail_height=150,
    gap=0.2 ):
    """
    Generate a card with title bar and buttons.

    Parameters:
        name (str): The name of the card.
        thumbnail (str): The path to the thumbnail. Defaults to None.
        content (str): The content of the card. Defaults to None.
        link (str): The link to the card. Defaults to an empty string.
        thumbnail_width (int): The width of the thumbnail. Defaults to 200.
        thumbnail_height (int): The height of the thumbnail. Defaults to 150.
        gap (float): The gap between vertical elements [ thumbnail, content, title bar ]. Defaults to 0.2.

    Returns:
        Card View: A marimo frame representing the card.
    """
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

    thumbnail = mo.image(
        src=thumbnail, alt=f"{name}", 
        rounded=True, width=thumbnail_width, height=thumbnail_height )

    _open_button = frame(
        content=mo.md(f"<a href=\"{link}\">&nbsp; Open &nbsp;</a>\n"), 
        padding=0 , border_color="#CCFFCC", border_width=1, border_radius=7, 
        bg_color="#CCFFCC" )
    _buttons = mo.hstack([_open_button] , gap=0.2)
    
    _title_name = mo.md(f"<h3>{name}</h3>")
    _title_bar = mo.hstack([_title_name, _buttons])

    # _view = mo.md(f"{mo.center(thumbnail)}<br>{content}<br>{_title_bar}")
    _view = mo.vstack([mo.center(thumbnail),content,_title_bar], gap=gap)
    _card = frame(_view, box_min_width=270, box_min_height=80)

    return _card


def Gallery(data: list[dict] , max_column=2 , v_gap=2, h_gap=2, orientation = "vertical"):
    """
    A function to generate a gallery view of cards based on the given data.

    It takes a list of dictionaries as an argument, where each dictionary
    represents a card. The dictionary should contain the following keys:
    - name: The name of the card.
    - thumbnail: The thumbnail of the card.
    - content: The content of the card.
    - link: The link of the card.

    It will display a search box and an orientation box above the gallery view.
    The search box allows users to search for cards by name, and the orientation
    box allows users to change the orientation of the cards.

    The gallery view will be updated based on the search query and the orientation.

    If the search query is empty, it will display all the cards.

    If the search query is not empty, but there is no matching card, it will
    display a "No results" message.

    Parameters
    ----------
    data : list[dict]
        A list of dictionaries representing the cards to display.
    max_column : int
        The maximum number of columns to display in the gallery view.
        Defaults to 2.
    v_gap : float
        The vertical gap between the cards in the gallery view.
        Defaults to 2.
    h_gap : float
        The horizontal gap between the cards in the gallery view.
        Defaults to 2.
    orientation : str
        The orientation of the cards in the gallery view. Can be "vertical",
        "horizontal", or "mixed". Defaults to "vertical".

    Returns
    -------
    None
    """
    search_box = mo.ui.text(
        placeholder="Search", 
        label=f"{mo.icon('lucide:search')}",
        on_change=lambda x: _gallery_view()
        )
    orientation_box = mo.ui.dropdown( 
        label="Orientation" , 
        options=["vertical" , "horizontal", "mixed"] , 
        value=orientation,
        on_change=lambda x: _gallery_view()
        ) 
    controller = mo.hstack([search_box, orientation_box])

    def _gallery_view():
        """
        A function to update the gallery view based on the search query.

        It takes no argument, but it updates the gallery view by reading the search
        query from the search box and the orientation from the orientation box.

        It appends the search query to the output, and then appends the card view
        based on the search query and the orientation.

        If the search query is empty, it will display all the cards.

        If the search query is not empty, but there is no matching card, it will
        display a "No results" message.

        """
        orientation = orientation_box.value
        search = search_box.value

        mo.output.append(controller)

        if search != "":
            mo.output.append( mo.md(f"Search: {search}") )

        cards = _get_cards(index_csv_to_dict(search=search))

        if len(cards) == 0:
            mo.output.append( mo.md("<div style=\"text-align: center;\">No results</div>"))

        _card_view(cards, orientation)

    def _card_view(cards, orientation):
        """
        Render a list of cards in a specific orientation.

        Parameters
        ----------
        cards : list[mo.Card]
            List of cards to render.
        orientation : str
            Orientation of the card. Can be "vertical", "horizontal", or "mixed".
        """
        if orientation == "vertical":
            mo.output.append( mo.vstack(cards, gap=v_gap) )
        elif orientation == "horizontal":
            mo.output.append( mo.hstack(cards, gap=h_gap, justify="start") )
        elif orientation == "mixed":
            _view = []
            for i in range(0, len(cards), max_column):
                _view.append(mo.hstack(cards[i:i+max_column], justify="start", align="stretch", gap=h_gap) )
            mo.output.append( mo.vstack(_view, gap=v_gap) )

    mo.output.append(controller)
    _card_view(_get_cards(), orientation)



def _get_cards(card_dict: list[dict]= index_csv_to_dict()):
    """
    Convert a list of card dictionaries into a list of card widgets.

    Args:
        card_dict (list[dict]): A list of dictionaries containing the following keys:
            - name (str): The name of the card.
            - thumbnail (str): The path to the thumbnail.
            - content (str): The content of the card.
            - link (str): The link to the card.
    Returns:
        list[mo.Html]: A list of card widgets.
    """
    cards = []
    for item in card_dict:
        cards.append(
            card(
                name=item["name"],
                thumbnail=item["thumbnail"],
                content=item["content"],
                link=item["link"]
            )
            )
    return cards


def frame(content, box_min_width=10, box_min_height=10, padding=5, border_width=2, border_radius=10 , border_type="solid", border_color="#CCCCCC", bg_color="", margin_size=10):
    return mo.Html( f"<div style='min-width: {box_min_width}px; min-height: {box_min_height}px; background-color: {bg_color}; border: {border_width}px {border_type} {border_color}; border-radius: {border_radius}px; padding: {padding}px;'> {content} </div>" )
