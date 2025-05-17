    ####################
    #   About Screen   #
    ####################

image return_idle:
    "gui/screens/return_idle.png"
    zoom 0.75

image return_hover:
    "gui/screens/return_hover.png"
    zoom 0.75


image ig_idle:
    "images/icons/icn-instagram.png"
    zoom 0.6

image ig_hover:
    "images/icons/icn-instagram-hover.png"
    zoom 0.6


image tk_idle:
    "images/icons/icn-tiktok.png"
    zoom 0.6

image tk_hover:
    "images/icons/icn-tiktok-hover.png"
    zoom 0.6


image twt_idle:
    "images/icons/icn-twitter.png"
    zoom 0.6

image twt_hover:
    "images/icons/icn-twitter-hover.png"
    zoom 0.6



screen about():

    tag menu

    # style_prefix "about"

    # Background image
    add "gui/screens/about_bg.png" xysize (config.screen_width, config.screen_height)

    # Return Button
    imagebutton:
        idle "return_idle"
        hover "return_hover"
        xpos 1605
        ypos 555
        action Return()

    frame:
        style "game_menu_outer_frame"
        xfill True
        yfill True
        xsize 1300 # width
        ysize 680 # height

        xpos 0.48
        xanchor 0.5
        ypos 0.45
        yanchor 0.5


        viewport:
            scrollbars "vertical"
            mousewheel True
            draggable True
            yinitial 0.0

            vbox:
                xsize 1300
                xalign 0.5
                
                # Hiraya Studios Logo
                add "gui/hiraya-studios-logo.png" zoom 0.7 xalign 0.5

                text "{i}Hiraya Studios{/i}" style "about_logo_text" xalign 0.5
                
                null height 120

                # Game Name
                add "gui/title-horizontal.png" zoom 0.32 xalign 0.5

                null height 120

                # MR - Hannah
                text "Hannah" style "member_text" xalign 0.5
                text "UI Artist" style "body_text" xalign 0.5
                text "Level Designer" style "body_text" xalign 0.5

                null height 50

                # MR - Princess
                text "Princess" style "member_text" xalign 0.5
                text "Writer" style "body_text" xalign 0.5
                text "Programmer" style "body_text" xalign 0.5

                null height 50

                # MR - Sandy
                text "Sandy" style "member_text" xalign 0.5
                text "Sprite, BG, CG Artist" style "body_text" xalign 0.5
                text "Color Designer" style "body_text" xalign 0.5
            
                null height 50

                # MR - Patrice
                text "Patrice" style "member_text" xalign 0.5
                text "Item Artist" style "body_text" xalign 0.5
                text "Sound Designer" style "body_text" xalign 0.5
                
                null height 120

                # Music & SFX
                text "Music & SFX" style "headers_text" xalign 0.5
                text "Gnossiennes No.1 - Alfred Eric Leslie Satie (1866-1925)" style "body_text" xalign 0.5
                text "Turkish Towel - Johnny Hamp's Kentucky Serenaders (1926)" style "body_text" xalign 0.5
                text "Togetherless - Franz Gordon (2020)" style "body_text" xalign 0.5
                text "Youtube" style "body_text" xalign 0.5
                text "SoundCloud" style "body_text" xalign 0.5
                text "Pixabay" style "body_text" xalign 0.5
                

                null height 80

                # Fonts
                text "Fonts" style "headers_text" xalign 0.5
                text "Cotta Free" style "body_text" xalign 0.5
                text "Sora" style "body_text" xalign 0.5
                
                null height 80

                # Main in Renpy
                text "Made in" style "headers_text" xalign 0.5
                text "Ren’Py 8.3.7" style "body_text" xalign 0.5
                
                null height 80

                # Socmed cta
                text "Stay Updated & Follow Us On" style "headers_text" xalign 0.5

                null height 20  
                hbox:
                    xalign 0.5  # Center the icons
                    spacing 20

                    # Instagram
                    imagebutton:
                        idle "ig_idle"
                        hover "ig_hover"
                        action OpenURL("https://www.instagram.com/thelasttoast_official/")
                        ysize 20 #button size

                    # Tiktok
                    imagebutton:
                        idle "tk_idle"
                        hover "tk_hover"
                        action OpenURL("https://www.tiktok.com/@thelasttoast_official")
                        ysize 20

                    # Twitter
                    imagebutton:
                        idle "twt_idle"
                        hover "twt_hover"
                        action OpenURL("https://x.com/studioshiraya")
                
                null height 20
                text "Official website coming soon!" style "body_text" xalign 0.5
                # text "Visit our official website {a=https://www.renpy.org/}link here{/a}" style "body_text" xalign 0.5
                
                



## Text Styles

# Logo Name (Hiraya Studios)
style about_logo_text:
    font "fonts/Sora-Medium.ttf"
    size 30
    color "#E7ECF2"

# Team Member Name
style member_text:
    font "fonts/Sora-Medium.ttf"
    size 28
    color "#F1E293"

# Roles of Each Member
style body_text:
    font "fonts/Sora-Regular.ttf"
    size 26
    color "#E7ECF2"

# Team Member Name
style headers_text:
    font "fonts/Sora-Medium.ttf"
    size 29
    color "#E3BD6A"




# style about_label_text:
#     # size gui.label_text_size
#     font 'fonts/Sora-Regular.ttf'
#     size 24
#     color "#E7ECF2"

# style about_text:
#     font 'fonts/Sora-Regular.ttf'
#     size 24