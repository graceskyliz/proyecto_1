from manim import *
import json

class AnimacionHashTable(Scene):
    def construct(self):
        # 1. Carátula Inicial (Títulos y Autores)
        titulo = Text("Tabla Hash - Separate Chaining", font_size=36)
        autores = Text("CS2023 - Algoritmos y Estructuras de Datos\nIntegrantes: [Nombre 1], [Nombre 2], [Nombre 3]", font_size=20, color=GRAY)
        autores.next_to(titulo, DOWN)

        self.play(Write(titulo), FadeIn(autores))
        self.wait(2)
        self.play(FadeOut(titulo), FadeOut(autores))

        # 2. Cargar eventos exportados desde C++
        try:
            with open("trace.json", "r") as f:
                eventos = json.load(f)
        except FileNotFoundError:
            eventos = []

        # 3. Dibujar la estructura visual de la Tabla Hash (5 Buckets)
        capacidad = 5
        buckets = VGroup(*[Square(side_length=0.8) for _ in range(capacidad)]).arrange(DOWN, buff=0.15)
        buckets.move_to(LEFT * 3)

        indices = VGroup(*[
            Text(f"[{i}]", font_size=18).next_to(buckets[i], LEFT, buff=0.2)
            for i in range(capacidad)
        ])

        self.play(Create(buckets), Write(indices))
        self.wait(0.5)

        # Referencias visuales para conectar listas enlazadas en colisiones
        ultimos_nodos = [buckets[i] for i in range(capacidad)]

        # 4. Animar cada evento grabado por C++
        for ev in eventos:
            b_idx = ev["bucket"]

            # Resaltar el bucket destino en amarillo
            self.play(buckets[b_idx].animate.set_color(YELLOW), run_time=0.4)

            # Crear el elemento/nodo nuevo de la lista
            rect = Rectangle(width=1.2, height=0.6, color=BLUE)
            txt = Text(f"{ev['key']}:{ev['val']}", font_size=16).move_to(rect.get_center())
            nodo = VGroup(rect, txt)

            # Posicionar el nodo a la derecha
            nodo.next_to(ultimos_nodos[b_idx], RIGHT, buff=0.6)
            flecha = Arrow(start=ultimos_nodos[b_idx].get_right(), end=rect.get_left(), buff=0.05, stroke_width=2)

            # Animar aparición del nodo y flecha
            self.play(GrowArrow(flecha), FadeIn(nodo))
            self.play(buckets[b_idx].animate.set_color(WHITE), run_time=0.3)

            ultimos_nodos[b_idx] = rect
            self.wait(0.5)

        self.wait(2)