from tkinter import *
from tkinter import ttk 
import platform

#this is because pip install ThemedTK only works on linux and we also only use it for linux users
if platform.system() == "Linux":
    from ttkthemes import ThemedTk
from PIL import ImageTk
import pika

def main():

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
                if query.get().lower() in button['text'].lower():
                    updatedButtons.append(button)
                
            updateButtonGrid(updatedButtons)

        #increase the time waited for higher button counts to reduce lag based glitches
        root.after(500, updateScroll)


    
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.56.1', credentials=pika.PlainCredentials('admin1', 'admin1')))
    channel = connection.channel()

    channel.exchange_declare(exchange='GUI', exchange_type='fanout')

    channel.basic_publish(exchange='GUI', routing_key='', body='GUI is up')


    ##########################
    # setting up main window #
    ##########################
    if platform.system() == "Windows":
        root = Tk()
    # if user is on linux use 'scidgrey' theme
    elif platform.system() == "Linux":
        root = ThemedTk(theme='scidgrey')
    root.title("Py-Clops Control Deck")
    root.geometry('1100x650')
    root.minsize(975,620)
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)


    #setting up Styles
    style = ttk.Style(root)

    #root style, all ttk widgets will default to this unless otherwise specified
    style.configure('.', background = '#313338', foreground = '#a1a1a1')

    #specific styles for specific widgets
    style.configure("button.TButton", foreground = "#000000", font = ('arial',9,'bold'))
    style.configure("gridButton.button.TButton", background = '#7f7f7f')
    style.configure('botButtons.TFrame', background= '#7f7f7f')
    style.configure('botFrame.TFrame' , background = '#7f7f7f')


    #setting up overarching frame (pretty much just for background color)
    allFrame = ttk.Frame(root)
    allFrame.columnconfigure(0, weight=1)
    allFrame.rowconfigure(1, weight=6)
    allFrame.grid(row=0, column=0, sticky=N+E+S+W)


    #allows for scrolling in the button grid in the bottom frame its just up here bc it looks better to have all the root configuration in one place
    # the logic:     Scroll IF ((mouse is over botFrame buttons OR mouse is over botFrame) AND (the buttons go beyond the screen AKA the canvas is scrollable))
    if platform.system() == 'Windows':
        root.bind("<MouseWheel>", lambda event: botCanvas.yview_scroll(int(-event.delta/120), 'units') if ((event.widget in buttons) or (event.widget == botFrame) or event.widget == buttonScroll) and botCanvas.bbox('all')[3] > botCanvas.winfo_height() else None)
    elif platform.system() == 'Linux':
        root.bind("<Button-4>", lambda event: botCanvas.yview_scroll(-1, 'units') if ((event.widget in buttons) or (event.widget == botFrame)) and botCanvas.bbox('all')[3] > botCanvas.winfo_height() else None)
        root.bind("<Button-5>", lambda event: botCanvas.yview_scroll(1, 'units') if ((event.widget in buttons) or (event.widget == botFrame)) and botCanvas.bbox('all')[3] > botCanvas.winfo_height() else None)
        

    #########################
    #       top frame       #
    #########################
    topFrame  = ttk.Frame(allFrame, padding = '12 3 12 3')
    topFrame.grid(row = 0, column = 0, sticky = N + E + W + S)
    topFrame.columnconfigure(0, weight=1, minsize=70)
    topFrame.columnconfigure(2, weight=1)

    #setting up labels
    textFont = ('arial',12,'bold')
    ttk.Label(topFrame, text='Pi-Clops Control Deck', font=("Yu Gothic UI ", 25)).grid(row=0,column=0, columnspan=3, pady= ( 20, 20 ))
    ttk.Label(topFrame, text='Search:', font=textFont).grid(column=0, sticky=E)

    #Setting up the entry widget and making sure any updates to it will run the search command
    searchTerm = StringVar()
    searchTerm.trace_add('write', searchButtons)
    query = ttk.Entry(topFrame, width = 30, textvariable=searchTerm)
    query.grid(row = 1, column = 1)


    #initialize pause button
    ttk.Button(topFrame, style= 'button.TButton', width=10, text = 'Pause', command = lambda: channel.basic_publish(exchange='GUI', routing_key='control', body='stop')).grid(row=2, column=0, sticky = E, ipady = 7, pady = (15, 0), padx= (4, 0))
    #initialize unpause button
    ttk.Button(topFrame, style= 'button.TButton', width = 10, text = 'Unpause', command = lambda: channel.basic_publish(exchange='GUI', routing_key='control', body='start')).grid(row=2, column=1, sticky = E, ipady = 7, pady = (15, 0), padx= (4, 7))




    ############################
    #       bottom frame       #
    ############################
    #                                                  THE SETUP:
    # 
    #                                                    Root ------Top Frame ---...
    #                                                     |
    #                                                     |
    #                                                 botFrame (Frame)
    #                                                  /     \ 
    #                                                 /        \ 
    #                                               /             \ 
    #                                      botCanvas (Canvas)    buttonScroll (ScrollBar)
    #                                           /     
    #                                         /         
    #                                       /              
    #                 botButtons (implented as a windowed widget in botCanvas)
    # 
    # 


    #setting up bot frame
    botFrame = ttk.Frame(allFrame, borderwidth=5, relief='solid', takefocus=1, style= 'botFrame.TFrame')
    botFrame.grid(row=1, column=0, sticky= N + E + W + S, padx=10, pady=10)
    botFrame.columnconfigure(0, weight=1)
    botFrame.rowconfigure(0, weight=1)



    #setting up bottom canvas
    botCanvas = Canvas(botFrame, highlightthickness=0, background='gray50')
    botCanvas.grid(row=0, column=0, sticky=N + E + S + W)
    #config the canvas to handle resizing of window and initial sizing of botButtons
    botCanvas.bind("<Configure>", lambda event: botCanvas.itemconfig(botButtonsWindow, width=event.width))

    #setting up the scroll bar
    buttonScroll = Scrollbar(botFrame, orient='vertical', command=botCanvas.yview)
    buttonScroll.grid(row=0, column=1, sticky = N + S)


    #   START OF BUTTON GRID CODE   #

    #initialize needed variables
    botButtons  = ttk.Frame(botCanvas, style= 'botButtons.TFrame')
    buttons = []       #list of the button objects
    buttonImages = []  #list of the button's images
    buttonNum = 80     #amount of buttons
    #all the different detectable objects
    buttonNames = ['Airplane', 'Apple', 'Backpack', 'Banana', 'Baseball Bat', 'Baseball Glove', 'Bear', 'Bed', 'Bench', 'Bicycle', 'Bird', 'Boat', 'Book', 'Bottle', 'Bowl', 'Broccoli', 'Bus', 'Cake', 'Car', 'Carrot', 'Cat', 'Cell Phone', 'Chair', 'Clock', 'Couch', 'Cow', 'Cup', 'Dining Table', 'Dog', 'Donut', 'Elephant', 'Fire Hydrant', 'Fork', 'Frisbee', 'Giraffe', 'Hair Drier', 'Handbag', 'Horse', 'Hot Dog', 'Keyboard', 'Kite', 'Knife', 'Laptop', 'Microwave', 'Motorcycle', 'Mouse', 'Orange', 'Oven', 'Parking Meter', 'Person', 'Pizza', 'Potted Plant', 'Refrigerator', 'Remote', 'Sandwich', 'Scissors', 'Sheep', 'Sink', 'Skateboard', 'Skis', 'Snowboard', 'Spoon', 'Sports Ball', 'Stop Sign', 'Suitcase', 'Surfboard', 'Teddy Bear', 'Tennis Racket', 'Tie', 'Toaster', 'Toilet', 'Toothbrush', 'Traffic Light', 'Train', 'Truck', 'TV', 'Umbrella', 'Vase', 'Wine Glass', 'Zebra']
    

    #set up columns in the grid to fill extra space by stretching and all have uniform width
    for i in range(10):
        botButtons.columnconfigure(i, weight=1, uniform='smef')

    #generate each button and place in the appropriate row/column
    for i in range(buttonNum):
        buttonImages.append(ImageTk.PhotoImage(file=f'images/{buttonNames[i]}.png'))
        buttons.append(ttk.Button(botButtons, text = buttonNames[i], style = 'gridButton.button.TButton', image = buttonImages[i], compound = TOP))

        buttons[i].config(command = lambda j=buttons[i]['text']: channel.basic_publish(exchange='GUI', routing_key='class', body=j))
        buttons[i].grid(row = int(i/10), column = i%10, sticky = N + S + W + E, ipady = 3)

    

    #set botButtonsWindow not to the frame object but to the object returned by the create_window function
    botButtonsWindow = botCanvas.create_window(0, 0, window=botButtons, anchor='nw')


    #configure the canvas's scroll bar
    botCanvas.update() # needed or botCanvas.bbox() will be all 1s
    botCanvas.configure(yscrollcommand=buttonScroll.set, scrollregion=botCanvas.bbox('all'))

    #   END OF BUTTON GRID CODE   #


    root.mainloop()


if __name__ == '__main__':
    main()