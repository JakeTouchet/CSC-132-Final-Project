from tkinter import *
from tkinter import ttk 


#updates the scroll wheel depending on the size/amount of buttons
def updateScroll(*args):
    botCanvas.update()
    botCanvas.configure(scrollregion=(botCanvas.bbox('all')))


def updateButtonGrid(updatedButtons):
    
    #remove everything on the screen
    for i in buttons:
        i.grid_remove()


    #generate each button and place in the appropriate row/column
    for i in range(len(updatedButtons)):
        updatedButtons[i].grid(row = int(i/10), column = i%10, sticky = N + S + W + E)
    

def searchButtons(*args):
    updatedButtons = []

    if query.get() == '':
        updateButtonGrid(buttons)

    else:
        for button in buttons:
            if query.get() in button['text']:
                updatedButtons.append(button)
            
        updateButtonGrid(updatedButtons)

    root.after(1000, updateScroll)


##########################
# setting up main window #
##########################
root = Tk()
root.title("Prototype GUI")
root.geometry('1000x800')
root.minsize(955,620)
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=1)

#allows for scrolling in the button grid
# the logic is:     Scroll IF ((mouse is over frame2 buttons OR mouse is over frame2) AND (the buttons go beyond the screen AKA the canvas is scrollable)) --- Frame2 is botFrame internally
root.bind("<MouseWheel>", lambda event: botCanvas.yview_scroll(int(-event.delta/120), 'units') if (('frame2' in root.winfo_containing(event.x_root, event.y_root).winfo_parent()) or (root.winfo_containing(event.x_root, event.y_root) == botFrame)) and botCanvas.bbox('all')[3] > botCanvas.winfo_height() else None)

#########################
#       top frame       #
#########################
topFrame  = ttk.Frame(root, padding = '12 3 12 3')
topFrame.grid(row = 0, column = 0, sticky = N + E + W + S)

#setting up labels
ttk.Label(topFrame, text='Testing testing', font=("Arial", 25)).grid(row=0,column=0, columnspan=3)
ttk.Label(topFrame, text='Search:', font='Arial').grid(column=0, sticky=E+N)

searchTerm = StringVar()
searchTerm.trace_add('write', searchButtons)
# searchTerm.trace_add('write', updateScroll)
query = ttk.Entry(topFrame, width = 30, textvariable=searchTerm)
query.grid(row = 1, column = 1, sticky=N)
topFrame.columnconfigure(0, weight=1, minsize=70)
topFrame.columnconfigure(2, weight=1)
topFrame.rowconfigure(0,weight=2)
topFrame.rowconfigure(1,weight=1)



############################
#       bottom frame       # nightmare
############################
#                                                  THE SETUP:
# 
#                                                    Root ------Top Frame ---...
#                                                     |
#                                                     |
#                                                 Bot Frame
#                                                  /     \ 
#                                                 /        \ 
#                                               /             \ 
#                                           botCanvas         buttonScroll
#                                           /     
#                                         /         
#                                       /              
#                 botButtons (implented as a windowed widget in botCanvas)
# 
# 


#setting up bot frame
botFrame = ttk.Frame(root, borderwidth=5, relief='solid', takefocus=1)
botFrame.grid(row=1, column=0, sticky= N + E + W + S, padx=10, pady=10)
botFrame.columnconfigure(0, weight=1)
botFrame.rowconfigure(0,weight=1)



#setting up bottom canvas
botCanvas = Canvas(botFrame, highlightthickness=0)
botCanvas.grid(row=0, column=0, sticky=N + E + S + W)
#config the canvas to handle resizing of window and initial sizing of botButtons
botCanvas.bind("<Configure>", lambda x: botCanvas.itemconfig(botButtonsWindow, width=x.width-5))

#setting up the scroll bar
buttonScroll = Scrollbar(botFrame, orient='vertical', command=botCanvas.yview)
buttonScroll.grid(row=0, column=1, sticky = N + S)


#   START OF BUTTON GRID CODE   #
#initialize needed variables
botButtons  = ttk.Frame(botCanvas)
buttons = []
#all the different detectable objects
buttonNames = ['Airplane', 'Apple', 'Backpack', 'Banana', 'Baseball Bat', 'Baseball Glove', 'Bear', 'Bed', 'Bench', 'Bicycle', 'Bird', 'Boat', 'Book', 'Bottle', 'Bowl', 'Broccoli', 'Bus', 'Cake', 'Car', 'Carrot', 'Cat', 'Cell Phone', 'Chair', 'Clock', 'Couch', 'Cow', 'Cup', 'Dining Table', 'Dog', 'Donut', 'Elephant', 'Fire Hydrant', 'Fork', 'Frisbee', 'Giraffe', 'Hair Drier', 'Handbag', 'Horse', 'Hot Dog', 'Keyboard', 'Kite', 'Knife', 'Laptop', 'Microwave', 'Motorcycle', 'Mouse', 'Orange', 'Oven', 'Parking Meter', 'Person', 'Pizza', 'Potted Plant', 'Refrigerator', 'Remote', 'Sandwich', 'Scissors', 'Sheep', 'Sink', 'Skateboard', 'Skis', 'Snowboard', 'Spoon', 'Sports Ball', 'Stop Sign', 'Suitcase', 'Surfboard', 'Teddy Bear', 'Tennis Racket', 'Tie', 'Toaster', 'Toilet', 'Toothbrush', 'Traffic Light', 'Train', 'Truck', 'Tv', 'Umbrella', 'Vase', 'Wine Glass', 'Zebra']
buttonNum = 80

#set up all rows and columns in the grid
for i in range(int(buttonNum/10)+1):
    botButtons.rowconfigure(i)

for i in range(10):
    botButtons.columnconfigure(i, minsize=90, weight=1)

#generate each button and place in the appropriate row/column
for i in range(buttonNum):
    buttons.append(ttk.Button(botButtons, text = buttonNames[i], command = lambda: print('f')))
    buttons[i].grid(row = int(i/10), column = i%10, sticky = N + S + W + E, ipady = 30)


#set botButtonsWindow not to the frame object but to the object returned by the create_window function
botButtonsWindow = botCanvas.create_window(0, 0, window=botButtons, anchor='nw')


#configure the canvas's scroll bar
botCanvas.update() # needed or botCanvas.bbox() will be all 1s
botCanvas.configure(yscrollcommand=buttonScroll.set, scrollregion=botCanvas.bbox('all'))

#   END OF BUTTON GRID CODE   #


root.mainloop()
