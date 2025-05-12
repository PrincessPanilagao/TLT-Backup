    ####################
    #   About Screen   #
    ####################

image return_idle:
    "gui/screens/return_idle.png"
    zoom 0.75

image return_hover:
    "gui/screens/return_hover.png"
    zoom 0.75


screen about():

    tag menu

    style_prefix "about"

    # Background image
    add "gui/screens/about_bg.png" xysize (config.screen_width, config.screen_height)

    # Return Button
    imagebutton:
        idle "return_idle"
        hover "return_hover"
        xpos 1605
        ypos 555
        action Return()


    vbox:
        xalign 0.5
        yalign 0.5
        xsize 1300

        label "[config.name!t]"
        text _("Version [config.version!t]\n")

        ## gui.about is usually set in options.rpy.
        if gui.about:
            text "[gui.about!t]\n"

        text _("Made with {a=https://www.renpy.org/}Ren'Py{/a} [renpy.version_only].\n\n[renpy.license!t]")


style about_label is gui_label
style about_label_text is gui_label_text
style about_text is gui_text

style about_label_text:
    # size gui.label_text_size
    font 'fonts/Sora-Regular.ttf'
    size 26

style about_text:
    font 'fonts/Sora-Regular.ttf'
    size 26