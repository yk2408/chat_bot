from django.test import TestCase
from .models import ChatLog, User
# Create your tests here.


class SaveChat:
    def __init__(self, user, send_msg, receive_msg):
        self.user = user
        self.send_msg = send_msg
        self.receive_msg = receive_msg

    def check_value(self):
        if self.receive_msg == "":
            return "Success"
        else:
            ChatLog.objects.create(user=self.user, send_msg=self.send_msg, receive_msg=self.receive_msg)
            return "Failed"

    def check_number(self):
        try:
            send_number_value = float(self.send_msg)
            return "Number"
        except:
            return "Not Number"


class ChatTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@gmail.com', full_name="test_user", password='12345')
        self.send_msg = "123"
        self.receive_msg = ""
        print("setUp method execute")

    # test1 check received message value is empty?
    def test_empty_value_case(self):
        chat = SaveChat(self.user, self.send_msg, self.receive_msg)
        self.assertEqual(chat.check_value(), "Success", "Message value is not empty!!")

    # test2 check send message is number type?
    def test_number_value_case(self):
        chat = SaveChat(self.user, self.send_msg, self.receive_msg)
        self.assertEqual(chat.check_number(), "Number", "Sending message is not number type!!")

    def tearDown(self):
        print("tearDown method execute")