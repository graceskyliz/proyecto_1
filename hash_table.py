from manim import *
import json


class AnimacionHashTable(Scene):
    def construct(self):
        minimum_video_duration = 8
        operation_pause = 1.1
        title = Text("TABLA HASH", font_size=36, weight=BOLD)
        subtitle = Text("Separate chaining | operaciones paso a paso", font_size=18, color=GRAY_B)
        nombres = Text("Integrantes: \nZavaleta Alvino, Roger \nAquino Reyna, Jesus Emmanue \nMendoza Palacios, Gracia Luz", font_size=20, color=GRAY)
        subtitle.next_to(title, DOWN, buff=0.12)
        nombres.next_to(subtitle, DOWN, buff=0.12)

        self.play(Write(title), FadeIn(subtitle),FadeIn(nombres), run_time=1.2)
        self.wait(1.5)
        self.play(FadeOut(title), FadeOut(subtitle),FadeOut(nombres) ,run_time=0.5)
        title = Text("TABLA HASH", font_size=28, weight=BOLD).to_edge(UP, buff=0.22)
        self.add(title)

        try:
            with open("trace.json", "r") as f:
                eventos = json.load(f)
        except FileNotFoundError:
            eventos = []

        capacidad = eventos[0].get("capacity", 5) if eventos else 5
        buckets = VGroup()
        indices = VGroup()
        nodes = [[] for _ in range(capacidad)]
        table_title = Text("BUCKETS", font_size=16, color=GRAY_B).move_to([-4.35, 2.55, 0])
        chain_title = Text("CADENA DE NODOS", font_size=16, color=GRAY_B)
        chain_title.scale_to_fit_width(2.15).move_to([-1.65, 2.55, 0])
        self.add(table_title, chain_title)

        panel = RoundedRectangle(width=4.1, height=5.35, corner_radius=0.12,
                                 color=BLUE_E).move_to([4.25, -0.05, 0])
        panel_title = Text("METODO EN EJECUCION", font_size=15, color=GRAY_B)
        panel_title.move_to([4.25, 2.18, 0])
        method_label = Text("PREPARANDO", font_size=27, weight=BOLD, color=YELLOW)
        method_label.move_to([4.25, 1.45, 0])
        operation_label = Text("", font_size=19).move_to([4.25, 0.68, 0])
        detail_label = Text("", font_size=17, color=GRAY_B).move_to([4.25, -0.05, 0])
        result_label = Text("", font_size=18).move_to([4.25, -0.82, 0])
        formula = Text("indice = hash(clave) % capacidad", font_size=14, color=GRAY_C)
        formula.move_to([4.25, -1.72, 0])
        self.add(panel, panel_title, method_label, operation_label, detail_label, result_label, formula)

        panel_center_x = 4.25
        panel_inner_width = 3.45

        def panel_text(content, font_size, color=WHITE, weight=NORMAL, y=0):
            text = Text(content, font_size=font_size, color=color, weight=weight)
            text.scale_to_fit_width(panel_inner_width)
            return text.move_to([panel_center_x, y, 0])

        progress = Text("Operacion 0/0", font_size=15, color=GRAY_B).to_edge(DOWN, buff=0.22)
        self.add(progress)

        method_names = {
            "insert": "INSERTAR",
            "update": "ACTUALIZAR",
            "remove": "ELIMINAR",
            "search": "BUSCAR",
            "contains": "CONTIENTE",
            "bucketSize": "TAMANO DE BUCKET",
            "size": "TAMANO",
            "getCapacity": "OBTENER CAPACIDAD",
            "getK": "OBTENER K",
            "getFillFactor": "FACTOR DE CARGA",
            "getMaxFillFactor": "CARGA MAXIMA",
            "empty": "ESTA VACIA",
            "print": "IMPRIMIR",
        }

        def draw_table(new_capacity):
            nonlocal buckets, indices, capacidad
            capacidad = new_capacity
            buckets = VGroup(*[Square(side_length=0.48) for _ in range(capacidad)])
            buckets.arrange(DOWN, buff=0.10).move_to([-4.3, -0.10, 0])
            indices = VGroup(*[
                Text(f"[{i}]", font_size=13).next_to(buckets[i], LEFT, buff=0.14)
                for i in range(capacidad)
            ])
            self.play(Create(buckets), Write(indices), run_time=0.7)

        def node_group(key, value, color):
            rect = Rectangle(width=0.92, height=0.38, color=color)
            text = Text(f"{key}:{value}", font_size=13).move_to(rect.get_center())
            return rect, text, VGroup(rect, text)

        def place_node(node, bucket):
            x = -3.58 + len(nodes[bucket]) * 1.04
            node["group"].move_to([x, buckets[bucket].get_center()[1], 0])

        def show_operation(ev, number):
            action = ev["action"]
            value = ev.get("val", "")
            operation = f"{action}( {ev.get('key', '')}"
            if value:
                operation += f", {value}"
            operation += " )"
            result = "RESULTADO: " + (ev.get("detail", "").upper() or "OK")
            color = GREEN if ev.get("result", True) else RED
            new_method = panel_text(method_names.get(action, action.upper()), 27,
                                    YELLOW, BOLD, 1.45)
            new_operation = panel_text(operation, 19, y=0.68)
            new_detail = panel_text(
                f"bucket [{ev.get('bucket', '-')}] | capacidad {ev.get('capacity', capacidad)}",
                17, GRAY_B, y=-0.05)
            new_result = panel_text(result, 18, color, y=-0.82)
            new_progress = Text(f"Operacion {number}/{len(eventos)}", font_size=15,
                                color=GRAY_B).to_edge(DOWN, buff=0.22)
            self.play(Transform(method_label, new_method),
                      Transform(operation_label, new_operation),
                      Transform(detail_label, new_detail),
                      Transform(result_label, new_result),
                                Transform(progress, new_progress), run_time=0.55)

        draw_table(capacidad)
        for event_number, ev in enumerate(eventos, start=1):
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
                    rect, text, group = node_group(key, value, ORANGE)
                    node = {"key": key, "value": value, "rect": rect,
                            "text": text, "group": group}
                    nodes[bucket].append(node)
                    place_node(node, bucket)
                    self.play(FadeIn(group), run_time=0.15)

            action = ev["action"]
            show_operation(ev, event_number)
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
                    rect, text, group = node_group(ev["key"], ev["val"], BLUE)
                    node = {"key": ev["key"], "value": ev["val"], "rect": rect,
                            "text": text, "group": group}
                    nodes[bucket].append(node)
                    place_node(node, bucket)
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
            self.wait(operation_pause)

        final_message = panel_text("TRAZA COMPLETADA", 24, GREEN, y=-0.82)
        self.play(Transform(method_label, panel_text("FINAL", 27, GREEN, BOLD, 1.45)),
                  Transform(operation_label, final_message), run_time=0.5)
        self.wait(2)
        elapsed_time = self.renderer.time
        remaining_time = minimum_video_duration - elapsed_time
        if remaining_time > 0:
            self.wait(remaining_time)