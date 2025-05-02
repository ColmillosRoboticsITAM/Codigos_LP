# import cv2
# import numpy as np
#
# def nothing(x):
#     pass
#
# # Crear ventana para trackbars
# cv2.namedWindow("Calibración HSV")
# cv2.createTrackbar("H min", "Calibración HSV", 100, 179, nothing)
# cv2.createTrackbar("H max", "Calibración HSV", 140, 179, nothing)
# cv2.createTrackbar("S min", "Calibración HSV", 100, 255, nothing)
# cv2.createTrackbar("S max", "Calibración HSV", 255, 255, nothing)
# cv2.createTrackbar("V min", "Calibración HSV", 50, 255, nothing)
# cv2.createTrackbar("V max", "Calibración HSV", 255, 255, nothing)
#
# # Cargar imagen
# imagen = cv2.imread('../Latas/azul1.png')  # Cambia la ruta según tu estructura
#
# while True:
#     # Convertir a HSV
#     hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)
#
#     # Leer valores de las trackbars
#     h_min = cv2.getTrackbarPos("H min", "Calibración HSV")
#     h_max = cv2.getTrackbarPos("H max", "Calibración HSV")
#     s_min = cv2.getTrackbarPos("S min", "Calibración HSV")
#     s_max = cv2.getTrackbarPos("S max", "Calibración HSV")
#     v_min = cv2.getTrackbarPos("V min", "Calibración HSV")
#     v_max = cv2.getTrackbarPos("V max", "Calibración HSV")
#
#     # Crear la máscara
#     lower_blue = np.array([h_min, s_min, v_min])
#     upper_blue = np.array([h_max, s_max, v_max])
#     mascara = cv2.inRange(hsv, lower_blue, upper_blue)
#
#     # Mostrar imagen y máscara
#     cv2.imshow("Imagen Original", imagen)
#     cv2.imshow("Mascara Azul", mascara)
#
#     key = cv2.waitKey(1)
#     if key == 27:  # ESC para salir
#         break
#
# cv2.destroyAllWindows()