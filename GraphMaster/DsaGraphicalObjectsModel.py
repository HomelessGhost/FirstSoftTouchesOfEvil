from PyQt5.QtCore import QAbstractListModel, QModelIndex
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QColor, QIcon


class DsaGraphicalObjectsModel(QAbstractListModel):
    def __init__(self, data=[], parent=None):
        QAbstractListModel.__init__(self, parent)
        self.__data = data

    def rowCount(self, parent):
        return len(self.__data)

    def data(self, index, role):

        if role == Qt.EditRole:
            return self.__data[index.row()][0]

        if role == Qt.ToolTipRole:
            return "Element" + str(self.__data[index.row()][0])

        if role == Qt.DecorationRole:
            row = index.row()
            try:
                value = self.__data[row][1][0].get_color()
                pixmap = QPixmap(26, 26)
                pixmap.fill(QColor(value))
                icon = QIcon(pixmap)
            except:
                pixmap = QPixmap(26, 26)
                pixmap.fill(QColor('black'))
                icon = QIcon(pixmap)
            return icon

        if role == Qt.DisplayRole:
            row = index.row()
            value = self.__data[row][0]
            return value

    def setData(self, index, value, role):
        if role == Qt.EditRole:
            row = index.row()
            data_value = value
            self.__data[row][0] = data_value
            self.dataChanged.emit(index, index)
            return True

    def flags(self, index):
        return Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def insertRows(self, position, rows, data,  parent=QModelIndex()):
        self.beginInsertRows(parent, position, position + rows - 1)
        for i in range(rows):
            self.__data.insert(position, data)
        self.endInsertRows()
        return True

    def removeRows(self, position, rows,  parent=QModelIndex()):
        __instance_of_graphical_object = self.__data[position][1]
        if type(__instance_of_graphical_object) is list:
            __instance_of_graphical_object.pop(0).remove()
        if type(__instance_of_graphical_object) is not list:
            __instance_of_graphical_object.remove()

        self.beginRemoveRows(parent, position, position + rows - 1)
        for i in range(rows):
            value = self.__data[position]
            self.__data.remove(value)
        self.endRemoveRows()
        return True







