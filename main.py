import sys
import interfaz
from PyQt5 import QtWidgets

class MyApp(QtWidgets.QMainWindow, interfaz.Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        interfaz.Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.qNombre = list()
        self.qIzquierda = list()
        self.estadosQ = list()
        self.filas = None

        self.btnCargarTabla.clicked.connect(self.cargarTabla)
        self.btnCalcularCadena.setEnabled(False)
        self.btnLimpiar.setEnabled(False)
        self.campoQ0.setEnabled(False)
        self.campoF.setEnabled(False)

    def cargarTabla(self):
        self.tabla.setRowCount(0)
        self.btnCargarTabla.setEnabled(False)
        self.nQ.setEnabled(False)
        self.qNombre = list()
        self.estadosQ = list()
        self.filas = 0

        # Asignar los valores Qn a la tabla.
        self.filas = int(self.nQ.text())
        for i in range(0, self.filas):
            self.tabla.insertRow(i)
            self.qNombre.append("Q{}".format(i))

        # Asignar valores Q a los headers de cada fila
        self.tabla.setVerticalHeaderLabels(self.qNombre)
        self.btnCalcularCadena.setEnabled(True)
        self.campoQ0.setEnabled(True)
        self.campoF.setEnabled(True)
        self.btnCalcularCadena.clicked.connect(self.calcularCadena)
        self.btnLimpiar.clicked.connect(self.limpiar_casillas_tablas)

    def calcularCadena(self):
        self.btnCalcularCadena.setEnabled(False)
        self.btnLimpiar.setEnabled(True)

        # Guarda los estados asignados según la tabla.
        for i in range(0, self.filas):
            self.estadosQ.append([self.retornarNumeroStr(self.tabla.item(i, 0).text()),
                                  self.retornarNumeroStr(self.tabla.item(i, 1).text())])

        #Se llenan las tablas de conversión
        self.tablaConversion()
        self.cargarR()
        self.obtenerResultadoF()

    def tablaConversion(self):
        self.arreglo_tabla_0_1 = list()
        self.qIzquierda = list()

        self.qActualNumerica = self.retornarNumeroStr(self.campoQ0.text()) # q1,q2 -> 12
        self.qIzquierda.append(self.retornarEstructuraOriginalQn(self.qActualNumerica)) # 12 -> q1,q2

        fila_iteracion = 0

        while fila_iteracion < len(self.qIzquierda):
            self.arreglo_tabla_0_1.append([0] * 2) #Agregar nuevo espacio a la lista de conversion

            if self.qIzquierda[fila_iteracion] != 'none': #Si el valor actual de la izquierda NO es none...

                if len(self.retornarNumeroStr(self.qIzquierda[fila_iteracion])) > 1: # Si hay mas de dos Q's

                    for k in range(0, 2): # Se toman los estados para evaluar 0 y 1 independientemente
                        conjuntos = list()
                        for j in list(self.retornarNumeroStr(self.qIzquierda[fila_iteracion])): # Para cada estado... (12 -> 1)

                            conjunto_actual = self.estadosQ[int(j)][k] # Se toma el conjunto actual. Ex: 1 -> 0: 1,2; 1: 2

                            if conjunto_actual != 'none': # Si es diferente a la nada...
                                conjuntos.append(conjunto_actual)
                                qActualNumerica = "".join(set(''.join(conjuntos))) # Se eliminan los duplicados con conversiones

                                #Se agrega a la tabla conversion....
                                self.arreglo_tabla_0_1[fila_iteracion][k] = self.retornarEstructuraOriginalQn(qActualNumerica)

                        #Si el valor obtenido no esta en la izquierda se agrega
                        if self.arreglo_tabla_0_1[fila_iteracion][k] not in self.qIzquierda:
                            self.qIzquierda.append(self.arreglo_tabla_0_1[fila_iteracion][k])

                else: # Si solo es un estado. Ex: q1
                    for j in range(0, 2):
                        qActualNumerica = self.estadosQ[int(self.retornarNumeroStr(self.qIzquierda[fila_iteracion]))][j]

                        if qActualNumerica != 'none': # Si el valor obtenido NO es nada...
                            qActual_original = self.retornarEstructuraOriginalQn(qActualNumerica)
                            self.arreglo_tabla_0_1[fila_iteracion][j] = qActual_original

                            if self.arreglo_tabla_0_1[fila_iteracion][j] not in self.qIzquierda: # Si lo obtenido no esta en izq...
                                self.qIzquierda.append(self.arreglo_tabla_0_1[fila_iteracion][j])

                        else: # Si el valor SI es nada, al ser un unico estado, se evalua

                            if 'none' not in self.qIzquierda:
                                self.qIzquierda.append('none')
                            self.arreglo_tabla_0_1[fila_iteracion][j] = 'none'

            else: # Si el valor izq actual es NONE, entonces en su tabla de estados se asiga a NONE
                self.arreglo_tabla_0_1[fila_iteracion][0] = 'none'
                self.arreglo_tabla_0_1[fila_iteracion][1] = 'none'

            fila_iteracion = fila_iteracion + 1

        self.cargarSegundaTabla()


    def cargarSegundaTabla(self):
        for iteracion_tabla in range(len(self.qIzquierda)):
            self.tabla_2.insertRow(iteracion_tabla)
            self.tabla_2.setItem(iteracion_tabla, 0, QtWidgets.QTableWidgetItem(str(self.arreglo_tabla_0_1[iteracion_tabla][0])))
            self.tabla_2.setItem(iteracion_tabla, 1, QtWidgets.QTableWidgetItem(str(self.arreglo_tabla_0_1[iteracion_tabla][1])))

        self.tabla_2.setVerticalHeaderLabels(self.qIzquierda)


    def cargarR(self):
        self.encabezado_vertical_r = list()
        for iteracion in range(len(self.qIzquierda)): # Rellenar tabla de R'
            self.encabezado_vertical_r.append('R{0}'.format(iteracion))

            self.tabla_3.insertRow(iteracion)
            self.tabla_3.setItem(iteracion, 0, QtWidgets.QTableWidgetItem(str('R{0}'.format(self.qIzquierda.index(
                self.arreglo_tabla_0_1[iteracion][0])))))
            self.tabla_3.setItem(iteracion, 1, QtWidgets.QTableWidgetItem(str('R{0}'.format(self.qIzquierda.index(
                self.arreglo_tabla_0_1[iteracion][1])))))

        self.tabla_3.setVerticalHeaderLabels(self.encabezado_vertical_r)

        self.lb_resultados_qR.setText('Q´=') # Llenar los estados Q resultantes
        for iteracionR in range(len(self.encabezado_vertical_r)):
            self.lb_resultados_qR.setText('{0}{1}, '.format(self.lb_resultados_qR.text(), self.encabezado_vertical_r[iteracionR]))


    def obtenerResultadoF(self):
        self.lb_resultados_F.setText('F´=')  # Llenar los estados F resultantes
        listaF = self.generarConjuntosValores(self.campoF.text())

        for iteracion_qIzquierda in range(len(self.qIzquierda)): #Si los valores F se encuentra...
            if not listaF.isdisjoint(self.generarConjuntosValores(self.qIzquierda[iteracion_qIzquierda])):
                self.lb_resultados_F.setText('{0} R{1}, '.format(self.lb_resultados_F.text(),iteracion_qIzquierda))


    def retornarEstructuraOriginalQn(self, valor):
        valor = list(valor)
        valor.sort()
        estructura_original = ''

        for j in list(valor):
            estructura_original = estructura_original + 'q{},'.format(j)

        return estructura_original[:len(estructura_original) - 1]


    def retornarNumeroStr(self, texto):
        return texto.lower().translate({ord(j): None for j in ' q,'})


    def generarConjuntosValores(self, valor_normal):
        i = 0
        longitud_ln = len(valor_normal)
        conjuntos_limpios = set()
        while i < longitud_ln: #Generar conjuntos_limpios de valores de formato: ['q1','q2', ...]
            qActual = ''
            while i < longitud_ln and valor_normal[i] != ',':
                qActual = qActual + valor_normal[i]
                i = i + 1
            conjuntos_limpios.add(qActual)
            i = i + 1
        return conjuntos_limpios


    def limpiar_casillas_tablas(self):
        self.nQ.setEnabled(True)
        self.btnCargarTabla.setEnabled(True)
        self.btnCalcularCadena.setEnabled(True)
        self.btnLimpiar.setEnabled(False)
        self.nQ.setText(None)
        self.campoQ0.setText(None)
        self.campoF.setText(None)

        self.lb_resultados_qR.setText('Q´=')
        self.lb_resultados_F.setText('F´=')

        self.tabla_2.clear()
        self.tabla_2.setRowCount(0)
        self.tabla_3.clear()
        self.tabla_3.setRowCount(0)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ventana = MyApp()
    ventana.setWindowTitle('Universidad Autónoma de Tamaulipas - 2022')
    ventana.show()
    sys.exit(app.exec_())
