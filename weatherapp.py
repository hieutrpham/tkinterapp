import tkinter as tk

HEIGHT = 700
WIDTH = 800

def test_function(entry):
    print('button clicked', entry)

root = tk.Tk()

canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()

# background_image = tk.PhotoImage(file='landscape.png')
# background_label = tk.Label(root, image=background_image)
# background_image.place(relwidth=1, relheight=1)

frame = tk.Frame(root, bg='#80c1ff', bd=5)
frame.place(relx=.5, rely=.1, relwidth=.75, relheight=.1, anchor='n')

entry = tk.Entry(frame, font=40)
entry.place(relwidth=.65, relheight=1)

button = tk.Button(frame, text='Get Weather', font=40, command=lambda: test_function(entry.get()))
button.place(relx=.7, rely=0, relwidth=.3, relheight=1)

lower_frame = tk.Frame(root, bg='#80c1ff', bd=10)
lower_frame.place(relx=.5, rely=.25, relwidth=.75, relheight=.6, anchor='n')

label = tk.Label(lower_frame)
label.place(relwidth=1, relheight=1)

root.mainloop()