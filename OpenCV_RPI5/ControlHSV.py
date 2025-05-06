import cv2
import numpy as np

def nothing(x):
    pass

# Cargar imagen
frame = cv2.imread('../Latas/azul1.png')  # Cambia la ruta
fr = cv2.GaussianBlur(frame, (3, 5), 0)
imagen = cv2.resize(fr, (720,480), interpolation=cv2.INTER_LINEAR)

# Crear ventana para controles
cv2.namedWindow("Controles")

# Crear trackbars para el rango HSV
cv2.createTrackbar("H Min", "Controles", 100, 179, nothing)
cv2.createTrackbar("H Max", "Controles", 140, 179, nothing)
cv2.createTrackbar("S Min", "Controles", 150, 255, nothing)
cv2.createTrackbar("S Max", "Controles", 255, 255, nothing)
cv2.createTrackbar("V Min", "Controles", 50, 255, nothing)
cv2.createTrackbar("V Max", "Controles", 255, 255, nothing)

while True:
    # Obtener valores de los sliders
    h_min = cv2.getTrackbarPos("H Min", "Controles")
    h_max = cv2.getTrackbarPos("H Max", "Controles")
    s_min = cv2.getTrackbarPos("S Min", "Controles")
    s_max = cv2.getTrackbarPos("S Max", "Controles")
    v_min = cv2.getTrackbarPos("V Min", "Controles")
    v_max = cv2.getTrackbarPos("V Max", "Controles")

    # Convertir a HSV
    hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)

    # Crear máscara
    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])
    mascara = cv2.inRange(hsv, lower, upper)

    # Mostrar resultados
    resultado = cv2.bitwise_and(imagen, imagen, mask=mascara)

    cv2.imshow("Imagen Original", imagen)
    cv2.imshow("Mascara", mascara)
    cv2.imshow("Resultado", resultado)

    # Salir con tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()

