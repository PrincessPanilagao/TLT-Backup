    ######################
    #   History Screen   #
    ######################

image return_idle:
    "gui/screens/return_idle.png"
    zoom 0.75

image return_hover:
    "gui/screens/return_hover.png"
    zoom 0.75


image mainmenu_idle:
    "gui/screens/mainmenu_idle.png"
    zoom 0.75

image mainmenu_hover:
    "gui/screens/mainmenu_hover.png"
    zoom 0.75


screen history():
    tag menu

    ## Avoid predicting this screen, as it can be very large.
    predict False

    # Background image
    add "gui/screens/history_bg.png" xysize (config.screen_width, config.screen_height)

    # Main Menu Button
    imagebutton:
        idle "mainmenu_idle"
        hover "mainmenu_hover"
        xpos 790
        xanchor 0.5
        ypos 797
        action MainMenu()

    # Return Button
    imagebutton:
        idle "return_idle"
        hover "return_hover"
        xpos 1170
        xanchor 0.5
        ypos 800
        action Return()


    frame:
        style "game_menu_outer_frame"
        xfill True
        yfill True
        xsize 1310
        ysize 620

        xpos 0.45
        xanchor 0.5
        ypos 0.44
        yanchor 0.5


        viewport:
            scrollbars "vertical"
            mousewheel True
            draggable True
            yinitial 1.0

            vbox:
                spacing gui.history_spacing
                style_prefix "history"
                
                
                for h in _history_list:

                    window style "history_window":

                        has fixed:
                            yfit True

                        if h.who:
                            $ display_name = "Edmond" if h.who == "Edmond Quinn" else h.who

                            label display_name:
                                style "history_name"
                                substitute False
                                if "color" in h.who_args:
                                    text_color h.who_args["color"]

                        $ what = renpy.filter_text_tags(h.what, allow=gui.history_allow_tags)
                        text what:
                            substitute False

                if not _history_list:
                    label _("The dialogue history is empty.")


## This determines what tags are allowed to be displayed on the history screen.

define gui.history_allow_tags = { "alt", "noalt", "rt", "rb", "art" }


style history_window is empty

style history_name is gui_label
style history_name_text is gui_label_text
style history_text is gui_text

style history_label is gui_label
style history_label_text is gui_label_text

style history_window:
    xfill True
    ysize gui.history_height
    background None


# Character Name
style history_name:
    xpos gui.history_name_xpos
    xanchor gui.history_name_xalign
    ypos gui.history_name_ypos
    xsize gui.history_name_width

style history_name_text:
    min_width gui.history_name_width
    textalign gui.history_name_xalign
    font 'fonts/Sora-Regular.ttf'
    size 26
    color "#DAAE60"


# History Text
style history_text:
    xpos gui.history_text_xpos
    ypos gui.history_text_ypos
    xanchor gui.history_text_xalign
    xsize gui.history_text_width
    min_width gui.history_text_width
    textalign gui.history_text_xalign
    layout ("subtitle" if gui.history_text_xalign else "tex")
    font 'fonts/Sora-Regular.ttf'
    size 24
    line_spacing 1


style history_label:
    xfill True

style history_label_text:
    xalign 0.5