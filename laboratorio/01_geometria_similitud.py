"""Geometría de la similitud, sin base de datos y sin modelo.

Los ejes están etiquetados a propósito. En un embedding real de 1024
dimensiones los ejes no significan nada por separado; aquí sí, para
poder hacer la cuenta a mano y contrastarla con este script.
"""

from __future__ import annotations


def producto(a: list[float], b: list[float]) -> float:
    if len(a) != len(b):
        raise ValueError("Los dos vectores tienen que tener la misma dimensión")
    return sum(x * y for x, y in zip(a, b))


def norma(a: list[float]) -> float:
    return producto(a, a) ** 0.5


def coseno(a: list[float], b: list[float]) -> float:
    denominador = norma(a) * norma(b)
    if denominador == 0:
        raise ValueError("No se puede calcular el coseno de un vector nulo")
    return producto(a, b) / denominador


# Ejes didácticos: (trámites de matrícula, horas y módulos, convivencia)
FRAGMENTOS = [
    ("Procedimiento de formalización de matrícula", [0.90, 0.10, 0.00]),
    ("Cómo me matriculo en el ciclo", [0.85, 0.20, 0.05]),
    ("El módulo de Big Data tiene 190 horas", [0.05, 0.95, 0.00]),
    ("Plan de convivencia del centro", [0.00, 0.05, 0.90]),
]


def ranking(consulta: list[float], fragmentos: list[tuple[str, list[float]]]) -> None:
    ordenados = sorted(
        ((coseno(consulta, vector), texto) for texto, vector in fragmentos),
        reverse=True,
    )
    for similitud, texto in ordenados:
        print(f"  {similitud:0.3f}  {texto}")


def main() -> None:
    print("Pregunta: ¿cómo me matriculo?")
    ranking([0.88, 0.15, 0.02], FRAGMENTOS)

    print("\nPregunta: ¿cuántas horas tiene el módulo?")
    ranking([0.05, 0.90, 0.05], FRAGMENTOS)

    print("\nProducto escalar y coseno no coinciden si el vector no está normalizado")
    a = [2.0, 0.0]
    b = [1.0, 1.0]
    print(f"  a · b = {producto(a, b):0.3f}")
    print(f"  cos(a, b) = {coseno(a, b):0.3f}")
    print(f"  ||a|| = {norma(a):0.3f}   ||b|| = {norma(b):0.3f}")


if __name__ == "__main__":
    main()
