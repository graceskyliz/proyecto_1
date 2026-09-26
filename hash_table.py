from manim import *
import json

class AnimacionHashTable(Scene):
    def construct(self):
        titulo = Text("Tabla Hash - Separate Chaining", font_size=36)
        autores = Text("Operaciones y colisiones", font_size=20, color=GRAY)
        autores.next_to(titulo, DOWN)

        self.play(Write(titulo), FadeIn(autores))
        self.wait(2)
        self.play(FadeOut(titulo), FadeOut(autores))

        try:
            with open("trace.json", "r") as f:
                eventos = json.load(f)
        except FileNotFoundError:
            eventos = []

        capacidad = eventos[0].get("capacity", 5) if eventos else 5
        buckets = VGroup()
        indices = VGroup()
        nodes = [[] for _ in range(capacidad)]
        status = Text("", font_size=18).to_edge(DOWN)

        def draw_table(new_capacity):
            nonlocal buckets, indices, capacidad
            capacidad = new_capacity
            buckets = VGroup(*[Square(side_length=0.65) for _ in range(capacidad)])
            buckets.arrange_in_grid(rows=min(8, capacidad), cols=(capacidad + 7) // 8,
                                    buff=(0.28, 0.12)).move_to(LEFT * 3.2)
            indices = VGroup(*[
                Text(f"[{i}]", font_size=14).next_to(buckets[i], LEFT, buff=0.12)
                for i in range(capacidad)
            ])
            self.play(Create(buckets), Write(indices), run_time=0.5)

        draw_table(capacidad)

        def show_status(ev):
            text = f"{ev['action']}: {ev.get('detail', '')}"
            self.play(Transform(status, Text(text, font_size=18).to_edge(DOWN)), run_time=0.25)

        for ev in eventos:
            new_capacity = ev.get("capacity", capacidad)
            if new_capacity != capacidad:
                previous_entries = [
                    (node["key"], node["value"])
                    for bucket_nodes in nodes for node in bucket_nodes
                ]
                for bucket_nodes in nodes:
                    self.play(*[FadeOut(node["group"]) for node in bucket_nodes], run_time=0.15)
                self.play(FadeOut(buckets), FadeOut(indices), run_time=0.25)
                nodes = [[] for _ in range(new_capacity)]
                draw_table(new_capacity)
                for key, value in previous_entries:
                    bucket = key % new_capacity
                    rect = Rectangle(width=1.0, height=0.45, color=ORANGE)
                    text = Text(f"{key}:{value}", font_size=14).move_to(rect.get_center())
                    previous = nodes[bucket][-1]["rect"] if nodes[bucket] else buckets[bucket]
                    group = VGroup(rect, text).next_to(previous, RIGHT, buff=0.3)
                    nodes[bucket].append({"key": key, "value": value, "rect": rect,
                                          "text": text, "group": group})
                    self.play(FadeIn(group), run_time=0.15)

            action = ev["action"]
            if action in {"insert", "update"}:
                bucket = ev["bucket"]
                self.play(buckets[bucket].animate.set_color(YELLOW), run_time=0.2)
                if action == "update":
                    for node in nodes[bucket]:
                        if node["key"] == ev["key"]:
                            replacement = Text(f"{ev['key']}:{ev['val']}", font_size=14).move_to(node["rect"])
                            self.play(Transform(node["text"], replacement), run_time=0.3)
                            node["value"] = ev["val"]
                else:
                    rect = Rectangle(width=1.0, height=0.45, color=BLUE)
                    text = Text(f"{ev['key']}:{ev['val']}", font_size=14).move_to(rect.get_center())
                    previous = nodes[bucket][-1]["rect"] if nodes[bucket] else buckets[bucket]
                    group = VGroup(rect, text).next_to(previous, RIGHT, buff=0.3)
                    node = {"key": ev["key"], "value": ev["val"], "rect": rect,
                            "text": text, "group": group}
                    nodes[bucket].append(node)
                    self.play(FadeIn(group), run_time=0.3)
                self.play(buckets[bucket].animate.set_color(WHITE), run_time=0.2)
            elif action == "remove":
                bucket = ev["bucket"]
                for node in nodes[bucket][:]:
                    if node["key"] == ev["key"]:
                        self.play(FadeOut(node["group"]), run_time=0.3)
                        nodes[bucket].remove(node)
                        break
            elif action in {"search", "contains", "bucketSize"}:
                bucket = ev["bucket"]
                color = GREEN if ev["result"] else RED
                self.play(buckets[bucket].animate.set_color(color), run_time=0.25)
                self.wait(0.25)
                self.play(buckets[bucket].animate.set_color(WHITE), run_time=0.2)
            show_status(ev)
            self.wait(0.25)

        self.play(FadeOut(status))
        self.wait(2)