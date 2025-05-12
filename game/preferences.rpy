    #########################
    #   Preference Screen   #
    #########################

image return_idle:
    "gui/screens/return_idle.png"
    zoom 0.75

image return_hover:
    "gui/screens/return_hover.png"
    zoom 0.75

screen preferences():

    tag menu

    # use game_menu(_("Preferences"), scroll="viewport"):

    # Background image
    add "gui/screens/preferences_bg.png" xysize (config.screen_width, config.screen_height)

    # Return Button
    imagebutton:
        idle "return_idle"
        hover "return_hover"
        xpos 1605
        ypos 555
        action Return()


    vbox:

        xalign 0.6
        yalign 0.57

        hbox:
            box_wrap True

            xalign 0.53

            if renpy.variant("pc") or renpy.variant("web"):

                vbox:
                    style_prefix "radio"
                    label _("DISPLAY")
                    
                    # space beween label and textbuttons
                    null height 4

                    spacing 8
                    # textbutton _("Window") action Preference("display", "window")
                    textbutton _("Window"):
                        action Preference("display", "window")
                        style "radio_button"
                        selected Preference("display", "window").get_selected()
                        left_padding 50
                    
                    # textbutton _("Fullscreen") action Preference("display", "fullscreen")
                    textbutton _("Fullscreen"):
                        action Preference("display", "fullscreen")
                        style "radio_button"
                        selected Preference("display", "fullscreen").get_selected()
                        left_padding 50

            vbox:
                style_prefix "check"
                label _("SKIP")

                # space beween label and textbuttons
                null height 4

                spacing 8

                # textbutton _("Unseen Text") action Preference("skip", "toggle"):
                # textbutton _("After Choices") action Preference("after choices", "toggle")
                # textbutton _("Transitions") action InvertSelected(Preference("transitions", "toggle"))

                textbutton _("Unseen Text"):
                    action Preference("skip", "toggle")
                    style "check_button"
                    left_padding 50

                textbutton _("After Choices"):
                    action Preference("after choices", "toggle")
                    style "check_button"
                    left_padding 50

                textbutton _("Transitions"):
                    action InvertSelected(Preference("transitions", "toggle"))
                    style "check_button"
                    left_padding 50

            ## Additional vboxes of type "radio_pref" or "check_pref" can be
            ## added here, to add additional creator-defined preferences.

        # space difference beween radio/check buttons & sliders
        null height (4 * gui.pref_spacing)

        hbox:
            style_prefix "slider"
            box_wrap True

            vbox:

                label _("Text Speed")
                null height 8
                bar value Preference("text speed"):
                    thumb_offset 22

                null height 16


                label _("Auto-Forward Time")
                null height 8
                bar value Preference("auto-forward time"):
                    thumb_offset 22

            vbox:
            
                if config.has_music:
                    label _("Music Volume")
                    null height 8

                    hbox:
                        bar value Preference("music volume"):
                            thumb_offset 22
                null height 16

                if config.has_sound:

                    label _("Sound Volume")
                    null height 8

                    hbox:
                        bar value Preference("sound volume") style_prefix "slider":
                            thumb_offset 22

                        if config.sample_sound:
                            textbutton _("Test") action Play("sound", config.sample_sound)

                # null height 14
                # if config.has_voice:
                #     label _("Voice Volume")
                #     null height 9

                #     hbox:
                #         bar value Preference("voice volume"):
                #             thumb_offset 22
                #         null height 9

                #         if config.sample_voice:
                #             textbutton _("Test") action Play("voice", config.sample_voice)

                null height 16
                if config.has_music or config.has_sound or config.has_voice:
                    null height gui.pref_spacing

                    textbutton _("Mute All"):
                        action Preference("all mute", "toggle")
                        style "mute_all_button"
                        left_padding 50


style pref_label is gui_label
style pref_label_text is gui_label_text
style pref_vbox is vbox

style radio_label is pref_label
style radio_label_text is pref_label_text
style radio_button is gui_button
style radio_button_text is gui_button_text
style radio_vbox is pref_vbox

style check_label is pref_label
style check_label_text is pref_label_text
style check_button is gui_button
style check_button_text is gui_button_text
style check_vbox is pref_vbox

style slider_label is pref_label
style slider_label_text is pref_label_text
style slider_slider is gui_slider
style slider_button is gui_button
style slider_button_text is gui_button_text
style slider_pref_vbox is pref_vbox

style mute_all_button is check_button
style mute_all_button_text is check_button_text


style pref_label:
    top_margin gui.pref_spacing
    bottom_margin 3

# Headers
style pref_label_text:
    yalign 1.0
    font 'fonts/Sora-Regular.ttf'
    color '#E3BD6A'
    size 26

style pref_vbox:
    xsize 338

style radio_vbox:
    spacing gui.pref_button_spacing
    
style radio_button:
    properties gui.button_properties("radio_button")
    foreground "gui/button/radio_[prefix_]foreground.png"

style radio_button_text:
    properties gui.text_properties("radio_button")
    font 'fonts/Sora-Regular.ttf'
    size 27
    color "#B8B5AE"
    hover_color "#F1E293"
    selected_color "#E3BD6A"


style check_vbox:
    spacing gui.pref_button_spacing

style check_button:
    properties gui.button_properties("check_button")
    foreground "gui/button/check_[prefix_]foreground.png"

style check_button_text:
    properties gui.text_properties("check_button")
    font 'fonts/Sora-Regular.ttf'
    size 27
    color "#B8B5AE"
    hover_color "#F1E293"
    selected_color "#E3BD6A"


style slider_slider:
    xsize 525

style slider_button:
    properties gui.button_properties("slider_button")
    yalign 0.5
    left_margin 15

style slider_button_text:
    properties gui.text_properties("slider_button")

style slider_vbox:
    xsize 675