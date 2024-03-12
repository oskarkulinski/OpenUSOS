import usosapi
import os

# USOS API Base URL, trailing slash included.
Usosapi_base_url = 'https://apps.usos.uj.edu.pl/'

# Consumer Key to use.
Consumer_key = '748apdbMm3Ggh6KGXMyp'
Consumer_secret = 'Y33JYY3vgjNym6aFP5qnxcMtE7WrejLt8VDjWS87'

# We use usosapi.py in order to do EVERYTHING much easier:

# We create connection object (We will be using that to call requests): 
# Valid consumer_key and consumer_secret is needed for that:
Main = usosapi.USOSAPIConnection(Usosapi_base_url, Consumer_key, Consumer_secret)

def Send_an_email():
    Subject = input('Input the subject for your message: ')
    Content = input('Input the content of your message: ')
    Recepient = input('Input an e-mail of the recepient: ')

    Recepient_list = {Recepient}
    # We create the message:
    Message_id = Main.get('services/mailclient/create_message', subject=Subject, content=Content)

    # We update (create) recepient:
    Main.get('services/mailclient/update_recipients_group', message_id=Message_id["message_id"], emails=Recepient_list)
    # Then we refresh them:
    Main.get('services/mailclient/refresh_recipients', message_id=Message_id["message_id"] )

    # Finally, we send the message:

    Main.get('services/mailclient/send_message', message_id=Message_id["message_id"])

# Returning the time(s) of all activities for the week
def Get_times():
    print("Getting times of all your activities:")
    print("")
    #We get the List of Activity objects
    List = Main.get('services/tt/student')
    num = 0
    for activity in List:
        num = num + 1
    print("Test: You have " + str(num) + " activities")

# Function that will save Access token of user, allowing us to log in without authorization:
def Remember_me():
    if os.path.exists("usos_token.txt"):
        # First we delete this file if it exists:
        os.remove("usos_token.txt")
    AT, ATS = Main.get_access_data()
    with open("token.txt", "w") as file:
        file.write(AT)
        file.write("\n")
        file.write(ATS)
# Function that checks if token is saved and valid:
def No_verification() -> bool:
    if os.path.exists("token.txt"):
        with open("token.txt", "r") as file:
            line1 = file.readline()
            AT = str(line1.strip())
            line2 = file.readline()
            ATS = str(line2.strip())
        if(Main.set_access_data(AT, ATS)):
            return True;
        else:
            return False;


# Some function to choose what user wants
def Choose_What_To_Do():
    print("Welcome to SUS!")
    print("")
    print("What would you like to do?")

    print("1: Register for a course (not yet possible)" )
    print("2: Make a mail (quite possible)")
    print("3: Make a reminder of my activities (test, for now it just counts your activities)")
    print("4: Keep me logged in (works!)")
    print("5: Log out")
    Choice = int(input('Please, input a number '))
    while Choice not in {1, 2, 3, 4, 5}:
        Choice = int(input('Please, input a VALID number '))
    if Choice == 1:
        print('nah')
        pass
    if Choice == 2:
        Send_an_email()
    if Choice == 3:
        Get_times()
    if Choice == 4:
        Remember_me()
    if Choice == 5:
        Main.logout()

#--------------------------------------------------------------------------------------------
# 'Main' here
#--------------------------------------------------------------------------------------------

# Test  to check if connection is valid:
print(Main.test_connection())
# We try to verify without PIN first
if(No_verification() == False):    
    # User has to visit using some internet browser to obtain a PIN code required for authorization.
    # IDK, you do frontend lul
    AuthURL = Main.get_authorization_url()
    print(AuthURL) # Pass it to user somehow
    PIN = input('What is the PIN code? ')
    PIN.replace(" ", "")
    # Authorization:
    Main.authorize_with_pin(PIN)
# test: return users firstname, lastname, id:
lalala = Main.current_identity()
print(lalala)
# Access token, can be used to continue a session:
Access = Main.get_access_data()
print(Access) # We should probably save it, so that user doesn't have to log in all the time.

# Now, do stuff:
Choose_What_To_Do()

# Logging out:
# Main.logout()
# Lul, do not logout without asking, it deletes the access token
# It took me like an hour to realize that :(
