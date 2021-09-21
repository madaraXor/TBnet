from tkinter import *

root = Tk()

root.grid_columnconfigure(1,weight=1) # the text and entry frames column
root.grid_rowconfigure(0,weight=1) # all frames row

# conf frame 1
frame1 = Frame(root, bg ="red", relief=GROOVE ,borderwidth=2)
frame1.grid(column=0, row=0, sticky='news')
Label(frame1, text="frame1 0:0").grid(column=0, row=0)

# conf frame 2
frame2 = Frame(root, bg ="grey", relief=GROOVE, borderwidth=2)
frame2.grid_rowconfigure(0,  weight =0)
frame2.grid_rowconfigure(1,  weight =1)
frame2.grid_columnconfigure(0,  weight =1)
frame2.grid(column=1, row=0, sticky='news')
Label(frame2, text="Mon text").grid(column=0, row=0)
text = Text(frame2)
text.config(state=DISABLED)
text.grid(column=0, row=1, sticky='news')

# conf frame 3
frame3 = Frame(frame2, bg ="blue", relief=GROOVE ,borderwidth=2)
frame3.grid(column=0, row=2, sticky='news')
frame3.grid_columnconfigure(0,  weight =1)
frame3.grid_columnconfigure(1,  weight =1)
frame3.grid_columnconfigure(1,  weight =1)
value = StringVar() 
value.set("texte par défaut")
boutonShowInfo = Button(frame3, text="Show Info")
boutonShowInfo.grid(column=0, row=0, sticky='w')
entree = Entry(frame3, textvariable=value, width=30)
entree.grid(column=1, row=0, sticky='w')
boutonEnvoyer = Button(frame3, text="Envoyer")
boutonEnvoyer.grid(column=2, row=0, sticky='e')


root.mainloop()