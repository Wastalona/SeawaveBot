WELCOME_TEXT:str = "Welcome to the Sea Wave Camp. I'm a telegram bot for employees and administrators who work there. Here are the functions that are available to you."
ADMIN_CMDS: str = "Admin commands:\n1. reports\n2. repcard\n3. set notify\n4. notify\n5. hire\n6. release\n7. transfer\n8. staff"
EMPL_CMDS: str = "Employee commands:\n1. photo_report\n2. video_report\n3. open_shift\n4. close_shift"

# Reports loads
SUCC_LOAD: str = "The report has been uploaded successfully."
FAIL_LOAD: str = "An error occurred while uploading reports."

# Admin reports
FAIL_LOAD_REP: str = "Reports could not be loaded."
FAIL_LOAD_REPCARD: str = "The report card could not be loaded."

# Notifications
SET_NOTIFY_TEXT: str = "Enter the notification text that you want to display."
NOTIFY_TEXT: str = "The text of the message has been successfully installed."
NOTIFY_ERR: str = "An error occurred while trying to send notifications."
SET_NOTIFY_ERR: str = "An error occurred while trying to set the notification text. Please make sure that you have set up an alert message."

# Staff editor
STAFF_TRS: str = "Here is a template \"staff_id new_profession\" that you can use to transfer an employee."
STAFF_RELEASE: str = "Enter the staff ID. You can get a list of IDs using the \"staff\" command."
STAFF_HIRE: str = "Enter the employee ID and profession, separated by a space. You can get a list of IDs using the \"staff\" command."
STAFF_LOAD_ERR: str = "An error occurred while trying to get a list of employees."
STAFF_SUC_ADD: str = "New staff has been successfully added."
STAFF_SUC_REL: str = "New staff has been successfully released."
STAFF_SUC_TRS: str = "New staff has been successfully transferred."
STAFF_ERR: str = "An error occurred when changing staff."

# Errors
LOG_ERR: str = "Something went wrong: "