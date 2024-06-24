"""
MyDataLab library
Data Science - Universidad Nacional del Litoral
"""


import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import statsmodels.api as sm
import pandas as pd

class ResumenNumerico:
    def __init__(self, datos):
        self.datos = np.array(datos)

    def calculo_de_media(self):
        self.media = np.mean(self.datos)
        return self.media

    def calculo_de_mediana(self):
        mediana = np.mean(self.datos)
        return mediana
    def calculo_de_desvio_estandar(self):
        desvio = np.std(self.datos)

        return desvio

    def calculo_de_cuartiles(self):
        q1 = np.percentile(self.datos, 25)
        q2 = np.percentile(self.datos, 50)
        q3 = np.percentile(self.datos, 75)

        return [q1, q2, q3]

    def generacion_resumen_numerico(self):
        res_num = {
        'Media': self.calculo_de_media(),
        'Mediana': self.calculo_de_mediana(),
        'Desvio': self.calculo_de_desvio_estandar(),
        'Cuartiles': self.calculo_de_cuartiles(),
        'Mínimo': min(self.datos),
        'Máximo': max(self.datos)
        }

        return res_num

    def muestra_resumen(self):
      for estad, valor in res_num.items():
        print(f"{estad}: {np.round(valor,3)}")


class ResumenGrafico:
    def __init__(self, datos):
        self.datos = np.array(datos)

    def generacion_histograma(self, h):
        minimo = np.min(self.datos)
        maximo = np.max(self.datos)
        n = len(self.datos)

        bins = np.arange(minimo, maximo, h)
        if maximo > bins[-1]:
            bins = np.append(bins, bins[-1] + h)
        frec = np.zeros((len(bins)-1,))

        for ing in self.datos:
            for i in range(len(bins)-1):
                if ing > bins[i] and ing <= bins[i+1]:
                    frec[i] += 1
                    break

        frec /= (n*h)

        return bins, frec

    def evaluacion_histograma(self, h, x):
        bins, frec = self.generacion_histograma(h)
        restx = np.zeros((len(x),))

        for val in range(len(x)):
            for i in range(len(bins)-1):
                if x[val] > bins[i] and x[val] <= bins[i+1]:
                    restx[val] = frec[i]
                    break
        return restx

    def kernel_gaussiano(self, x):
        # Kernel gaussiano estándar
        valor_kernel_gaussiano = (1/(np.sqrt(2*np.pi)))*np.exp(-0.5*x**2)
        ## Completar
        return valor_kernel_gaussiano

    def kernel_uniforme(self, x):
        # Kernel uniforme
        if np.abs(x) <= 1:
            valor_kernel_uniforme = 0.5
        else:
            valor_kernel_uniforme = 0

        return valor_kernel_uniforme

    def kernel_cuadratico(self, x):
      valor_kernel_cuadratico = 3/4 * (1-x**2) if np.abs(x) <= 1 else 0
      return valor_kernel_cuadratico

    def kernel_triangular (self,x):
      if -1<x<0:
        valor_kernel_triangular = 1+x
      elif 0<x<1:
        valor_kernel_triangular = 1-x
      else:
        valor_kernel_triangular = 0
      return valor_kernel_triangular


    def mi_densidad(self, x, data, h, kernel):
        # x: Puntos en los que se evaluará la densidad
        # data: Datos
        # h: Ancho de la ventana (bandwidth)
        densidad = np.zeros(len(x))

        for i in range(len(x)):
            for j in range(len(data)):
                u = (x[i] - data[j]) / h  # Normalización de la distancia
                if kernel == "gaussiano":
                    densidad[i] += self.kernel_gaussiano(u)
                elif kernel == "uniforme":
                    densidad[i] += self.kernel_uniforme(u)
                elif kernel == "cuadratico":
                    densidad[i] += self.kernel_cuadratico(u)
                elif kernel == "triangular":
                    densidad[i] += self.kernel_triangular(u)

            densidad[i] /= (len(data) * h)

        return densidad

    def miqqplot(self):

      media = np.mean(self.datos)
      desvio = np.std(self.datos)

      x_ord = np.sort(self.datos)
      x_ord_s = (x_ord - media) / desvio
      n = len(self.datos)

      cuantiles_teoricos = []

      for p in range(1,n+1):
        pp = p/(n+1) #convierte lista en decimales
        valor_cuantil = norm.ppf(pp)
        cuantiles_teoricos.append(valor_cuantil)


      plt.scatter(cuantiles_teoricos, x_ord_s, color='blue', marker='o')
      plt.xlabel('Cuantiles teóricos')
      plt.ylabel('Cuantiles muestrales')
      plt.plot(cuantiles_teoricos, cuantiles_teoricos, linestyle='-', color='red')
      plt.show()


class GeneradoraDeDatos:
    def __init__(self, n):
        self.n = n

    def generar_datos_dist_norm(self, media, desvio):
        datos = np.random.normal(loc=media, scale=desvio, size=self.n)
        return datos

    def pdf_norm(self, x, media, desvio):
        distribucion = 1 / (desvio * np.sqrt(2 * np.pi)) * np.exp(-(x - media)**2 / (2 * desvio**2))
        return distribucion

    def generar_datos_dist_BS(self):
        u = np.random.uniform(size=(self.n,))
        y = u.copy()
        ind = np.where(u > 0.5)[0]
        y[ind] = np.random.normal(0, 1, size=len(ind))
        for j in range(5):
            ind = np.where((u > j * 0.1) & (u <= (j+1) * 0.1))[0]
            y[ind] = np.random.normal(j/2 - 1, 1/10, size=len(ind))
        return y

    def f_bs(x):
        phi = norm.pdf
        return 0.5 * phi(x, 0, 1) + 0.1 * sum([phi(x, j/2 - 1, 1/10) for j in range(5)])

    def generar_datos_uniforme(self, min, max):
        datos = np.random.uniform(min, max, self.n)
        return datos


class Regresion:
    """
    Clase que ajusta el modelo lineal (simple o multiple) o el modelo logístico.
    Atributos:
        x (np.ndarray): Variable/s predictora/s.
        y (np.ndarray): Variable que se intenta explicar.
    """
    def __init__(self, x, y):
        """
        Inicializa una instancia de la clase Regresion.
        Args:
            x (np.ndarray): Matriz de características.
            y (np.ndarray): Vector de valores objetivo.
        """
        self.x = x
        self.y = y

    def ajustar_modelo_lineal(self):
        """
        Ajusta el modelo de regresión lineal usando la librería statsmodels.
        
        Returns:
            result: El resultado del ajuste del modelo.
        """
        X = sm.add_constant(self.x)
        model = sm.OLS(self.y, X)
        result = model.fit()
        return result

    def ajustar_modelo_logistico(self):
        """
        Ajusta el modelo de regresión logistica usando la librería statsmodels.

        Returns:
            result: El resultado del ajuste del modelo.
        """
        X = sm.add_constant(self.x)
        model = sm.Logit(self.y, X)
        result = model.fit()
        return result


class RegresionLinealSimple(Regresion):
    """
    Clase que predice la variable respuesta a partir de un nuevo valor de la variable explicativa 
    mediante el modelo lineal ajustado con la clase Regresion. También grafica la recta ajustada.
    Atributos:
        x (np.ndarray): Variable predictora.
        y (np.ndarray): Variable que se intenta explicar.
    """
    def __init__(self, x, y):
        """
        Inicializa una instancia de la clase RegresionLinealSimple.
        Args:
            x (np.ndarray): Variable predictora.
            y (np.ndarray): Variable que se intenta explicar.
        """
        super().__init__(x, y)

    def predecir(self, new_x):
        """
        Predice el valor de la variable respuesta ante un nuevo valor de la variable explicativa (new_x) 
        mediante el modelo de regresión lineal simple usando la librería statsmodels.
        
        Args:
            new_x (np.ndarray): Nuevo valor de la variable predictora.
            
        Returns:
            np.ndarray: Predicciones del modelo.
        
        Ejemplo:
            >>> x = np.array([[3], [5], [6]])
            >>> y = np.array([2, 4, 6])
            >>> model = RegresionLinealSimple(x, y)
            >>> model.predecir(np.array([[7]]))
        """
        miRLS = self.ajustar_modelo_lineal()
        X_new = sm.add_constant(new_x)
        return miRLS.predict(X_new)

    def graficar_recta_ajustada(self):
        """
        Grafica la recta ajustada mediante el modelo de regresión lineal simple junto con el diagrama de dispersión.
        """
        res = self.ajustar_modelo_lineal()
        plt.scatter(self.x, self.y, color='blue', label='Datos')
        plt.plot(self.x, res.predict(sm.add_constant(self.x)), color='red', label='Recta Ajustada')
        plt.xlabel('Variable Predictora')
        plt.ylabel('Variable Respuesta')
        plt.legend()
        plt.show()


class RegresionLinealMultiple(Regresion):
    """
    Clase que predice la variable respuesta a partir de un nuevo valor de la variable explicativa mediante el modelo lineal ajustado 
    con la clase Regresion.
    Atributos:
        x (np.ndarray): Variables predictoras.
        y (np.ndarray): Variable que se intenta explicar.
    """
    def __init__(self, x, y):
        """
        Inicializa una instancia de la clase RegresionLinealMultiple.
        Args:
            x (np.ndarray): Variables predictoras.
            y (np.ndarray): Variable que se intenta explicar.
        """
        super().__init__(x, y)

    def predecir(self, new_x):
        """
        Predice el valor de la variable respuesta ante un nuevo vector de las variables explicativas (new_x) 
        mediante el modelo de regresión lineal multiple usando la librería statsmodels.
        
        Args:
            new_x (np.ndarray): Nuevo valor de las variables predictoras.
            
        Returns:
            np.ndarray: Predicciones del modelo.
        
        Ejemplo:
            >>> x = np.array([[3, 2], [5, 4], [6, 5]])
            >>> y = np.array([2, 4, 6])
            >>> model = RegresionLinealMultiple(x, y)
            >>> model.predecir(np.array([[7, 6]]))
        """
        miRLM = self.ajustar_modelo_lineal()
        X_new = sm.add_constant(new_x)
        return miRLM.predict(X_new)


class RegresionLogistica(Regresion):
    """
    Clase que predice la variable respuesta a partir de un nuevo valor de la variable explicativa mediante el modelo logístico ajustado 
    con la clase Regresion.
    Atributos:
        x (np.ndarray): Variables predictoras.
        y (np.ndarray): Variable que se intenta explicar.
    """
    def __init__(self, x, y):
        """
        Inicializa una instancia de la clase RegresionLogistica.
        Args:
            x (np.ndarray): Variables predictoras.
            y (np.ndarray): Variable que se intenta explicar.
        """
        super().__init__(x, y)

    def predecir(self, new_x):
        """
        Predice el valor de la variable respuesta ante un nuevo vector de las variables explicativas (new_x) 
        mediante el modelo logístico usando la librería statsmodels.
        
        Args:
            new_x (np.ndarray): Nuevo valor de las variables predictoras.
            
        Returns:
            np.ndarray: Predicciones del modelo.
        
        Ejemplo:
            >>> x = np.array([[3, 2], [5, 4], [6, 5]])
            >>> y = np.array([0, 1, 1])
            >>> model = RegresionLogistica(x, y)
            >>> model.predecir(np.array([[7, 6]]))
        """
        miRLog = self.ajustar_modelo_logistico()
        X_new = sm.add_constant(new_x)
        return miRLog.predict(X_new)

   
  
class Cualitativas:
    def __init__(self, observados, probabilidades):
        """
        Test de bondad de ajuste mediante Método de Chi Cuadrado
        Entradas: observados = datos muestrales
                  probabilidades teóricas bajo la hipótesis nula
        """
        self.observados = observados
        self.p = probabilidades
        self.n = sum(observados)  # Sumar los observados para calcular los esperados

        # Verificar que las probabilidades sumen 1
        if not np.isclose(sum(self.p), 1):
            raise ValueError("Las probabilidades deben ser una lista de números que sumen 1.")

        # Verificar que las longitudes de observados y probabilidades sean iguales
        if len(self.p) != len(self.observados):
            raise ValueError("Probabilidades y observados deben tener igual tamaño.")

        # Calcular los esperados
        self.esperados = [self.n * p for p in probabilidades]

    def chi_cuadrado(self):
        """
        Calcula el estadístico Chi Cuadrado
        """
        self.estadistico = np.sum((np.array(self.observados) - np.array(self.esperados)) ** 2 / np.array(self.esperados))
        return self.estadistico

    def percentil(self, alpha):
        """
        Calcula el valor crítico del estadístico (el cual no debe superar)
        En la entrada se debe agregar como parámetro el alfa correspondiente.
        """
        self.df = len(self.observados) - 1  # grados de libertad
        percentil_chi2 = chi2.ppf(q=1 - alpha, df=self.df)
        return percentil_chi2

    def p_valor(self):
        """
        Calcula el p_valor correspondiente con significancia 1-alfa del test de hipótesis
        H_0 = La distribución de los datos sigue la probabilidad teórica
        H_1 = La distribución de los datos NO sigue la probabilidad teórica
        """
        p_valor = 1 - chi2.cdf(self.estadistico, self.df)
        return p_valor
