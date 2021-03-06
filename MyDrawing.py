import sys
import os
import shutil
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QMenuBar, QMenu
from PyQt5.QtWidgets import QAction, QFileDialog, QColorDialog
from PyQt5.QtWidgets import QInputDialog, QLabel, QMessageBox
from PyQt5.QtGui import QImage, QIcon, QPainter, QPen, QColor, QPolygon, QFont
from PyQt5.QtCore import Qt, QPoint
# Импортирование нужных библиотек


class Paint(QMainWindow):  # Создание окна
    def __init__(self):  # Инициализация
        super().__init__()

        try:  # Попытка прочитать файл
            f = open('size.txt', 'r')
            width = int(f.readline())  # Ширина окна
            height = int(f.readline())  # Высота окна
            f.close()
        except Exception:  # Если ошибка
            f = open('size.txt', 'w')  # Создать файл
            f.write('1200' + '\n' + '900')  # Перезапись файла
            f.close()  # Закрытие файла
            width = 1200
            height = 900

        self.coords = QLabel(self)  # Координаты мыши
        self.coords.setText("Координаты:None, None")  # Изначальные координаты
        self.coords.resize(150, 15)  # Изменение размера
        self.coords.move(width - 150, height - 20)  # Перемещение

        self.last = 0  # Количество изображений

        self.setMouseTracking(True)  # Отслеживание мыши без нажатия

        self.copyA = False  # Переменная для области копирования

        icon = 'icons/main.png'  # Ссылка на основную иконку

        os.makedirs('last')  # Создание путой папки

        self.setWindowTitle('MyDrawing')  # Назвние окна
        self.setGeometry(0, 35, width, height)  # Размеры окна
        self.setWindowIcon(QIcon(icon))  # Иконка окна

        # Создание изображения
        self.image = QImage(self.size(), QImage.Format_RGB32)
        self.image.fill(Qt.white)  # Заливка изображения белым цветом

        # Добавление картинки
        self.image.save('last/' + str(self.last) + '.png')
        self.last += 1  # Добавление к количеству картинок

        self.drawing = False  # Переменная для рисования
        self.brushSize = 2  # Размер кисти
        self.brushColor = Qt.black  # Цвет кисти
        self.lastPoint = QPoint()  # Координаты последней точки

        mainMenu = self.menuBar()  # Создание меню
        fileMenu = mainMenu.addMenu('Файл')  # Добавление в меню вкладки "Файл"
        # Добавление в меню кнопки "Размер кисти"
        brushMenu = mainMenu.addMenu('Размер кисти')
        # Добавление в меню кнопки "Цвет кисти"
        brushColor = mainMenu.addMenu('Цвет кисти')
        # Добавление в меню кнопки "Геометричсекие фигуры"
        shapes = mainMenu.addMenu('Геометрические фигуры')

        # Создание кнопки сохранения и добавление иконки
        saveAction = QAction(QIcon('icons/save.jpg'), 'Сохранить', self)
        saveAction.setShortcut('Ctrl+S')  # Добавление комбинации клавиш
        fileMenu.addAction(saveAction)  # Добавление в меню

        # Вызов функции save() при нажатии
        saveAction.triggered.connect(self.save)

        # Создание кнопки очистки и добавление иконки
        clearAction = QAction(QIcon('icons/clear.jpeg'), 'Очистить', self)
        clearAction.setShortcut('Ctrl+A')  # Добавление комбинации клавиш
        fileMenu.addAction(clearAction)  # Добавление в меню
        clearAction.triggered.connect(self.clear)  # Вызов функции при нажатии

        # Создание кнопки для изменения размера окна
        sizeAction = QAction(QIcon('icons/size.png'), 'Изменить размер', self)
        sizeAction.setShortcut('Ctrl+T')  # Добавление комбинации клавиш
        fileMenu.addAction(sizeAction)  # Добавление в меню
        sizeAction.triggered.connect(self.sizeAdd)  # Вызов функции при нажатии

        # Создание кнопки для добавления изображения
        addAction = QAction(QIcon('icons/picture.jpg'),
                            'Добавить изображение', self)
        addAction.setShortcut('Ctrl+N')  # Добавление комбинации клавиш
        fileMenu.addAction(addAction)  # Добавление в меню

        # При нажатии вызов функции
        addAction.triggered.connect(self.addPicture)

        # Создание кнопки для копирования области
        copyAction = QAction(QIcon('icons/copy.png'), 'Копировать', self)
        copyAction.setShortcut('Ctrl+C')  # Добавление комбинации клавиш
        fileMenu.addAction(copyAction)  # Добавление в меню

        # При нажатии вызов функции
        copyAction.triggered.connect(self.copyArea)

        # Создание кнопки вырезать
        cutAction = QAction(QIcon('icons/cut.jpg'), 'Вырезать', self)
        cutAction.setShortcut('Ctrl+X')  # Добавление комбинации клавиш
        fileMenu.addAction(cutAction)  # Добавление в меню

        # Вызов функции при нажатии
        cutAction.triggered.connect(self.cutArea)

        # Создание кнопки для вставки области
        pasteAction = QAction(QIcon('icons/paste.jpg'), 'Вставить', self)
        pasteAction.setShortcut('Ctrl+V')  # Добавление комбинации клавиш
        fileMenu.addAction(pasteAction)  # Добавление в меню

        # При нажатии вызов функции
        pasteAction.triggered.connect(self.pasteArea)

        # Создание кнопки для заливки
        pourAction = QAction(QIcon('icons/pour.jpg'), 'Залить', self)
        pourAction.setShortcut('Ctrl+H')  # Добавление комбинации клавиш
        fileMenu.addAction(pourAction)  # Добавление в меню

        # Вызов функции при нажатии
        pourAction.triggered.connect(self.fillAll)

        # Создание кнопки отмена
        cancelAction = QAction(QIcon('icons/back.png'), 'Отмена', self)
        cancelAction.setShortcut('Ctrl+Z')  # Добавление комбинации клавиш
        fileMenu.addAction(cancelAction)  # Добавление в меню

        # Вызов функции при нажатии
        cancelAction.triggered.connect(self.returnLast)

        undoAction = QAction(QIcon('icons/undo.png'), 'Вернуть', self)
        undoAction.setShortcut('Ctrl+Shift+Z')  # Добавление комбинации клавиш
        fileMenu.addAction(undoAction)  # Добавление в меню

        # Вызов функции при нажатии
        undoAction.triggered.connect(self.returnUp)

        # Создание кнопки 3 px и добавление иконки
        px3Action = QAction(QIcon('icons/3.jpg'), '3 px', self)
        px3Action.setShortcut('Ctrl+3')  # Добавление комбинации клавиш
        brushMenu.addAction(px3Action)  # Добавление в меню
        px3Action.triggered.connect(self.px3)  # Вызов функции при нажатии

        # Создание кнопки 5 px и добавление иконки
        px5Action = QAction(QIcon('icons/5.jpg'), '5 px', self)
        px5Action.setShortcut('Ctrl+5')  # Добавление комбинации клавиш
        brushMenu.addAction(px5Action)  # Добавление в меню
        px5Action.triggered.connect(self.px5)  # Вызов функции при нажатии

        # Создание кнопки 7 px и добавление иконки
        px7Action = QAction(QIcon('icons/7.jpg'), '7 px', self)
        px7Action.setShortcut('Ctrl+7')  # Добавление комбинации клавиш
        brushMenu.addAction(px7Action)  # Добавление в меню
        px7Action.triggered.connect(self.px7)  # Вызов функции при нажатии

        # Создание кнопки 9 px и добавление иконки
        px9Action = QAction(QIcon('icons/9.jpg'), '9 px', self)
        px9Action.setShortcut('Ctrl+9')  # Добавление комбинации клавиш
        brushMenu.addAction(px9Action)  # Добавление в меню
        px9Action.triggered.connect(self.px9)  # Вызов функции при нажатии

        # Создание кнопки для всех размеров
        pxOtherAction = QAction(QIcon('icons/pxO.jpg'), 'Все размеры', self)
        pxOtherAction.setShortcut('Ctrl+P')  # Добавление комбинации клавиш
        brushMenu.addAction(pxOtherAction)  # Добавление в меню

        # Вызов функции при нажатии
        pxOtherAction.triggered.connect(self.pxOther)

        # Создание кнопки для выбора черного цвета
        blackAction = QAction(QIcon('icons/black.jpg'), 'Черный цвет', self)
        blackAction.setShortcut('Ctrl+B')  # Добавление комбинации клавиш
        brushColor.addAction(blackAction)  # Добавление в меню
        # Вызов функции при нажатии
        blackAction.triggered.connect(self.blackColor)

        # Создание кнопки для выбора белого цвета
        whiteAction = QAction(QIcon('icons/clean.jpg'), 'Ластик', self)
        whiteAction.setShortcut('Ctrl+W')  # Добавление комбинации клавиш
        brushColor.addAction(whiteAction)  # Добавление в меню

        # Вызов функции при нажатии
        whiteAction.triggered.connect(self.whiteColor)

        # Создание кнопки для выбора красного цвета
        redAction = QAction(QIcon('icons/red.png'), 'Красный цвет', self)
        redAction.setShortcut('Ctrl+R')  # Добавление комбинации клавиш
        brushColor.addAction(redAction)  # Добавление в меню
        redAction.triggered.connect(self.redColor)  # Вызов функции при нажатии

        # Создание кнопки для выбора зеленого цвета
        greenAction = QAction(QIcon('icons/green.png'), 'Зеленый цвет', self)
        greenAction.setShortcut('Ctrl+G')  # Добавление комбинации клавиш
        brushColor.addAction(greenAction)  # Добавление в меню

        # Вызов функции при нажатии
        greenAction.triggered.connect(self.greenColor)

        # Создание кнопки для выбора желтого цвета
        yellowAction = QAction(QIcon('icons/yellow.png'), 'Желтый цвет', self)
        yellowAction.setShortcut('Ctrl+Y')  # Добавление комбинации клавиш
        brushColor.addAction(yellowAction)  # Добавление в меню

        # Вызов функции при нажатии
        yellowAction.triggered.connect(self.yellowColor)

        # Создание кнопки для выбора всех цветов
        otherAction = QAction(QIcon('icons/other.jpg'), 'Другие цвета', self)
        otherAction.setShortcut('Ctrl+O')  # Добавление комбинации клавиш
        brushColor.addAction(otherAction)  # Добавление в меню

        # Вызов функции при нажатии
        otherAction.triggered.connect(self.otherColor)

        # Создание кнопки для прямоугольника
        rectangleAction = QAction(QIcon('icons/rectangle.jpg'),
                                  'Прямоугольник', self)
        shapes.addAction(rectangleAction)  # Добавление прямоугольника в меню

        # Вызов функции при нажатии
        rectangleAction.triggered.connect(self.rectangle)

        # Создание кнопки эллипса
        ellipsAction = QAction(QIcon('icons/ellipse.png'), 'Эллипс', self)
        shapes.addAction(ellipsAction)  # Добавление эллипса в меню

        # Вызов функции при нажатии
        ellipsAction.triggered.connect(self.ellips)

        # Создание кнопки для линии
        lineAction = QAction(QIcon('icons/line.jpg'), 'Линия', self)
        shapes.addAction(lineAction)  # Добавление линии в меню

        # Вызов функции при нажатии
        lineAction.triggered.connect(self.line)

        # Создание кнопки для звезды
        starAction = QAction(QIcon('icons/star.png'), 'Звезда', self)
        shapes.addAction(starAction)  # Добавление звезды в меню

        # Вызов функции при нажатии
        starAction.triggered.connect(self.star)

        # Создание кнопки для текста
        textAction = QAction(QIcon('icons/text.png'), 'Текст', self)
        shapes.addAction(textAction)  # # Добавление текста в меню

        # Вызов функции при нажатии
        textAction.triggered.connect(self.writeText)

        # Создание кнопки для треугольник
        triangleAction = QAction(QIcon('icons/triangle.png'),
                                 'Треугольник', self)
        shapes.addAction(triangleAction)

        # Вызов функции при нажатии
        triangleAction.triggered.connect(self.triangle)

    # Функция нажатия кнопки мыши
    def mousePressEvent(self, event, cord=False):
        if event.button() == Qt.LeftButton:  # Если нажата левая кнопка
            self.drawing = True  # То переменная рисования True
            self.lastPoint = event.pos()  # Координаты послдней точки

    def mouseMoveEvent(self, event):  # Функция перемещения мышки
        # Изменение координаты в QLabel
        self.coords.setText("Координаты:{}, {}".format(event.x(),
                                                                 event.y()))

        # Если нажата левая кнопка и переменная рисования
        if event.buttons() and Qt.LeftButton and self.drawing:
            painter = QPainter(self.image)  # Создание объекта QPainter
            # Цвет и свойства
            painter.setPen(QPen(self.brushColor, self.brushSize,
                                Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            painter.drawLine(self.lastPoint, event.pos())  # Рисование линии
            self.lastPoint = event.pos()  # Изменение последней координаты
            self.update()  # Обновление окна

    def mouseReleaseEvent(self, event):  # Функция отжатия кнопки
        self.lastImage()
        self.drawing = False  # переменна рисования False

    def paintEvent(self, event):  # Функция рисовая
        canvasPainter = QPainter(self)  # Создание объекта
        # Рисование линии
        canvasPainter.drawImage(self.rect(), self.image, self.image.rect())

    def save(self):  # Функция сохранения
        # Сохранение пути
        files = 'PNG(*.png);;JPEG(*.jpg *jpeg);; ALL Files(*.*)'
        filePath, _ = QFileDialog.getSaveFileName(self,
                                                  'Сохранить изображение',
                                                  '',
                                                  files)
        if not filePath:  # Проверка на пустоту пути
            return
        self.image.save(filePath)  # Сохранение

    def clear(self):  # Функция очистки
        self.image.fill(Qt.white)  # Заливка изображения белым
        self.update()  # Обновление изображения

    def px3(self):  # Функция изменения размера
        self.brushSize = 3

    def px5(self):  # Функция изменения размера
        self.brushSize = 5

    def px7(self):  # Функция изменения размера
        self.brushSize = 7

    def px9(self):  # Функция изменения размера
        self.brushSize = 9

    def pxOther(self):  # Функция изменения размера
        i, okBtnPressed = QInputDialog.getInt(self, "Толщина",
                                              "Толщина линии", 2, 1, 80, 1)
        self.brushSize = i

    def blackColor(self):  # Функция изменения цвета
        self.brushColor = Qt.black

    def whiteColor(self):  # Функция изменения цвета
        self.brushColor = Qt.white

    def redColor(self):  # Функция изменения цвета
        self.brushColor = Qt.red

    def greenColor(self):  # Функция изменения цвета
        self.brushColor = Qt.green

    def yellowColor(self):  # Функция изменения цвета
        self.brushColor = Qt.yellow

    def otherColor(self):  # Функция изменения цвета
        self.brushColor = QColorDialog.getColor()

    # Функция получения координат от пользователя
    def get_cord(self, title, qustion, _min, _max):
        cord, okBtnPressed = QInputDialog.getInt(self, title, qustion,
                                                 0, _min, _max, 1)
        return cord

    # Функция для создания прямоугольника
    def rectangle(self):
        # Координата левого верхнего угла по x
        leftX = self.get_cord("Координата x",
                              "Координата левого верхнего угла по x", 0, 1200)
        # Координата левого верхнего угла по y
        leftY = self.get_cord("Координата y",
                              "Координата левого верхнего угла по y", 0, 2000)
        width = self.get_cord("Длина", "Длина", 0, 2000)  # Длина
        height = self.get_cord("Высота", "Высота", 0, 2000)  # высота
        cP = QPainter(self.image)  # Создание объекта класса QPainter
        cP.setPen(self.brushColor)  # Цвет границ
        cP.setBrush(self.brushColor)  # Цвет фигуры
        cP.drawRect(leftX, leftY, width, height)  # Нанесение прямоугольника
        self.lastImage()
        self.update()  # Обновление рисунка

    def ellips(self):  # Функция создания эллипса
        x = self.get_cord('Координата x',
                          'Координата центра по x',
                          0, 2000)  # Координата центра по x
        y = self.get_cord('Координата по y',
                          'Координата центра по y',
                          0, 2000)  # Координата центра по y
        w = self.get_cord("Ширина", "Ширина", 0, 2000)  # ширина
        h = self.get_cord("Высота", "Высота", 0, 2000)  # высота
        cP = QPainter(self.image)  # Создание объекта класса QPainter
        cP.setPen(self.brushColor)  # Цвет границ
        cP.setBrush(self.brushColor)  # Цвет фигуры
        cP.drawEllipse(x, y, w, h)  # Рисование эллипса
        self.lastImage()  # Добавление изображения
        self.update()  # обновление рисунка

    def addPicture(self):

        # Выбор разрешений
        files = 'PNG(*.png);;JPEG(*.jpg *jpeg);; ALL Files(*.*)'

        # Выбор файла
        filePath, _ = QFileDialog.getOpenFileName(self, 'Выбрать', '', files)
        img = QImage(filePath)  # Открытие изображения
        painter = QPainter(self.image)  # Создание объекта
        x = self.get_cord('Координата x',
                          'Координата левого верхнего угла по x',
                          0, 2000)  # Координата левого верхнего угла по x
        y = self.get_cord('Координата по y',
                          'Координата левого верхнего угла по y',
                          0, 2000)  # Координата левого верхнего угла по y
        painter.drawImage(x, y, img)  # Вывод изображения
        self.lastImage()  # Добавление изображения
        self.update()  # Обновление окна

    def line(self):
        x1 = self.get_cord('Координата x',
                           'Координата первой точки по x',
                           0, 2000)  # Координата первой точки по x
        y1 = self.get_cord('Координата по y',
                           'Координата первой точки по y',
                           0, 2000)  # Координата первой точки по y
        x2 = self.get_cord('Координата x',
                           'Координата второй точки по x',
                           0, 2000)  # Координата второй точки по x
        y2 = self.get_cord('Координата по y',
                           'Координата второй точки по y',
                           0, 2000)  # Координата второй точки по y
        cP = QPainter(self.image)
        cP.setPen(QPen(self.brushColor, self.brushSize))  # Цвет границ
        cP.setBrush(self.brushColor)  # Цвет фигуры
        cP.drawLine(x1, y1, x2, y2)  # Рисование линии
        self.lastImage()  # Добавление изображения
        self.update()  # Обновление окна

    def star(self):
        x1 = self.get_cord('Координата x',
                           'Координата верхней точки по x',
                           0, 2000)  # Координата верхней точки по x
        y1 = self.get_cord('Координата по y',
                           'Координата верхней точки по y',
                           0, 2000)  # Координата верхней точки по y
        x2 = self.get_cord('Координата x',
                           'Координата левой точки по x',
                           0, 2000)  # Координата левой точки по x
        y2 = self.get_cord('Координата по y',
                           'Координата левой точки по y',
                           0, 2000)  # Координата левой точки по y
        x3 = self.get_cord('Координата x',
                           'Координата левой нижней точки по x',
                           0, 2000)  # Координата левой нижней точки по x
        y3 = self.get_cord('Координата по y',
                           'Координата левой нижней точки по y',
                           0, 2000)  # Координата левой нижней точки по y
        cP = QPainter(self.image)
        cP.setPen(self.brushColor)  # Цвет границ
        cP.setBrush(self.brushColor)  # Цвет фигуры
        points = QPolygon([QPoint(x2, y2), QPoint(x1 + x1 - x2, y2),
                           QPoint(x3, y3), QPoint(x1, y1),
                           QPoint(x1 + x1 - x3, y3)
                           ])
        self.lastImage()  # Добавление изображения
        cP.drawPolygon(points)  # Нарисовать полигон

    def triangle(self):  # Функция для рисования треугольника
        x1 = self.get_cord('Координата x',
                           'Координата первой точки по x',
                           0, 2000)  # Координата первой точки по x
        y1 = self.get_cord('Координата по y',
                           'Координата первой точки по y',
                           0, 2000)  # Координата первой точки по y
        x2 = self.get_cord('Координата x',
                           'Координата второй точки по x',
                           0, 2000)  # Координата второй точки по x
        y2 = self.get_cord('Координата по y',
                           'Координата второй точки по y',
                           0, 2000)  # Координата второй точки по y
        x3 = self.get_cord('Координата x',
                           'Координата третьей точки по x',
                           0, 2000)  # Координата третьей нижней точки по x
        y3 = self.get_cord('Координата по y',
                           'Координата третьей точки по y',
                           0, 2000)  # Координата третьей нижней точки по y
        cP = QPainter(self.image)
        cP.setPen(self.brushColor)  # Цвет границ
        cP.setBrush(self.brushColor)  # Цвет фигуры
        points = QPolygon([QPoint(x1, y1), QPoint(x2, y2), QPoint(x3, y3)])
        self.lastImage()  # Добавление изображения
        cP.drawPolygon(points)  # Нарисовать полигон

    def copyArea(self):  # Функция копирования области
        x = self.get_cord('Координата x',
                          'Координата левого верхнего угла по x',
                          0, 2000)  # Координата левого верхнего угла по x
        y = self.get_cord('Координата по y',
                          'Координата левого верхнего угла по y',
                          0, 2000)  # Координата левого верхнего угла по y
        w = self.get_cord("Ширина", "Ширина", 0, 2000)  # ширина
        h = self.get_cord("Высота", "Высота", 0, 2000)  # высота
        self.copyA = QImage.copy(self.image, x, y, w, h)

    def writeText(self):  # Функция для вывода текста
        i, okBtnPressed = QInputDialog.getText(
            self, "Текст", "Введите текст"
                    )  # Диалоговое окно для ввода текста
        cP = QPainter(self.image)
        cP.setPen(self.brushColor)
        cP.setFont(QFont('Decorative', self.get_cord('Шрифт', 'Шрифт',
                                                     1, 150)))  # Шрифт
        cP.drawText(self.get_cord('Координата x',
                                  'Координата левого нижнего угла по x',
                                  0, 2000),
                    self.get_cord('Координата y',
                                  'Координата левого нижнего угла по y',
                                  0, 2000),
                    i)  # Координата
        self.lastImage()  # Добавление изображения
        self.update()  # Обновление страницы

    def fillAll(self):  # Функция для заливки окна
        self.image.fill(self.brushColor)  # Заливка цветом
        self.lastImage()  # Добавление изображения
        self.update()  # Обновление картины

    def cutArea(self):  # Функция для вырезания области
        x = self.get_cord('Координата x',
                          'Координата левого верхнего угла по x',
                          0, 2000)  # Координата левого верхнего угла по x
        y = self.get_cord('Координата по y',
                          'Координата левого верхнего угла по y',
                          0, 2000)  # Координата левого верхнего угла по y
        w = self.get_cord("Ширина", "Ширина", 0, 2000)  # ширина
        h = self.get_cord("Высота", "Высота", 0, 2000)  # высота
        self.copyA = QImage.copy(self.image, x, y, w, h)
        cP = QPainter(self.image)  # Создание объекта класса QPainter
        cP.setPen(Qt.white)
        cP.setBrush(Qt.white)
        cP.drawRect(x, y, w, h)  # Закраска области в белый
        self.update()  # Обновление рисунка

    def pasteArea(self):  # Функция вставки области
        if not self.copyA:  # Если область пустая
            return
        x = self.get_cord('Координата x',
                          'Координата левого верхнего угла по x',
                          0, 2000)  # Координата левого верхнего угла по x
        y = self.get_cord('Координата по y',
                          'Координата левого верхнего угла по y',
                          0, 2000)  # Координата левого верхнего угла по y
        painter = QPainter(self.image)  # Создание объекта
        painter.drawImage(x, y, self.copyA)  # Вывод изображения
        self.lastImage()  # Добавление изображения
        self.update()  # Обновление окна

    def sizeAdd(self):  # Функция изменения размера окна
        w = self.get_cord('Ширина окна',
                          'Ширина окна',
                          0, 2000)  # Ширина окна
        h = self.get_cord('Высота окна',
                          'Высота окна',
                          0, 2000)  # Высота окна
        f = open('size.txt', 'w')  # Открытие файла с размерами
        f.write(str(w) + '\n' + str(h))  # Перезапись файла
        f.close()  # Закрытие файла
        QMessageBox.about(self, "Перезапустите программу",
                          "Перезапустите программу")  # Сообщение

    def closeEvent(self, event):  # Функция для закрытия
        # Сообщение при закрытии приложения
        reply = QMessageBox.question(self, 'Сообщение',
                                     "Вы уверены, что хотите выйти?",
                                     QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:  # Если Да
            try:
                shutil.rmtree('last')
            except Exception:
                pass
            event.accept()  # То выход
        else:
            event.ignore()  # Иначе игнорировать

    def lastImage(self):  # Функция добавления картинки в папку
        self.image.save('last/' + str(self.last) + '.png')  # Сохранение
        self.last += 1
        i = 0
        while len(os.listdir('last/')) > self.last:  # Если картинок больше
            os.remove('last/' + str(self.last + i) + '.png')
            i += 1

    def returnLast(self):  # Функция возвращения последней картинки
        if self.last - 1 >= 0:
            self.image.fill(Qt.white)  # Заливки пустым
            self.last -= 2
            painter = QPainter(self.image)

            # Возвращение последней картинки
            painter.drawImage(0, 0, QImage('last/' + str(self.last) + '.png'))
            self.last += 1
            self.update()  # Обновление картинки

    def returnUp(self):  # Функция возвращения передней картинки
        if self.last != len(os.listdir('last/')):
            self.image.fill(Qt.white)
            painter = QPainter(self.image)

            # Возвращение передней картинки
            painter.drawImage(0, 0, QImage('last/' + str(self.last) + '.png'))
            self.last += 1
            self.update()  # Обновление картинки


if __name__ == '__main__':
    app = QApplication(sys.argv)
    p = Paint()
    p.show()
    sys.exit(app.exec())
