import cv2
import cv2 as cv
import imutils

def buscar_mar(captura):
    

    return (cx, cy)

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
    cv2.imshow('Objetos detectados', image)
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

capture =  cv.VideoCapture(1, cv.CAP_DSHOW)

while True:
    isTrue, original = capture.read()
    #cv.imshow('vid', frame)
    frame = original.copy()

    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    cv.imshow('gray', gray)
    threshold, mask = cv.threshold(gray, 15, 100, cv.THRESH_BINARY_INV)
    cv.imshow('thresh', mask)
    #th, thresh_inv = cv.threshold(gray, 100, 255, cv.THRESH_BINARY_INV)
    #cv.imshow('thresh_inv', thresh_inv)
    latas = buscar_latas(frame, mask)
    coordenadas = objeto_mas_grande(latas)
    print(coordenadas)
    cv.circle(frame, coordenadas, 40, (182, 252, 235), thickness=6)
    cv.imshow('circ', frame)
    if cv.waitKey(20) & 0xFF==ord('d'):
        break
capture.release()
cv.destroyAllWindows()



