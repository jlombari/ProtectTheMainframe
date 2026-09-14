# Player variables -------------------
default player_score = 0
default player_health = 100
default player_completed = False
default persistent.past_attempts = []

# Python Initialize ------------------
init python:
    import random
    from datetime import datetime
    
    h3lp_speech = [
            "voice/h3lp_talk1.ogg",
            "voice/h3lp_talk2.ogg",
            "voice/h3lp_talk3.ogg",
            "voice/h3lp_talk4.ogg",
        ]
    def h3lp_callback(event, interact=True, **kwargs):
        if event == "show":
            renpy.sound.play(
                random.choice(h3lp_speech),
                relative_volume=1.3
            )
    def play_squish(trans, st, at):
        renpy.sound.play("audio/bug_squished.ogg", relative_volume=0.99)
        return none
    def save_score(score, health, completed):
        new_attempt = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "score": score,
            "health": health,
            "status": "Completed" if completed else "Defeated"
        }
        persistent.past_attempts.append(new_attempt)
    _preferences.set_volume("music", 0.45)

# Player UI --------------------------
screen health_ui():
    zorder 100
    frame:
        xalign 0.89
        yalign 0.02
        padding (15, 10)
        text "HP: [player_health]" size 24 color "#ffffff"
screen score_ui():
    zorder 100
    frame:
        xalign 0.98
        yalign 0.02
        padding (15, 10)
        text "Score: [player_score]" size 24 color "#ffffff"
screen attempts_history_screen():
    modal True
    tag menu
    
    frame:
        xalign 0.5
        yalign 0.5
        xsize 800
        ysize 600
        padding (30, 30)
        
        vbox:
            spacing 15
            
            text "Previous Attempts" size 32 bold True xalign 0.5
            null height 10
            hbox:
                spacing 10
                text "Date/Time" bold True xsize 260
                text "Status" bold True xsize 150
                text "Score" bold True xsize 120
                text "Health" bold True xsize 120
            null height 5
            viewport:
                scrollbars "vertical"
                mousewheel True
                draggable True
                yfill False
                vbox:
                    spacing 8
                    if not persistent.past_attempts:
                        text "No previous attempts have been recorded yet." italic True color "#aaa" xalign 0.5
                    else:
                        for attempt in reversed(persistent.past_attempts):
                            frame:
                                xsize 720
                                padding (10, 8)
                                background "#22222288"
                                hbox:
                                    spacing 10
                                    text attempt.get("date", "N/A") size 18 xsize 250
                                    if attempt.get("status") == "Completed":
                                        text attempt.get("status", "N/A") size 18 xsize 140 color "#4CAF50"
                                    else:
                                        text attempt.get("status", "N/A") size 18 xsize 140 color "#F44336"
                                    text str(attempt.get("score", 0)) size 18 xsize 110
                                    text str(attempt.get("health", 0)) size 18 xsize 110
            textbutton "Close" action Hide("attempts_history_screen") xalign 0.5
# Character Initialize ---------------
define h = Character(
    "H-3lP",
    color="#60db02",
    callback=h3lp_callback
)

# Animations & Effects ---------------
transform apply_blur(amount=20):
    mesh True
    blur amount
transform bounce:
    linear 3.0 yalign 0.5 xalign 0.5
    linear 3.0 yalign 0.6 xalign 0.5
    repeat
transform leftIdle:
    linear 2.5 yalign 0.5 xalign 0.15
    linear 2.5 yalign 0.55 xalign 0.15
    repeat

# Character images -------------------
image H3lP Happy = "H3lP_Happy.png"
image H3lP Sad = "H3lP_Sad.png"
image H3lP Question = "H3lP_Question.png"
image Bug Default = "Bug_Default.png"
image Bug Squish:
    "Bug_Squished.png"
    
    on show:
        function play_squish

# Start of game ----------------------
label start:
    # Introduction
    play music "bg_default.ogg" volume 0.60
    scene bg room with dissolve
    show H3lP Happy at bounce with dissolve
    pause 3.0
    h "Welcome to Protect the Mainframe!\n..."
    show H3lP Happy at truecenter with dissolve
    h "I found some bugs in our mainframe and I need your help to destroy them!\n..."
    show H3lP Question at truecenter with dissolve
    menu:
        "Will you help me?"
        # play sound "h3lp_question.ogg"
        "Let's Do This!":
            show H3lP Happy at truecenter with dissolve
            h "Great! Let me load you in\n..."
            stop music
            jump quiz
        "Previous Attempts":
            show screen attempts_history_screen
            jump start
        "No Thank you...":
            return
        "DEV: Jump to game_over":
            jump game_over
        "DEV: Jump to game_complete":
            jump game_complete
    # Start of quiz ------------------
    label quiz:        
        # Initialize quiz UI
        play music "bg_mainframe.ogg"
        play sound "entering_mainframe.ogg" volume 0.7
        scene bg mainframe at apply_blur(20)
        with dissolve
        show screen score_ui
        show screen health_ui
        pause 5.0
        # Quiz instructions
        show H3lP Happy at truecenter with dissolve
        h "Welcome to the mainframe! Let's get started\n..."
        show H3lP Happy at leftIdle
        h "You must destroy the bugs by answering questions correctly.\n..."
        h "Wrong answers will take away your health.\nLose all your health and we lose the mainframe\n..."
        
        label q1:
            show Bug Default at Position(xalign=0.5, yalign=0.05) with dissolve
            show H3lP Question at leftIdle with dissolve
            play sound "h3lp_positive1.ogg" # REPLACEME
            menu:
                "Question 1: What data type is used for whole numbers like 5, 42, or 1007?"
                "int (integer)":
                    $ player_score += 5
                    show Bug Squish at truecenter with dissolve
                    show H3lP Happy at Position(xalign=0.15, yalign=0.5) with dissolve
                    play sound "h3lp_positive1.ogg" # REPLACEME
                    h "Bug destroyed!\n..."
                    jump q2
                "str (string)":
                    $ player_health -= 10
                    hide Bug Default with dissolve
                    show H3lP Sad at Position(xalign=0.5, yalign=0.5) with dissolve
                    h "oh no! That bug got away..."
                    if player_health <= 0:
                        jump game_over
                    jump q2
                "boolean":
                    $ player_health -= 10
                    hide Bug Default with dissolve
                    show H3lP Sad at Position(xalign=0.5, yalign=0.5) with dissolve
                    h "oh no! That bug got away..."
                    if player_health <= 0:
                        jump game_over
                    jump q2
                "DEV: JUMP TO LAST":
                    jump q11
        label q2:
            show Bug Default at Position(xalign=0.5, yalign=0.05) with dissolve
            show H3lP Question at leftIdle with dissolve
            menu:
                "Question 2: What data type is text inside quotes, like \"Hello World\"?"
                "int":
                    $ player_health -= 10
                    hide Bug Default with dissolve
                    show H3lP Sad at Position(xalign=0.5, yalign=0.5) with dissolve
                    h "oh no! That bug got away..."
                    if player_health <= 0:
                        jump game_over
                    jump q3
                "str":
                    $ player_score += 5
                    play sound "bug_squished.ogg"
                    show Bug Squish at truecenter with dissolve
                    show H3lP Happy at Position(xalign=0.15, yalign=0.5) with dissolve
                    h "Bug destroyed!"
                    jump q3
                "bool":
                    $ player_health -= 10
                    hide Bug Default with dissolve
                    show H3lP Sad at truecenter with dissolve
                    h "oh no! That bug got away..."
                    if player_health <= 0:
                        jump game_over
                    jump q3
        label q3:
            show Bug Default at Position(xalign=0.5, yalign=0.05) with dissolve
            show H3lP Question at leftIdle with dissolve
            menu:
                "Which data type can only be either TRUE or FALSE?"
                "float":
                    $ player_health -= 10
                    hide Bug Default with dissolve
                    show H3lP Sad at Postion(xalign=0.5, yalign=0.5) with dissolve
                    h "Oh no! That bug got away..."
                    if player_health <= 0:
                        jump game_over
                    jump q4
                "int":
                    $ player_health -= 10
                    hide Bug Default with dissolve
                    show H3lP Sad at Position(xalign=0.5, yalign=0.5) with dissolve
                    h "Oh no! that bug got away..."
                    if player_health <= 0:
                        jump game_over
                    jump q4
                "boolean":
                    $ player_score += 5
                    play sound "bug_squished.ogg"
                    show Bug Squish at truecenter with dissolve
                    show H3lP Happy at Position(xalign=0.15, yalign=0.5) with dissolve
                    h "Bug destroyed!"
                    jump q4
        label q4:
            show Bug Default at Position(xalign=0.5, yalign=0.05) with dissolve
            show H3lP Question at leftIdle with dissolve
            menu:
                "What data type is a decimal number like 3.14 or 9.5?"
                "float":
                    $ player_score += 5
                    play sound "bug_squished.ogg"
                    show Bug Squish at truecenter with dissolve
                    show H3lP Happy at Position(xalign=0.15, yalign=0.5) with dissolve
                    h "Bug destroyed!"
                    jump q5
                "string":
                    $ player_health -= 10
                    hide Bug Default with dissolve
                    show H3lP Sad at truecenter
                    h "Oh no! That bug got away..."
                    if player_health <= 0:
                        jump game_over
                    jump q5
                "integer":
                    $ player_health -= 10
                    hide Bug Default with dissolve
                    show H3lP Sad at truecenter
                    h "Oh no! That bug got away..."
                    if player_health <= 0:
                        jump game_over
                    jump q5
        label q5:
            show Bug Default at Position(xalign=0.5, yalign=0.05) with dissolve
            show H3lP Question at leftIdle with dissolve
            menu:
                "What type of data does the input() function ALWAYS return?"
                "int":
                    $ player_health -= 10
                    hide Bug Default with dissolve
                    show H3lP Sad at truecenter with dissolve
                    h "Oh no! That bug got away..."
                    if player_health <= 0:
                        jump game_over
                    jump q6
                "str":
                    $ player_score += 5
                    play sound "bug_squished.ogg"
                    show Bug Squish at truecenter with dissolve
                    show H3lP Happy at Position(xalign=0.15, yalign=0.5) with dissolve
                    h "Bug destroyed!"
                    jump q6
                "bool":
                    $ player_health -= 10
                    hide Bug Default with dissolve
                    show H3lP Sad at truecenter with dissolve
                    h "Oh no! That wasn't it..."
                    if player_health <= 0:
                        jump game_over
                    jump q6           
        label q6:
            show Bug Default at Position(xalign=0.5, yalign=0.05) with dissolve
            show H3lP Question at leftIdle with dissolve
            menu:
                "Which Python function prints text onto the screen?"
                "output()":
                    $ player_health -= 10
                    hide Bug Default with dissolve
                    show H3lP Sad at truecenter with dissolve
                    h "Oh no! That bug got away..."
                    if player_health <= 0:
                        jump game_over
                    jump q7
                "write()":
                    $ player_health -= 10
                    hide Bug Default with dissolve
                    show H3lP Sad at truecenter with dissolve
                    h "Oh no! That bug got away..."
                    if player_health <= 0:
                        jump game_over
                    jump q7
                "print()":
                    $ player_score += 5
                    play sound "bug_squished.ogg"
                    show Bug Squish at truecenter with dissolve
                    show H3lP Happy at Position(xalign=0.15, yalign=0.5) with dissolve
                    h "Bug destroyed!"
                    jump q7
        label q7:
            show Bug Default at Position(xalign=0.5, yalign=0.05) with dissolve
            show H3lP Question at leftIdle with dissolve
            menu:
                "How do you store the value 10 inside a variable named 'score'?"
                "score = 10":
                    $ player_score += 5
                    play sound "bug_squished.ogg"
                    show Bug Squish at truecenter with dissolve
                    show H3lP Happy at Position(xalign=0.15, yalign=0.5) with dissolve
                    h "Bug destroyed!"
                    jump q8
                "10 = score":
                    $ player_health -= 10
                    hide Bug Default with dissolve
                    show H3lP Sad at truecenter with dissolve
                    h "Oh no! That bug got away..."
                    if player_health <= 0:
                        jump game_over
                    jump q8
                "set score to 10":
                    $ player_health -= 10
                    hide Bug Default with dissolve
                    show H3lP Sad at truecenter with dissolve
                    h "Oh no! That bug got away..."
                    if player_health <= 0:
                        jump game_over
                    jump q8
        label q8:
            show Bug Default at Position(xalign=0.5, yalign=0.05) with dissolve
            show H3lP Question at leftIdle with dissolve
            menu:
                "Which variable name is written correctly in Python?"
                "my score":
                    $ player_health -= 10
                    hide Bug Default with dissolve
                    show H3lP Sad at truecenter with dissolve
                    h "Oh no! That bug got away..."
                    if player_health <= 0:
                        jump game_over
                    jump q9
                "my_score":
                    $ player_score += 5
                    play sound "bug_squished.ogg"
                    show Bug Squish at truecenter with dissolve
                    show H3lP Happy at Position(xalign=0.15, yalign=0.5) with dissolve
                    h "Bug destroyed!"
                    jump q9
                "1st_score":
                    $ player_health -= 10
                    hide Bug Default with dissolve
                    show H3lP Sad at truecenter with dissolve
                    h "Oh no! That bug got away..."
                    if player_health <= 0:
                        jump game_over
                    jump q9                
        label q9:
            show Bug Default at Position(xalign=0.5, yalign=0.05) with dissolve
            show H3lP Question at leftIdle with dissolve
            menu:
                "What symbol is used to check if two values are EQUAL in Python?"
                " = ":
                    $ player_health -= 10
                    hide Bug Default with dissolve
                    show H3lP Sad at truecenter with dissolve
                    h "Oh no! That bug got away..."
                    if player_health<= 0:
                        jump game_over
                    jump q10
                " == ":
                    $ player_score += 5
                    play sound "bug_squished.ogg"
                    show Bug Squish at truecenter with dissolve
                    show H3lP Happy at Position(xalign=0.15, yalign=0.5) with dissolve
                    h "Bug destroyed!"
                    jump q10
                " -> ":
                    $ player_health -= 10
                    hide Bug Default with dissolve
                    show H3lP Sad at truecenter with dissolve
                    h "Oh no! That bug got away..."
                    if player_health <= 0:
                        jump game_over
                    jump q10               
        label q10:
            show Bug Default at Position(xalign=0.5, yalign=0.05) with dissolve
            show H3lP Question at leftIdle with dissolve
            menu:
                "What will be the output of \'print(5 + 3 * 2)\' be?"
                " 11 ":
                    $ player_score += 5
                    play sound "bug_squished.ogg"
                    show Bug Squish at truecenter with dissolve
                    show H3lP Happy at Position(xalign=0.15, yalign=0.5) with dissolve
                    h "Bug destroyed!"
                    jump q11
                " 16 ":
                    $ player_health -= 10
                    hide Bug Default with dissolve
                    show H3lP Sad at truecenter with dissolve
                    h "Oh no! That bug got away..."
                    if player_health <= 0:
                        jump game_over
                    jump q11
                " 10 ":
                    $ player_health -= 10
                    hide Bug Default with dissolve
                    show H3lP Sad at truecenter with dissolve
                    h "Oh no! That bug got away..."
                    if player_health <= 0:
                        jump game_over
                    jump q11
        label q11:
            show Bug Default at Position(xalign=0.5, yalign=0.05) with dissolve
            show H3lP Question at leftIdle with dissolve
            menu:
                "What symbol is used for multiplication in Python?"
                " x ":
                    $ player_health -= 10
                    hide Bug Default with dissolve
                    show H3lP Sad at truecenter with dissolve
                    h "Oh no! That bug got away..."
                    if player_health <= 0:
                        jump game_over
                    jump q12
                " \* ":
                    $ player_score += 5
                    play sound "bug_squished.ogg"
                    show Bug Squish at truecenter with dissolve
                    show H3lP Happy at Position(xalign=0.15, yalign=0.5) with dissolve
                    h "Bug destroyed!"
                    jump q12
                " \% ":
                    $ player_health -= 10
                    hide Bug Default with dissolve
                    show H3lP Sad at truecenter with dissolve
                    h "Oh no! That bug got away..."
                    if player_health <= 0:
                        jump game_over
                    jump q12               
        label q12:
            show Bug Default at Position(xalign=0.5, yalign=0.05) with dissolve
            show H3lP Question at leftIdle with dissolve
            menu:
                "Which keyword is used to test a condition if the first \'if\' statement was False?"
                "else if":
                    $ player_health -= 10
                    hide Bug Default with dissolve
                    show H3lP Sad at truecenter with dissolve
                    h "Oh no! That bug got away..."
                    if player_health <= 0:
                        jump game_over
                    jump q13                
                "elif":
                    $ player_score += 5
                    play sound "bug_squished.ogg"
                    show Bug Squish at truecenter with dissolve
                    show H3lP Happy at Position(xalign=0.15, yalign=0.5) with dissolve
                    h "Bug destroyed!"
                    jump q13
                "check":
                    $ player_health -= 10
                    hide Bug Default with dissolve
                    show H3lP Sad at truecenter with dissolve
                    h "Oh no! That bug got away..."
                    if player_health <= 0:
                        jump game_over
                    jump q13            
        label q13:
            show Bug Default at Position(xalign=0.5, yalign=0.05) with dissolve
            show H3lP Question at leftIdle with dissolve
            menu:
                "Which loop runs continuously as long as a condition remains True?"
                "while loop":
                    $ player_score += 5
                    play sound "bug_squished.ogg"
                    show Bug Squish at truecenter with dissolve
                    show H3lP Happy at Position(xalign=0.15, yalign=0.5) with dissolve
                    h "Bug destroyed!"
                    jump q14
                "repeat loop":
                    $ player_health -= 10
                    hide Bug Default with dissolve
                    show H3lP Sad at truecenter with dissolve
                    h "Oh no! That bug got away..."
                    if player_health <= 0:
                        jump game_over
                    jump q14                    
                "for loop":
                    $ player_health -= 10
                    hide Bug Default with dissolve
                    show H3lP Sad at truecenter with dissolve
                    h "Oh no! That bug got away..."
                    if player_health <= 0:
                        jump game_over
                    jump q14
        label q14:
            show Bug Default at Position(xalign=0.5, yalign=0.05) with dissolve
            show H3lP Question at leftIdle with dissolve
            menu:
                "What symbol MUST go at the end of an \'if\' or \'while\' line in Python?"
                "Semicolon (;)":
                    $ player_health -= 10
                    hide Bug Default with dissolve
                    show H3lP Sad at truecenter with dissolve
                    h "Oh no! That bug got away..."
                    if player_health <= 0:
                        jump game_over
                    jump q15
                "Colon (:)":
                    $ player_score += 5
                    play sound "bug_squished.ogg"
                    show Bug Squish at truecenter with dissolve
                    show H3lP Happy at Position(xalign=0.15, yalign=0.5) with dissolve
                    h "Bug destroyed!"
                    jump q15
                "Period (.)":
                    $ player_health -= 10
                    hide Bug Default with dissolve
                    show H3lP Sad at truecenter with dissolve
                    h "Oh no! That bug got away..."
                    if player_health <= 0:
                        jump game_over
                    jump q15
        label q15:
            show Bug Default at Position(xalign=0.5, yalign=0.05) with dissolve
            show H3lP Question at leftIdle with dissolve
            menu:
                "What keyword is used to exit out of a loop early?"
                "stop":
                    $ player_health -= 10
                    hide Bug Default with dissolve
                    show H3lP Sad at truecenter with dissolve
                    h "Oh no! That bug got away..."
                    if player_health <= 0:
                        jump game_over
                    jump game_complete
                "exit":
                    $ player_health -= 10
                    hide Bug Default with dissolve
                    show H3lP Sad at truecenter with dissolve
                    h "Oh no! That bug got away..."
                    if player_health <= 0:
                        jump game_over
                    jump game_complete
                "break":
                    $ player_score += 5
                    play sound "bug_squished.ogg"
                    show Bug Squish at truecenter with dissolve
                    show H3lP Happy at Position(xalign=0.15, yalign=0.5) with dissolve
                    h "Bug destroyed!"
                    hide Bug Squish with dissolve
                    show H3lP Happy at truecenter with dissolve
                    h "That was the last of them! Great job!"
                    jump game_complete
                    
        label game_over:
            play music "bg_game_over.ogg"
            scene bg corrupted with dissolve
            show H3lP Sad at truecenter with dissolve
            play sound h3lp_game_over
            h "There are too many bugs! The mainframe has been destroyed..."
            h "Score: [player_score]\nHP: [player_health]"
            menu:
                "Try Again?"
                "Yes":
                    stop music
                    jump quiz
                "Not now":
                    return
        label game_complete:
            # play music "bg_game_complete.ogg"
            scene bg room with dissolve
            show H3lP Happy at truecenter with dissolve
            h "You did it! Thank you so much!"
            h "Score: [player_score]\nHP: [player_health]"
            return
        
        
    # End of game

    return
