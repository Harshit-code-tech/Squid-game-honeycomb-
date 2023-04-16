import cv2
import numpy as np
import turtle

# Read the intro, death, and victory images and resize them
intro_img = cv2.imread('frames/img1.jpeg')
intro_img = cv2.resize(intro_img, (0,0), fx=0.69, fy=0.69)
death_img = cv2.imread('frames/img2.png')
death_img = cv2.resize(death_img, (0,0), fx=0.69, fy=0.69)
victory_img = cv2.imread('frames/img3.png')
victory_img = cv2.resize(victory_img, (0,0), fx=0.69, fy=0.69)

# Read the honeycomb image and the square to be cut out
honeycomb_img = cv2.imread('img/honeycomb.png')
honeycomb_img = cv2.resize(honeycomb_img, (0,0), fx=0.69, fy=0.69)
square_img = cv2.imread('img/sqr(2).png')

# Set up the turtle
turtle.setup(honeycomb_img.shape[1], honeycomb_img.shape[0])
turtle.bgpic("frames/img1.jpeg")

# Define the turtle movement functions
def move_up():
    turtle.setheading(90)
    turtle.forward(10)

def move_down():
    turtle.setheading(270)
    turtle.forward(10)

def move_left():
    turtle.setheading(180)
    turtle.forward(10)

def move_right():
    turtle.setheading(0)
    turtle.forward(10)

# Set up the key bindings
def start_game():
    turtle.onkey(move_up, 'w')
    turtle.onkey(move_down, 's')
    turtle.onkey(move_left, 'a')
    turtle.onkey(move_right, 'd')
    turtle.listen()

def stop_game():
    turtle.onkey(None, 'w')
    turtle.onkey(None, 's')
    turtle.onkey(None, 'a')
    turtle.onkey(None, 'd')
    turtle.done()

turtle.onkey(start_game, 'q')
turtle.listen()

# Define the game logic
def cut_square(x, y):
    # Convert the turtle position to image coordinates
    img_x = int((x + honeycomb_img.shape[1] / 2) * honeycomb_img.shape[1] / turtle.window_width())
    img_y = int((turtle.window_height() / 2 - y) * honeycomb_img.shape[0] / turtle.window_height())

    # Get the sub-image of the honeycomb around the turtle position
    honeycomb_sub = honeycomb_img[max(img_y-20, 0):min(img_y+20, honeycomb_img.shape[0]), max(img_x-20, 0):min(img_x+20, honeycomb_img.shape[1])]

    # Calculate the squared difference between the honeycomb sub-image and the square image
    sq_diff = cv2.absdiff(honeycomb_sub, square_img)
    sq_diff = cv2.cvtColor(sq_diff, cv2.COLOR_BGR2GRAY)
    sq_diff = cv2.threshold(sq_diff, 25, 255, cv2.THRESH_BINARY)[1]
    squared_diff = cv2.countNonZero(sq_diff)

    # If the squared difference is below a certain threshold, the square has been cut out
    if squared_diff <= 5000:
        # Get the location of the top-left corner of the square
        square_y, square_x = np.where(sq_diff == 0)
square_y_min = np.min(square_y)
square_x_min = np.min(square_x)

# Get the dimensions of the square
square_height = np.max(square_y) - square_y_min
square_width = np.max(square_x) - square_x_min

# Cut out the square from the honeycomb image
honeycomb_img[square_y_min:square_y_min+square_height, square_x_min:square_x_min+square_width] = 0

# Draw the updated honeycomb image
cv2.imshow('Honeycomb', honeycomb_img)

# Check if the entire square has been cut out
square_rows, square_cols = np.where(honeycomb_img == 0)
min_row = np.min(square_rows)
max_row = np.max(square_rows)
min_col = np.min(square_cols)
max_col = np.max(square_cols)
if max_row - min_row + 1 == square_height and max_col - min_col + 1 == square_width:
    print('You won!')
    cv2.destroyAllWindows()
    turtle.bye()

# Draw the updated honeycomb image
cv2.imshow('Honeycomb', honeycomb_img)

# Redraw the turtle
turtle.clear()
for row in range(min_row, max_row):
    for col in range(min_col, max_col):
        if honeycomb_img[row, col, 0] > 0:
            turtle.penup()
            turtle.goto(col, honeycomb_img.shape[0]-row)
            turtle.pendown()
            turtle.dot(10, 'black')
            turtle.penup()
#Set up the mouse click event to cut the square
turtle.onscreenclick(cut_square)

#Start the game
turtle.mainloop()
# Wait for a key press and then close the window
cv2.waitKey(0)
cv2.destroyAllWindows()
