import math

# Calculo de cargas criticas
def calcular_cargas(q, S):
    ye = {k: q[k] / S[k] for k in q}
    yp_1 = max(ye['este'], ye['oeste'])
    yp_2 = max(ye['norte'], ye['sur'])
    Y = yp_1 + yp_2
    return ye, yp_1, yp_2, Y

# Tiempo total perdico por ciclo(T)
def calcular_tiempo_total_perdido(num_fases, tiempo_todo_rojo, tiempo_perdido_por_fase):
    T = num_fases * (tiempo_todo_rojo + tiempo_perdido_por_fase)
    return T

#Ciclo semaforico segun el metodo de Webster
def calcular_ciclo_webster(T, Y):
    if Y >= 1:
        raise ValueError("La carga total Y excede 1. No se puede aplicar el método de Webster.")
    Co = (1.5 * T + 5) / (1 - Y)
    return math.ceil(Co / 5) * 5

# Verde disponible por fase
def calcular_verdes(C, T, yp_1, yp_2, Y):
    v_total = C - T
    v1 = round(v_total * (yp_1 / Y), 0)
    v2 = round(v_total * (yp_2 / Y), 0)
    if v1 + v2 != v_total:
        raise ValueError("El tiempo verde no coincide con el tiempo disponible.")
    return v_total, v1, v2

# Tiempo verde real
def calcular_verde_real(v1, v2, tiempo_perdido_por_fase, tiempo_ambar):
    v1_real = v1 + tiempo_perdido_por_fase - tiempo_ambar
    v2_real = v2 + tiempo_perdido_por_fase - tiempo_ambar
    return v1_real, v2_real

#VERIFICACION PEATONAL
def verificar_tiempo_rojo(nombre_fase, rojo_fase, tiempo_cruce):
    if rojo_fase > tiempo_cruce:
        return f"Fase {nombre_fase}: Rojo = {rojo_fase}s → ✅"
    else:
        return (f"Fase {nombre_fase}: Rojo = {rojo_fase}s → ❌\n"
                f"El tiempo de rojo de la fase {nombre_fase} no es suficiente para el cruce peatonal.")

# Si no cumple debemos ampliar la fase de rojo vehicular y que sea igual al verde peatonal
def ajustar_tiempos(tiempo_cruce, TR, tiempo_perdido_por_fase, yp_1, yp_2, tiempo_ambar, T):
    rojo_I_fase_nuevo = math.ceil(tiempo_cruce)
    verde_fase_II_nuevo = rojo_I_fase_nuevo - (TR * 2) - tiempo_perdido_por_fase
    verde_fase_I_nuevo = math.ceil((verde_fase_II_nuevo / yp_2) * yp_1)
    C_nuevo = verde_fase_I_nuevo + verde_fase_II_nuevo + T
    verde_fase_I_real = verde_fase_I_nuevo + tiempo_perdido_por_fase - tiempo_ambar
    verde_fase_II_real = verde_fase_II_nuevo + tiempo_perdido_por_fase - tiempo_ambar
    return rojo_I_fase_nuevo, verde_fase_II_nuevo, verde_fase_I_nuevo, C_nuevo, verde_fase_I_real, verde_fase_II_real
