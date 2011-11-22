from Fbot import *
from Tkinter import *
from PIL import Image, ImageTk
import time


class MyStatusBar(Frame):
	def __init__(self, master):
		Frame.__init__(self, master)
		self.label = Label(self, bd=1, relief=SUNKEN, anchor=W)
		self.label.pack(fill=X)
		self.pack(side=BOTTOM, fill=X)

	def setText(self, text):
		self.label.config(text=text)
		self.label.update_idletasks()

	def setColor(self, color):
		self.label.config(fg=color)
		self.label.update_idletasks()

	def clear(self):
		self.label.config(text="")
		self.label.update_idletasks()

class MyToolBar(Frame):
	def __init__(self, master):
		Frame.__init__(self, master)
		self.pack(side=TOP, fill=X)
		self.createButtons(5)

	def createButtons(self, number):
		image = Image.open("button.png")
		self.photo = ImageTk.PhotoImage(image)
		self.buttonList = []
		for i in range (0, number):
			button = Button(self, image=self.photo)
			button.pack(side=LEFT)
			self.buttonList.append(button)

	def bindButton(self, index, callback):
		self.buttonList[index-1].config(command=callback)

class MyConsole(Frame):
	def __init__(self, master):
		Frame.__init__(self, master)
		self.text = Text(self)
		self.text.config(state=DISABLED)
		self.text.pack()
		self.pack()

	def setTextColor(self, color):
		self.text.config(fg=color)

	def setBackgroundColor(self, color):
		self.text.config(bg=color)

	def appendLine(self, line):
		self.text.config(state=NORMAL)
		self.text.insert(END, line+'\n')
		self.text.config(state=DISABLED)
		
	def clear(self):
		self.text.config(state=NORMAL)
		self.text.delete(1.0, END)
		self.text.config(state=DISABLED)

class GUI(Tk):
	def __init__(self, config):
		Tk.__init__(self, None)
		self.perso = config
		self.bot = Fbot(self.perso)
		self.buildGui()

	def buildGui(self):
		self.title(self.perso.login_username)
		self.statusBar = MyStatusBar(self)
		self.toolbar = MyToolBar(self)
		self.console = MyConsole(self)
		
		self.crashCount = 0

	def clean(self):
		self.bot.running = False
		self.bot.join()
		print ("exiting")

	def refresh(self):
		self.console.clear()
		self.console.appendLine("crash " + str(self.crashCount) + " time(s)")
		if (not self.bot.isRunning()):
			self.crashCount = self.crashCount + 1
			self.bot.join()
			time.sleep(15)
			self.bot = Fbot(self.perso)
