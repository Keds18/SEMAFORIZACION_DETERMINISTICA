import matplotlib.pyplot as plt
import streamlit as st  # Importar Streamlit para mostrar las figuras

# Diagrama de fases vehiculares
def graficar_fases(C, v1_real, v2_real, tiempo_ambar, tiempo_todo_rojo):
    V_EO = int(v1_real)
    V_NS = int(v2_real)
    R_EO = C - V_EO - tiempo_ambar - tiempo_todo_rojo
    R_NS = C - V_NS - tiempo_ambar - tiempo_todo_rojo
    TR = tiempo_todo_rojo

    fig, ax = plt.subplots(figsize=(10, 3))
    SGI = [V_EO, tiempo_ambar, TR, R_EO]
    SGI_colors = ['green', 'yellow', '#DC143C', 'red']
    SG2 = [R_NS, V_NS, tiempo_ambar, TR]
    SG2_colors = ['red', 'green', 'yellow', '#DC143C']

    start = 0
    for i, seg in enumerate(SGI):
        ax.barh('SG I E-O', seg, left=start, color=SGI_colors[i], edgecolor='black')
        ax.text(start + seg/2, 0, f'{int(seg)}s', va='center', ha='center',
                color='white' if SGI_colors[i] != 'yellow' else 'black', fontsize=8)
        start += seg

    start = 0
    for i, seg in enumerate(SG2):
        ax.barh('SG II N-S', seg, left=start, color=SG2_colors[i], edgecolor='black')
        ax.text(start + seg/2, 1, f'{int(seg)}s', va='center', ha='center',
                color='white' if SG2_colors[i] != 'yellow' else 'black', fontsize=8)
        start += seg

    ax.legend(['Verde', 'Ámbar', 'Todo rojo', 'Rojo'], loc='upper right', bbox_to_anchor=(1.18, 1),
              fontsize=9, frameon=False)
    ax.set_xlim(0, C)
    ax.set_xlabel('Ciclo semafórico (s)')
    ax.set_ylabel('Fases semafóricas')
    ax.set_title('DIAGRAMA DE FASES VEHICULARES', fontsize=14, fontweight='bold')
    ax.set_xticks(range(0, C + 1, max(2, C // 20)))  # Mejor escala adaptable
    ax.grid(axis='x', linestyle='--', alpha=0.2)
    plt.tight_layout()

    return fig  # Se retorna la figura

# Diagrama de fases peatonales
def graficar_fases_peatonal(verde_fase_I_real, verde_fase_II_real, R_EO_nuevo, R_NS_nuevo, tiempo_ambar, tiempo_todo_rojo, C_nuevo):
    V_EO_p = R_EO_nuevo
    V_NS_p = R_NS_nuevo
    R_EO_p = verde_fase_I_real + tiempo_ambar + tiempo_todo_rojo
    R_NS_p = verde_fase_II_real + tiempo_ambar + tiempo_todo_rojo

    fig, ax = plt.subplots(figsize=(12, 3.5))
    SGI_p = [R_EO_p, V_EO_p]
    SGI_colors_p = ['red', 'green']
    SG2_p = [V_NS_p, R_NS_p]
    SG2_colors_p = ['green', 'red']

    ax.barh('SG I E-O (peatonal)', SGI_p[0], color=SGI_colors_p[0], edgecolor='black')
    ax.barh('SG I E-O (peatonal)', SGI_p[1], left=SGI_p[0], color=SGI_colors_p[1], edgecolor='black')
    ax.barh('SG II N-S (peatonal)', SG2_p[0], color=SG2_colors_p[0], edgecolor='black')
    ax.barh('SG II N-S (peatonal)', SG2_p[1], left=SG2_p[0], color=SG2_colors_p[1], edgecolor='black')

    ax.text(R_EO_p / 2, 0, f'{R_EO_p}s', va='center', ha='center', color='white', fontsize=8)
    ax.text(R_EO_p + V_EO_p / 2, 0, f'{V_EO_p}s', va='center', ha='center', color='white', fontsize=8)
    ax.text(V_NS_p / 2, 1, f'{V_NS_p}s', va='center', ha='center', color='white', fontsize=8)
    ax.text(V_NS_p + R_NS_p / 2, 1, f'{R_NS_p}s', va='center', ha='center', color='white', fontsize=8)

    ax.set_xlim(0, C_nuevo)
    ax.set_xticks(range(0, C_nuevo + 1, max(2, C_nuevo // 20)))
    ax.set_xlabel('Ciclo semafórico (s)', fontsize=12)
    ax.set_ylabel('Fases semafóricas', fontsize=12)
    ax.set_title('DIAGRAMA DE FASES PEATONALES', fontsize=14, fontweight='bold')
    ax.set_yticks([0, 1])
    ax.set_yticklabels(['SG I E-O (peatonal)', 'SG II N-S (peatonal)'])
    ax.grid(axis='x', linestyle='--', alpha=0.2)
    ax.legend(['Rojo', 'Verde'], loc='upper right', bbox_to_anchor=(1.13, 1), fontsize=10, frameon=False)
    plt.tight_layout()

    return fig  # Se retorna la figura
