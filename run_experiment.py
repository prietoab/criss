import sys
from os import system

USER_CONFIG_BUILD_SCRIPT_NAME = "build_user_config_file.py"
WEB_APP_SCRIPT_NAME = "webapp.py"

# ----------------------------------
# BULDING THE USER CONFIG FILE
# ----------------------------------

volunteer_id = int(sys.argv[1])

bash_command_user_config = (
    "python "
    + USER_CONFIG_BUILD_SCRIPT_NAME
    + " "
    + str(volunteer_id)
)

system(bash_command_user_config)

# ----------------------------------
# RUNNING THE WEB APP
# ----------------------------------

bash_command_web_abb = (
    "python "
    + WEB_APP_SCRIPT_NAME
)

system(bash_command_web_abb)
