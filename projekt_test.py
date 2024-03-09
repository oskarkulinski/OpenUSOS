import usosapi
import flet as ft

# USOS API Base URL, trailing slash included.
USOS_API_BASE_URL = 'https://apps.usos.uj.edu.pl/'

# Consumer Key to use.
CONSUMER_KEY = '748apdbMm3Ggh6KGXMyp'
CONSUMER_SECRET = 'Y33JYY3vgjNym6aFP5qnxcMtE7WrejLt8VDjWS87'

# We use usosapi package in order to do EVERYTHING much easier:

# We create connection object (We will be using that to call requests):
# Valid consumer_key and consumer_secret is needed for that:
Main = usosapi.USOSAPIConnection(USOS_API_BASE_URL, CONSUMER_KEY, CONSUMER_SECRET)


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
    Main.get('services/mailclient/refresh_recipients', message_id=Message_id["message_id"])

    # Finally, we send the message:

    Main.get('services/mailclient/send_message', message_id=Message_id["message_id"])




#  Some function to choose what user wants
def Choose_What_To_Do():
    print("Welcome to SUS!")
    print("")
    print("What would you like to do?")

    print("1: Register for a course (not yet possible)" )
    print("2: Make a mail (quite possible)")
    Choice = int(input('Please, input a number '))
    while Choice not in {1, 2}:
        Choice = int(input('Please, input a VALID number '))
    if Choice == 1:
        print('nah')
        pass
    if Choice == 2:
        Send_an_email()


#--------------------------------------------------------------------------------------------
# 'Main' here
#--------------------------------------------------------------------------------------------

def main(page: ft.Page):

    # Test  to check if connection is valid:
    print(Main.test_connection())

    # User has to visit using some internet browser to obtain a PIN code required for authorization.
    # IDK, you do frontend lul
    AuthURL = Main.get_authorization_url()
    print(AuthURL)  # Pass it to user somehow
    PIN = input('What is the PIN code? ')
    PIN.replace(" ", "")
    # Authorization:
    Main.authorize_with_pin(PIN)
    # test: return users firstname, lastname, id:
    lalala = Main.current_identity()
    print(lalala)
    # Access token, can be used to continue a session:
    Access = Main.get_access_data()
    print(Access)  # We should probably save it, so that user doesn't have to log in all the time.

    # Now, do stuff:
    Choose_What_To_Do()

    # Logging out:
    Main.logout()


ft.app(target=main)
