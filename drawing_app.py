import tkinter as tk
from shutil import which
from tkinter import colorchooser, filedialog, messagebox
from tkinter.constants import NW

from PIL import Image, ImageDraw


class DrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Рисовалка с сохранением в PNG")

        self.image = Image.new("RGB", (600, 400), "white")
        self.draw = ImageDraw.Draw(self.image)

        self.canvas = tk.Canvas(root, width=600, height=400, bg='white')
        self.canvas.pack()

        self.setup_ui()

        self.last_x, self.last_y = None, None
        self.pen_color = 'black'

        self.canvas.bind('<B1-Motion>', self.paint)
        self.canvas.bind('<ButtonRelease-1>', self.reset)
        self.canvas.bind('<Button-3>', self.pick_color)
        self.root.bind('<Control-s>', lambda event: self.save_image())
        self.root.bind('<Control-c>', lambda event: self.choose_color())



    def setup_ui(self):
        '''
        Инициализация графического интерфейса
        '''
        control_frame = tk.Frame(self.root)
        control_frame.pack(fill=tk.X)

        control_frame2 = tk.Frame(self.root)
        control_frame2.pack(fill=tk.X)

        clear_button = tk.Button(control_frame, text="Очистить", command=self.clear_canvas)
        clear_button.pack(side=tk.LEFT)

        color_button = tk.Button(control_frame, text="Выбрать цвет", command=self.choose_color)
        color_button.pack(side=tk.LEFT)

        label_color = tk.Label(control_frame, text='цвет кисти:')
        label_color.pack(side=tk.LEFT)
        self.label_color_value = tk.Label(control_frame,  bg='black', width=10)
        self.label_color_value.pack(side=tk.LEFT)

        save_button = tk.Button(control_frame, text="Сохранить", command=self.save_image)
        save_button.pack(side=tk.LEFT)

        button_size_change = tk.Button(control_frame, text="Изменить размер", command=self.change_size)
        button_size_change.pack(side=tk.RIGHT)

        self.brush_size_scale = tk.Scale(control_frame2, from_=1, to=10, orient=tk.HORIZONTAL)
        self.brush_size_scale.pack(side=tk.LEFT)

        self.brash_s_m = tk.OptionMenu(control_frame2, self.brush_size_scale, *range(1, 11))
        self.brash_s_m.pack(side=tk.LEFT)

        self.eraser_button = tk.Button(control_frame2, text="Ластик", command=self.eraser )
        self.eraser_button.pack(side=tk.LEFT)

        self.brash_button = tk.Button(control_frame2, text="Кисть", command=self.drawing)
        self.brash_button.pack_forget()

        button_text = tk.Button(control_frame2, text="Текст", command=self.set_text)
        button_text.pack(side=tk.RIGHT)

        button_change_canvas = tk.Button(control_frame2, text="Изменить фон", command=self.change_canvas)
        button_change_canvas.pack(side=tk.RIGHT)

    def paint(self, event):
        '''
        Метод для рисования
        '''
        if self.last_x and self.last_y:
            self.canvas.create_line(self.last_x, self.last_y, event.x, event.y,
                                    width=self.brush_size_scale.get(), fill=self.pen_color,
                                    capstyle=tk.ROUND, smooth=tk.TRUE)
            self.draw.line([self.last_x, self.last_y, event.x, event.y], fill=self.pen_color,
                           width=self.brush_size_scale.get())

        self.last_x = event.x
        self.last_y = event.y

    def reset(self, event):
        '''
        Метод для сброса координат
        '''
        self.last_x, self.last_y = None, None

    def clear_canvas(self):
        '''
        Метод для очистки холста
        '''
        self.canvas.delete("all")
        self.image = Image.new("RGB", (600, 400), "white")
        self.draw = ImageDraw.Draw(self.image)

    def choose_color(self):
        '''
        Метод для выбора цвета
        '''
        self.pen_color = colorchooser.askcolor(color=self.pen_color)[1]
        self.label_color_value.config(bg=self.pen_color)

    def save_image(self):
        '''
        Метод для сохранения изображения
        '''
        file_path = filedialog.asksaveasfilename(filetypes=[('PNG files', '*.png')])
        if file_path:
            if not file_path.endswith('.png'):
                file_path += '.png'
            self.image.save(file_path)
            messagebox.showinfo("Информация", "Изображение успешно сохранено!")

    def eraser(self):
        '''
        Метод вызывается при нажатии на кнопку "Ластик"
        '''
        self.previous_color = self.pen_color
        self.previous_size_brash = self.brush_size_scale.get()
        self.pen_color = "white"
        self.brash_button.pack(side=tk.LEFT)
        self.eraser_button.pack_forget()

    def drawing(self):
        '''
        Метод вызывается при нажатии на кнопку "Кисть"
        '''
        self.pen_color = self.previous_color
        self.brush_size_scale.set(self.previous_size_brash)
        self.eraser_button.pack(side=tk.LEFT)
        self.brash_button.pack_forget()

    def get_rgb(self, rgb):
        '''
        Метод для получения цвета из RGB
        '''
        return "#%02x%02x%02x" % rgb

    def pick_color(self, event):
        '''
        Метод для выбора цвета из изображения, инструмент "Пипетка"
        '''
        copy_color = self.image.getpixel((event.x, event.y))
        self.pen_color = self.get_rgb(copy_color)
        self.label_color_value.config(bg=self.pen_color)

    def change_size(self):
        '''
        Метод для изменения размера холста
        '''
        w = tk.simpledialog.askinteger(title="Изменить размер холста", prompt='Введите ширину'
                                                 , minvalue=100, maxvalue=1000)
        h = tk.simpledialog.askinteger(title="Изменить размер холста", prompt='Введите высоту'
                                                 , minvalue=100, maxvalue=1000)
        self.canvas.config(width=w, height=h)
        self.image = Image.new("RGB", (w, h), "white")
        self.draw = ImageDraw.Draw(self.image)
        self.canvas.delete("all")

    def set_text(self):
        '''
        Метод установления текста
        '''
        self.text_ = tk.simpledialog.askstring(title="Вставить текст", prompt='Введите текст')
        self.root.bind('<Button-1>', lambda event: self.paste_canv(self.text_, event))

    def paste_canv(self, text, event):
        '''
        Метод для вставки текста на холст
        '''
        self.canvas.create_text(event.x, event.y, text=text, fill=self.pen_color, anchor=NW)
        self.text_ = ''

    def change_canvas(self):
        '''
        Метод для измения цвета холста
        '''
        new_color = colorchooser.askcolor()
        self.canvas.config(background=new_color[1])



def main():
    root = tk.Tk()
    app = DrawingApp(root)

    root.mainloop()


if __name__ == "__main__":
    main()
