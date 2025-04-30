    #####################################################
    #   The Last Toast: A Murder Mystery Visual Novel   #
    #                (c) Hiraya Studios                 #
    #####################################################


## Mouse design ##
define config.mouse = {}
define config.mouse['default'] = [("gui/cursor_default.png", 0, 0)]
define config.mouse['button'] = [ ( "gui/cursor_pointer.png", 0, 0) ]
define config.mouse['pressed_default'] = [ ( "gui/cursor_grab.png", 0, 0 ) ]

## Animations ##
transform small_rotated:
    rotate -5.39
    zoom 0.555
    xpos 567.5
    ypos 104

transform zoom_in:
    zoom 0.3
    xalign 0.5
    yalign 0.5
    linear 0.2 zoom 0.42

transform slide_in_from_left:
    xpos -500  # start off the screen on the left
    yalign 0.1
    linear 0.5 xpos 0  # Slide to x=0 (centered)

transform shake:
    linear 0.1 yoffset -2
    linear 0.1 yoffset 2
    linear 0.1 yoffset 0
    repeat


## Characters ##
define mc = Character("[mcname]")
define player_title = ""

define footman = Character("Footman")
define herald = Character("Herald")

define e = Character("Bianca")

## Character Flips ##
image maleser flip = Transform("images/characters/maleser.png", xzoom=-1)


## Python Codes ##
default letter_opened = False

init python:
    def dragged_func(dragged_items, dropped_on):
        if dropped_on is not None:
            if dragged_items[0].drag_name == "letter opener" and dropped_on.drag_name == "trigger":
                dragged_items[0].snap(dropped_on.x, dropped_on.y)
                renpy.store.letter_opened = True  # Set the flag
                renpy.hide_screen("tutorial_openletter")
                renpy.jump("invitation_letter")


## ---Game Starts Here--- ##
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
    scene bg table with dissolve
    call screen invitation_button
    return

image invitation = "images/envelope/envelope_invitation.png"


# MC's name input :)
label input_name:
    scene bg table blurred
    show invitation at zoom_in

    $ mcname = ""
    $ valid_name = False
    while not valid_name:
        $ mcname = renpy.input("", length=32).strip()

        # if empty
        if mcname == "":
            "Please confirm name to accept the invitation."
        elif mcname in ["Emory", "Stella", "emory", "stella"]:
            "You can't choose that name."
        # if emory or stella
        else:
            $ valid_name = True

    $ mcname = mcname.capitalize()

    show screen show_mcname("[mcname] Winslow")

    "In truth, if the papers are to be believed, the De Montfort galas always graced headlines in its unmatched grandeur."
    "You were deeply honored that you were thought of and invited, but this doesn’t feel like just another of their gala or society affairs."
    "There’s something deeper. Somehow, it seems like a revival. A {i}return{/i}."
    mc "Ex funere, vita resurgit"
    "{i}From death, to life.{/i}
    A mark of the De Montforts’ first breath after a very long silence."
    window hide
    hide screen show_mcname
    $ quick_menu = False

    # Show act 1 title screen
    show placeholder_act1
    with fade
    $ renpy.pause(2)

    jump act_1

    return

## ---Act 1: The Guest List---##
label act_1:
    window hide
    $ quick_menu = True
    scene bg forest at shake
    with fade
    $ renpy.pause(1)
    window show
    # rain effect
    # car shaking
    "The road winds through open fields and towering trees, a light drizzle misting the windows. 
    You run gloved fingers over the broken De Montfort crest on the invitation you carry."
    "The De Montforts, with multiple automobile businesses across the states, stood as a symbol of wealth, influence, and connection."
    "At the head of the family was Edmond Montague De Montfort, who had two sons: Edmond Quinn and Vincent Augustus."
    "After the tragic, undisclosed death of his daughter, Edmond Quinn, the eldest son, withdrew from public life, consumed by grief as his wife quietly returned to her family."
    "As a result, responsibility for the family business fell to the younger son, Vincent, who briefly flourished—until his involvement in illegal dealings came to light. He now serves time in prison."
    "Now, in the aftermath, the estate and its fragile legacy have returned to the hands of their aging father, Edmond Montague De Montfort."
    "Through the car window, the manor looms into view."

    scene bg housedoor with fade
    "The car glides to a smooth stop at the grand entrance, where a footman steps forward without delay."
    show maleser with dissolve
    footman "Welcome to De Montfort Manor..."

    window hide
    menu:
        "Lord":
            "Welcome to De Montfort Manor, my Lord. Allow me."
            $ player_title = "Lord"
            jump act_1_aftertitle
        "Lady":
            "Welcome to De Montfort Manor, my Lady. Allow me."
            $ player_title = "Lady"
            jump act_1_aftertitle
        
label act_1_aftertitle:
    mcname "Thank you. I believe I\’m expected."
    "He holds an umbrella over your head as you take his gloved hand and step down."
    footman "Please head to the main hall. The master of the house is eager to see who accepted his invitation."
    hide maleser with dissolve
    # NEW BG
    "The foyer rises high above you. The ceilings are tall, and chandeliers hang like stars caught in glass. {i}Everything seems to shine.{/i}"
    "You can already hear the clink of glasses, low laughter, and the soft hum of conversation drifting in from the hall."
    "At the entrance, a herald stands beside a podium. He gives you a quick once-over."
    show maleser flip at right with dissolve
    herald "Announcing the arrival of—"
    "He pauses, scanning the guest register."
    herald "[player_title] [mcname] Winslow."
    hide maleser flip with dissolve
    "A few heads turn."
    # NO textbox - chatter stops (2 seconds)
    # The chatter picks back up again
    "You catch a few lingering, curious glances."



    







# MC display name + Winslow
screen show_mcname(name_text):
    text name_text:
        xalign 0.5
        yalign 0.68 
        size 36
        color "#000000"
        font 'fonts/Cotta Free.otf'


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

screen invitation_button:
    tag menu
    imagebutton:
        idle Transform("images/envelope/envelope_open.png", zoom=0.28)  # when not hovered
        hover Transform("images/envelope/envelope_open.png", zoom=0.28)
        xalign 0.5
        yalign 0.24
        action Jump("input_name")  # Jump to the next scene/label


# screen input_name:
    #add "images/envelope/envelope_invitation.png" zoom 0.42 xalign 0.5 yalign 0.5 at zoom_in
    