import cv2
import cv2 as cv
import math
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

def objeto_mas_grande(objetos, image):
    ang = 0
    if not objetos:
        return (0, 0), 540
    # Encontrar el objeto con el área máxima
    objeto_max = max(objetos, key=lambda o: o['area'])

    # Obtener centroide
    cx, cy = objeto_max['x'], objeto_max['y']
    if cx == 0 and cy == 0:
        ang = 540
    else:
        h, w = image.shape[:2]
        max_x = w // 2
        # Coordenadas del centro de la imagen
        c_x = w // 2
        c_y = h // 2

        # Vector desde el centro al punto
        dx = cx - c_x
        dy = cy - c_y

        # Ángulo en radianes y grados
        ang = dx * (-120 / max_x)
    return (cx, cy), ang

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
    objetos = []
    cx, cy = 0, 0
    ang = 0
    for i, cnt in enumerate(contours):
        area = cv2.contourArea(cnt)
        if area > 300:
            M = cv2.moments(cnt)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
            else:
                cx, cy = 0, 0
            objetos.append({'area': area, 'x': cx, 'y': cy, 'ctrs': cnt})
            cv2.drawContours(captura_mar, [cnt], -1, (0, 255, 0), 2)
            # Dibujar centroide
            cv2.circle(captura_mar, (cx, cy), 4, (0, 0, 255), -1)
            #Salida de datos
            flag_contenedor = np.sum(mascara_suave == 255)>300
    if not objetos:
        return mascara_suave, False, (0, 0), 540
    # Encontrar el objeto con el área máxima
    objeto_max = max(objetos, key=lambda o: o['area'])
    # Obtener centroide
    cx, cy = objeto_max['x'], objeto_max['y']
    if cx == 0 and cy == 0:
        ang = 540
    else:
        h, w = captura_mar.shape[:2]
        max_x = w // 2
        # Coordenadas del centro de la imagen
        c_x = w // 2
        c_y = h // 2

        # Vector desde el centro al punto
        dx = cx - c_x
        dy = cy - c_y

        # Ángulo en radianes y grados
        ang = dx * (-120/max_x)
    return mascara_suave, flag_contenedor, (cx, cy), ang

def llegando_a(m_latas, m_cont):
    bandera_lata, bandera_cont = False, False
    alto, ancho = m_latas.shape
    w = ancho//4
    h = alto//3
    blank = np.zeros((alto, ancho), dtype='uint8')
    blank = cv.rectangle(blank, ((ancho//2)-w, alto - h), ((ancho//2)+w, alto), 255, -1)
    salida1 = cv.bitwise_and(blank, m_latas)
    salida2 = cv.bitwise_and(blank, m_cont)
    #cv2.imshow("blank_m", blank)
    #cv2.imshow("blank1", salida1)
    #cv2.imshow("blank2", salida2)

    bandera_lata = np.sum(salida1 > 0) >300
    bandera_cont = np.sum(salida2 > 0) > 300
    return bandera_lata, bandera_cont

capture =  cv.VideoCapture(0, cv.CAP_DSHOW)

while True:
    isTrue, original = capture.read()
    #cv.imshow('vid', frame)
    frame = original.copy()
    frame_mar = original.copy()
    frame_contenedor = original.copy()

    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    #cv.imshow('gray', gray)
    threshold, mask = cv.threshold(gray, 15, 100, cv.THRESH_BINARY_INV)
    cv.imshow('thresh', mask)

    flag_mar = buscar_mar(frame_mar)

    latas = buscar_latas(frame, mask)

    mask_Cont, hayCont, coords_Cont, ang_Cont = encontrar_contenedor(frame_contenedor)

    coordenadas, ang_lata = objeto_mas_grande(latas, mask)
    flag_lata, flag_cont = llegando_a(mask, mask_Cont)
 #flag_lata y flag_cont son para reconocer si a mbos onjetos estan lo suficientemente cerca del tobot
    #print(ang_lata,flag_lata, flag_mar, hayCont, ang_Cont, flag_cont)
    print(ang_lata,int(flag_lata), int(flag_mar), int(hayCont), ang_Cont, int(flag_cont))

    cv.circle(frame, coordenadas, 40, (182, 252, 235), thickness=6)
    cv.imshow('circ', frame)
    cv.imshow('contenedor', frame_contenedor)
    if cv.waitKey(20) & 0xFF==ord('d'):
        break
capture.release()
cv.destroyAllWindows()



