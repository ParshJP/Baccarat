from tkinter import Tk, Canvas, PhotoImage, Entry, Button, END, INSERT, Frame, messagebox, simpledialog #import necessary tkinter modules
from decimal import Decimal     #import Decimal module to accurately round numbers
from Card import Card           #import Card class
from DeckOfCards import DeckOfCards     #import DeckOfCards class

WINDOW_WIDTH, WINDOW_HEIGHT, pointTotal, bet = 800, 534, 500, 0     #vars initializing window dimensions, point and bet amounts


def place_bet():        #when the place bet btn is pressed, reset any changed values and objects and acquire the bet placed
    global bet      #set global vars
    global deck
                            # reset images and text outputs
    canvas.itemconfig(c1img, image=blue), canvas.itemconfig(c2img, image=blue), canvas.itemconfig(c3img, image=blue)
    canvas.itemconfig(c4img, image=red), canvas.itemconfig(c5img, image=red), canvas.itemconfig(c6img, image=red)
    canvas.itemconfig(bottomMessage, text=""), canvas.itemconfig(outputMessage, text = 'Place BET to begin!')
    canvas.itemconfig(outputPlayer, text='-'), canvas.itemconfig(outputBanker, text='-')

    try:
        bet = float(entryBet.get())             #round the bet to a int, if necessary
        bet = round(Decimal(entryBet.get()))

        if bet == -20201023:        #this restarts program when user chooses to replay
            entryBet.delete(0, END), entryBet.insert(0, 'Place Bet'), entryBet.focus(), entryBet.selection_range(0, END)

        elif bet > pointTotal or bet < 1:         #do not accept a bet that is 0 or higher then the points the player has
            messagebox.showerror('Error', 'Your bet cannot exceed ' + str(pointTotal) + ' points and it must be at least 1 point!')
            entryBet.focus(), entryBet.selection_range(0, END)

        else:
            deck = DeckOfCards()                        #reset object values and widget states
            c1, c2, c3 = Card(0), Card(0), Card(0)      #prompt user to click DEAL btn to continue
            c4, c5, c6 = Card(1), Card(1), Card(1)
            entryBet.config(state = 'readonly'), btnBet.config(state = 'disabled'), btnDeal.config(state = 'normal')
            canvas.itemconfig(outputMessage, text = 'Click DEAL!')
    except:
        messagebox.showerror('Error', 'You must enter an integer only!')    #if a non int is given, display the error
        entryBet.focus(), entryBet.selection_range(0, END)


def deal_card():            #if DEAL btn is pressed, deal 3 cards to player and 3 to banker
    c1, c2, c3 = deck.deal_card(0), deck.deal_card(1), deck.deal_card(2)    #get random cards from deck
    canvas.itemconfig(c1img, image=c1.get_image()), canvas.itemconfig(c2img, image=c2.get_image())      #update images for first 2 cards for each player
    c4, c5, c6 = deck.deal_card(3), deck.deal_card(4), deck.deal_card(5)
    canvas.itemconfig(c4img, image=c4.get_image()), canvas.itemconfig(c5img, image=c5.get_image())

    pc = 2      #amount of cards player has drawn
    p, b = (c1.get_value() + c2.get_value()) % 10, (c4.get_value() + c5.get_value()) % 10       #calculate value of cards for both players

    canvas.itemconfig(outputPlayer, text = p), canvas.itemconfig(outputBanker, text = b)    #output current values

    if p == 8 or p == 9 or b == 8 or b == 9:
        winner(p, b)                            #win conditions of baccarat

    elif 6 <= p <= 7:                           #determine whether a third card is drawn by either player
        if b > 5:                               #pass to function that determines winner by comparing values
            winner(p, b)
        if pc == 2 and b <= 5:
            b = (b + c6.get_value()) % 10       #change value of banker
            canvas.itemconfig(outputBanker, text=b), canvas.itemconfig(c6img, image=c6.get_image())     #banker draws
            winner(p, b)
    else:
        btnDeal.config(state = 'normal', text = 'DRAW CARD',
                       command = lambda p=p, b=b, pc=pc, c1=c1, c2=c2, c3=c3, c4=c4, c5=c5, c6=c6:
                       draw_third(p, b, pc, c1, c2, c3, c4, c5, c6))        #passed to function that draws third card for user
        canvas.itemconfig(outputMessage, text='Draw one more card!')


def draw_third(p, b, pc, c1, c2, c3, c4, c5, c6):       #determine if player draws third card based off Baccarat conditions
    if p <= 5:
        canvas.itemconfig(c3img, image=c3.get_image())      #change the image to display card front side
        p, pc = (p + c3.get_value()) % 10, 3            #change player's cards value and amount of cards player has drawn

        if (0 <= b <= 2) or (b == 3 and p != 8) or (b == 4 and 2 <= p <= 7) or (b == 5 and 4 <= p <= 7) or (b == 6 and 6 <= p <= 7):
            canvas.itemconfig(c6img, image=c6.get_image())
            b = (b + c6.get_value()) % 10                       #based off these conditions, the banker also draws
        elif b == 7:
            pass

    canvas.itemconfig(outputPlayer, text=p), canvas.itemconfig(outputBanker, text=b)        #update values
    winner(p, b)


def winner(p, b):       #compare final values of player and banker and determine winner
    global pointTotal           #change state of interface widgets so user doesn't do a runtime error

    btnBet.config(state='normal'), btnDeal.config(text = 'DEAL', state = 'disabled', command = deal_card)
    entryBet.config(state='normal'), entryBet.focus(), entryBet.selection_range(0, END)
    canvas.itemconfig(bottomMessage, text="-Place BET to deal new hand-")

    if p > b:               #if player has higher card value than banker
        pointTotal += bet       #add bet to points total and display
        canvas.itemconfig(outputMessage, text = 'Player wins!'), canvas.itemconfig(outputPoints, text = str(pointTotal) + ' P')

    elif b > p:         #if banker wins
        pointTotal -= bet       #take away bet from points total and display
        canvas.itemconfig(outputMessage, text='Banker wins!'), canvas.itemconfig(outputPoints, text=str(pointTotal) + ' P')

        if pointTotal <= 0:     #if user runs out of points, prompt user to replay or quit
            a = messagebox.askyesno('Baccarat', 'Game Over! You have 0 points remaining.\nWould you like to play again?')
            if a:
                pointTotal, x = 500, -20201023       #reset total points and set a value that is key to restart program
                canvas.itemconfig(outputPoints, text=str(pointTotal) + ' P')
                entryBet.delete(0, END), entryBet.insert(0, x)
                place_bet()     #place a bet automatically so all values reset and game restarts
            else:
                messagebox.showinfo('Baccarat', 'Thank you for playing!')       #if user chooses to quit then exit program
                exit()

    else:           #if player and banker tie, display message
        messagebox.showinfo('Baccarat', 'Tie.\nNo points lost/gained.\nPlace BET to deal new hand.')


def close_program():        #if user chooses to exit program, ask them to confirm
    a = messagebox.askyesno('Baccarat', 'Are you sure you want to QUIT?')

    if a:
        messagebox.showinfo('Baccarat', 'Thank you for playing!')
        exit()


root = Tk()     #create window and set function for event handling when user clicks X button
root.protocol("WM_DELETE_WINDOW", close_program)
root.title("Baccarat")
root.geometry("%dx%d+%d+%d" % (WINDOW_WIDTH, WINDOW_HEIGHT, root.winfo_screenwidth() // 2 - WINDOW_WIDTH // 2,
              root.winfo_screenheight() // 2 - WINDOW_HEIGHT // 2))

canvas = Canvas(root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT)     #create canvas
canvas.pack()

imgbackground = PhotoImage(file="images/card_table.png")        #create and set the background of the game and the title
canvas.create_image(0, 0, image=imgbackground, anchor='nw')

imgtitle = PhotoImage(file="images/baccarat.png")
canvas.create_image(WINDOW_WIDTH // 2 - imgtitle.width() // 2, 10, image=imgtitle, anchor='nw')

deck = DeckOfCards()        #create the deck of cards object

blue = PhotoImage(file = "images/back_blue.png")        #create the back sides of the 6 cards and set them on the canvas
red = PhotoImage(file = "images/back_red.png")             #blue are the player cards and red are the banker
c1img, c2img, c3img, c4img, c5img, c6img = canvas.create_image(250, 215, image = blue), canvas.create_image(250, 270, image = blue), \
                                           canvas.create_image(250, 325, image = blue), canvas.create_image(550, 215, image = red), \
                                           canvas.create_image(550, 270, image = red), canvas.create_image(550, 325, image = red)

outputPoints = canvas.create_text(WINDOW_WIDTH // 2, 160, font=('Century Gothic', 28, 'bold'),
                                  fill='white', text="{:,d}".format(pointTotal) + ' P') #create label that displays total points

canvas.create_text(250, 425, text='Player has:', font=('Century Gothic', 14, 'bold'), fill='white')
canvas.create_text(550, 425, text='Banker has:', font=('Century Gothic', 14, 'bold'), fill='white')
#texts that display the value of the cards that have been drawn and dealt

outputPlayer = canvas.create_text(250, 455, text='-', font=('Century Gothic', 14, 'bold'), fill='white')
outputBanker = canvas.create_text(550, 455, text='-', font=('Century Gothic', 14, 'bold'), fill='white')

outputMessage = canvas.create_text(WINDOW_WIDTH // 2, 385, text="Place BET to begin", font=('Century Gothic', 12, 'bold'),
                                   fill='white')        #text the prompts player throughout the game
#message to help guide player once a round is over
bottomMessage = canvas.create_text(WINDOW_WIDTH // 2, 520, font=('Century Gothic', 12, 'bold'), fill='white')

frame = Frame(root, borderwidth=2, relief='sunken')     #create and set frame for entry widget

entryBet = Entry(frame, width=12, font=('Century Gothic', 10, 'bold'), justify='center', borderwidth=5, relief='flat')
entryBet.insert(INSERT, '0')                #create entry box for placing a bet and focus on it
entryBet.focus()
entryBet.selection_range(0, END)
entryBet.pack()

root.update()
frame.place(x=WINDOW_WIDTH // 2 - frame.winfo_reqwidth() // 2, y=190)

btnBet = Button(canvas, width=13, text='BET', pady=5, command = place_bet)      #buttons for betting, dealing, drawing and exiting
btnBet.place(x=WINDOW_WIDTH // 2 - btnBet.winfo_reqwidth() // 2, y=235)
btnDeal = Button(canvas, width=13, text='DEAL', pady=5, state='disabled', command = deal_card)
btnDeal.place(x=WINDOW_WIDTH // 2 - btnDeal.winfo_reqwidth() // 2, y= 280)
btnQuit = Button(canvas, width=13, text='QUIT', pady=5, command = close_program)
btnQuit.place(x=WINDOW_WIDTH // 2 - btnQuit.winfo_reqwidth() // 2, y = 325)

root.mainloop()     #loop so program continues on until purposely closed
