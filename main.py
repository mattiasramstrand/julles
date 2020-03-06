import tkinter
import cv2
import PIL.Image, PIL.ImageTk
import pandas as pd
import numpy as np

class App:
    def __init__(self, window, window_title, image_path="original.jpg", excel_path="data.xlsx"):

        self.window = window
        self.window.title(window_title)

        self.image_path = image_path
        # Load an image using OpenCV
        self.cv_image = cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_BGR2RGB)
        self.drawn_image = self.cv_image.copy()

        # Get the image dimensions (OpenCV stores image data as NumPy ndarray)
        self.height, self.width, no_channels = self.cv_image.shape

        # Create a canvas that can fit the above image
        self.canvas = tkinter.Canvas(window, width = self.width, height = self.height)
        self.canvas.pack()

        # Use PIL (Pillow) to convert the NumPy ndarray to a PhotoImage
        self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(self.cv_image))

        # Add a PhotoImage to the Canvas
        self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)

        self.df = pd.read_excel(excel_path)

        self.q_values = np.array(self.df[self.df.keys()[0]])
        self.x_values = np.array(self.df[self.df.keys()[1]])
        self.span_values = np.array(self.df[self.df.keys()[4]])
        self.y_values = np.array(self.df[self.df.keys()[-1]])

        self.x_min = 94
        self.x_max = 892
        self.y_min = 133
        self.y_max = 532

        # Input Q
        self.q_entry = tkinter.Entry(window)
        self.q_entry.pack(anchor=tkinter.CENTER)

        # Input Span
        self.span_entry = tkinter.Entry(window)
        self.span_entry.pack(anchor=tkinter.CENTER)

        # Input filepath
        self.file_entry = tkinter.Entry(window)
        self.file_entry.pack(anchor=tkinter.CENTER)

        self.button = tkinter.Button(text='Draw', command=self.draw_lines, highlightbackground="#000000")
        self.button.pack(anchor=tkinter.CENTER, expand=True)

        self.save_button = tkinter.Button(text='Save', command=self.save_image, highlightbackground="#000000")
        self.save_button.pack(anchor=tkinter.CENTER, expand=True)

        self.window.mainloop()

    # Callback for the "Blur" button
    def draw_lines(self):
        q = min(1000, max(0.001, float(self.q_entry.get())))
        span = min(100, max(1 ,float(self.span_entry.get())))

        print(q, span)

        if q in self.q_values:
            x = self.x_values[np.where(self.q_values >= q)[0][0]]
        else:
            x = np.mean([self.x_values[np.where(self.q_values < q)[0][-1]],
                         self.x_values[np.where(self.q_values > q)[0][0]]])

        if span in self.span_values:
            y = self.y_values[np.where(self.span_values >= span)[0][0]]
        else:
            y = np.mean([self.y_values[np.where(self.span_values < span)[0][-1]],
                         self.y_values[np.where(self.span_values > span)[0][0]]])

        x = int(x)
        y = int(y)

        image = self.cv_image.copy()
        # Draw horisontal line
        cv2.line(image, (self.x_min, y),(self.x_max, y), (255, 0, 0), 3)
        # Draw vertical line
        cv2.line(image, (x, self.y_min),(x, self.y_max), (255, 0, 0), 3)
        self.drawn_image = image.copy()
        self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(image))
        self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)


    def save_image(self):
        path = self.file_entry.get()
        cv2.imwrite(path +  '.jpg', self.drawn_image[..., ::-1])

if __name__ == "__main__":
    # Create a window and pass it to the Application object
    App(tkinter.Tk(), "Tkinter and OpenCV")
