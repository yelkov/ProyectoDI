# Form implementation generated from reading ui file '.\\templates\\venPrincipal.ui'
#
# Created by: PyQt6 UI code generator 6.7.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_venPrincipal(object):
    def setupUi(self, venPrincipal):
        venPrincipal.setObjectName("venPrincipal")
        venPrincipal.resize(1310, 729)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(venPrincipal.sizePolicy().hasHeightForWidth())
        venPrincipal.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(".\\\\templates\\../img/icono.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        venPrincipal.setWindowIcon(icon)
        venPrincipal.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.centralwidget = QtWidgets.QWidget(parent=venPrincipal)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 0, 2, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout_2.addItem(spacerItem1, 0, 0, 1, 1)
        self.panPrincipal = QtWidgets.QTabWidget(parent=self.centralwidget)
        self.panPrincipal.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.panPrincipal.sizePolicy().hasHeightForWidth())
        self.panPrincipal.setSizePolicy(sizePolicy)
        self.panPrincipal.setMinimumSize(QtCore.QSize(1200, 660))
        self.panPrincipal.setObjectName("panPrincipal")
        self.pesClientes = QtWidgets.QWidget()
        self.pesClientes.setObjectName("pesClientes")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.pesClientes)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.btnGrabarcli = QtWidgets.QPushButton(parent=self.pesClientes)
        self.btnGrabarcli.setMinimumSize(QtCore.QSize(80, 25))
        self.btnGrabarcli.setMaximumSize(QtCore.QSize(80, 25))
        self.btnGrabarcli.setObjectName("btnGrabarcli")
        self.gridLayout_3.addWidget(self.btnGrabarcli, 0, 1, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout_3.addItem(spacerItem2, 0, 4, 1, 1)
        self.btnModifcli = QtWidgets.QPushButton(parent=self.pesClientes)
        self.btnModifcli.setMinimumSize(QtCore.QSize(80, 25))
        self.btnModifcli.setMaximumSize(QtCore.QSize(80, 25))
        self.btnModifcli.setObjectName("btnModifcli")
        self.gridLayout_3.addWidget(self.btnModifcli, 0, 2, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout_3.addItem(spacerItem3, 0, 0, 1, 1)
        self.btnDelcli = QtWidgets.QPushButton(parent=self.pesClientes)
        self.btnDelcli.setMinimumSize(QtCore.QSize(80, 25))
        self.btnDelcli.setMaximumSize(QtCore.QSize(80, 25))
        self.btnDelcli.setObjectName("btnDelcli")
        self.gridLayout_3.addWidget(self.btnDelcli, 0, 3, 1, 1)
        self.gridLayout_4.addLayout(self.gridLayout_3, 2, 0, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(0, 20, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.gridLayout_4.addItem(spacerItem4, 1, 0, 1, 1)
        self.line = QtWidgets.QFrame(parent=self.pesClientes)
        self.line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line.setLineWidth(3)
        self.line.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line.setObjectName("line")
        self.gridLayout_4.addWidget(self.line, 3, 0, 1, 2)
        self.tablaClientes = QtWidgets.QTableWidget(parent=self.pesClientes)
        self.tablaClientes.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.tablaClientes.setObjectName("tablaClientes")
        self.tablaClientes.setColumnCount(7)
        self.tablaClientes.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tablaClientes.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tablaClientes.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tablaClientes.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tablaClientes.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tablaClientes.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tablaClientes.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tablaClientes.setHorizontalHeaderItem(6, item)
        self.tablaClientes.verticalHeader().setVisible(False)
        self.gridLayout_4.addWidget(self.tablaClientes, 4, 0, 1, 1)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout.addItem(spacerItem5, 1, 14, 1, 1)
        self.lblMunicli = QtWidgets.QLabel(parent=self.pesClientes)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblMunicli.sizePolicy().hasHeightForWidth())
        self.lblMunicli.setSizePolicy(sizePolicy)
        self.lblMunicli.setObjectName("lblMunicli")
        self.gridLayout.addWidget(self.lblMunicli, 3, 9, 1, 1)
        self.lblProvcli = QtWidgets.QLabel(parent=self.pesClientes)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblProvcli.sizePolicy().hasHeightForWidth())
        self.lblProvcli.setSizePolicy(sizePolicy)
        self.lblProvcli.setObjectName("lblProvcli")
        self.gridLayout.addWidget(self.lblProvcli, 3, 6, 1, 1)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout.addItem(spacerItem6, 1, 0, 1, 1)
        self.txtBajacli = QtWidgets.QLineEdit(parent=self.pesClientes)
        self.txtBajacli.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.txtBajacli.sizePolicy().hasHeightForWidth())
        self.txtBajacli.setSizePolicy(sizePolicy)
        self.txtBajacli.setMinimumSize(QtCore.QSize(80, 0))
        self.txtBajacli.setMaximumSize(QtCore.QSize(80, 16777215))
        self.txtBajacli.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.txtBajacli.setObjectName("txtBajacli")
        self.gridLayout.addWidget(self.txtBajacli, 0, 9, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetFixedSize)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.txtDnicli = QtWidgets.QLineEdit(parent=self.pesClientes)
        self.txtDnicli.setMinimumSize(QtCore.QSize(120, 0))
        self.txtDnicli.setMaximumSize(QtCore.QSize(150, 16777215))
        self.txtDnicli.setStyleSheet("background-color: rgb(254, 255, 210);")
        self.txtDnicli.setObjectName("txtDnicli")
        self.horizontalLayout.addWidget(self.txtDnicli)
        self.lblTickcli = QtWidgets.QLabel(parent=self.pesClientes)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblTickcli.sizePolicy().hasHeightForWidth())
        self.lblTickcli.setSizePolicy(sizePolicy)
        self.lblTickcli.setMaximumSize(QtCore.QSize(20, 20))
        self.lblTickcli.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.lblTickcli.setText("")
        self.lblTickcli.setObjectName("lblTickcli")
        self.horizontalLayout.addWidget(self.lblTickcli)
        spacerItem7 = QtWidgets.QSpacerItem(0, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem7)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 2, 1, 1)
        spacerItem8 = QtWidgets.QSpacerItem(13, 20, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout.addItem(spacerItem8, 1, 3, 1, 1)
        self.txtDircli = QtWidgets.QLineEdit(parent=self.pesClientes)
        self.txtDircli.setMinimumSize(QtCore.QSize(400, 0))
        self.txtDircli.setMaximumSize(QtCore.QSize(400, 16777215))
        self.txtDircli.setObjectName("txtDircli")
        self.gridLayout.addWidget(self.txtDircli, 3, 2, 1, 4)
        self.cmbProvcli = QtWidgets.QComboBox(parent=self.pesClientes)
        self.cmbProvcli.setMinimumSize(QtCore.QSize(120, 0))
        self.cmbProvcli.setObjectName("cmbProvcli")
        self.gridLayout.addWidget(self.cmbProvcli, 3, 7, 1, 1)
        self.lblMovilcli = QtWidgets.QLabel(parent=self.pesClientes)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblMovilcli.sizePolicy().hasHeightForWidth())
        self.lblMovilcli.setSizePolicy(sizePolicy)
        self.lblMovilcli.setObjectName("lblMovilcli")
        self.gridLayout.addWidget(self.lblMovilcli, 2, 4, 1, 1)
        self.lblEmailcli = QtWidgets.QLabel(parent=self.pesClientes)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblEmailcli.sizePolicy().hasHeightForWidth())
        self.lblEmailcli.setSizePolicy(sizePolicy)
        self.lblEmailcli.setObjectName("lblEmailcli")
        self.gridLayout.addWidget(self.lblEmailcli, 2, 1, 1, 1)
        self.txtAltacli = QtWidgets.QLineEdit(parent=self.pesClientes)
        self.txtAltacli.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.txtAltacli.sizePolicy().hasHeightForWidth())
        self.txtAltacli.setSizePolicy(sizePolicy)
        self.txtAltacli.setMinimumSize(QtCore.QSize(80, 0))
        self.txtAltacli.setMaximumSize(QtCore.QSize(80, 16777215))
        self.txtAltacli.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.txtAltacli.setObjectName("txtAltacli")
        self.gridLayout.addWidget(self.txtAltacli, 0, 5, 1, 1)
        spacerItem9 = QtWidgets.QSpacerItem(13, 20, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout.addItem(spacerItem9, 2, 3, 1, 1)
        self.lblDnicli = QtWidgets.QLabel(parent=self.pesClientes)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblDnicli.sizePolicy().hasHeightForWidth())
        self.lblDnicli.setSizePolicy(sizePolicy)
        self.lblDnicli.setObjectName("lblDnicli")
        self.gridLayout.addWidget(self.lblDnicli, 0, 1, 1, 1)
        self.txtNomcli = QtWidgets.QLineEdit(parent=self.pesClientes)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.txtNomcli.sizePolicy().hasHeightForWidth())
        self.txtNomcli.setSizePolicy(sizePolicy)
        self.txtNomcli.setMinimumSize(QtCore.QSize(300, 0))
        self.txtNomcli.setObjectName("txtNomcli")
        self.gridLayout.addWidget(self.txtNomcli, 1, 5, 1, 8)
        self.lblNomcli = QtWidgets.QLabel(parent=self.pesClientes)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblNomcli.sizePolicy().hasHeightForWidth())
        self.lblNomcli.setSizePolicy(sizePolicy)
        self.lblNomcli.setObjectName("lblNomcli")
        self.gridLayout.addWidget(self.lblNomcli, 1, 4, 1, 1)
        self.lblAltacli = QtWidgets.QLabel(parent=self.pesClientes)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblAltacli.sizePolicy().hasHeightForWidth())
        self.lblAltacli.setSizePolicy(sizePolicy)
        self.lblAltacli.setObjectName("lblAltacli")
        self.gridLayout.addWidget(self.lblAltacli, 0, 4, 1, 1)
        self.txtMovilcli = QtWidgets.QLineEdit(parent=self.pesClientes)
        self.txtMovilcli.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.txtMovilcli.sizePolicy().hasHeightForWidth())
        self.txtMovilcli.setSizePolicy(sizePolicy)
        self.txtMovilcli.setMinimumSize(QtCore.QSize(90, 0))
        self.txtMovilcli.setMaximumSize(QtCore.QSize(150, 16777215))
        self.txtMovilcli.setObjectName("txtMovilcli")
        self.gridLayout.addWidget(self.txtMovilcli, 2, 5, 1, 5)
        self.lblDircli = QtWidgets.QLabel(parent=self.pesClientes)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblDircli.sizePolicy().hasHeightForWidth())
        self.lblDircli.setSizePolicy(sizePolicy)
        self.lblDircli.setObjectName("lblDircli")
        self.gridLayout.addWidget(self.lblDircli, 3, 1, 1, 1)
        self.lblApelcli = QtWidgets.QLabel(parent=self.pesClientes)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblApelcli.sizePolicy().hasHeightForWidth())
        self.lblApelcli.setSizePolicy(sizePolicy)
        self.lblApelcli.setObjectName("lblApelcli")
        self.gridLayout.addWidget(self.lblApelcli, 1, 1, 1, 1)
        self.txtEmailcli = QtWidgets.QLineEdit(parent=self.pesClientes)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.txtEmailcli.sizePolicy().hasHeightForWidth())
        self.txtEmailcli.setSizePolicy(sizePolicy)
        self.txtEmailcli.setMinimumSize(QtCore.QSize(200, 0))
        self.txtEmailcli.setMaximumSize(QtCore.QSize(200, 16777215))
        self.txtEmailcli.setObjectName("txtEmailcli")
        self.gridLayout.addWidget(self.txtEmailcli, 2, 2, 1, 1)
        spacerItem10 = QtWidgets.QSpacerItem(13, 20, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout.addItem(spacerItem10, 0, 3, 1, 1)
        self.btnAltacli = QtWidgets.QPushButton(parent=self.pesClientes)
        self.btnAltacli.setMinimumSize(QtCore.QSize(20, 20))
        self.btnAltacli.setMaximumSize(QtCore.QSize(32, 16777215))
        self.btnAltacli.setStyleSheet("background-color : rgb(255, 255, 255)")
        self.btnAltacli.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(".\\\\templates\\../img/calendar.ico"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.btnAltacli.setIcon(icon1)
        self.btnAltacli.setObjectName("btnAltacli")
        self.gridLayout.addWidget(self.btnAltacli, 0, 6, 1, 1)
        self.txtApelcli = QtWidgets.QLineEdit(parent=self.pesClientes)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.txtApelcli.sizePolicy().hasHeightForWidth())
        self.txtApelcli.setSizePolicy(sizePolicy)
        self.txtApelcli.setMinimumSize(QtCore.QSize(300, 0))
        self.txtApelcli.setMaximumSize(QtCore.QSize(300, 16777215))
        self.txtApelcli.setObjectName("txtApelcli")
        self.gridLayout.addWidget(self.txtApelcli, 1, 2, 1, 1)
        self.btnBajacli = QtWidgets.QPushButton(parent=self.pesClientes)
        self.btnBajacli.setMinimumSize(QtCore.QSize(20, 20))
        self.btnBajacli.setMaximumSize(QtCore.QSize(32, 16777215))
        self.btnBajacli.setStyleSheet("background-color : rgb(255, 255, 255)")
        self.btnBajacli.setText("")
        self.btnBajacli.setIcon(icon1)
        self.btnBajacli.setObjectName("btnBajacli")
        self.gridLayout.addWidget(self.btnBajacli, 0, 10, 1, 1)
        self.lblBajacli = QtWidgets.QLabel(parent=self.pesClientes)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblBajacli.sizePolicy().hasHeightForWidth())
        self.lblBajacli.setSizePolicy(sizePolicy)
        self.lblBajacli.setObjectName("lblBajacli")
        self.gridLayout.addWidget(self.lblBajacli, 0, 8, 1, 1)
        self.cmbMunicli = QtWidgets.QComboBox(parent=self.pesClientes)
        self.cmbMunicli.setMinimumSize(QtCore.QSize(180, 0))
        self.cmbMunicli.setObjectName("cmbMunicli")
        self.gridLayout.addWidget(self.cmbMunicli, 3, 10, 1, 1)
        self.chkHistoriacli = QtWidgets.QCheckBox(parent=self.pesClientes)
        self.chkHistoriacli.setObjectName("chkHistoriacli")
        self.gridLayout.addWidget(self.chkHistoriacli, 3, 13, 1, 1)
        spacerItem11 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout.addItem(spacerItem11, 3, 12, 1, 1)
        self.gridLayout_4.addLayout(self.gridLayout, 0, 0, 1, 2)
        self.panPrincipal.addTab(self.pesClientes, "")
        self.tabConstruccion = QtWidgets.QWidget()
        self.tabConstruccion.setObjectName("tabConstruccion")
        self.label = QtWidgets.QLabel(parent=self.tabConstruccion)
        self.label.setGeometry(QtCore.QRect(240, 260, 471, 71))
        font = QtGui.QFont()
        font.setPointSize(23)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setObjectName("label")
        self.panPrincipal.addTab(self.tabConstruccion, "")
        self.gridLayout_2.addWidget(self.panPrincipal, 0, 1, 1, 1)
        venPrincipal.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=venPrincipal)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1310, 21))
        self.menubar.setObjectName("menubar")
        self.menuArchivo = QtWidgets.QMenu(parent=self.menubar)
        self.menuArchivo.setObjectName("menuArchivo")
        self.menuHerramientas = QtWidgets.QMenu(parent=self.menubar)
        self.menuHerramientas.setObjectName("menuHerramientas")
        self.menuAyuda = QtWidgets.QMenu(parent=self.menubar)
        self.menuAyuda.setObjectName("menuAyuda")
        venPrincipal.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=venPrincipal)
        self.statusbar.setObjectName("statusbar")
        venPrincipal.setStatusBar(self.statusbar)
        self.actionSalir = QtGui.QAction(parent=venPrincipal)
        self.actionSalir.setObjectName("actionSalir")
        self.actionCrear_backup = QtGui.QAction(parent=venPrincipal)
        self.actionCrear_backup.setObjectName("actionCrear_backup")
        self.actionRestaurar_backup = QtGui.QAction(parent=venPrincipal)
        self.actionRestaurar_backup.setObjectName("actionRestaurar_backup")
        self.menuArchivo.addAction(self.actionSalir)
        self.menuHerramientas.addAction(self.actionCrear_backup)
        self.menuHerramientas.addAction(self.actionRestaurar_backup)
        self.menubar.addAction(self.menuArchivo.menuAction())
        self.menubar.addAction(self.menuHerramientas.menuAction())
        self.menubar.addAction(self.menuAyuda.menuAction())

        self.retranslateUi(venPrincipal)
        self.panPrincipal.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(venPrincipal)
        venPrincipal.setTabOrder(self.panPrincipal, self.txtDnicli)
        venPrincipal.setTabOrder(self.txtDnicli, self.txtAltacli)
        venPrincipal.setTabOrder(self.txtAltacli, self.txtApelcli)
        venPrincipal.setTabOrder(self.txtApelcli, self.txtNomcli)
        venPrincipal.setTabOrder(self.txtNomcli, self.txtEmailcli)
        venPrincipal.setTabOrder(self.txtEmailcli, self.txtMovilcli)
        venPrincipal.setTabOrder(self.txtMovilcli, self.txtDircli)
        venPrincipal.setTabOrder(self.txtDircli, self.btnGrabarcli)
        venPrincipal.setTabOrder(self.btnGrabarcli, self.btnModifcli)
        venPrincipal.setTabOrder(self.btnModifcli, self.btnDelcli)
        venPrincipal.setTabOrder(self.btnDelcli, self.tablaClientes)
        venPrincipal.setTabOrder(self.tablaClientes, self.btnAltacli)

    def retranslateUi(self, venPrincipal):
        _translate = QtCore.QCoreApplication.translate
        venPrincipal.setWindowTitle(_translate("venPrincipal", "InmoTeis"))
        self.btnGrabarcli.setText(_translate("venPrincipal", "Grabar"))
        self.btnModifcli.setText(_translate("venPrincipal", "Modificar"))
        self.btnDelcli.setText(_translate("venPrincipal", "Eliminar"))
        item = self.tablaClientes.horizontalHeaderItem(0)
        item.setText(_translate("venPrincipal", "DNI/NIE"))
        item = self.tablaClientes.horizontalHeaderItem(1)
        item.setText(_translate("venPrincipal", "Apellidos"))
        item = self.tablaClientes.horizontalHeaderItem(2)
        item.setText(_translate("venPrincipal", "Nombre"))
        item = self.tablaClientes.horizontalHeaderItem(3)
        item.setText(_translate("venPrincipal", "Móvil"))
        item = self.tablaClientes.horizontalHeaderItem(4)
        item.setText(_translate("venPrincipal", "Provincia"))
        item = self.tablaClientes.horizontalHeaderItem(5)
        item.setText(_translate("venPrincipal", "Municipio"))
        item = self.tablaClientes.horizontalHeaderItem(6)
        item.setText(_translate("venPrincipal", "Fecha Baja"))
        self.lblMunicli.setText(_translate("venPrincipal", "Municipio:"))
        self.lblProvcli.setText(_translate("venPrincipal", "Provincia:"))
        self.lblMovilcli.setText(_translate("venPrincipal", "Móvil:"))
        self.lblEmailcli.setText(_translate("venPrincipal", "Email:"))
        self.lblDnicli.setText(_translate("venPrincipal", "DNI/CIF:"))
        self.lblNomcli.setText(_translate("venPrincipal", "Nombre:"))
        self.lblAltacli.setText(_translate("venPrincipal", "Fecha alta:"))
        self.lblDircli.setText(_translate("venPrincipal", "Dirección:"))
        self.lblApelcli.setText(_translate("venPrincipal", "Apellidos:"))
        self.lblBajacli.setText(_translate("venPrincipal", "Fecha baja:"))
        self.chkHistoriacli.setText(_translate("venPrincipal", "Histórico"))
        self.panPrincipal.setTabText(self.panPrincipal.indexOf(self.pesClientes), _translate("venPrincipal", "CLIENTES"))
        self.label.setText(_translate("venPrincipal", "PANEL EN CONSTRUCCIÓN"))
        self.panPrincipal.setTabText(self.panPrincipal.indexOf(self.tabConstruccion), _translate("venPrincipal", "Tab 2"))
        self.menuArchivo.setTitle(_translate("venPrincipal", "Archivo"))
        self.menuHerramientas.setTitle(_translate("venPrincipal", "Herramientas"))
        self.menuAyuda.setTitle(_translate("venPrincipal", "Ayuda"))
        self.actionSalir.setText(_translate("venPrincipal", "Salir"))
        self.actionCrear_backup.setText(_translate("venPrincipal", "Crear backup"))
        self.actionRestaurar_backup.setText(_translate("venPrincipal", "Restaurar backup"))
