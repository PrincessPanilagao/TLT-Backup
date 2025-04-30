    ###################
    #   Help Screen   #
    ###################

image return_idle:
    "gui/screens/return_idle.png"
    zoom 0.75

image return_hover:
    "gui/screens/return_hover.png"
    zoom 0.75

screen help():

    # Background image
    add "gui/screens/gamepad_help.png"

    # Return Button
    imagebutton:
        # idle "gui/screens/return_idle.png"
        # hover "gui/screens/return_hover.png"
        idle "return_idle"
        hover "return_hover"
        xpos 1600
        ypos 550
        action Return()

    tag menu

    default device = "keyboard"

    style_prefix "help"

    vbox:
        spacing 40
        xalign 0.44
        yalign 0.37

        hbox:
            xalign 0.73
            spacing 15

            textbutton _("KEYBOARD") action SetScreenVariable("device", "keyboard")
            textbutton _("MOUSE") action SetScreenVariable("device", "mouse")

            if GamepadExists():
                textbutton _("GAMEPAD") action SetScreenVariable("device", "gamepad")

        frame:
            ysize 400
            background None

            if device == "keyboard":
                use keyboard_help
            elif device == "mouse":
                use mouse_help
            elif device == "gamepad":
                use gamepad_help


screen keyboard_help():
    vbox:
        spacing 20
        hbox:
            label _("Enter")
            text _("Advances dialogue and activates the interface.")

        hbox:
            label _("Space")
            text _("Advances dialogue without selecting choices.")

        hbox:
            label _("Arrow Keys")
            text _("Navigate the interface.")

        hbox:
            label _("Escape")
            text _("Accesses the game menu.")

        hbox:
            label _("Ctrl")
            text _("Skips dialogue while held down.")

        hbox:
            label _("Tab")
            text _("Toggles dialogue skipping.")

        hbox:
            label _("Page Up")
            text _("Rolls back to earlier dialogue.")

        hbox:
            label _("Page Down")
            text _("Rolls forward to later dialogue.")

        hbox:
            label "H"
            text _("Hides the user interface.")

        hbox:
            label "S"
            text _("Takes a screenshot.")

        hbox:
            label "V"
            text "Toggles assistive {a=https://www.renpy.org/l/voicing}{color=#E3BD6A}self-voicing{/color}{/a}."

        hbox:
            label "Shift+A"
            text _("Opens the accessibility menu.")


screen mouse_help():
    vbox:
        spacing 20
        hbox:
            label _("Left Click")
            text _("Advances dialogue and activates the interface.")

        hbox:
            label _("Middle Click")
            text _("Hides the user interface.")

        hbox:
            label _("Right Click")
            text _("Accesses the game menu.")

        hbox:
            label _("Mouse Wheel Up")
            text _("Rolls back to earlier dialogue.")

        hbox:
            label _("Mouse Wheel Down")
            text _("Rolls forward to later dialogue.")


screen gamepad_help():
    vbox:
        spacing 20
        hbox:
            label _("Right Trigger\nA/Bottom Button")
            text _("Advances dialogue and activates the interface.")

        hbox:
            label _("Left Trigger\nLeft Shoulder")
            text _("Rolls back to earlier dialogue.")

        hbox:
            label _("Right Shoulder")
            text _("Rolls forward to later dialogue.")

        hbox:
            label _("D-Pad, Sticks")
            text _("Navigate the interface.")

        hbox:
            label _("Start, Guide, B/Right Button")
            text _("Accesses the game menu.")

        hbox:
            label _("Y/Top Button")
            text _("Hides the user interface.")

        textbutton _("{i}Calibrate{/i}"):
            action GamepadCalibrate()
            xalign 1.0
            style "help_button_text"


# style help_button is gui_button
# style help_button_text is gui_button_text
# style help_label is gui_label
# style help_label_text is gui_label_text
# style help_text is gui_text

# Holds the toggle buttons
style help_button:
    properties gui.button_properties("help_button")
    xmargin 12

# Keboard / Mouse / Gamepad
style help_button_text:
    properties gui.text_properties("help_button")
    font 'fonts/Sora-Regular.ttf'
    size 25
    color "#B8B5AE"
    hover_color "#F1E293"
    selected_color "#E3BD6A"

# Labels for key functions style
style help_label:
    xsize 375
    right_padding 30

# Key action labels
style help_label_text:
    size 24
    textalign 1.0
    font 'fonts/Sora-Regular.ttf'
    color '#E3BD6A'

# Description for key actions
style help_text:
    size 24
    font 'fonts/Sora-Regular.ttf'