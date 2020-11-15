import tkinter as tk
from translate import Translator
import pyttsx3
from tkinter import messagebox


def speak(audio):
	engine = pyttsx3.init('sapi5')
	voices = engine.getProperty('voices')

	engine.setProperty('voice', voices[1].id)
	engine.say(audio)
	engine.runAndWait()


class Translate(object):

	LANGS = {
		'English': 'en-US',
		'Arabic': 'ar',
		'Spanish': 'es',
		'Chinese': 'zh',
		'German': 'de',
		'Frensh': 'fr',
		'Portugais': 'pt',
		'Hindi': 'hi',
		'Swedish': 'sv',
	}

	def __init__(self, master):

		self.master = master
		self.menu = tk.Menu(self.master)

		self.FROM = tk.StringVar(self.master)
		self.TO = tk.StringVar(self.master)
		self.var = tk.IntVar(self.master)
		self.result = ''

		self.option_menu = tk.Menu(self.menu, font=('Light',10), tearoff=False)

		self.mainFrame = tk.Frame(self.master)
		self.topFrame = tk.Frame(self.mainFrame)
		self.frame2 = tk.Frame(self.mainFrame)

		self.label1 = tk.Label(self.topFrame, text='from: ', font=('Helvetica', 15, 'underline'))
		self.l = tk.Label(self.topFrame, text=' ')
		self.label2 = tk.Label(self.topFrame, text='to: ', font=('Helvetica', 15, 'underline'))

		self.from_menu = tk.OptionMenu(self.topFrame, self.FROM, *list(self.LANGS.keys()))
		self.to_menu = tk.OptionMenu(self.topFrame, self.TO, *list(self.LANGS.keys()))

		self.FROM.set('English')
		self.TO.set('Spanish')

		self.entry = tk.Entry(self.frame2, width=25, bd=2, font=('Times', 18))
		self.button = tk.Button(self.frame2, text='go', width=5, bd=2, font=('Times', 18), bg='#00ff00',
			command=self.translate
		)
		self.speak_button = tk.Button(self.mainFrame, text='<< Speak >>', width=10, font=('Times', 18), bd=2,
			bg='#00ff00', command=lambda: speak(self.result), state='disabled'
		)

		self.text = tk.Text(self.mainFrame, width=30, bd=2, font=('Times', 20), height=10)

		self.master.bind('<Return>', self.translate)

	def setup(self):
		self.master.config(menu=self.menu)
		self.menu.add_cascade(label='options', menu=self.option_menu)

		self.option_menu.add_command(label='Dark Theme', command=self.set_dark)
		self.option_menu.add_command(label='Light Theme', command=self.set_light)
		self.option_menu.add_separator()
		self.option_menu.add_command(label='exit', command=self.master.destroy)

		self.mainFrame.pack(pady=20)
		self.topFrame.pack(pady=25)
		self.label1.grid(row=0, column=0, padx=15)
		self.from_menu.grid(row=0, column=1)
		self.l.grid(row=0, column=2, padx=35)
		self.label2.grid(row=0, column=3, padx=15)
		self.to_menu.grid(row=0, column=4)
		self.frame2.pack(pady=10)
		self.entry.grid(row=0, column=0, padx=5, ipady=7)
		self.button.grid(row=0, column=1)
		self.text.pack(pady=15)
		self.speak_button.pack(pady=20)

	def translate(self, *args):
		from_ = self.LANGS[self.FROM.get()]
		to_ = self.LANGS[self.TO.get()]

		if from_ == to_:
			messagebox.showerror('ERROR', 'You selected the same language !')
		else:
			translator = Translator(from_lang=from_, to_lang=to_)

			self.text.delete(1.0, 'end')
			self.result = translator.translate(self.entry.get())
			self.text.insert('end', self.result)
			self.speak_button['state'] = 'normal'

	def set_dark(self):
		self.master.config(bg='#00001a')
		self.mainFrame.config(bg='#00001a')
		self.topFrame.config(bg='#00001a')
		self.button.config(fg='white', bg='#004d00')
		self.frame2.config(bg='#00001a')
		self.l.config(bg='#00001a')
		self.label1.config(bg='#00001a', fg='white')
		self.label2.config(bg='#00001a', fg='white')
		self.speak_button.config(fg='white', bg='#004d00')

	def set_light(self):
		self.master.config(bg='SystemButtonFace')
		self.button.config(bg='#00ff00', fg='black')
		self.mainFrame.config(bg='SystemButtonFace')
		self.topFrame.config(bg='SystemButtonFace')
		self.frame2.config(bg='SystemButtonFace')
		self.l.config(bg='SystemButtonFace')
		self.label1.config(bg='SystemButtonFace', fg='black')
		self.label2.config(bg='SystemButtonFace', fg='black')
		self.speak_button.config(bg='#00ff00', fg='black')


def main():		
	root = tk.Tk()
	root.title('Translator')
	root.resizable(False, False)
	root.geometry('500x650')

	window = Translate(root)
	window.setup()

	root.mainloop()

main()

