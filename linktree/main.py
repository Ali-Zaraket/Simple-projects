import tkinter as t
import webbrowser
from database import Database
from tkinter import messagebox
from PIL import Image, ImageTk

db = Database()


class Link(t.Label):
	
	def __init__(self, master=None, link=None, fg='grey', font=('Arial', 10), *args, **kwargs):
		super().__init__(master, *args, **kwargs)
		self.master = master
		self.default_color = fg	# keeping track of the default color 
		self.color = 'blue'   # the color of the link after hovering over it 
		self.default_font = font 	# keeping track of the default font
		self.link = link 

		""" setting the fonts as assigned by the user or by the init function  """
		self['fg'] = fg
		self['font'] = font 

		""" Assigning the events to private functions of the class """

		self.bind('<Enter>', self._mouse_on) 	# hovering over 
		self.bind('<Leave>', self._mouse_out)	# away from the link
		self.bind('<Button-1>', self._callback) # clicking the link

	def _mouse_on(self, *args):
		""" 
			if mouse on the link then we must give it the blue color and an 
			underline font to look like a normal link
		"""
		self['fg'] = self.color
		self['font'] = self.default_font + ('underline', )

	def _mouse_out(self, *args):
		""" 
			if mouse goes away from our link we must reassign 
			the default color and font we kept track of   
		"""
		self['fg'] = self.default_color
		self['font'] = self.default_font

	def _callback(self, *args):
		webbrowser.open_new(self.link) 


class PlaceholderEntry(t.Entry):

	def __init__(self, master=None, placeholder='placeholder', color='grey', *args, **kwargs):
		super().__init__(master, *args, **kwargs)

		self.placeholder = placeholder
		self.color = color
		self.default_fg_color = self['fg']

		self.bind('<FocusIn>', self.focus_in)
		self.bind('<FocusOut>', self.focus_out)

		self.put_placeholder()

	def put_placeholder(self):
		self.insert(0, self.placeholder)
		self['fg'] = self.color

	def focus_in(self, *args):
		if self['fg'] == self.color:
			self.delete(0, t.END)
			self['fg'] = self.default_fg_color

	def focus_out(self, *args):
		if not self.get():
			self.put_placeholder() 


class MainGui(object):

	current_page = 1
	pages = []
	current_links = []

	def __init__(self, master):
		self.master = master
		self.background_image = ImageTk.PhotoImage(Image.open('back.jpg'))
		self.background_label = t.Label(self.master, image=self.background_image)
		self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
		self.menu = t.Menu(self.master)
		self.master.config(menu=self.menu)

		self.options_menu = t.Menu(self.menu, font=('Light',10), tearoff=False)
		self.menu.add_cascade(label='options', menu=self.options_menu)
		self.options_menu.add_command(label='Add Link', command=AddLinkWindow.start)
		self.options_menu.add_command(label='Delete Link', command=DeleteLinkWindow.start)
		self.options_menu.add_command(label='Update Link', command=UpdateLinkWindow.start)
		self.options_menu.add_command(label='Refresh', command=self.setup)
		self.options_menu.add_separator()
		self.options_menu.add_command(label='Exit', command=self.master.destroy)
		self.title_label = t.Label(self.master, text='...Linktree...', font=('courier', 25, 'underline'),
			bg='#770341', fg='white', padx=20, pady=5
		)
		self.title_label.pack(pady=20)
		self.next_button = t.Button(self.master, text='Next', bd=0, fg='white', bg='#770341',
			width=6, height=1, font=('Light', 13), command=self.next
		)
		self.previous_button = t.Button(self.master, text='Previous', bd=0, fg='white', bg='#770341',
			width=6, height=1, font=('Light', 12), command=self.previous
		)
		self.next_button.bind('<Enter>', lambda e: self.button_animation(self.next_button))
		self.previous_button.bind('<Enter>', lambda e: self.button_animation(self.previous_button))
		self.next_button.bind('<Leave>', lambda e: self.button_animation(self.next_button, 'leave'))
		self.previous_button.bind('<Leave>', lambda e: self.button_animation(self.previous_button, 'leave'))

	def button_animation(self, button, *args):
		button['width'] = 7
		button['height'] = 2

		if 'leave' in args:
			button['width'] = 6
			button['height'] = 1

	def setup(self):
		self.current_page = 1
		for lnk in self.current_links:
			lnk.pack_forget()

		self.current_links = []
		self.pages = []

		global pages_required	
		remaining = len(db.get())%5
		pages_required = len(db.get())//5 if not remaining else len(db.get())//5 + 1

		start = 0
		for i in range(1, pages_required+1):
			page = {}
			for element in db.get()[start:i*5]:
				
				title, url = element
				page[title] = url
			start += 5
			self.pages.append(page)

		self.refresh()

	def refresh(self):
		if len(db.get()) > 5:
			self.next_button.place(x=430, y=550)

		if self.current_page == pages_required:
			self.next_button.place_forget()

		if self.current_page == 1:
			self.previous_button.place_forget()

		if self.current_page > 1:
			self.previous_button.place(x=2, y=554)

		for idx, page in enumerate(self.pages):
			if self.current_page == idx+1:
				for key in page:
					canvas = t.Canvas(self.master, bg='#806000')
					link = Link(canvas, bg='#806000', text=key, link=page[key],
						fg='white', width=23, height=2, font=('Light', 18)
					)
					canvas.pack(pady=15)
					link.pack()
					self.current_links.append(canvas)

	def next(self):
		for c in self.current_links:
			c.pack_forget()

		self.current_page += 1
		self.refresh()

	def previous(self):
		for c in self.current_links:
			c.pack_forget()

		self.current_page -= 1
		self.refresh()

	@staticmethod
	def start():
		window = t.Tk()
		window.title('Linktree')
		window.resizable(False, False)
		window.geometry('500x600')

		guiApp = MainGui(window)
		guiApp.setup()

		window.mainloop()


class AddLinkWindow:

	def __init__(self, master):
		self.master = master
		self.mainFrame = t.Frame(self.master, bg='grey', highlightbackground="black", highlightthickness=1,
			padx=30, pady=50 
		)
		self.title = t.Label(self.mainFrame, text='...Add Link...', font=('Helvetica', 25, 'underline'), bg='grey')
		self.titleEntry = PlaceholderEntry(self.mainFrame, placeholder='   Enter link title', width=40, bd=1, font=('Light', 15))
		self.urlEntry = PlaceholderEntry(self.mainFrame, placeholder='   Enter link/url', width=40, bd=1, font=('Light', 15))
		self.submitButton = t.Button(self.mainFrame, text='Submit', width=25, bd=0, bg='green', fg='white',
			command=self.submit, height=1, font=('Times', 18)
		)

		self.master.bind('<Return>', self.submit)

	def setup(self):
		self.mainFrame.pack(pady=20, padx=20)
		self.title.pack()
		t.Label(self.mainFrame, text= '', bg='grey').pack(pady=18)
		self.titleEntry.pack(pady=5, ipady=5)
		self.urlEntry.pack(pady=5, ipady=5)
		self.submitButton.pack(pady=20)

	def submit(self, *args):
		if self.titleEntry.get() and self.urlEntry.get():
			db.save([self.titleEntry.get(), self.urlEntry.get()])
			messagebox.showinfo('Added', 'Your link has been added !!\nMake sure to refresh your linktree!')
			self.master.destroy()

		else:
			messagebox.showwarning('Blanks', 'Please fill up all blanks before submit..')

	@staticmethod
	def start():
		window = t.Tk()
		window.title('Add Link')
		window.geometry('500x420')
		window.resizable(False, False)

		window_add = AddLinkWindow(window)
		window_add.setup()

		window.mainloop()


class DeleteLinkWindow:

	def __init__(self, master):
		self.master = master
		self.mainFrame = t.Frame(self.master, bg='grey', highlightbackground="black", highlightthickness=1,
			padx=20, pady=25 
		)
		self.title = t.Label(self.mainFrame, text='...Delete Link...', font=('Helvetica', 25, 'underline'), bg='grey')
		self.frame2 = t.Frame(self.mainFrame, bg='grey')
		self.scroll = t.Scrollbar(self.frame2, orient=t.VERTICAL)
		self.listbox = t.Listbox(self.frame2, bd=2, font=('Times', 15), yscrollcommand=self.scroll.set)
		self.scroll.config(command=self.listbox.yview)
		self.listbox.insert('end', *[element[0] for element in db.get()])

		self.delete_button = t.Button(self.mainFrame, text='Delete', bd=0, bg='red', fg='white',
			width=20, font=('Times', 18), height=1, command=self.delete
		)
		self.master.bind('<Return>', self.delete)

	def setup(self):
		self.mainFrame.pack(pady=25)
		self.title.pack(pady=10)
		t.Label(self.mainFrame, text=' ', bg='grey').pack(pady=15)
		self.frame2.pack(pady=15)
		self.scroll.pack(side=t.RIGHT, fill=t.Y)
		self.listbox.pack(ipadx=80)
		self.delete_button.pack(pady=20)
	
	def delete(self, *args):
		if self.listbox.get(t.ANCHOR):
			
			msg = messagebox.askokcancel('Delete', 'Sure to delete the link?!')
			if msg:
				db.delete(self.listbox.get(t.ANCHOR))
				messagebox.showinfo('Done', 'Your Link Has Been Deleted !!\nMake sure to refresh your linktree!')
				self.master.destroy()

		else:
			messagebox.showwarning('Empty', 'Please Choose a link to delete!')

	@staticmethod
	def start():
		window = t.Tk()
		window.title('Delete Link')
		window.resizable(False, False)
		window.geometry('500x600')

		window_delete = DeleteLinkWindow(window)
		window_delete.setup()

		window.mainloop()


class UpdateLinkWindow:

	selected_link = None
	update_key = None

	def __init__(self, master):
		self.master = master
		self.mainFrame = t.Frame(self.master, bg='grey', highlightbackground="black", highlightthickness=1,
			padx=15, pady=40 
		)

		self.title = t.Label(self.mainFrame, text='...Update Link...', font=('Helvetica', 25, 'underline'), bg='grey')
		self.subtitle = t.Label(self.mainFrame, text=' ', font=('Light', 15), bg='grey', fg='white')
		self.mainFrame.pack(pady=25, ipadx=60)
		self.title.pack(pady=10)
		self.subtitle.pack(pady=5)
		self.first()

	def first(self):
		self.frame = t.Frame(self.mainFrame, bg='grey')
		self.scroll = t.Scrollbar(self.frame, orient=t.VERTICAL)
		self.listbox = t.Listbox(self.frame, font=('Times', 15), yscrollcommand=self.scroll.set, bd=2)
		self.scroll.config(command=self.listbox.yview)
		self.listbox.insert('end', *[element[0] for element in db.get()])
		self.frame.pack(pady=10)
		self.scroll.pack(side=t.RIGHT, fill=t.Y)
		self.listbox.pack(ipady=80, ipadx=50)
		self.subtitle.config(text='(Double click to select)')
		self.listbox.bind('<Double-Button-1>', self.next)

	def select(self, type_):
		self.update_key = type_
		self.final()

	def next(self, *args):
		self.selected_link = self.listbox.get(t.ANCHOR)
		self.frame.pack_forget()
		self.subtitle.config(text='(select what to edit)')
		self.title_button = t.Button(self.mainFrame, text='Edit title', bd=0, bg='green', fg='white',
			width=20, font=('Times', 18), height=1, command=lambda : self.select('title')
		)
		self.url_button = t.Button(self.mainFrame, text='Edit Url', bd=0, bg='green', fg='white',
			width=20, font=('Times', 18), height=1, command=lambda : self.select('url')
		)
		self.title_button.pack(pady=20)
		self.url_button.pack(pady=10)

	def final(self):
		self.title_button.pack_forget()
		self.url_button.pack_forget()
		self.subtitle.config(text='Press enter to update')
		self.new_value_entry = PlaceholderEntry(self.mainFrame, placeholder=f'   Enter new {self.update_key}',
			width=30, font=('Light', 15), bd=0
		)
		self.new_value_entry.pack(pady=50, ipady=5)
		self.new_value_entry.bind('<Return>', self.finish)

	def finish(self, *args):
		msg = messagebox.askokcancel('Update', 'Sure to update?\nPress ok to proceed..')
		if msg:
			db.update(self.update_key, self.new_value_entry.get(), self.selected_link)
			messagebox.showinfo('Done', 'Updated..!!\nMake sure to refresh your linktree!')
			self.master.destroy()

		else:
			pass

	@staticmethod
	def start():
		window = t.Tk()
		window.title('Update Link')
		window.geometry('450x450')

		window_update = UpdateLinkWindow(window)

		window.mainloop()


if __name__ == '__main__':
	MainGui.start()
