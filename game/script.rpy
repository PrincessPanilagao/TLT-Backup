# The script of the game goes in this file.

# Mouse design
define config.mouse = {}
define config.mouse['default'] = [("gui/cursor_default.png", 0, 0)]
# define config.mouse['pressed_default'] = [ ( "gui/cursor_grab.png", 0, 0) ]
define config.mouse['button'] = [ ( "gui/cursor_pointer.png", 0, 0) ]
define config.mouse['pressed_default'] = [ ( "gui/cursor_grab.png", 0, 0 ) ]

transform small_rotated:
    rotate -5.39
    zoom 0.555
    xpos 567.5
    ypos 104

transform zoom_in:
    zoom 0.5
    xalign 0.5
    yalign 0.5
    linear 0.5 zoom 1.0


transform slide_in_from_left:
    xpos -500  # start off the screen on the left
    yalign 0.1
    linear 0.5 xpos 0  # Slide to x=0 (centered)



# Declare characters used by this game. The color argument colorizes the
# name of the character.

define e = Character("Bianca")

default letter_opened = False

init python:
    

    def dragged_func(dragged_items, dropped_on):
        if dropped_on is not None:
            if dragged_items[0].drag_name == "letter opener" and dropped_on.drag_name == "trigger":
                dragged_items[0].snap(dropped_on.x, dropped_on.y)
                renpy.store.letter_opened = True  # Set the flag
                renpy.hide_screen("tutorial_openletter")
                renpy.jump("invitation_letter")

# The game starts here.

label start:

    scene bg envelope
    with fade

    "The envelope bears the unmistakable crest of the De Montfort family. The ink glistens as though freshly penned."
    "{i}An invitation.{/i}"
    "Once, the De Montforts were the crown of high society. Sought after by businessmen, envied by debutantes, idolized by heirs."
    "Now, they are but echoes of opulence. A family faded into obscurity, their name spoken only in hushed passing of what once was."
    "And yet, tonight…their doors open once more."
    "A {i}soirée{/i}. An opportunity for a new face among old names."

    scene bg envelope 2
    call screen tutorial_openletter

    # Wait until the letter is opened (drag action completes)
    while not letter_opened:
        $ renpy.pause(0.1)  # Small pause to prevent freezing
    return


label invitation_letter:
    scene bg table with fade
    call screen invitation
    return

label next_scene:
    call screen input_name
    "Now that the invitation is opened, the story continues."


    return

screen tutorial_openletter:
    # Objective 
    add "images/objectives/objective letter.png" zoom 0.23 xalign 0.0 yalign 0.1 xoffset -30 at slide_in_from_left
    
    draggroup:
        drag:
            drag_name "letter opener"
            xpos 1294
            ypos 512
            child Transform("images/envelope/letter_opener.png", zoom=0.429)
            drag_raise True
            droppable False
            draggable True
            dragged dragged_func
        drag:
            drag_name "trigger"
            child Null(width=90, height=80)
            xpos 835
            ypos 455
            draggable False
            droppable True
            dragged dragged_func
    image "images/envelope/envelope_front.png" ypos 104 xpos 568 rotate -5.25 zoom 0.555

screen invitation:
    tag menu
    imagebutton:
        idle Transform("images/envelope/envelope_open.png", zoom=0.28)  # when not hovered
        hover Transform("images/envelope/envelope_open.png", zoom=0.28)
        xalign 0.5
        yalign 0.24
        action Jump("next_scene")  # Jump to the next scene/label


screen input_name:
    add "images/envelope/envelope_invitation.png" zoom 0.42 xalign 0.5 yalign 0.5 at zoom_in