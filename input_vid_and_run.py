import sys
from os import system

USER_CONFIG_BUILD_SCRIPT_NAME = "build_user_config_file.py"
WEB_APP_SCRIPT_NAME = "webapp.py"


# ----------------------------------
# GET VOLUNTEER ID FROM KEYBOARD
# ----------------------------------

try:
    print("+=======================================================")
    print(" CRISS (Cognitive Response for Image Stimuli Software)  ")
    print("+=======================================================")
    print()
    volunteer_id = int(input('Input the volunteer ID (integer number) : '))
    vid_is_int = True
    print("Ok.")
except ValueError:
    print("Not a integer number")
    vid_is_int = False


if vid_is_int:
    # ----------------------------------
    # CREATING THE USER CONFIG FILE
    # ----------------------------------
    print("Creating the user configuration file ... ",end='')
    bash_command_user_config = (
        "python "
        + USER_CONFIG_BUILD_SCRIPT_NAME
        + " "
        + str(volunteer_id)
    )

    system(bash_command_user_config)
    print("Ok.")
    # ----------------------------------
    # RUNNING THE WEB APP
    # ----------------------------------

    print("Starting the experiment ... ")
    bash_command_web_abb = (
        "python "
        + WEB_APP_SCRIPT_NAME
    )

    system(bash_command_web_abb)
    print("Experiment completed.")