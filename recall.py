from kivy.graphics.texture import Texture
from kivymd.uix.label import MDLabel
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivy.uix.image import Image
from kivy.clock import Clock
import cv2
import random
import requests

random_number = random.randint(1000,9999)
class MainApp(MDApp):
	def build(self):
		self.theme_cls.theme_style = "Dark"
		layout = MDBoxLayout(orientation='vertical')

		self.image = Image()
		layout.add_widget(self.image)

		self.label = MDLabel(
                    text='Verification Uninitiated',
                    halign="center",
                    theme_text_color='Primary',
                )
		layout.add_widget(self.label)

		self.save_img_button = MDRaisedButton(
			text="Recall",
			pos_hint={'center_x': .5, 'center_y': .5},
			size_hint=(None, None))
		self.save_img_button.bind(on_press=self.take_picture)
		layout.add_widget(self.save_img_button)

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

		image_name = "recall_picture_"+str(random_number)+".png"
		cv2.imwrite(image_name, self.image_frame)

		self.label.text = self.facerecognition(image_name)

	def facerecognition(self, face_image):
		url = "http://113.53.253.55:5002/face_recognize"

		payload = {}
		files = [
			('image', (face_image, open(face_image, 'rb'), face_image))
		]
		headers = {}

		response = requests.request("POST", url, headers=headers, data=payload, files=files)

		return response.text

if __name__ == '__main__':
	MainApp().run()
