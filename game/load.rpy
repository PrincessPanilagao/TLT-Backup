    ###################
    #   Load Screen   #
    ###################

screen load():

    tag menu

    # Background image
    add "gui/screens/load_bg.png" xysize (config.screen_width, config.screen_height)

    # Return Button
    imagebutton:
        # idle "gui/screens/return_idle.png"
        # hover "gui/screens/return_hover.png"
        idle "return_idle"
        hover "return_hover"
        xpos 1605
        ypos 550
        action Return()

    use file_slots(_("Load"))

screen file_slots(title):

    default page_name_value = FilePageNameInputValue(pattern=_("PAGE {}"), auto=_("AUTOMATIC SAVES"), quick=_("QUICK SAVES"))

    fixed:

        ## This ensures the input will get the enter event before any of the
        ## buttons do.
        order_reverse True

        ## The page name, which can be edited by clicking on a button.
        button:
            style "page_label"

            key_events True
            xalign 0.5
            action page_name_value.Toggle()

            input:
                style "page_label_text"
                value page_name_value

        ## The grid of file slots.
        grid gui.file_slot_cols gui.file_slot_rows:
            style_prefix "slot"

            xalign 0.5
            yalign 0.54

            spacing gui.slot_spacing

            for i in range(gui.file_slot_cols * gui.file_slot_rows):

                $ slot = i + 1

                button:
                    action FileAction(slot)

                    has vbox
                    spacing 10

                    add FileScreenshot(slot) xalign 0.5

                    text FileTime(slot, format=_("{#file_time}%A, %B %d %Y, %H:%M"), empty=_("Empty Slot")):
                        style "slot_time_text"

                    text FileSaveName(slot):
                        style "slot_name_text"

                    key "save_delete" action FileDelete(slot)

        ## Buttons to access other pages.
        vbox:
            style_prefix "page"

            xalign 0.5
            yalign 0.88

            hbox:
                xalign 0.5

                spacing gui.page_spacing

                textbutton _("<") action FilePagePrevious()
                key "save_page_prev" action FilePagePrevious()

                if config.has_autosave:
                    textbutton _("{#auto_page}A") action FilePage("auto")

                if config.has_quicksave:
                    textbutton _("{#quick_page}Q") action FilePage("quick")

                ## range(1, 10) gives the numbers from 1 to 9.
                for page in range(1, 10):
                    textbutton "[page]" action FilePage(page)

                textbutton _(">") action FilePageNext()
                key "save_page_next" action FilePageNext()

            if config.has_sync:
                if CurrentScreenName() == "save":
                    textbutton _("Upload Sync"):
                        action UploadSync()
                        xalign 0.5
                else:
                    textbutton _("Download Sync"):
                        action DownloadSync()
                        xalign 0.5


# style page_label is gui_label
# style page_label_text is gui_label_text
# style page_button is gui_button
# style page_button_text is gui_button_text

# style slot_button is gui_button
# style slot_button_text is gui_button_text
# style slot_time_text is slot_button_text
# style slot_name_text is slot_button_text


style page_label:
    xpadding 75
    ypadding 5
    yalign 0.18

# Label on top of page (Automatic Save/Quick Save/Page 1, 2, etc...)
style page_label_text:
    textalign 0.5
    layout "subtitle"
    hover_color gui.hover_color
    font 'fonts/Sora-Regular.ttf'
    color '#E3BD6A'
    size 25

style page_button:
    properties gui.button_properties("page_button")

# Navigation button text
style page_button_text:
    # properties gui.text_properties("page_button")
    font 'fonts/Sora-Regular.ttf'
    size 24
    color "#B8B5AE"
    hover_color "#F1E293"
    selected_color "#E3BD6A"

style slot_button:
    properties gui.button_properties("slot_button")
    size 24

# Text below saved screenshot
style slot_button_text:
    # properties gui.text_properties("slot_button")
    font 'fonts/Sora-Regular.ttf'

style slot_time_text:
    size 20
    color "#E0B981"

style slot_name_text:
    size 20
    color "#E0B981"