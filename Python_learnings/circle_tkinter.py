import tkinter


def circle(page, radius, g, h):
    for x in range(int(g*100), int((g+radius)*100)):
        x /= 100
        y = h + (radius**2 - (x-g)**2)**0.5

        plot(page, x, y)
        plot(page, x, 2*h-y)
        plot(page, 2*g-x, y)
        plot(page, 2*g-x, 2*h-y)


def draw_axes(page):
    page.update()
    x_origin = page.winfo_width() / 2
    y_origin = page.winfo_height() / 2

    page.create_line(x_origin, 0, x_origin, page.winfo_height(), fill='black')
    page.create_line(0, y_origin, page.winfo_width(), y_origin, fill='black')


def plot(page, x, y):
    x_origin = page.winfo_width() / 2
    y_origin = page.winfo_height() / 2

    canvas_x = x_origin + x
    canvas_y = y_origin - y
    # page.create_line(canvas_x, canvas_y, canvas_x+1, canvas_y+1, fill='red', width=2)
    page.create_oval( canvas_x, canvas_y, canvas_x+2, canvas_y+2, fill='blue', outline='blue' )
# Main window
mainWindow = tkinter.Tk()
mainWindow.title('Circle')
mainWindow.geometry('400x400')

# Create canvas
canvas = tkinter.Canvas(mainWindow, width=400, height=400, bg='white')
canvas.pack()

# Draw axes
draw_axes(canvas)

# Draw circle (center at 0,0, radius=1.5)
circle(canvas, radius=10.5, g=0, h=0)

# Start loop
mainWindow.mainloop()