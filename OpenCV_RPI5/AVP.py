import cv2
import cv2 as cv
import numpy as np
#Algoritmo de vision principal

def buscar_mar(captura):
    hsv = cv2.cvtColor(captura, cv2.COLOR_BGR2HSV)
    h_min = 96
    h_max = 113
    s_min = 137
    s_max = 255
    v_min = 0
    v_max = 255
    # Crear máscara
    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])
    mascara = cv2.inRange(hsv, lower, upper)
    # Mostrar resultados
    resultado = cv2.bitwise_and(captura, captura, mask=mascara)

    #cv2.imshow("Imagen Original", captura)
    #cv2.imshow("Mascara", mascara)
    cv2.imshow("Resultado", resultado)

    alto, ancho, _ = captura.shape
    y = 250
    h = 150
    blank = np.zeros((alto, ancho), dtype='uint8')
    blank = cv.rectangle(blank, (0, alto-y), (ancho, alto-y+h), 255, -1)
    salida = cv.bitwise_and(blank, mascara)
    #crop_im = cv2.bitwise_and(captura, captura, mask=salida)
    cv2.imshow("blank", salida)

    Cant_mar = np.sum(salida == 255)
    return (Cant_mar>300)

def buscar_latas (image, maskedImage):
    contours, _ = cv2.findContours(maskedImage, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    objetos = []
    # Dibujar contornos y centroides
    for i, cnt in enumerate(contours):
        area = cv2.contourArea(cnt)
        if area > 2000:
            M = cv2.moments(cnt)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
            else:
                cx, cy = 0, 0
            objetos.append({'area': area, 'x': cx, 'y': cy, 'ctrs': cnt})
            # Dibujar contorno
            cv2.drawContours(image, [cnt], -1, (0, 255, 0), 2)
            # Dibujar centroide
            cv2.circle(image, (cx, cy), 4, (0, 0, 255), -1)
            # Escribir texto con área
            texto = f"{int(area)}"
            cv2.putText(image, texto, (cx + 10, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)

    # Mostrar imagen
    #cv2.imshow('Objetos detectados', image)
    lista = ""
    for i, obj in enumerate(objetos):
        lista += (f"{i + 1}: Á-{obj['area']:.2f}, P-({obj['x']}, {obj['y']}) \t")
    #print(lista)

    return (objetos)

def objeto_mas_grande(objetos):
    if not objetos:
        return None, None

    # Encontrar el objeto con el área máxima
    objeto_max = max(objetos, key=lambda o: o['area'])

    # Obtener centroide
    cx, cy = objeto_max['x'], objeto_max['y']

    return (cx, cy)

def encontrar_contenedor(captura_mar):
    rgb = cv2.cvtColor(captura_mar, cv2.COLOR_BGR2RGB)
    hsv = cv2.cvtColor(rgb, cv2.COLOR_BGR2HSV)
    # Crear máscara
    lower = np.array([84, 0, 9])
    upper = np.array([160, 35, 45])
    mascara1 = cv2.inRange(rgb, lower, upper)
    kernel = np.ones((5, 5), np.uint8)
    mascara_suave = cv2.morphologyEx(mascara1, cv2.MORPH_CLOSE, kernel)
    cv2.imshow("Mascara", mascara_suave)
    contours, _ = cv2.findContours(mascara_suave, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # Dibujar contornos y centroides
    flag_contenedor = False
    cx, cy = 0, 0
    for i, cnt in enumerate(contours):
        area = cv2.contourArea(cnt)
        if area > 300:
            M = cv2.moments(cnt)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
            else:
                cx, cy = 0, 0
            cv2.drawContours(captura_mar, [cnt], -1, (0, 255, 0), 2)
            # Dibujar centroide
            cv2.circle(captura_mar, (cx, cy), 4, (0, 0, 255), -1)
            #Salida de datos
            flag_contenedor = np.sum(mascara_suave == 255)>300

    return flag_contenedor, (cx, cy)

capture =  cv.VideoCapture(1, cv.CAP_DSHOW)

while True:
    isTrue, original = capture.read()
    #cv.imshow('vid', frame)
    frame = original.copy()
    frame_mar = original.copy()
    frame_contenedor = original.copy()

    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    #cv.imshow('gray', gray)
    threshold, 6
    mask = cv.threshold(gray, 70, 100, cv.THRESH_BINARY_INV)
    cv.imshow('thresh', mask)

    flag = buscar_mar(frame_mar)

    latas = buscar_latas(frame, mask)

    hayContenedor, coords_Contenedor = encontrar_contenedor(frame_contenedor)


    coordenadas = objeto_mas_grande(latas)
    print(coordenadas, flag, hayContenedor, coords_Contenedor)
    cv.circle(frame, coordenadas, 40, (182, 252, 235), thickness=6)
    cv.imshow('circ', frame)
    cv.imshow('contenedor', frame_contenedor)
    if cv.waitKey(20) & 0xFF==ord('d'):
        break
capture.release()
cv.destroyAllWindows()



