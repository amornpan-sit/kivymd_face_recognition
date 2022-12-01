from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
import cv2

class MainApp(MDApp):
	def build(self):
		layout = MDBoxLayout(orientation='vertical')
		layout.add_widget(MDRaisedButton(
			text = "Recall",
			pos_hint={'center_x': .5, 'center_y': .5},
			size_hint = (None,None))
		)
		return layout

if __name__ == '__main__':
	MainApp().run()