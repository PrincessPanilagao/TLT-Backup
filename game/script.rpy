    #####################################################
    #   The Last Toast: A Murder Mystery Visual Novel   #
    #                (c) Hiraya Studios                 #
    #####################################################


## Splash Screen ##
image splash = "splash-screen.png"
image disclaimer = "images/disclaimer.png"

label splashscreen:
    scene black
    with Pause (1)

    show splash with dissolve
    with Pause(2)

    scene black with dissolve
    with Pause(1)

    $ renpy.transition(fade, layer="master")

    # Show disclaimer
    show disclaimer
    with fade
    
    pause 15

    hide disclaimer
    with fade
    return

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



## Character Flips ##
image maleser flip = Transform("images/characters/maleser.png", xzoom=-1)


## Python Codes ##
default letter_opened = False
default quinn_done = False
default luclys_done = False
default bb_done = False

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

    
    # AUDIO
    # def play_open_letter():
    #     renpy.log("Playing sound now!")
    #     renpy.music.set_volume(0.4, channel="sfx_once")
    #     renpy.sound.play("audio/sfx/openletter.mp3", channel="sfx_once")


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
    show expression "images/thank-u-screen.png" with fade
    pause
    scene black with fade
    stop music fadeout 1.0
    return
















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

    