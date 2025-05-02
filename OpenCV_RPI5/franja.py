import cv2
import numpy as np

def nothing(x):
    pass

# Cargar imagen
imagen = cv2.imread('../Latas/azul1.png')  # Reemplaza con la ruta real
alto, ancho = imagen.shape[:2]

# Crear ventana con trackbars
cv2.namedWindow("Franja")
cv2.createTrackbar("Posición Y", "Franja", 0, alto - 1, nothing)
cv2.createTrackbar("Altura", "Franja", 50, alto, nothing)  # Altura inicial 50

while True:
    # Obtener valores de los trackbars
    y = cv2.getTrackbarPos("Posición Y", "Franja")
    h = cv2.getTrackbarPos("Altura", "Franja")

    # Asegurar que no se pase del borde inferior
    if y + h > alto:
        h = alto - y

    # Crear imagen negra
    salida = np.zeros_like(imagen)

    # Copiar solo la franja seleccionada
    salida[y:y+h, :] = imagen[y:y+h, :]

    # Mostrar resultado
    cv2.imshow("Franja", salida)

    # Salir con 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()