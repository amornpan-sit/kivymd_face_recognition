import cv2
from kivy.graphics.texture import Texture
from kivy.uix.image import Image
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivy.clock import Clock
import random
import requests

random_number = random.randint(1000,9999)
image_name = ""

class MainApp(MDApp):
	def build(self):
		self.theme_cls.theme_style = "Dark"
		layout = MDBoxLayout(orientation='vertical')

		self.txtName = MDTextField(
			hint_text = "Full Name",
		)
		layout.add_widget(self.txtName)

		self.txtEmail = MDTextField(
			hint_text="Email Address",
		)
		layout.add_widget(self.txtEmail)

		self.txtMobile = MDTextField(
			hint_text="Mobile",
		)
		layout.add_widget(self.txtMobile)

		self.image = Image()
		layout.add_widget(self.image)

		self.take_photo_button = MDRaisedButton(
			text="Take Photo",
			pos_hint={'center_x': .5, 'center_y': .5},
			size_hint=(None, None))
		self.take_photo_button.bind(on_press=self.take_picture)
		layout.add_widget(self.take_photo_button)

		self.submit_button = MDRaisedButton(
			text="Submit",
			pos_hint={'center_x': .5, 'center_y': .5},
			size_hint=(None, None))
		self.submit_button.bind(on_press=self.submit_form)
		layout.add_widget(self.submit_button)

		self.label = MDLabel(
			text='Register Result...',
			halign="center",
			theme_text_color='Primary',
		)
		layout.add_widget(self.label)

		self.capture = cv2.VideoCapture(0)
		Clock.schedule_interval(self.load_video, 1.0 / 30.0)

		return layout

	def load_video(self, *args):
		ret, frame = self.capture.read()
		# Frame initialize
		self.image_frame = frame
		buffer = cv2.flip(frame, 0).tostring()
		texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
		texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
		self.image.texture = texture

	def take_picture(self, *args):

		self.image_name = "register_picture_"+str(random_number)+".png"
		cv2.imwrite(self.image_name, self.image_frame)


	def register(self, email, name, mobile, face_image):
		url = "http://113.53.253.55:5002/register"

		payload = {
			'email': email,
			'name': name,
			'mobile': mobile,
			'pid': ''}
		files = [
			('file', (face_image, open(face_image, 'rb'), face_image))
		]
		headers = {}

		response = requests.request("POST", url, headers=headers, data=payload, files=files)

		if response.text != '':
			return "Register Successfully"
		else:
			return "Register failed!!"

	def submit_form(self, *args):

		self.label.text = self.register(self.txtEmail.text, self.txtName.text, self.txtMobile.text, self.image_name)

if __name__ == '__main__':
	MainApp().run()