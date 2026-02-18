#!/usr/bin/env python3
"""
Generador de datos financieros para el modelo de permanencia de Paulina en Madrid.
Genera: datos_paulina.json y escenarios_paulina.json
"""

import json
from datetime import datetime
from pathlib import Path

# ============================================================
# CONFIGURACION BASE
# ============================================================

OUTPUT_DIR = Path(__file__).parent.parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

# ============================================================
# DATOS BASE - PARAMETRIZADOS (Fuente: Guia IE Madrid)
# ============================================================

PERFIL = {
    "nombre": "Paulina",
    "edad": 19,
    "menor_26": True,
    "universidad": "IE University",
    "programa": "Grado 4 anos",
    "ciudad": "Madrid",
    "pais_origen": "Colombia",
    "ano_inicio": 2026,
    "duracion_anos": 4
}

SUPUESTOS = {
    "inflacion_espana": 0.03,
    "descuento_matricula_disponible": 0.40,
    "meses_por_ano": 12,
    "tasas_cambio": {
        "EUR_USD": 1.08,
        "EUR_COP": 4500
    }
}

# Rangos de costos mensuales (min, medio, max) - Fuente: Guia IE Madrid
COSTOS_BASE = {
    "matricula": {
        "descripcion": "Matricula anual IE University",
        "anual_base": 29000,
        "tipo": "anual",
        "fijo": True
    },
    "vivienda": {
        "descripcion": "Apartamento 2 habitaciones compartido (parte de Paulina)",
        "min": 600,
        "medio": 1000,
        "max": 1100,
        "tipo": "mensual",
        "compartido": True,
        "total_apartamento": 2000
    },
    "electricidad": {
        "descripcion": "Electricidad (parte de Paulina)",
        "min": 35,
        "medio": 68,
        "max": 100,
        "tipo": "mensual",
        "compartido": True
    },
    "gas_calefaccion": {
        "descripcion": "Gas y calefaccion (parte de Paulina)",
        "min": 50,
        "medio": 88,
        "max": 125,
        "tipo": "mensual",
        "compartido": True
    },
    "agua": {
        "descripcion": "Agua (parte de Paulina)",
        "min": 20,
        "medio": 25,
        "max": 30,
        "tipo": "mensual",
        "compartido": True
    },
    "internet": {
        "descripcion": "Internet fibra (parte de Paulina)",
        "min": 15,
        "medio": 23,
        "max": 30,
        "tipo": "mensual",
        "compartido": True
    },
    "celular": {
        "descripcion": "Plan celular",
        "min": 20,
        "medio": 40,
        "max": 60,
        "tipo": "mensual",
        "compartido": False
    },
    "supermercado": {
        "descripcion": "Alimentacion y supermercado",
        "min": 200,
        "medio": 300,
        "max": 400,
        "tipo": "mensual",
        "compartido": False
    },
    "transporte": {
        "descripcion": "Abono transporte publico Madrid",
        "min": 8,
        "medio": 8,
        "max": 55,
        "tipo": "mensual",
        "nota": "8 EUR para menores de 26 anos, 55 EUR normal"
    },
    "seguro_medico": {
        "descripcion": "Seguro medico privado espanol",
        "min": 35,
        "medio": 46,
        "max": 57,
        "tipo": "mensual",
        "obligatorio": True
    },
    "ocio_cultura": {
        "descripcion": "Ocio, restaurantes, cultura, salidas",
        "min": 50,
        "medio": 150,
        "max": 300,
        "tipo": "mensual",
        "opcional": True,
        "nota": "No incluido en guia IE - estimado"
    },
    "ropa_personal": {
        "descripcion": "Ropa, higiene, cuidado personal",
        "min": 30,
        "medio": 75,
        "max": 150,
        "tipo": "mensual",
        "opcional": True
    },
    "materiales_estudio": {
        "descripcion": "Libros, materiales, software educativo",
        "min": 25,
        "medio": 50,
        "max": 100,
        "tipo": "mensual",
        "opcional": True
    },
    "vuelos_colombia": {
        "descripcion": "Vuelos Colombia-Espana (ida y vuelta)",
        "min": 800,
        "medio": 1000,
        "max": 1400,
        "tipo": "por_viaje",
        "viajes_por_ano": 2,
        "nota": "Estimado 2 viajes/ano (verano y navidad)"
    },
    "emergencias": {
        "descripcion": "Fondo de emergencia",
        "porcentaje_del_total": 0.05,
        "min_porcentaje": 0.05,
        "max_porcentaje": 0.10,
        "tipo": "porcentaje",
        "opcional": True
    }
}

# ============================================================
# FUNCIONES DE CALCULO
# ============================================================

def calcular_gastos_mensuales(nivel: str, incluir_opcionales: dict) -> dict:
    """
    Calcula gastos mensuales segun nivel (austero/moderado/comodo)
    nivel: 'min', 'medio', 'max'
    incluir_opcionales: dict con flags para cada categoria opcional
    """
    gastos = {}
    total = 0

    for categoria, datos in COSTOS_BASE.items():
        if categoria == "matricula":
            continue  # Se maneja aparte
        if categoria == "emergencias":
            continue  # Se calcula al final como %
        if categoria == "vuelos_colombia":
            continue  # Se maneja aparte (anual)

        # Verificar si es opcional y si esta incluido
        es_opcional = datos.get("opcional", False)
        if es_opcional and not incluir_opcionales.get(categoria, True):
            gastos[categoria] = {
                "valor": 0,
                "incluido": False,
                "descripcion": datos["descripcion"]
            }
            continue

        # Obtener valor segun nivel
        if nivel == "min":
            valor = datos.get("min", datos.get("medio", 0))
        elif nivel == "max":
            valor = datos.get("max", datos.get("medio", 0))
        else:  # medio
            valor = datos.get("medio", 0)

        gastos[categoria] = {
            "valor": valor,
            "incluido": True,
            "descripcion": datos["descripcion"],
            "compartido": datos.get("compartido", False)
        }
        total += valor

    gastos["_total_sin_emergencias"] = total
    return gastos


def calcular_escenario(nombre: str, nivel: str, descuento_matricula: bool,
                       incluir_opcionales: dict, viajes_por_ano: int) -> dict:
    """Calcula un escenario completo con proyeccion de 4 anos"""

    # Matricula
    matricula_base = COSTOS_BASE["matricula"]["anual_base"]
    descuento = SUPUESTOS["descuento_matricula_disponible"] if descuento_matricula else 0
    matricula_anual = matricula_base * (1 - descuento)

    # Gastos mensuales
    gastos_mensuales = calcular_gastos_mensuales(nivel, incluir_opcionales)
    total_mensual_base = gastos_mensuales["_total_sin_emergencias"]

    # Vuelos anuales
    vuelo_datos = COSTOS_BASE["vuelos_colombia"]
    if nivel == "min":
        costo_vuelo = vuelo_datos["min"]
    elif nivel == "max":
        costo_vuelo = vuelo_datos["max"]
    else:
        costo_vuelo = vuelo_datos["medio"]

    incluir_vuelos = incluir_opcionales.get("vuelos_colombia", True)
    vuelos_anual = costo_vuelo * viajes_por_ano if incluir_vuelos else 0

    # Total anual sin emergencias
    gastos_vida_anual = (total_mensual_base * 12) + vuelos_anual

    # Emergencias como % del total
    if incluir_opcionales.get("emergencias", True):
        if nivel == "min":
            pct_emergencias = COSTOS_BASE["emergencias"]["min_porcentaje"]
        elif nivel == "max":
            pct_emergencias = COSTOS_BASE["emergencias"]["max_porcentaje"]
        else:
            pct_emergencias = COSTOS_BASE["emergencias"]["porcentaje_del_total"]

        emergencias_anual = (gastos_vida_anual + matricula_anual) * pct_emergencias
    else:
        emergencias_anual = 0
        pct_emergencias = 0

    # Total ano 1
    total_anual_ano1 = matricula_anual + gastos_vida_anual + emergencias_anual

    # Proyeccion 4 anos con inflacion
    inflacion = SUPUESTOS["inflacion_espana"]
    proyeccion = []
    total_acumulado = 0

    for i in range(PERFIL["duracion_anos"]):
        ano = PERFIL["ano_inicio"] + i
        factor_inflacion = (1 + inflacion) ** i

        mat = matricula_anual * factor_inflacion
        gastos = gastos_vida_anual * factor_inflacion
        emerg = emergencias_anual * factor_inflacion
        total = mat + gastos + emerg
        total_acumulado += total

        proyeccion.append({
            "ano": ano,
            "numero_ano": i + 1,
            "factor_inflacion": round(factor_inflacion, 4),
            "matricula": round(mat, 2),
            "gastos_vida": round(gastos, 2),
            "emergencias": round(emerg, 2),
            "total_anual": round(total, 2),
            "total_mensual_promedio": round(total / 12, 2)
        })

    return {
        "nombre": nombre,
        "nivel": nivel,
        "descripcion": {
            "austero": "Gastos minimos, sin extras, maximo ahorro",
            "moderado": "Balance calidad-costo, vida comoda pero consciente",
            "comodo": "Sin restricciones, todos los extras incluidos"
        }.get(nombre.lower(), ""),
        "configuracion": {
            "descuento_matricula": descuento_matricula,
            "porcentaje_descuento": descuento,
            "viajes_por_ano": viajes_por_ano if incluir_vuelos else 0,
            "incluir_opcionales": incluir_opcionales,
            "porcentaje_emergencias": pct_emergencias
        },
        "resumen_ano_1": {
            "matricula_base": matricula_base,
            "matricula_con_descuento": round(matricula_anual, 2),
            "ahorro_por_descuento": round(matricula_base - matricula_anual, 2),
            "gastos_mensuales": round(total_mensual_base, 2),
            "gastos_vida_anual": round(gastos_vida_anual, 2),
            "vuelos_anual": round(vuelos_anual, 2),
            "emergencias_anual": round(emergencias_anual, 2),
            "total_anual": round(total_anual_ano1, 2),
            "total_mensual_promedio": round(total_anual_ano1 / 12, 2)
        },
        "desglose_mensual": {k: v for k, v in gastos_mensuales.items() if not k.startswith("_")},
        "proyeccion_anual": proyeccion,
        "totales": {
            "total_4_anos_eur": round(total_acumulado, 2),
            "total_4_anos_usd": round(total_acumulado * SUPUESTOS["tasas_cambio"]["EUR_USD"], 2),
            "total_4_anos_cop": round(total_acumulado * SUPUESTOS["tasas_cambio"]["EUR_COP"], 2),
            "promedio_anual": round(total_acumulado / PERFIL["duracion_anos"], 2),
            "promedio_mensual": round(total_acumulado / (PERFIL["duracion_anos"] * 12), 2)
        }
    }


def generar_datos_base() -> dict:
    """Genera el JSON de datos base"""
    return {
        "metadata": {
            "proyecto": "Modelo Financiero de Permanencia - Paulina en Madrid",
            "version": "2.0",
            "fecha_generacion": datetime.now().isoformat(),
            "generado_por": "Claude Code - Financial Analysis Skill"
        },
        "perfil": PERFIL,
        "supuestos": SUPUESTOS,
        "costos_base": COSTOS_BASE,
        "categorias": {
            "fijas": ["vivienda", "electricidad", "gas_calefaccion", "agua", "internet",
                     "celular", "supermercado", "transporte", "seguro_medico"],
            "opcionales": ["ocio_cultura", "ropa_personal", "materiales_estudio",
                          "vuelos_colombia", "emergencias"],
            "compartidas": ["vivienda", "electricidad", "gas_calefaccion", "agua", "internet"]
        },
        "notas": [
            "Datos de costos basados en Guia Oficial IE Madrid",
            "Viajes Colombia-Espana estimados segun precios promedio 2024-2025",
            "Ocio y cultura no incluido en guia IE - valores estimados",
            "Transporte: 8 EUR/mes para menores de 26 anos (Abono Joven Madrid)",
            "Emergencias calculadas como porcentaje del total (5-10%)"
        ]
    }


def generar_escenarios() -> dict:
    """Genera el JSON de escenarios"""

    # Configuracion de opcionales por escenario
    opcionales_austero = {
        "ocio_cultura": False,
        "ropa_personal": True,  # Minimo necesario
        "materiales_estudio": True,
        "vuelos_colombia": True,  # 1 viaje
        "emergencias": True
    }

    opcionales_moderado = {
        "ocio_cultura": True,
        "ropa_personal": True,
        "materiales_estudio": True,
        "vuelos_colombia": True,  # 2 viajes
        "emergencias": True
    }

    opcionales_comodo = {
        "ocio_cultura": True,
        "ropa_personal": True,
        "materiales_estudio": True,
        "vuelos_colombia": True,  # 2 viajes
        "emergencias": True
    }

    escenarios = {
        "metadata": {
            "fecha_generacion": datetime.now().isoformat(),
            "descripcion": "Tres escenarios financieros para la permanencia de Paulina en Madrid"
        },
        "escenarios": {
            "austero": calcular_escenario(
                nombre="Austero",
                nivel="min",
                descuento_matricula=True,
                incluir_opcionales=opcionales_austero,
                viajes_por_ano=1
            ),
            "moderado": calcular_escenario(
                nombre="Moderado",
                nivel="medio",
                descuento_matricula=True,
                incluir_opcionales=opcionales_moderado,
                viajes_por_ano=2
            ),
            "comodo": calcular_escenario(
                nombre="Comodo",
                nivel="max",
                descuento_matricula=True,
                incluir_opcionales=opcionales_comodo,
                viajes_por_ano=2
            )
        },
        "comparativa": {}
    }

    # Agregar comparativa rapida
    for key in ["austero", "moderado", "comodo"]:
        esc = escenarios["escenarios"][key]
        escenarios["comparativa"][key] = {
            "total_4_anos": esc["totales"]["total_4_anos_eur"],
            "promedio_mensual": esc["totales"]["promedio_mensual"],
            "ahorro_beca_4_anos": esc["resumen_ano_1"]["ahorro_por_descuento"] * 4
        }

    return escenarios


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("GENERADOR DE DATOS FINANCIEROS - PAULINA MADRID")
    print("=" * 60)

    # Generar datos base
    print("\n[1/2] Generando datos_paulina.json...")
    datos = generar_datos_base()
    with open(OUTPUT_DIR / "datos_paulina.json", "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=2, ensure_ascii=False)
    print(f"      -> {OUTPUT_DIR / 'datos_paulina.json'}")

    # Generar escenarios
    print("\n[2/2] Generando escenarios_paulina.json...")
    escenarios = generar_escenarios()
    with open(OUTPUT_DIR / "escenarios_paulina.json", "w", encoding="utf-8") as f:
        json.dump(escenarios, f, indent=2, ensure_ascii=False)
    print(f"      -> {OUTPUT_DIR / 'escenarios_paulina.json'}")

    # Resumen
    print("\n" + "=" * 60)
    print("RESUMEN DE ESCENARIOS (Total 4 anos)")
    print("=" * 60)
    for nombre, datos_esc in escenarios["escenarios"].items():
        total = datos_esc["totales"]["total_4_anos_eur"]
        mensual = datos_esc["totales"]["promedio_mensual"]
        print(f"\n{nombre.upper()}:")
        print(f"  Total 4 anos: EUR {total:,.0f}")
        print(f"  Promedio mensual: EUR {mensual:,.0f}")
        print(f"  En USD: ${datos_esc['totales']['total_4_anos_usd']:,.0f}")
        print(f"  En COP: ${datos_esc['totales']['total_4_anos_cop']:,.0f}")

    print("\n" + "=" * 60)
    print("Generacion completada exitosamente!")
    print("=" * 60)
