from customtkinter import CTkBaseClass, CTkTabview
from typing import Union, Tuple, Dict, List, Callable, Optional


class VerticalTabView(CTkTabview):
    def __init__(self,
                 master: any,
                 width: int = 300,
                 height: int = 250,
                 corner_radius: Optional[int] = None,
                 border_width: Optional[int] = None,

                 bg_color: Union[str, Tuple[str, str]] = "transparent",
                 fg_color: Optional[Union[str, Tuple[str, str]]] = None,
                 border_color: Optional[Union[str, Tuple[str, str]]] = None,

                 segmented_button_fg_color: Optional[Union[str, Tuple[str, str]]] = None,
                 segmented_button_selected_color: Optional[Union[str, Tuple[str, str]]] = None,
                 segmented_button_selected_hover_color: Optional[Union[str, Tuple[str, str]]] = None,
                 segmented_button_unselected_color: Optional[Union[str, Tuple[str, str]]] = None,
                 segmented_button_unselected_hover_color: Optional[Union[str, Tuple[str, str]]] = None,

                 text_color: Optional[Union[str, Tuple[str, str]]] = None,
                 text_color_disabled: Optional[Union[str, Tuple[str, str]]] = None,

                 command: Union[Callable, None] = None,
                 anchor: str = "center",
                 state: str = "normal",
                 **kwargs):
        super().__init__(master=master, width=width, height=height, corner_radius=corner_radius,
                         border_width=border_width,
                         bg_color=bg_color, fg_color=fg_color, border_color=border_color,
                         segmented_button_fg_color=segmented_button_fg_color,
                         segmented_button_selected_color=segmented_button_selected_color,
                         segmented_button_selected_hover_color=segmented_button_selected_hover_color,
                         segmented_button_unselected_color=segmented_button_unselected_color,
                         segmented_button_unselected_hover_color=segmented_button_unselected_hover_color,
                         text_color=text_color, text_color_disabled=text_color_disabled,
                         command=command, anchor=anchor, state=state, **kwargs)
