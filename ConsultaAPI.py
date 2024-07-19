import requests
from selenium.webdriver.common.by import By
from selenium import webdriver
from datetime import datetime

urlbase="https://ofertadecursos.uniandes.edu.co/api/courses?nameInput="

browser = webdriver.Firefox()
browser.get("https://sistemas.uniandes.edu.co/es/isis-activos/electivas/reguladas")
#browser.get("https://sistemas.uniandes.edu.co/es/isis-activos/electivas/profesionales")

elems = browser.find_elements(By.CLASS_NAME, "codigo")
materias = []
for i in range(len(elems)):
    actual = elems[i].text
    letras = actual[:4]
    nums = actual[5:9]
    materias.append(letras+nums)
    if letras+nums == "IQYA2042":
        break

print(materias)
browser.close()

encontradas = []

with open("Clases.csv", "w", encoding="utf-8") as archivo:
    archivo.write("Clase;CRN;Nombre;Campus;Cupos;% Cupos;Profe;Ciclo;Dias;Desde;Hasta\n")
    for i in range(len(materias)):
        clases = requests.get(urlbase + materias[i]).json()
        if len(clases) == 0:
            continue
        for j in range(len(clases)):
            escribible = ""
            escribir = True
            aEscribir=clases[j]
            if aEscribir["term"] != "202410":
                continue
            clase =materias[i]
            CRN = aEscribir["nrc"]
            nombre = aEscribir["title"]
            encontradas.append("{};{}".format(clase, nombre))
            ciclo = "-"
            if "(Ciclo " in nombre:
                strings = nombre.split("(Ciclo ")
                nombre = strings[0]
                ciclo = strings[1][0]
            campus = aEscribir["campus"]
            quedan = aEscribir["seatsavail"]
            inscr = aEscribir["maxenrol"]

            try:
                porc = ((int(quedan) / int(inscr))) * 100
            except:
                porc = 0
            try:
              profeSinOrdenar = aEscribir["instructors"][0]["name"].split(" ")
              if len(profeSinOrdenar) == 2:
                    profe = profeSinOrdenar[1] + " " + profeSinOrdenar[0]
              elif len(profeSinOrdenar) == 3:
                    profe = profeSinOrdenar[1] + " " + profeSinOrdenar[2] + " " + profeSinOrdenar[0]
              elif len(profeSinOrdenar) == 4:
                    profe = profeSinOrdenar[2] + " " + profeSinOrdenar[3] + " " + profeSinOrdenar[0] + " " + profeSinOrdenar[1]
            except:
                profe=""
            schedules = aEscribir["schedules"][0]
            desde = schedules["time_ini"]
            hasta = schedules["time_fin"]
            dias = ""
            if(schedules["l"] is not None):
                dias = dias + "l"
            if(schedules["m"] is not None):
                dias = dias + "m"
            if (schedules["i"] is not None):
                dias = dias + "i"
            if (schedules["j"] is not None):
                dias = dias + "j"
            if (schedules["v"] is not None):
                dias = dias + "v"
            if (schedules["s"] is not None):
                dias = dias + "s"
            escribible = "{};{};{};{};{};{};{};{};{};{};{}\n".format(clase, CRN, nombre, campus, quedan + "/" + inscr, str(porc)+"%", profe, ciclo, dias, desde, hasta)
            if len(aEscribir["schedules"]) != 1:
                for k in range(len(aEscribir["schedules"])):
                    if k == 0:
                        continue
                    schedules =aEscribir["schedules"][k]
                    desde = schedules["time_ini"]
                    hasta = schedules["time_fin"]
                    dias = ""
                    if (schedules["l"] is not None):
                        dias = dias + "l"
                    if (schedules["m"] is not None):
                        dias = dias + "m"
                    if (schedules["i"] is not None):
                        dias = dias + "i"
                    if (schedules["j"] is not None):
                        dias = dias + "j"
                    if (schedules["v"] is not None):
                        dias = dias + "v"
                    if (schedules["s"] is not None):
                        dias = dias + "s"
                    numeroHorario = "Clase " + CRN + " - Horario #" + str(k)
                    escribible = escribible + "-;-;{};-;-;-;-;-;{};{};{}\n".format(numeroHorario, dias, desde, hasta)
            if escribir:
                print(escribible)
                archivo.write(escribible)
with open("materias.csv", "w", encoding="utf-8") as archivo:
    written_names = set()
    for i in range(len(encontradas)):
        name = encontradas[i]
        if name not in written_names:
            archivo.write(name + "\n")
            written_names.add(name)


