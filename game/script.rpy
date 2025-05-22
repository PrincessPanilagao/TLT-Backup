    #####################################################
    #   The Last Toast: A Murder Mystery Visual Novel   #
    #                (c) Hiraya Studios                 #
    #####################################################


## Splash Screen ##
image splash = "splash-screen.png"
image disclaimer = "images/disclaimer.png"

# label splashscreen:
#     scene black
#     with Pause (1)

#     show splash with dissolve
#     with Pause(2)

#     scene black with dissolve
#     with Pause(1)

#     $ renpy.transition(fade, layer="master")

#     # Show disclaimer
#     show disclaimer
#     with fade
    
#     pause 15

#     hide disclaimer
#     with fade
#     return

## Prompt Management ##
init python:
    from store import layout
    layout.MAIN_MENU = _("Return to the main menu?\nThis will lose unsaved progress.")
    layout.LOADING = _("Loading will lose unsaved progress.\nContinue?")
    layout.OVERWRITE_SAVE = _("Are you sure you want to \noverwrite your save?")


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

transform slide_in_pause_out:
    xpos -500 # Start off-screen
    linear 0.5  xpos 0 # Slide in
    pause 5.0 # Stay in place
    linear 0.5  xpos -500 # Slide out again
    alpha 0

transform shake:
    linear 0.1 yoffset -2
    linear 0.1 yoffset 2
    linear 0.1 yoffset 0
    repeat

transform card_resize:
    xalign 0.5
    yalign 0.45
    zoom 0.6

transform pulse:
    alpha 0.2
    linear 1.0 alpha 0.4
    linear 1.0 alpha 0.2
    repeat

# transform panic_pulse:
#     alpha 0.0
#     linear 1.0 alpha 0.5
#     linear 1.0 alpha 0.0
#     repeat


## Characters ##
define mc = Character("[mcname]")
define player_title = ""

define footman = Character("Footman")
define herald = Character("Herald")
define lux = Character("Lux")
define bia = Character("Bianca")
define ben = Character("Benette")
define luc = Character("Lucien")
define lys = Character("Lysander")
define eq = Character("Edmond Quinn")
define quinn = Character("Quinn")
define fadein = Fade(1.5, 0.0, 0.5)



## Character Flips ##
image maleser flip = Transform("images/characters/maleser.png", xzoom=-1)


## Python Codes ##
default letter_opened = False
default quinn_done = False
default luclys_done = False
default bb_done = False
default seen_investroom_objective = False
default secretroute = 0
default callalily = False
default makeupbox = False
default sepbia = False
default teaset = False

init python:
    def dragged_func(dragged_items, dropped_on):
        if dropped_on is not None:
            if dragged_items[0].drag_name == "letter opener" and dropped_on.drag_name == "trigger":
                dragged_items[0].snap(dropped_on.x, dropped_on.y)
                renpy.sound.play("audio/sfx/slice.mp3")
                renpy.store.letter_opened = True  # Set the flag
                renpy.hide_screen("tutorial_openletter")
                renpy.jump("invitation_letter")

    # Define a custom ambient channel that won't conflict with music
    renpy.music.register_channel("amb", mixer="ambient", loop=True, stop_on_mute=True)
    renpy.music.register_channel("amb1", mixer="ambient", loop=True, stop_on_mute=True)


## ---Game Starts Here--- ##
label start:
    stop music fadeout 1.0
    play music "audio/m_prologue.mp3" fadein 1.0 volume 0.6

    $ quick_menu = True
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

image invitation = "images/envelope/envelope_invitation.png"


# MC's name input :)
label input_name:
    play sound "audio/sfx/openletter.mp3" volume 0.5
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
    "There’s something deeper. Somehow, it seems like a revival. A {b}{i}return{/i}{/b}."
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
    
    # Ambient car/rain on separate channel
    $ renpy.music.play("audio/amb/carwrain.mp3", channel="amb", loop=True, fadein=1.0)
    $ renpy.music.set_volume(0.55, channel="amb")
    
    with fade
    $ renpy.pause(1)
    window show
    # rain effect
    # car shaking
    "The road winds through open fields and towering trees, a light drizzle misting the windows. 
    You run gloved fingers over the broken De Montfort crest on the invitation you carry."
    "The De Montforts, with multiple automobile businesses across the states, stood as a symbol of wealth, influence, and connection."
    "At the head of the family was {b}Edmond Montague De Montfort{/b}, who had two sons: Edmond Quinn and Vincent Augustus."
    "After the tragic, undisclosed death of his daughter, {b}Edmond Quinn{/b}, the eldest son, withdrew from public life, consumed by grief as his wife quietly returned to her family."
    "As a result, responsibility for the family business fell to the younger son, {b}Vincent{/b}, who briefly flourished—until his involvement in illegal dealings came to light."
    "He now serves time in prison."
    "In the aftermath, the estate and its fragile legacy have returned to the hands of their aging father."

    ## UGHH FIXXX!!!!!
    # $ renpy.music.stop(channel="amb", fadeout=1.0)

    # $ renpy.music.play("audio/amb/cararriveogg.ogg", channel="amb1", loop=True, fadein=1.0)
    # $ renpy.music.set_volume(0.1, channel="amb1")

    "Through the car window, the manor looms into view."
    scene bg housedoor with fade
    "The car glides to a smooth stop at the grand entrance, where a footman steps forward without delay."
    play sound "audio/sfx/cardoor.mp3" volume 0.6
    show maleser with dissolve
    footman "Welcome to De Montfort Manor..."

    window hide
    menu:
        "Lord":
            footman "Welcome to De Montfort Manor, my Lord. Allow me."
            $ player_title = "Lord"
            jump act_1_aftertitle
        "Lady":
            footman "Welcome to De Montfort Manor, my Lady. Allow me."
            $ player_title = "Lady"
            jump act_1_aftertitle
        
label act_1_aftertitle:
    mcname "Thank you. I believe I\’m expected."
    "He holds an umbrella over your head as you take his gloved hand and step down."

    footman "Please head to the main hall. The master of the house is eager to see who accepted his invitation."
    
    $ renpy.music.stop(channel="amb", fadeout=1.0)
    # Now play walking-in ambient
    $ renpy.music.play("audio/amb/walkingin.mp3", channel="amb1", loop=True)
    $ renpy.music.set_volume(1.0, channel="amb1")

    # Music 
    stop music fadeout 1.0
    play music "audio/m_soiree.mp3" fadein 1.0 volume 0.3

    hide maleser with dissolve

    # Foyer!
    scene bg foyer with dissolve

    "The foyer rises high above you. The ceilings are tall, and chandeliers hang like stars caught in glass."
    $ renpy.music.stop(channel="amb1", fadeout=1.0)
    $ renpy.music.play("audio/amb/chatter.mp3", channel="amb1", loop=True, fadein=1.0)
    $ renpy.music.set_volume(0.5, channel="amb1")

    "{b}{i}Everything seems to shine.{/i}{/b}"
    "You can already hear the clink of glasses, low laughter, and the soft hum of conversation drifting in from the hall."
    "At the entrance, a herald stands beside a podium. He gives you a quick once-over."
    
    show maleser flip at right with dissolve
    with Pause(0.3)

    $ renpy.music.set_volume(0.2, delay=1.0)

    herald "Announcing the arrival of—"
    "He pauses, scanning the guest register."
    herald "[player_title] [mcname] Winslow."
    hide maleser flip with dissolve

    # awkward yikes
    $ renpy.music.stop(channel="amb1")
    window hide
    scene bg foyerdark with dissolve
    pause(1.5)
    "All eyes are on you."
    "You catch a few lingering, curious glances."
    scene bg foyer with dissolve
    $ renpy.music.set_volume(0.7, delay=1.0)
    $ renpy.music.play("audio/amb/chatter.mp3", channel="amb1", loop=True, fadein=1.0)
    $ renpy.music.set_volume(0.15, channel="amb1")

    "But before you can dwell too long on how to fit into the social bustle, a young man approaches."
    "He appears to be in his early twenties, with sharp features and an unexpectedly polished grace to his movements."

    ## Lux Scene ##
    show lux slyclosedeye with dissolve
    with Pause(0.5)
    "He bows with practiced poise."
    show lux smiletalk
    "???" "[player_title] Winslow, it is a pleasure to welcome you. May I offer you a drink to mark your arrival?"
    
    show lux neutral
    mc "Not as of now. Thank you."

    show lux neutraltalk
    "???" "Of course."

    "You regard the guests around the room."
    show lux lookaway
    with Pause(2)

    show lux sly
    "???" "The house is full tonight."
    "???" "Should you require anything, my name is Lux. I shall be at your service."

    show lux slyclosedeye
    "Lux dips into another bow, disappearing as quickly as he arrived, offering drinks and making his rounds again."

    jump interactive_characters


## - Interactive Characters (GTK) | Main Hall - ##
label interactive_characters:
    hide screen show_chartag
    scene bg hall with fade
    window hide
    call screen gtk_characters


# GTK Bianca & Benette
label gtk_bb:
    $ renpy.music.set_volume(0.1, channel="amb1")
    scene bg nobb with dissolve
    show bia flirtsmile at left
    show screen show_chartag("char_bia", xalign_val=0.35, yalign_val=0.25)
    with dissolve
    bia "Oh, come now, Benette, surely even your ink has its secrets. That last column of yours? Positively dazzling. You do have a way with words, darling." 
    bia "Now, tell me…if I were to host a little gala next week, would you come?"
    show bia flirtblush
    bia "Assuming I send an invitation, of course."

    show ben nervoussmile at right
    show screen show_chartag("char_ben", xalign_val=0.63, yalign_val=0.25)
    with dissolve
    "Benette laughs nervously, his fingers tightening around the pen."
    ben "Ah—well…only the dull secrets, I assure you... Lady Lucertia. And that’s very kind of you to say."
    show ben lookaway
    ben "If an invitation were to find its way to me, I-I wouldn’t dream of declining."
    $ bb_done = True
    jump interactive_characters


# GTK Lucien & Lysander
label gtk_ll:
    $ renpy.music.set_volume(0.1, channel="amb1")
    scene bg noll with dissolve
    show luc pondering at left
    show screen show_chartag("char_luc", xalign_val=0.35, yalign_val=0.15)
    with dissolve
    luc "No one’s buying quiet success anymore, Lysander. They want fireworks, headlines."
    show luc neutraltalk
    luc "Tell me, how was that shipping deal in Marlowe? Quite the opportunity, I’d imagine."

    show lys neutraltalk at right
    show screen show_chartag("char_lys", xalign_val=0.59, yalign_val=0.15)
    with dissolve
    lys "Careful, Lucien. Fireworks tend to burn."
    show lys amused
    lys "But now that you’ve mentioned it…there are a few people I could connect you with."
    $ luclys_done = True
    jump interactive_characters


# GTK Quinn
label gtk_qn:
    $ renpy.music.set_volume(0.1, channel="amb1")
    scene bg noquinn with dissolve
    show quinn madtalk at left
    show screen show_chartag("char_quin", xalign_val=0.35, yalign_val=0.25)
    with dissolve
    eq "What do you mean you don’t have Cognac? My father always kept it in stock. I {i}prefer{/i} it!"
    eq "Everyone on this estate knows this. Are you new here?"
    show maid at right with dissolve
    "Maid" "I’m terribly sorry, sir. I remember Lord De Montfort specifically requested its removal. We can check in the cellar, but for now, would you care for some Armagnac instead?"
    show quinn annoyedce
    "Edmond’s expression darkened, frustration flashing in his eyes."
    show quinn mad
    eq "Forget it. I’ll get my own damn drink. Thanks."
    "With an irritated huff, he reaches into his pocket, retrieving a flask. He takes a long pull from it instead."
    "Maid" "Of course, sir. My apologies again."
    show quinn annoyedce
    eq "Unbelievable…"
    $ quinn_done = True
    jump interactive_characters


label after_gtk_1:
    scene bg hall
    "Everyone seems well-acquainted already…"
    $ renpy.music.stop(channel="amb1", fadeout=1.0)

    scene bg nobia big:
        xalign 0.5
        yalign 0.5
    with dissolve

    "From the corner of your eye, you notice someone approaching, dazzling under the chandelier’s glow."

    $ renpy.music.set_volume(0.5, delay=1.0)
    play sound "audio/sfx/heelswood.mp3" volume 1.0

    "All your focus narrows to her alone. Her silk attire and unmistakable lavish jewelry are a gleaming symbol of high society."
    "A soft trail of perfume lingers in the air around her, it smells of something floral with a sharp undercurrent that cuts through the sweetness."
    show bia flirtsmile with dissolve
    bia "Oh my…you look as though you’ve wandered into the wrong place. You’re not from here, are you? Or at least, I haven’t seen you around before."
    menu:
        "Is it that obvious?":
            mc "Is it that obvious? I was hoping to at least blend in for the entirety of the evening."
            show bia flirtce
            bia "Well, blending in is dreadfully overrated. I much prefer standing out."
            mc "You can say that—my sister was a natural when it came to standing out in these social affairs."
            show bia surprise
            bia "A sister? Oh, how lovely. Is she here tonight as well?"
            jump after_gtk_2
        "I was invited.":
            mc "I was invited, same as everyone else."
            show bia flirtsmile
            bia "A mystery guest, now {i}that’s{/i} how you make an entrance."
            show bia flirtblush
            mc "Yes, well, my sister has always been the more sociable one."
            show bia surprise
            bia "A sister? Oh, how lovely. Is she here tonight as well?"
            jump after_gtk_2
        "I'm not partial to parties...":
            mc "I'm not partial to parties...my sister has always been the more sociable one."
            show bia surprise
            bia "A sister? Oh, how lovely. Is she here tonight as well?"
            jump after_gtk_2


label after_gtk_2:
    show bia flirtsmile
    mc "No, sadly, she couldn’t make it. She’s…still recovering from a rather persistent bout of flu."
    mc "Which, I suppose, works in my favor as I get the chance to finally feel what it’s like to be in her place for a while."
    mc "If she were here in my stead, she would already be dazzling everyone in conversation."
    show bia flirtce
    "Bianca lets out a soft laugh, sipping her drink with a knowing smile."
    show bia flirtsmile
    bia "I used to have a dear friend like that. Always the light in the room, the one everyone gravitated towards."
    "Her voice dips slightly. The smile holds, but only just. She grips her glass just a little too tightly."
    bia "She could charm a room without saying a word. The staff adored her, the men adored her, everyone did."
    bia "And she {i}knew{/i} it. Walked through every ballroom like she owned the place. I used to think…maybe, if I stood close enough, some of that shine would rub off on me too."
    show bia neutraltalk
    bia "But it never did."
    show bia petulanttalk
    bia "Still…who’s to say? We lost touch ages ago."
    menu:
        "What happened?":
            mc "She sounds…lovely. What happened?"
            show bia petulant
            bia "We grew up. Priorities shifted. She disappeared on all of us, no goodbye, no explanation."
            bia "Some said she moved to the family’s estate near the coast. Others whispered that she got engaged. Truth is…no one really knows."
            mc "I’m sorry to hear that."
            mc "...But you know…you remind me a great deal of my sister. Something about the way you carry yourself. The way you dress. It feels…familiar."
            show bia flirtblush
            "She raises a brow, eyes narrowing slightly with interest. Then, her lips curl into a smirk."
            show bia flirtsmile
            bia "Really?"
            show bia flirtce
            "She flicks her hair back in a manner that suggests she's fixing it—though nothing is truly out of place."
            bia "Well, I {i}am{/i} flattered. But I do hope your sister had better taste in friends than I did."
            jump after_gtk_3
        
        "You seem to know everyone here.":
            mc "You seem to know everyone here. Are you always the life of the party?"
            show bia flirtce
            bia "That’s not a {i}no{/i}. But yes, I tend to make the most of these evenings. And I have a feeling we’re going to get along just fine."
            jump after_gtk_3

        "Time separates us.":
            show bia neutral
            mc "Funny how time pulls us away from people."
            show bia petulanttalk
            bia "Time, distance, secrets…yes, all of the above. It’s a wonder we remember anyone at all."
            jump after_gtk_3

label after_gtk_3:
    "Bianca finishes her drink, her attention already drifting toward the mingling crowd."
    show bia petulanttalk
    bia "Enough of the nostalgia. That reminds me… where is our elusive host? I feel like I’ve been here half the evening already."
    "She scans the room, eyes narrowing, then waves down a passing figure."
    show bia neutraltalk
    bia "You! Pretty boy—Lux, was it?"
    show bia neutral at left with moveinleft
    show lux neutraltalk at right with dissolve
    lux "Yes, madam?"
    show bia neutraltalk
    show lux neutral
    bia "Would you be so kind as to fetch our host? It’s well past the hour on the invitation."
    show bia neutral
    show lux lookaway
    lux "I’ve checked with Lord De Montfort, madam. He asked me to assure you he’ll be down shortly. He’s just caught up with something at the moment."
    show lux neutral
    show bia neutraltalk
    bia "Well, it would be nice if he–" 

    play sound "audio/sfx/womanscream.mp3" volume 0.01
    with vpunch
    
    show lux surprise
    show bia surprise

    window hide
    pause (0.5)

    stop music fadeout 1.0
    play music "audio/m_mystery1.mp3" fadein 1.0 volume 0.6

    "A sudden scream cuts through the air, freezing everyone in place."
    "The room falls into immediate silence. Eyes dart toward the stairs, where a maid stands, pale-faced, her trembling finger pointed frantically toward the upper floor."
    
    show bia offended
    bia "What the hell was that?"
    "The maid, visibly shaking, stumbles over her words. She struggles to convey what she’s just witnessed, clinging to the wall for support."
    "Maid" "Sir—He—Lord—Lord De Montfort... He—"
    show lux nervous
    lux "Everyone, please remain calm! I ask you to enjoy the refreshments while we investigate–"
    show bg nobq with dissolve
    "But Lux’s voice is swallowed by the chaos as Edmond Quinn is the first to dart from the room, his panic palpable."
    
    eq "No…No! This can’t be…!"
    hide lux
    hide bia
    show bg black
    # make entire image blurred
    # BLACK SCREEN
    with fade
    $ renpy.music.play("audio/sfx/grouprunning.mp3", channel="amb1", loop=False, fadein=1.0)
    $ renpy.music.set_volume(0.5, channel="amb1")
    "You could feel yourself moving, swept up by the tide of panicked guests. Your mind scrambled to catch up, to make sense of the endless possibilities of what could have happened."
    "The smell reaches you first."
    "A putrid stench, unmistakable, hanging thick in the air. It’s the rancid, nauseating scent of burning flesh, like something entirely inhuman. It claws at your throat and stings your eyes."
    "You’re forced to clasp a hand over your nose, fighting the overwhelming urge to gag."

    play sound "audio/sfx/glassshatter.mp3" volume 0.5
    "Beside you, you hear a soft retch followed by the sharp crack of a glass shattering on the floor."
    "And then you see it. "

    show expression Solid("#000") as bg_black at pulse zorder 100
    $ renpy.music.play("audio/amb/heavybreathing.mp3", channel="amb1", loop=True, fadein=1.0)
    $ renpy.music.set_volume(0.05, channel="amb1")
    show bg upperhw with fade

    pause (0.9)

    "Nothing could have prepared you for the sight."
    "Lord Edmond Montague De Montfort lies lifeless on the floor, his face gruesomely disfigured. The skin eaten away by some sort of acid."
    "What remains are the remnants of his formal attire, unmistakably marked by the De Montfort family crest."
    "Blood, too much blood, spreads across the carpeted stairs in dark pools, seeping into the fibers and dripping slowly."
    "It stains everything."
    "It stains the air, making it hard to breathe."
    "The sight was so grotesque—harrowing—that it burns itself on your memory."

    play sound "audio/sfx/fallingtoknees.mp3" volume 0.8
    
    "Edmond Quinn, his eldest son, kneels next to the body. His face contorts in a mix of disbelief, grief, and sheer horror as he presses a trembling hand to the chest of what remains of his father."
    "The instant his hand makes contact, he recoils, a choked cry escaping him as he stumbles back, eyes wide."
    "Silence stretches over the room as everyone watches the scene unfold."

    hide bg_black with dissolve 
    $ renpy.music.stop(channel="amb1", fadeout=1.5)


    show bia horrified at left
    with dissolve
    "Bianca, grips tightly onto you, her fingers digging into your arm. Her face is pale, almost ghostly, her breath shallow and erratic, like she might faint at any moment."
    hide bia
    show lux panictalk
    with dissolve
    "Lux immediately takes control of the situation, shouting to the staff."
    lux "Everyone—with me. Call for help, immediately!"
    hide lux with dissolve 
    "But Edmond is already on his feet, grief giving way to rage as he turns to the rest of you."
    show quinn enraged with dissolve
    eq "This-this is murder. Someone must have done this! Who would dare…?!"
    "Gasps ripple around the group. It was a bold accusation."
    hide quinn with dissolve
    "Lysander steps forward, his voice composed."
    show lys neutraltalk at right with dissolve
    lys "Grief blinds the eyes, Edmond. This may be a terrible accident."
    "You agree, though it doesn’t take much to arrive at the obvious. Judging by Lord De Montfort’s state, the likelihood of an accident seems slim."
    show bia sneer at left
    with dissolve
    show lys neutral
    bia "Oh, {i}please{/i}. Accident? I’d say the list of suspects is not long. And if you ask me…"
    show bia petulant
    "Bianca’s eyes gleam, scanning the six guests present. She locked eyes with you…narrows, then flicks to Lucien."
    hide lys
    show luc neutral at right
    with dissolve
    show bia sneer
    bia "I saw you by the stairs earlier, didn’t I?"
    "Edmond turns, his glare sharp and immediate, locking on Lucien."
    hide bia
    show quinn mad at left
    with dissolve
    show luc shock
    "The implication hitting fast."
    show luc eyesnarrowed
    "Lucien steps forward, his voice composed."
    show luc neutraltalk
    luc "Now, let’s not lose our heads. Throwing around accusations won’t help anyone. And for all we know, it could have been an accident."
    show luc neutral
    show quinn madtalk
    eq "Oh? What kind of accident melts a man’s face?!"
    hide quinn
    show bia neutraltalk at left
    with dissolve
    bia "Well, Mr. Velasco, surely you’d know a thing or two about accidents…wouldn’t you?"
    hide bia
    hide luc
    with dissolve

    show bg upperhw vignettee with dissolve

    "Everyone tenses. The tangible jab hangs in the air, almost suffocating."
    show luc eyesnarrowed with dissolve
    "Lucien’s jaw tightens. He takes a step forward, eyes dark with fury, but Lysander blocks his path with a raised hand."
    "You glance around. Suspicion blooming as the tension thickens."
    "Time to choose where you stand."
    hide luc with dissolve
    menu:
        "Edmond's right...":
            mc "Edmond’s right. This doesn’t look like some tragic mishap. Someone planned this. The question is…who?"
            show quinn mad with dissolve
            "Edmond doesn’t acknowledge you outright, but he meets your gaze for the briefest moment. Red-eyed."
            "But you can feel it, you’ve now drawn a clear line. Others glance at you warily."
            mc "For all we know, every one of us here has been in the main hall since the scream."
            hide quinn with dissolve
            jump fm_1
        "Bianca's right...":
            mc "Well, the guilty usually out themselves. One way or another."
            "The words leave your lips like a challenge."
            show bia flirtsmile with dissolve
            "Bianca’s eyes flick to you, her smile hinting something close to approval or amusement."
            show bia flirtsmile at left with moveinleft
            show luc eyesnarrowed at right with dissolve
            luc "This is not a game, Bianca."
            hide luc
            show ben panic at right with dissolve 
            ben "Th-this is insane…The authorities! W-we need the authorities!"
            show bia sneer
            bia "And how do you propose we get them? In case you missed it, the staff left!"
            hide bia
            hide ben
            with dissolve
            jump fm_1
        "Lucien's right...":
            mc "We won’t get answers if we just tear each other apart."
            "Your voice cuts through the room, clear and firm."
            show luc neutral with dissolve
            "Lucien turns slightly toward you. The faintest nod."
            hide luc
            show lys neutraltalk with dissolve
            lys "I suggest you keep your principles close. They might be the first to go."
            hide lys
            show ben nervous with dissolve
            ben "I–I agree with them. We can’t just…we can’t fight like this."
            ben "For all we know, every one of us here has been in the main hall since the scream."
            hide ben with dissolve
            jump fm_1


label fm_1:
    "You frown. Wait."
    "The staff...the ones who served you drinks, hovering at the walls… they’re gone."
    show bg upperhw with dissolve
    mc "Where are the staff?"
    "Nervous glances dart across the room. The accusations are replaced by the realization that the manor has fallen into eerie silence."
    mc "Lux!"
    "Your voice echoes in the empty hall. No answer."
    jump second_murder

## - Second Murder - ##
label second_murder:
    scene bg hallway with fade
    
    $ renpy.music.set_volume(0.4, delay=1.0)
    $ renpy.music.play("audio/amb/gwc.mp3", channel="amb1", loop=True, fadein=1.0)
    $ renpy.music.set_volume(0.2, channel="amb1")

    "The group moves cautiously now."
    show luc pondering with dissolve
    "Lucien walks a few phases ahead, checking corners."
    hide luc
    show bia petulant
    with dissolve
    "Bianca lingers close to your side."
    hide bia
    show ben nervous
    with dissolve
    "Benette, still visibly shaken, trails behind. He fidgets with his hair, words forming and dissolving under his breath."
    hide ben
    show quinn mad
    with dissolve
    "You hadn’t expected Edmond to follow as well."

    scene bg hallclear:
        xalign 0.5
        yalign 0.5
    with fade

    $ renpy.music.stop(channel="amb1", fadeout=1.0)
    show bia horrified at left with vpunch 
    bia "Oh my god–!"
    show luc shock at right with dissolve
    luc "This can’t be…"

    hide bia
    hide luc
    with dissolve
    "Your heart lurches. You round the corner—"

    "The staff…Lux…all of them lie collapsed on the floor."
    "No blood. No wounds. Just bodies—still and lifeless."

    play sound "audio/sfx/fallingtoknees.mp3" volume 0.8

    "You rush forward, dropping to your knees beside Lux and pressing your fingers to his neck."
    "Nothing."
    # show expression Solid("#000") as pulse_overlay at panic_pulse
    scene bg hallcleardark with dissolve
    mc "They’re not…breathing."
    "The room erupts, panic swelling, voices picking up again."

    show luc eyesnarrowed with dissolve
    luc "Poison? But how? When?"
    "You sit back, shock catching up to your system. It doesn’t make sense. How could this happen?"
    hide luc
    show quinn enraged
    with dissolve
    eq "Whoever did this—they’re still here!"
    eq "Face us, you cowards!"
    hide quinn with dissolve
    "You scan what’s left of the group. And you can’t help but wonder if any of them can still be trusted."
    show bia offended at left
    with dissolve
    bia "This is…this is a game. A sick, twisted game!"
    bia "I’m done. I didn’t sign up for this!"
    show ben neutral at right with dissolve

    play sound "audio/sfx/luxcoat.mp3" volume 0.3

    ben "What is this?"
    "You notice movement beside you. Benette is rifling through Lux’s coat. His fingers tremble as he pulls out a stack of cards." 
    
    # hide pulse_overlay
    "{b}{i}Calling cards.{/i}{/b}"

    show bia petulant
    bia "Give that to me!"
    hide bia
    hide ben
    with dissolve
    "The cards make their way to each person, name inscribed in gold ink. But as you turn yours over, your stomach sinks."
    
    stop music fadeout 1.0
    play music "audio/m_suspensevio2.mp3" fadein 1.0 volume 0.4
    # show calling card
    window hide
    scene bg hallcleardarker
    show callingcard at card_resize
    with dissolve
    window hide
    pause

    "A cold sweat creeps over you."
    "You glance up to find everyone holding their own card. Silent. Pale."
    # "And that’s when it dawns on you–"
    "None of this is an accident."
    "You weren’t just invited."
    "You were chosen."
    "And the night has only just begun."

    $ quick_menu = False

    # Show act 2 title screen
    show placeholder_act2
    with fade
    $ renpy.pause(2)

    jump act_2
    # show expression "images/thank-u-screen.png" with fade
    # pause
    # scene black with fade
    # stop music fadeout 1.0
    # return


# Pressable character images
image quinn_idle:
    "images/mainhall/btn_quinn_idle.png"
image quinn_hover:
    "images/mainhall/btn_quinn_hover.png"
    
image luclys_idle:
    "images/mainhall/btn_lylu_idle.png"
image luclys_hover:
    "images/mainhall/btn_lylu_hover.png"
    xpos -11
    ypos -8

image bb_idle:
    "images/mainhall/btn_bibe_idle.png"
image bb_hover:
    "images/mainhall/btn_bibe_hover.png"
    xpos -11
    ypos -8

# Character tags images
image char_bia = "images/mainhall/tags/bianca-tag.png"
image char_ben = "images/mainhall/tags/benette-tag.png"
image char_luc = "images/mainhall/tags/lucien-tag.png"
image char_lys = "images/mainhall/tags/lysander-tag.png"
image char_quin = "images/mainhall/tags/edmond-tag.png"

# Show character tag
screen show_chartag(tagid, xalign_val=0.35, yalign_val=0.25):
    add tagid xalign xalign_val yalign yalign_val zoom 1.5


# Pressable characters
screen gtk_characters:
    if store.bb_done and store.quinn_done and store.luclys_done:
        timer 0.1 action Jump("after_gtk_1")

    # Quinn
    imagebutton:
        idle "quinn_idle"
        hover "quinn_hover"
        xpos 1681
        ypos 537
        action Jump("gtk_qn")
    
    # Lucien & Lys
    imagebutton:
        idle "luclys_idle"
        hover "luclys_hover"
        xpos 540
        ypos 524
        action Jump("gtk_ll")
    
    # Bianca & Ben
    imagebutton:
        idle "bb_idle"
        hover "bb_hover"
        xpos 154
        ypos 407
        action Jump("gtk_bb")

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

 


## ---Act 2: “Out, damned spot!”---##
label act_2:
    # CHANGE THIS!!!
    stop music fadeout 1.0
    play music "audio/m_mystery2.mp3" fadein 1.0 volume 0.8

    window hide
    $ quick_menu = True
    scene bg hallclear:
        xalign 0.5
        yalign 0.5
    with fade
    $ renpy.pause(1)
    window show
    "{i}To leave, you must face what you have buried.{/i}"
    "The note feels heavier in your hand now as the message burns into your mind."
    "You feel it dig into your gut like a quiet accusation."

    show ben neutraltalk at left
    with dissolve
    ben "...What does that even mean?"

    show luc neutraltalk at right with dissolve
    luc "This is clearly a threat."

    show bia petulanttalk at center
    with dissolve
    bia "Well, if that’s the case, isn’t it safe to assume {i}one of us{/i} is involved with the culprit?"

    show ben nervous
    show luc pondering
    "No one meets her gaze."

    show ben neutraltalk
    ben "Or…"
    ben "Or maybe all of us?"
    show ben nervous
    show luc shock
    show bia offended
    ben "Maybe we’re not here by accident."

    show ben panic
    play sound "audio/sfx/ripcard1.mp3" volume 0.4
    "Without a word, Lysander rips his own card, letting it fall on the floor."

    hide ben
    hide bia
    show lys mad at left
    with dissolve
    show luc neutral
    lys "We’re being toyed with."
    show lys neutral
    show luc neutraltalk
    luc "How about this, let’s split up–"

    hide lys
    show bia sneer at left
    with dissolve
    show luc neutral

    bia "Are you insane? The culprit could still be in here. What if we’re picked off one by one the moment we split?"
    "She makes a point by subtly gesturing to the scattered remains of the staff."

    show bia petulant
    show quinn madtalk at center with dissolve
    eq "I’m not trusting a single one of you."

    show luc neutraltalk
    show quinn mad
    luc "Yes, but that doesn’t mean we rip each other apart. We’ll cover more ground if we work together."

    hide bia
    hide quinn 
    hide luc
    show ben nervous
    with dissolve
    ben "Okay, okay, stop! Let’s just…think."
    ben "We were all invited here, but why? There must be some connection to the De Montforts or something?"

    "The question lingers in the air."
    hide ben with dissolve
    "Of course, that much is true. If this is some masterfully cultivated plan, then everyone should at least have some connection to the family."

    "Lucien is the first to speak."

    show luc neutraltalk
    with dissolve
    luc "Vincent has been a close friend of mine for years. He treated me like a brother in and out of business. I would never hurt him or his family."

    hide luc with dissolve
    "Vincent, the youngest son of Edmond Montague. A man now serving time in prison."
    "Everyone seems to quiet at that, their thoughts retreating inward, weighing the possible reasons they could be dragged into this."

    "Even Bianca doesn’t look at anyone."

    show bia petulanttalk with dissolve
    bia "I was Vincent’s daughter’s best friend."
    bia "Seraphine."
    bia "We used to attend and host galas together. Everyone knows this."
    show bia petulant
    "Lucien nods at her."

    hide bia
    show ben nervous
    with dissolve
    ben "I-"
    show ben neutral
    "Benette fidgets with the pen that is usually tucked in his breast pocket; glancing briefly toward Lysander."

    show ben nervous
    ben "I’ve written press for the De Montforts for years. Always gave them good coverage when it mattered."
    ben "I-I figured I was invited to cover tonight’s soirée for this week’s column."
    show ben lookaway
    "He nods once to himself, as if affirming his own presence."
    "Benette Hawthorne—the leading journalist in The Marlowe Gazette—had covered countless features on the De Montforts over the years."

    hide ben
    show lys neutralla
    with dissolve
    "Lysander doesn’t speak. He crosses his arms and leans against the wall, expression unreadable."
    "But something in the confidence of his posture tells everyone he doesn’t need to explain himself."

    show lys neutralce
    "His connection to the family runs deep. Known."
    "You vaguely recall headlines: the governor of Marlowe receiving major sponsorships from the De Montforts."

    hide lys
    show luc neutraltalk at right
    with dissolve
    luc "Edmond, I know you’re—"

    show quinn annoyedce at left with dissolve
    eq "It’s only Quinn now."
    show luc shock
    "Lucien stops. Estranged heir or not, Quinn is not inclined to elaborate further."

    show bia raisedbrow at center with dissolve
    bia "And you...[mcname], was it? I don’t recall ever seeing you at any of the family’s gatherings."
    show bia eyesnarrowed
    show luc eyesnarrowed
    bia "What exactly are you to them?"

    hide bia
    hide quinn
    hide luc
    scene bg hallcleardark
    with dissolve
    "You feel everyone’s attention land squarely on you. You were sure their suspicions had always been there."
    "All of them seem to have a clear connection to the family, one known and longstanding. And yet you…you are not one whose presence has echoed since birth."
    "But that does not mean you are less than. Or any less tied to the De Montforts."
    window hide

    menu:
        "My sister attended Seraphine’s events.":
            mc "My sister attended Seraphine’s events. I tagged along sometimes, but it goes a long way back, when I was younger."
            show bia raisedbrow with dissolve
            bia "Really?"
            "But you were sure it {i}was{/i} a long time ago. Because had it been recent, you would’ve remembered these people, too."
            "You catch Lysander’s lingering gaze across the room."
            hide bia with dissolve
            jump eschouse
        
        "Vilhelm and I...":
            mc "Vilhelm and I…we’ve known each other for a long time."
            show bia surprise at left with dissolve
            bia "Vilhelm?"
            show luc shock at right with dissolve
            luc "Vincent’s son, the youngest?"
            mc "Yeah. Cards and wagers. He knew me well enough from the table."
            hide bia
            hide luc
            with dissolve
            "You feel the others glance your way."
            "Vilhelm De Montfort, the youngest of Vincent’s children, known for his long list of connections and tangled past."
            "They don’t seem to pry further."
            jump eschouse

label eschouse:
    scene bg hallclear:
        xalign 0.5
        yalign 0.5
    show quinn annoyedce at left
    with dissolve
    quinn "Great. So we all know someone rich. That really narrowed it down."

    show luc pondering at right with dissolve
    luc "We don’t have a choice, we need to focus on how we can get out."

    "Everyone seems to have already chosen where to check, probably opting for the safest one."
    hide quinn
    hide luc
    with dissolve
    "You hang back, weighing your own choice."
    jump esc_menu

# try to escape the manor
label esc_menu:
    menu:
        "Break the window":
        #change to bg foyer
            play sound "audio/sfx/dragchair.mp3" volume 0.3
            "Lucien grabs a nearby chair and moves toward the window, nodding for everyone to step aside."
            show luc neutraltalk with dissolve
            luc "Move back."
            play sound "audio/sfx/windowhit.mp3" volume 0.4
            "With a firm grip, he swings the chair into the large pane. A dull thud echoes through the room, but the window remains intact."
            "A closer look reveals {i}laminated glass{/i}."
            hide luc with dissolve
            jump esc_menu

        "Try the main door":
            #change to bg foyer
            show lys neutralla with dissolve
            play sound "audio/sfx/doorhandle.mp3" volume 0.5
            "Lysander strides across the floor to the grand entrance. He grips the ornate brass handle, twisting it hard."
            "It doesn’t budge."
            show lys annoyed
            play sound "audio/sfx/doorweight.mp3" volume 0.4
            "He throws his weight against the door."
            "Once."
            "Twice."
            "A heavy thud shakes the frame, but the lock holds."
            "{i}Sealed from the outside.{/i}"
            hide lys with dissolve
            jump esc_menu

        "Check the servant's area":
            #change to bg foyer
            show ben frown with dissolve
            "Benette reappears, brushing dust from his pants and muttering under his breath."
            ben "Servant’s hallway leads straight to the kitchens, but it’s no use."
            show ben nervous
            ben "Blocked off. Padlocked from the inside."
            "He glances back over his shoulder, the unease in his voice barely masked."
            hide ben with dissolve
            jump esc_menu

        "Check the hallways":
            #change to bg foyer
            show bia petulant with dissolve
            "Bianca huffs, smoothing her skirt."
            play sound "audio/sfx/biaheels.mp3" volume 0.2
            hide bia with dissolve
            "Her heels echo sharply against the marble as she disappears down one of the long halls, shoulders squared."
            "A few tense seconds pass."
            stop sound fadeout 1.0
            bia "...This one’s unlocked."
            jump biasroom


## ---Bianca's Room (Tea Room)--- ##
label biasroom:
    scene bg hallway with dissolve
    play sound "audio/sfx/grouprunning.mp3" volume 0.5
    "Everyone rushes to her voice."
    play sound "audio/sfx/doorcreakopen.mp3" volume 0.5
    "The door creaks as she pushes it open with a single hand."
    "A faint but distinct scent drifts from the room. A blend of lavender and herbs, rolling out in waves."
    bia "This used to be the family’s tea room…which would explain why it’s still open, but…"
    "She trails off, her gaze sweeping across the space."

    show bia eyesnarrowed with dissolve
    bia "This…this isn’t how I remember it."
    play music "audio/m_tearoom.mp3" fadein 1.0 fadeout 1.0 volume 0.6
    scene bg trwcard with fade
    "At first glance, the room feels oddly out of place within the grand estate."
    quinn "This wasn’t here before."

    "The room feels paused in time."
    "The tea set in the far corner still releases gentle steam as if someone had just been pouring a cup seconds before."
    "The scent of jasmine and lavender lingers in the air, calming. Your shoulders relax without thinking."
    
    scene bg hallway
    show bia petulanttalk at left
    with dissolve
    "Bianca, however, hasn’t moved from the doorway. Her usual practiced elegance falters as her eyes roam the room, searching for something or someone."
    mc "What's wrong?"

    show bia surprise
    "The question snaps her out of her daze."

    show bia flirtsmile
    "She pulls her boa closer, shielding the pause in her expression behind a well-worn smirk."
    hide bia with dissolve
    play sound "audio/sfx/biaheels.mp3" volume 0.1
    "Without answering, she strides forward, heels tapping against polished wood."

    scene bg trnocard with dissolve
    stop sound fadeout 1.0
    "She stops near the center of the room where Benette is crouched by a small carved table, holding a piece of cream-colored paper."
    show ben confused at right with dissolve
    ben "…‘A cup shared, a life stolen.’"

    show luc raisedbrow at left with dissolve
    luc "What’s that supposed to mean?"

    show bia petulant at center
    with dissolve
    pause 0.3
    show bia frownla

    bia "..."

    hide ben
    show lys annoyed at right
    with dissolve
    show luc pondering
    lys "What is this? Some kind of theatrical nonsense?"

    hide lys
    hide luc
    hide bia
    with dissolve
    "Lysander aims for the door in the room."
    play sound "audio/sfx/hittingdoor.mp3" volume 0.11
    "It wouldn’t budge."
    
    play sound "audio/sfx/paperturn.mp3" volume 0.3
    "Benette turns the paper over."

    show ben frown at left with dissolve
    ben "Wait—there’s more on the back."
    ben "Clues are hidden around. Look closely, for the room remembers."

    show lys neutralla at right with dissolve
    lys "Riddles? How quaint."

    hide ben
    hide lys
    scene bg trblur
    with dissolve


    menu:
        "Someone was just here...":
            scene bg trnocard with dissolve
            "You fixate on the steaming teacups."
            mc "That tea isn’t cold…Someone was just here."
            show ben nervous with dissolve
            ben "Or still {i}is{/i} h-here."
            "You feel the faint shift of Bianca’s posture beside you."
            hide ben
            show quinn neutraltalk at left
            with dissolve
            quinn "So what now? We find these clues?"
            show quinn mad
            quinn "What, and the door magically unlocks?"
            mc "Or…a key to the main door."
            show luc neutraltalk at right with dissolve
            luc "Do we really have another option?"
            hide quinn
            hide luc
            with dissolve
            jump investigate_biaroom

        "Bianca seems familiar with the place.":
            scene bg trnocard with dissolve
            mc "Bianca, do you recognize this room?"
            show bia neutraltalk with dissolve
            bia "...This used to be the family’s parlour. But it—it didn’t look like this before."
            show bia neutral
            mc "So you know this place?"
            show bia petulanttalk
            bia "Not more than a faint memory."
            hide bia
            show quinn neutraltalk at left
            with dissolve
            quinn "So what now? We find these clues?"
            show quinn mad
            quinn "What, and the door magically unlocks?"
            mc "Or…a key to the main door."
            show luc neutraltalk at right with dissolve
            luc "Do we really have another option?"
            hide quinn
            hide luc
            with dissolve
            jump investigate_biaroom

        "Something feels off...":
            scene bg trnocard with dissolve
            mc "This feels too targeted."
            show bia sneer with dissolve
            bia "Because it is."
            hide bia
            show quinn neutraltalk at left
            with dissolve
            quinn "Then someone in this room’s the target."
            show luc neutraltalk at right with dissolve
            luc "Or the {i}reason{/i} we’re all here."
            luc "So we look. Clearly, they’re telling us the answers lie in this room."
            hide quinn
            hide luc
            with dissolve
            jump investigate_biaroom

## ---INVESTIGATE THE ROOM--- ##
label investigate_biaroom:
    scene bg trnocard
    call screen investigate_biaitems

# # Items to investigate (imagebuttons)
image cl_idle:
    "images/biasroom/btn_callalily_idle.png"
image cl_hover:
    "images/biasroom/btn_callalily_hover.png"
image mu_idle:
    "images/biasroom/btn_makeup_idle.png"
image mu_hover:
    "images/biasroom/btn_makeup_hover.png"
image ts_idle:
    "images/biasroom/btn_teaset_idle.png"
image ts_hover:
    "images/biasroom/btn_teaset_hover.png"
image sb_idle:
    "images/biasroom/btn_sepbia_idle.png"
    zoom 0.99
image sb_hover:
    "images/biasroom/btn_sepbia_hover.png"
    xpos -11
    ypos -7
    zoom 0.99

screen investigate_biaitems:
    # continue to main story after all items are interacted with
    if store.callalily and store.makeupbox and store.sepbia and store.teaset:
        timer 0.1 action Jump("bfr_connectmirror")

    # Callalillies
    imagebutton:
        idle "cl_idle"
        hover "cl_hover"
        xpos 23
        ypos 508
        action Jump("callalilies")
    
    # Makeup
    imagebutton:
        idle "mu_idle"
        hover "mu_hover"
        xpos 1680
        ypos 460
        action Jump("makeup")

    # Teaset
    imagebutton:
        idle "ts_idle"
        hover "ts_hover"
        xpos 630
        ypos 697
        action Jump("teaset")
    
    # Sepbia Poster
    imagebutton:
        idle "sb_idle"
        hover "sb_hover"
        xpos 307
        ypos 80
        action Jump("sepbia_poster")

    # bronzemirror for layering
    add "images/biasroom/bronzemirror.png":
        xpos 418
        ypos 404
        zoom 1.0

    # Objective 
    # add "images/objectives/objective investroom.png" zoom 1.0 xalign 0.0 yalign 0.1 xoffset -30 at slide_in_pause_out
    if not seen_investroom_objective:
        add "images/objectives/objective investroom.png":
            at slide_in_pause_out
            zoom 1.0
            xalign 0.0
            yalign 0.1
            xoffset -30

        timer 6.0 action SetVariable("seen_investroom_objective", True)


# IR - Callalilies
label callalilies:
    scene bg trblur with dissolve
    $ seen_investroom_objective = True

    show callalily:
        zoom 0.9
        xalign 0.5
        yalign 0.35
    with dissolve
    pause (3)
    show lys neutraltalk at left with dissolve
    lys "It’s calla lilies."
    hide lys with dissolve
    "Tucked within is a folded note, edges yellowed and the ink slightly faded but still legible."
    hide callalily
    show callanote:
        zoom 0.62
        xalign 0.5
        yalign 0.4
    with dissolve
    pause
    show luc raisedbrow at left with dissolve
    luc "Wait a minute. The date…it’s five years ago."
    show ben neutraltalk at right with dissolve
    ben "Marcus…"
    show ben frown
    ben "Isn’t that your husband?"
    hide luc
    hide ben
    show bia petulant at left
    with dissolve
    "Everyone turns to Bianca."
    bia "You’re mistaken."

    show luc eyesnarrowed at right with dissolve
    luc "Bianca…wasn’t Marcus courting Seraphine before he married you?"
    show bia sneer
    bia "That was a long time ago. Whatever happened between them–"

    hide luc
    show ben neutraltalk at right with dissolve
    show bia petulant
    ben "No, wait—I remember this."
    ben "The story broke just after the engagement was abruptly called off. The papers barely had time to catch up before she vanished."

    show bia neutral
    show ben neutral
    mc "And yet, Marcus married you just a month after Seraphine left."

    show bia eyesnarrowed
    bia "What are you implying? You think I forced him to choose? That I took him from her?"

    hide ben
    show quinn mad at right with dissolve
    quinn "Didn't you?"
    show bia offended
    bia "He chose me!"
    mc "And Seraphine?"
    show bia petulant
    show quinn annoyedce
    bia "She chose to disappear. That’s on her."
    hide callanote
    hide bia
    hide quinn
    with dissolve
    $ callalily = True
    jump investigate_biaroom


# IR Seraphine & Bianca Photo
label sepbia_poster:
    scene bg trblur with dissolve
    $ seen_investroom_objective = True

    show sepbia:
        zoom 0.9
        xalign 0.5
        yalign 0.32
    with dissolve
    pause (3)

    "A portrait hangs above the fireplace."
    mc "Huh. Look at this."
    "Two young women smile at the portrait."
    "One, with softer features, dressed in a timeless and understated gown. The other—striking in red lipstick and dramatic kohl—wears a daringly cut dress and a smirk you easily recognized."
    mc "...Was that you, Bianca?"
    show bia neutraltalk at left with dissolve
    bia "That was the summer before Seraphine debutted…We were inseparable then."
    hide bia with dissolve
    "They were both smiling in the portrait. Two young women, certain the world would yield to them, so long as they had each other."
    show luc neutraltalk at right with dissolve
    luc "You looked different back then."
    show bia petulanttalk at left with dissolve
    bia "...Yes, I suppose I did."
    show bia neutral
    hide luc with dissolve
    show lys neutraltalk at right with dissolve
    lys "You and her don’t look all that different now."
    hide lys
    with dissolve
    "Seeing Bianca beside the portrait, you can't stop comparing her to the girl in the photo. {i}Seraphine{/i}."
    "Their outfits are strikingly similar in shape. But gone is the bold, daring air of Bianca’s younger self, replaced with something more subdued. Softer."
    show bia flirtsmile
    "The mirrored smile."
    "The way her posture has shifted."
    "It's harder to differentiate the two now. Apart from Seraphine’s signature violet hair while Bianca’s remains blonde."
    show bia neutraltalk
    bia "Well, everyone changes. We grow."
    hide bia
    with dissolve
    menu:
        "You really admired her, didn’t you?":
            mc "You really admired her, didn’t you?"
            show bia petulant at left with dissolve
            bia "Of course I admired her. Who didn’t?"
            show bia neutraltalk
            bia "But I earned what I have. I will never be ashamed of that."
            hide bia
            hide sepbia
            with dissolve
            $ sepbia = True
            jump investigate_biaroom
        "You looked happier then. Freer.":
            mc "You looked happier then. Freer."
            show bia petulant at left with dissolve
            bia "I still am."
            show bia raisedbrow
            bia "But what is freedom if you're always hidden in someone else's shadow?"
            hide bia
            hide sepbia
            with dissolve
            $ sepbia = True
            jump investigate_biaroom
        "Why’d you stop dressing the way you used to?":
            mc "Why’d you stop dressing the way you used to?"
            show bia neutraltalk at left with dissolve
            bia "I used to think turning heads was enough. That if people looked, I mattered."
            show bia petulanttalk
            bia "But I soon realized…these are fleeting."
            bia "I don’t want to be noticed. I want to be remembered. Admired."
            show bia frownla
            bia "So I learnt to soften my edges too."
            hide bia
            hide sepbia
            with dissolve
            $ sepbia = True
            jump investigate_biaroom

# IR Makeup/Laquered Box
label makeup:
    scene bg trblur with dissolve
    $ seen_investroom_objective = True
    show makeupbox:
        zoom 0.7
        xalign 0.5
        yalign 0.5
    with dissolve
    pause (3)
    show quinn neutral at left with dissolve
    "On the far side of the tea room, Quinn lingers by a sideboard, his hand resting on an ornate lacquered box."
    play sound "audio/sfx/openlaqueredbox.mp3" volume 0.6
    "He opens it slowly. Inside are lipsticks in muted tones, and one bold rouge."
    hide quinn
    hide makeupbox
    show lipstick:
        zoom 0.7
        xalign 0.5
        yalign 0.5
    with dissolve
    "Benette leans over, casting a glance between the set and the portrait."
    show ben surprise at left with dissolve
    ben "These shades…"
    "Benette lifts the pink one in a gold tube."
    show ben neutraltalk
    ben "Lady Seraphine used to wear something like this. Or at least from the magazines."
    show ben nervoussmile
    ben "My daughters asked for these exact ones on their last birthday."
    show ben neutral
    show bia neutraltalk at right with dissolve
    bia "She did but she always kept it minimal. Just a touch of color."
    bia "She wouldn’t even let me give her anything ‘too loud,’ she would say."
    show bia neutral
    show ben nervoussmile
    ben "She didn’t need it."
    show ben lookaway
    ben "Even in the papers…Beauty sure, but it was the way she spoke. Like everything she said mattered."
    show bia petulant
    "Bianca’s mouth twitches, the corner falling ever so slightly."
    show bia petulanttalk
    bia "Yes, well. That was Seraphine."
    hide ben
    show luc smile at left
    with dissolve
    show bia petulant
    luc "She made it look easy."
    show bia neutraltalk
    bia "Well, appearances are always easier to perfect than who we really are underneath."
    hide luc
    hide bia
    hide lipstick
    with dissolve
    $ makeupbox = True
    jump investigate_biaroom

label teaset:
    scene bg trblur with dissolve
    $ seen_investroom_objective = True
    show teaset:
        zoom 0.8
        xalign 0.5
        yalign 0.35
    with dissolve
    pause (3)
    "An elegant tea table sits near the fireplace, laid out perfectly as if a gathering had just left. The china glints under the low light."
    "Steam rises from the full teacups and etched in faint gold along the rim of the teapot are the initials:"
    mc "S.D.M…"
    "You trace your finger along the rim of the cup."
    "{b}Seraphine De Montfort{/b}."
    "Tucked beneath one of the saucers seems to be a torn page from a letter. Old and creased from being read more than once."
    play sound "audio/sfx/pulloutpaper.mp3" volume 0.5
    "You ease it out."
    hide teaset
    show teanote:
        zoom 0.7
        xalign 0.5
        yalign 0.35
    with dissolve
    pause
    show luc neutraltalk at left with dissolve
    luc "It’s signed…B…"
    show luc eyesnarrowed
    "He squints at the paper."
    luc "Wait, you—"
    "Lucien turns fully to Bianca, holding the letter up."
    show luc mad
    luc "You wrote this?"
    show bia sneer at right with dissolve
    bia "This is ridiculous. Anyone could’ve written that."
    show bia neutraltalk
    bia "It’s not even dated."
    hide luc
    show bia neutral
    show ben confused at left
    with dissolve
    ben "Marcus? Wasn’t that Seraphine’s long-time suitor?"
    hide ben
    show luc eyesnarrowed at left
    with dissolve
    luc "You were referring to Seraphine in these letters, weren’t you?"
    show bia neutraltalk
    bia "You’re reaching."
    show bia frownla
    bia "Maybe someone just finally said what others were too afraid to."
    show luc pondering
    luc "But this…here—{i}‘Always tearing up over nothing.’{/i} And the mention of Marcus?"
    show luc frown
    luc "Only someone who knew them both well…Someone close to them both…would write something like this."
    mc "Seraphine only ever had one true friend."
    show bia neutraltalk
    bia "Well, whoever wrote it was clearly observant. I’m not the only one who’s ever attended a garden party or overheard the gossip."
    show bia neutral
    hide luc with dissolve
    show lys neutraltalk at left with dissolve
    lys "But you were the only one always by her side."
    show bia sneer
    bia "Oh, so now I’m guilty just because I was close to her? Please, this is pathetic. Even for you, governor."
    hide lys
    show quinn mad at left
    with dissolve
    quinn "Seraphine was not one to cheat. She would rather lose everything than betray someone’s trust. That was never in her nature."
    show bia raisedbrow
    "Bianca folds her arms, standing unyielding in the middle of the room."
    bia "And how are you so sure of that?"
    show quinn neutraltalk
    quinn "Because when the rumors started, she didn’t deny them."
    show quinn mad
    quinn "Not even Vincent nor Vilhelm could get her out of her room. She locked herself in and stopped seeing anyone."
    show quinn annoyedce
    quinn "She was destroyed. That wasn’t guilt. That was grief."
    show bia surprise
    "It wasn’t the engagement that broke her heart; it was the betrayal by someone who had known her for who she truly was and used it against her."
    show bia frownla
    bia "I did try to help her, but she refused. She pushed me away."
    show quinn madtalk
    quinn "And why do you think that is?"
    hide bia
    hide quinn
    hide teanote
    with dissolve
    menu:
        "Did you ever think she deserved better.":
            mc "Did you ever think she deserved better from the people closest to her? That maybe all Seraphine ever wanted was an apology?"
            show bia raisedbrow with dissolve
            bia "And why would I apologize for something I didn’t do?"
            show bia neutraltalk
            bia "She did this to herself. Marcus deserved the truth, and I simply gave it to him."
            show bia neutral
            mc "Let’s say you walked into a room, and there’s a cake on the table, meant for someone else."
            mc "You want it. Bad enough that you tell everyone it’s gone stale, that it’s poisoned, that no one should have it at all. But then you take a slice anyway."
            mc "Would you still say you just told the truth?"
            show bia eyesnarrowed
            bia "I didn’t poison it. I didn’t take anything that wasn’t already slipping, already molding."
            bia "If she let him slip, then maybe she never had him at all."
            mc "But, it wasn’t yours to take."
            show bia sneer
            bia "Is that what this is about? Ownership? Possession? You all talk about Seraphine like she was untouchable. But you never saw what I saw. She wasn’t some perfect doll, she was cracking."
            show bia petulanttalk
            bia "And maybe...maybe I just stopped trying to save someone who didn't want to be saved."
            show bia petulant
            mc "You didn't try to save her. You could’ve been the one person who understood her, but instead…you made sure no one else did either."
            show bia raisedbrow
            bia "You think this is regret? That ship sank long ago. And she let it."
            mc "Then why are you still standing in the wreckage?"
            show bia sneer
            "Her hands tremble at her sides before she curls them into fists."
            show bia eyesnarrowed
            bia "She was everything that I couldn’t be…"
            show bia surprise
            mc "I think she had always saw you as {i}you{/i}. That’s what made this hurt the way it did."
            $ secretroute =+ 1
            hide bia
            with dissolve
            $ teaset = True
            jump investigate_biaroom
        "Do you deny it?":
            mc "You don’t deny knowing what happened?"
            show bia neutraltalk with dissolve
            bia "I know what everyone thinks happened. But does it really matter what’s true anymore? People believe what they want."
            show bia eyesnarrowed
            bia "Seraphine had every chance to defend herself and she chose not to."
            hide bia
            with dissolve
            $ teaset = True
            jump investigate_biaroom
        "Say nothing":
            show bia annoyed at right with dissolve
            bia "Fine. Be above it all. But let me remind you, Seraphine wasn’t a saint."
            show quinn annoyedce at left with dissolve
            quinn "Until now, you’re still spreading lies. Do you ever get tired of it?"
            hide bia
            hide quinn
            with dissolve
            $ teaset = True
            jump investigate_biaroom

label bfr_connectmirror:
    scene bg trnocard
    show ben frown at left
    with dissolve
    ben "What now? We’ve tried everything already but nothing’s happening."
    show bia frownla at right with dissolve
    bia "This is pointless."
    hide bia
    show quinn annoyedce at right
    with dissolve
    quinn "We’ve already looked around. What else is there to see?"
    mc "Sometimes…things don’t reveal themselves directly in the light."
    hide quinn
    show ben surprise at center
    with dissolve
    "A beat passes. Benette’s eyes snap to yours, realization dawning."
    ben "That’s it!"
    hide ben with dissolve
    "He strides to the far wall."
    play sound "audio/sfx/lightswitch.mp3" volume 0.5
    scene bg black
    "The room plunges into darkness."
    scene bg trnolight with fadein
    lys "Oh, great."
    lys "How clever. Now we really can’t see anything."
    luc "Wait."
    play sound "audio/sfx/curtainrustling.mp3" volume 0.5
    scene bg tropencurt with dissolve
    pause (0.1)
    scene bg trstartgame with dissolve
    "A stream of moonlight spills into the room as Lucien moves the curtain."
    show ben smile at left with dissolve
    ben "Yes! Look—on the mirror!"
    hide ben
    show luc shock at left
    with dissolve
    luc "It’s reflecting from it..."
    hide luc with dissolve
    "Your eyes follow moonlight as it bounces off a mirror and points back toward the wall."
    "You glance around. And then you see them. Mirrors. Each one carefully tilted and precisely placed, scattered across the furniture."
    pause (1.0)
    show ben surprise at left with dissolve
    ben "There’s something there…it shines differently…"
    scene bg c1 with dissolve
    play sound "audio/sfx/mirrorlight/lightmove.mp3" volume 0.12
    "He moves one mirror slightly. The beam shifts."

    # start game
    # jump ()
    jump connectmirror_mg



##---CONNECT MIRROR MINI-GAME---##
label connectmirror_mg:
    play music "audio/m_cm.mp3" fadein 1.0 fadeout 1.0 volume 0.6
    scene bg cmdark with fade
    $ setup_pipe_game()
    call screen connect_the_pipes
    return

label after_cm:
    play music "audio/m_tearoom.mp3" fadein 1.0 fadeout 1.0 volume 0.6
    scene bg c1 with fade
    "One by one, the mirrors come alive, reflecting the silver light in a steady, deliberate path."
    scene bg c2 with dissolve
    play sound "audio/sfx/mirrorlight/lightmove.mp3" volume 0.18
    pause (0.1)
    scene bg c3 with dissolve
    play sound "audio/sfx/mirrorlight/lightmove.mp3" volume 0.18
    pause (0.1)
    scene bg c4 with dissolve
    play sound "audio/sfx/mirrorlight/lightmove.mp3" volume 0.18
    pause (0.1)
    scene bg c5 with dissolve
    play sound "audio/sfx/mirrorlight/lightmove.mp3" volume 0.18
    "It dances across the room, catching glints of the group’s anxious faces before landing on a final piece."
    "{b}A bronze mirror.{/b}"
    "The light strikes it—\nAnd a shadow burns on the opposite wall. A projection of some sorts."
    "At first, it looks like a strange pattern. But as your eyes adjust, the scattered shapes focuses."
    "They're not just shadows. No. They're words."

# cutsceneee
# music here

label aftr_cutscene:
    # music changes here
    stop music fadeout 1.0
    scene bg c5bigger:
        xalign 0.5
        yalign 0.5
    show bia frownla
    with dissolve
    bia "After all these years, she’s still after me."
    show bia eyesnarrowed
    mc "She was your friend. Why are you treating her like she’s—"
    show bia offended
    bia "I didn’t treat her any more than she deserved…!"
    "You can sense the tension building, and your body instinctively shifts, stepping back, distancing yourself."
    show bia grit
    show luc mad  at right with dissolve
    luc "So that’s your attitude toward her? You spread lies about her for god’s sake, Bianca!"
    show bia sneer
    bia "Those lies were true! She never got over her mother’s passing. She was weak."
    show luc eyesnarrowed
    bia "If everyone knew who she really was underneath they would finally see her for who she is."
    show bia petulant
    bia "Marcus didn’t deserve that."
    show ben surprise at left
    with dissolve
    show luc shock
    ben "So you stole him from her?"
    show luc eyesnarrowed
    show bia frownla
    bia "No, I didn’t."
    hide ben
    hide luc
    show bia surprise
    with vpunch
    quinn "You stole her life!"
    "The words sting, and you take another step back, away from the rising anger."
    show bia eyesnarrowed
    bia "She didn’t deserve what she had."
    show luc eyesnarrowed at right with dissolve
    luc "Well, as much as she didn’t deserve you. What was all this for? Pettiness?"
    show lys mad at left with dissolve
    show bia annoyed
    lys "Jealousy."
    show bia mad
    show lys annoyed
    show luc mad
    bia "She had everything!"
    show bia grit
    bia "Seraphine had everything and never had to try. People flocked to her like mindless sheep, just because she opened her mouth."
    "And it’s out."
    "The truth is raw in the air now. You step back again, searching for anything to cool the tension."
    hide luc
    hide lys
    show quinn mad at right
    with dissolve
    show bia offended
    quinn "So you’re happy now? She’s gone, and all the attention’s on you? Is that why?"
    show quinn annoyedce
    quinn "This is stupid. Even the way you dress—it’s like you’re trying to be her."
    show bia mad
    show ben neutral at left with dissolve
    "Bianca steps forward, her hands raised in anger, but Benette moves quickly, pulling her back."
    show ben surprise
    show quinn mad
    show bia sneer
    bia "Don’t touch me!" with vpunch
    show ben frown
    "Benette lets go but stays close, her finger now aimed squarely at Quinn."
    hide ben
    hide quinn
    with dissolve
    show bia eyesnarrowed
    bia "You don’t get to lecture me about mimicry. You, of all people, should know what it’s like to be overshadowed."
    scene bg c5bigdark:
        xalign 0.5
        yalign 0.5
    show bia mad
    "Bianca whirls on the group, gesturing broadly."
    show bia mad 
    bia "Are you happy now? Fine. I admit it! Maybe I misled Marcus, maybe I lied to our friends! But it doesn’t change the fact that she chose to hide away."
    bia "This—"
    "Her words break off. The Bianca you met earlier, confident and poised, has dissolved completely. What’s left is someone frantic and desperate."
    "You withdraw slightly at the sight."
    show bia yell with vpunch
    bia "It’s always been mine. This…This was mine to take. Our friends. Marcus—he’s mine!"

    play sound "audio/sfx/doorclick.mp3" volume 0.9
    "As the words echo in the room. The door at the far back creaks open."
    show bia horrified
    show luc frown at right
    with dissolve
    luc "Despite everything, you still haven’t changed."
    "Disappointment. It hangs thick in the air. Palpable."
    scene bg c5bigger:
        xalign 0.5
        yalign 0.5
    hide luc
    hide bia
    with dissolve
    hide bg_black with dissolve
    "Lysander is the first to separate from the group, moving toward the open door with a quiet finality."
    "You feel a cold chill brush your shoulder. He is suddenly beside you, a hand maneuvering you out of the way but he’s not looking at the door."
    "Before you can dwell on it, he steps past and disappears through the doorway."
    "Quinn follows, his expression unreadable."
    "Lucien moves in next, slow but certain. Benette hesitates at the threshold and then steps in after them."
    "Bianca remains behind, running a hand through her hair, her breath uneven with exasperation."
    scene black with fade

    
