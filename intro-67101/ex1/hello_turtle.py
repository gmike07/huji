#############################################################
# FILE : hello_turtle.py
# WRITER : Mike Greenbaum , mikeg , 211747639
# EXERCISE : intro2cs1 ex1 2018-2019
# DESCRIPTION: A program that draws a garden using the turtle library
#############################################################
import turtle
def draw_petal():
    """
    draws a leaf from the flower
    """
    turtle.circle(100, 90)  # draws 90 degrees of a circle with radius 100
    turtle.left(90)  # turn the turtle 90 degrees left
    turtle.circle(100, 90)  # draws 90 degrees of a circle with radius 100
def draw_flower():
    """
    draws a flower, by drawing 4 leafs and a a line down
    """
    turtle.setheading(0)  # set direction of the turtle to 0 degrees
    draw_petal()  # draw a leaf
    turtle.setheading(90)  # set direction of the turtle to 90 degrees
    draw_petal()  # draw a leaf
    turtle.setheading(180)  # set direction of the turtle to 180 degrees
    draw_petal()  # draw a leaf
    turtle.setheading(270)  # set direction of the turtle to 270 degrees
    draw_petal()  # draw a leaf
    turtle.setheading(270)  # set direction of the turtle to 270 degrees
    turtle.forward(250)  # move forth 250 steps
def draw_flower_advance():
    """
    draws a flower and moves to the next flower location to draw
    """
    draw_flower()  # draw a flower at your current position
    turtle.right(90)  # turn the turtle 90 degrees right
    turtle.up()  # stop the turtle from drawing line after it
    turtle.forward(250)  # move forth 250 steps
    turtle.right(90)  # turn the turtle 90 degrees right
    turtle.forward(250)  # move forth 250 steps
    turtle.left(90)  # turn the turtle 90 degrees left
    turtle.down()  # start the turtle from drawing line after it
def draw_flower_bed():
    """
    moves the turtle to an init position, then draws 3 flower
    """
    turtle.up()  # stop the turtle from drawing line after it
    turtle.forward(200)  # move forth 200 steps
    turtle.right(180)  # turn the turtle 180 degrees right
    turtle.down()  # start the turtle from drawing line after it
    draw_flower_advance()  # draw the first flower
    draw_flower_advance()  # draw the second flower
    draw_flower_advance()  # draw the third flower
if __name__ == "__main__":
    draw_flower_bed()  # call the draw flowers function
    turtle.done()  # the turtle finished drawing
