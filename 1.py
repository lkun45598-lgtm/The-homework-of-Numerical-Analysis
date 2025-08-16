import turtle
turtle.pencolor("yellow")
turtle.fillcolor("red")
turtle.begin_fill()
for i in range(5):
    turtle.forward(100)
    turtle.right(144)
    turtle.forward(100)
    turtle.left(72)
turtle.end_fill()
turtle.hideturtle()
turtle.done()