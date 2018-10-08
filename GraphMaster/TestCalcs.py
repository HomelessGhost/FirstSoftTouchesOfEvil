from GraphMaster.StringFunc import StringFunction
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QGridLayout, QVBoxLayout, QLineEdit, QWidget, QLabel, QHBoxLayout, QListView
from PyQt5.QtGui import QIcon, QPixmap
from GraphMaster.PlotCanvas import Canvas
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from GraphMaster.DsaGraphicalObjectsModel import DsaGraphicalObjectsModel
import numpy as np
import sys


class MainWindow(QMainWindow):
    graph_legend = []

    def __init__(self):
        super().__init__()

        self.setWindowTitle('GraphMaster')
        self.setWindowIcon(QIcon('../Icons/formula.png'))
        self.setGeometry(400, 400, 900, 600)
        self.MyUI()

    def MyUI(self):
        self.fig, self.axes = self.plot_sigle_empty_graph()
        self.canvas = Canvas(self.fig)
        self.toolbar = NavigationToolbar(self.canvas, self)

        self.v_layout = QVBoxLayout()
        self.h_layout = QHBoxLayout()

        self.list_view = QListView()
        self.plot_dots_model = DsaGraphicalObjectsModel()
        self.list_view.setModel(self.plot_dots_model)
        self.btn_clear = QPushButton('Delete')
        self.btn_clear.clicked.connect(self.remove_plot)




        self.v_layout.addWidget(self.canvas)
        self.v_layout.addWidget(self.toolbar)

        self.lbl_func = QLabel()
        self.lbl_func.setPixmap(QPixmap('../Icons/function-mathematical-symbol.png'))
        self.f_field = QLineEdit()

        self.h_layout.addWidget(self.lbl_func)
        self.h_layout.addWidget(self.f_field)

        self.layout = QGridLayout()

        self.btn = QPushButton('Plot')
        self.btn.clicked.connect(self.on_clicked_plot)

        self.layout.addLayout(self.h_layout, 0, 0, 1, 6)

        self.layout.addWidget(self.btn, 1, 4, 1, 2)
        self.layout.addWidget(self.btn_clear, 1, 0, 1, 2)
        self.layout.addLayout(self.v_layout, 0, 6, 5, 5)
        self.layout.addWidget(self.list_view, 2, 0, 5, 6)

        self.central_widget = QWidget()
        self.central_widget.setLayout(self.layout)

        self.setCentralWidget(self.central_widget)

    def get_f_str(self):
        return self.f_field.text()

    def on_clicked_plot(self):
        self.plot()

    def plot_sigle_empty_graph(self):
        fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(10, 7), dpi=100,
                                 facecolor='grey', frameon=True, edgecolor='black', linewidth=1)
        fig.subplots_adjust(wspace=0.4, hspace=0.6, left=0.15, right=0.85, top=0.9, bottom=0.1)
        axes.grid(True, c='lightgrey', alpha=0.7)
        axes.set_title('Diagram Header', fontsize=10)
        axes.set_xlabel('X', fontsize=8)
        axes.set_ylabel('Y', fontsize=8)
        return fig, axes

    def plot_custom_function(self, axes=None, function=None,
                             legend=None, name=None, limits=None, type='y=f(x)'):
        left_limit = limits[0]
        right_limit = limits[1]
        step = (max(limits) - min(limits))/100000
        if type == 'y=f(x)':
            legend.append('y=' + str(function))
            x_vals = np.arange(left_limit, right_limit, step)
            f = StringFunction(function)
            y_vals = [f.calculate_f(x) for x in x_vals]
            plot_instance = axes.plot(x_vals, y_vals, '-', lw=1)
            axes.set_xlim(left_limit, right_limit)
            axes.set_ylim(left_limit, right_limit)
            axes.legend(legend, loc='best', fontsize=8)
        return plot_instance

    def plot(self):
        function = self.f_field.text()
        instance = self.plot_custom_function(axes=self.axes,
                                             function=function,
                                             legend=self.graph_legend,
                                             limits=[0.01, 40])
        self.fig.canvas.draw()
        self.plot_dots_model.insertRows(0, 1, data=['y=' + function, instance])

    def remove_plot(self):
        index = self.list_view.currentIndex()
        position = index.row()
        model = index.model()
        model.removeRows(position=position, rows=1)
        self.fig.canvas.draw()


app = QApplication(sys.argv)
window = MainWindow()
window.show()
exit(app.exec_())
