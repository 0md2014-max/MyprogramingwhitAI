import tkinter as tk
from tkinter import ttk
import math

# =====================================================================
# PALETA DE COLORES (60-30-10 Disciplinada)
# =====================================================================
BG_MAIN = "#020617"      # Slate 950 (60% Lienzo dominante)
BG_PANEL = "#0f172a"     # Slate 900 (30% Estructuras)
BG_CARD = "#1e293b"      # Slate 800
BORDER_COL = "#334155"   # Slate 700
TEXT_MAIN = "#f8fafc"    # Slate 50
TEXT_MUTED = "#94a3b8"   # Slate 400

ACCENT_DNA = "#06b6d4"   # Cian eléctrico (ADN / Núcleo)
ACCENT_MIT = "#a855f7"   # Violeta (Cromosomas / Mitosis)
ACCENT_MEI = "#ec4899"   # Magenta (Meiosis / Crossing-over)
ACCENT_CEN = "#f59e0b"   # Ámbar (Centrosomas / Huso)
ACCENT_CYT = "#10b981"   # Esmeralda (Citoplasma / Membrana)

# =====================================================================
# BASE DE DATOS LOCAL DE CONOCIMIENTO
# =====================================================================
NODES_DATA = {
    "celula": {
        "title": "Célula Madre", "x": 120, "y": 240, "color": ACCENT_CYT,
        "def": "La unidad básica de la vida. Antes de dividirse, debe prepararse y hacer una copia exacta de su manual de instrucciones (ADN).",
        "metaphor": "Imagina que tienes una panadería exitosa y quieres abrir una sucursal idéntica: primero debes fotocopiar todas tus recetas.",
        "glossary": "• Membrana: Muralla flexible de la célula.\n• Citoplasma: Gel interior donde flotan los orgánulos.\n• Diploide (2n): 46 cromosomas en humanos."
    },
    "interfase": {
        "title": "Interfase (G1, S, G2)", "x": 310, "y": 130, "color": ACCENT_DNA,
        "def": "El 90% de la vida de la célula. En G1 crece, en la fase S duplica su ADN, y en G2 revisa que todo esté listo para dividirse.",
        "metaphor": "Son los ensayos generales antes de un concierto de piano: practicas, afinas el instrumento y duplicas las partituras.",
        "glossary": "• Fase G1: Crecimiento físico.\n• Fase S (Síntesis): El ADN se replica exactamente.\n• Fase G2: Control de calidad pre-división."
    },
    "adn": {
        "title": "ADN y Genes", "x": 310, "y": 350, "color": ACCENT_DNA,
        "def": "El Ácido Desoxirribonucleico contiene las instrucciones genéticas en una doble hélice. Un gen es un segmento que codifica una proteína.",
        "metaphor": "El ADN es todo el código fuente de un sistema operativo; un gen es una función específica dentro de ese código.",
        "glossary": "• Bases: Adenina (A) con Timina (T), Citosina (C) con Guanina (G).\n• Cromatina: ADN desenrollado mezclado con proteínas histonas."
    },
    "cromosomas": {
        "title": "Cromosomas", "x": 510, "y": 350, "color": ACCENT_MIT,
        "def": "ADN súper empaquetado y condensado en forma de 'X' para poder moverse sin romperse durante la división celular.",
        "metaphor": "Si te mudas de casa, no llevas los cables sueltos por la calle; los enrollas y los guardas en cajas compactas.",
        "glossary": "• Cromátidas hermanas: Las dos mitades idénticas de la 'X'.\n• Centrómero: El cinturón central donde se engancha el huso."
    },
    "mitosis": {
        "title": "Mitosis (Clonación)", "x": 540, "y": 110, "color": ACCENT_MIT,
        "def": "División celular para crecimiento y reparación. De 1 célula madre diploide (2n=46) salen 2 células hijas genéticamente idénticas.",
        "metaphor": "Hacer 'Ctrl+C' y 'Ctrl+V' a un archivo: obtienes dos copias exactas para reemplazar tejidos dañados.",
        "glossary": "• Fases: Profase -> Metafase -> Anafase -> Telofase.\n• Huso mitótico: Microtúbulos que arrastran cromátidas."
    },
    "meiosis": {
        "title": "Meiosis (Diversidad)", "x": 540, "y": 220, "color": ACCENT_MEI,
        "def": "Doble división para crear gametos (óvulos y espermatozoides). Produce 4 células haploides (n=23) únicas gracias al crossing-over.",
        "metaphor": "Barajar un mazo de cartas antes de repartir: cada mano es única, por eso no eres un clon de tus hermanos.",
        "glossary": "• Crossing-over: Intercambio de genes en Profase I.\n• Haploide (n): Mitad del juego cromosómico (23)."
    },
    "citocinesis": {
        "title": "Citocinesis", "x": 740, "y": 165, "color": ACCENT_CEN,
        "def": "El corte físico final del citoplasma y la membrana celular para separar definitivamente a las nuevas células hijas.",
        "metaphor": "Cortar una masa de pizza por la mitad después de haber repartido los ingredientes en partes iguales.",
        "glossary": "• Anillo contráctil: Filamentos de actina que estrangulan el centro celular."
    }
}

NODE_EDGES = [
    ("celula", "interfase"), ("celula", "adn"), ("interfase", "mitosis"),
    ("interfase", "meiosis"), ("adn", "cromosomas"), ("cromosomas", "mitosis"),
    ("cromosomas", "meiosis"), ("mitosis", "citocinesis"), ("meiosis", "citocinesis")
]

SIM_PHASES = {
    "Mitosis": [
        ("1. Interfase (G1 -> S -> G2)", "El ADN está descondensado como cromatina. En la fase S se duplica (2n=46, 92 cromátidas) y los centrosomas se replican.", "2n = 46 (ADN duplicado)"),
        ("2. Profase", "La cromatina se condensa en cromosomas en 'X'. La envoltura nuclear se desintegra y los centrosomas proyectan el huso mitótico.", "46 cromosomas dobles"),
        ("3. Metafase", "Los microtúbulos del huso alinean todos los cromosomas en el ecuador celular (placa metafásica). Máxima condensación.", "46 alineados en ecuador"),
        ("4. Anafase", "El centrómero se escinde. Las cromátidas hermanas se separan y viajan hacia polos opuestos convertidas en cromosomas individuales.", "46 simples hacia cada polo"),
        ("5. Telofase y Citocinesis", "Se reconstruyen dos envolturas nucleares, el ADN vuelve a ser cromatina y el anillo contráctil divide el citoplasma en 2 clones.", "2 células hijas idénticas (2n=46)")
    ],
    "Meiosis": [
        ("1. Profase I (Crossing-Over)", "Los cromosomas homólogos se aparean formando tétradas e intercambian segmentos de ADN (recombinación genética).", "23 pares recombinados"),
        ("2. Metafase I", "Los pares de cromosomas homólogos se alinean en doble fila sobre la placa ecuatorial.", "23 pares en el centro"),
        ("3. Anafase I y Telofase I", "Se separan los cromosomas homólogos enteros (las cromátidas hermanas permanecen unidas). Nacen 2 células haploides con cromosomas dobles.", "2 células (n=23 dobles)"),
        ("4. Meiosis II (Profase II a Metafase II)", "Sin nueva replicación de ADN, las 2 células vuelven a formar el huso y alinean sus 23 cromosomas dobles en el centro.", "23 dobles alineados"),
        ("5. Anafase II y Citocinesis Final", "Se separan las cromátidas hermanas. Resultan 4 gametos haploides (n=23) genéticamente irrepetibles.", "4 gametos únicos (n=23)")
    ]
}

CHAT_KNOWLEDGE = [
    (["hola", "buenas", "quien eres"], "¡Hola! Soy BioGuía, tu motor local de consulta biológica. Pregúntame sobre mitosis, meiosis, ADN, fases o escribe tu duda de clase."),
    (["no duplica", "sin duplicar", "error", "mutacion"], "Si una célula no duplica su ADN en la Fase S, el punto de control G2 detiene el ciclo. Si lograra dividirse, las células hijas recibirían cromosomas incompletos y morirían por apoptosis."),
    (["cromatida", "cromosoma", "diferencia"], "Mientras están unidos por el centrómero formando una 'X', todo el conjunto cuenta como 1 cromosoma doble formado por 2 cromátidas hermanas. En cuanto se separan en Anafase, cada cromátida pasa a ser un cromosoma independiente."),
    (["mitosis", "meiosis", "comparar"], "• Mitosis: 1 división -> 2 células clones diploides (2n=46) -> Crecimiento y cicatrización.\n• Meiosis: 2 divisiones + Crossing-Over -> 4 gametos haploides únicos (n=23) -> Reproducción sexual."),
    (["crossing", "entrecruzamiento", "hermanos", "parecido"], "El crossing-over ocurre en la Profase I de la Meiosis. Los cromosomas homólogos intercambian bloques de genes al azar, garantizando que cada gameto sea único."),
    (["interfase", "g1", "g2", "fase s"], "La Interfase abarca tres etapas:\n• G1: Crecimiento celular y síntesis de proteínas.\n• S: Replicación exacta del ADN.\n• G2: Verificación de errores y preparación del huso.")
]

# Muestras generadas por código para el Analizador Visual (Sin imágenes externas)
SYNTHETIC_SLIDES = [
    {
        "name": "Muestra #1: Meristemo de Cebolla (Zona Central)",
        "type": "metafase",
        "question": "Observa los cromosomas condensados formando una línea recta perfecta en el ecuador celular y los hilos amarillos sujetándolos desde los polos.",
        "correct": "Metafase (Mitosis)",
        "explanation": "¡Exacto! En la Metafase la placa ecuatorial está completa. Es la fase ideal para fotografiar el cariotipo porque los cromosomas alcanzan su máxima condensación."
    },
    {
        "name": "Muestra #2: Epitelio en Regeneración (Migración Polar)",
        "type": "anafase",
        "question": "Las estructuras en forma de 'V' se están alejando del centro hacia extremos opuestos mientras la célula se estira.",
        "correct": "Anafase (Separación de cromátidas)",
        "explanation": "¡Correcto! El centrómero ya se partió y las proteínas motoras acortan los microtúbulos del huso arrastrando las cromátidas hermanas."
    },
    {
        "name": "Muestra #3: Tejido Gonadal (Bivalentes Quismáticos)",
        "type": "crossing",
        "question": "Dos cromosomas de distinto origen están pegados intercambiando fragmentos de color en sus extremos.",
        "correct": "Profase I de Meiosis (Crossing-Over)",
        "explanation": "¡Bien visto! Ese punto de cruce se llama quiasma y solo ocurre en la Profase I meiótica para generar variabilidad genética."
    },
    {
        "name": "Muestra #4: Hepatocito en Reposo Activo",
        "type": "interfase",
        "question": "La envoltura nuclear circular está intacta y el ADN se ve como una red difusa sin forma de bastones ni 'X'.",
        "correct": "Interfase (Cromatina descondensada)",
        "explanation": "¡Así es! Durante la Interfase el ADN debe estar desenrollado (cromatina) para que las enzimas puedan leer los genes y duplicarlo en la Fase S."
    }
]

# =====================================================================
# APLICACIÓN PRINCIPAL
# =====================================================================
class CitoLabApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("CitoLab - Explorador Interactivo Celular (100% Standalone • Cero Archivos Externos)")
        self.geometry("1220x760")
        self.configure(bg=BG_MAIN)
        self.minsize(1024, 680)

        self.selected_node = "celula"
        self.dragging_node = None
        self.sim_mode = "Mitosis"
        self.sim_step = 0
        self.sim_playing = False
        self.anim_tick = 0.0
        self.current_slide_idx = 0

        self._setup_styles()
        self._build_topbar()
        self._build_views()
        self.show_view("map")
        self._animate_loop()

    def _setup_styles(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TFrame", background=BG_MAIN)

    def _build_topbar(self):
        top = tk.Frame(self, bg=BG_PANEL, height=56, highlightbackground=BORDER_COL, highlightthickness=1)
        top.pack(side="top", fill="x")
        top.pack_propagate(False)

        tk.Label(top, text="🧬 CitoLab", font=("Segoe UI", 16, "bold"), bg=BG_PANEL, fg=ACCENT_DNA).pack(side="left", padx=20)
        tk.Label(top, text="AUTOCONTENIDO • SECUNDARIA (11-14 AÑOS)", font=("Consolas", 9), bg=BG_PANEL, fg=TEXT_MUTED).pack(side="left", padx=5)

        nav_frame = tk.Frame(top, bg=BG_PANEL)
        nav_frame.pack(side="right", padx=15)

        self.nav_btns = {}
        modes = [
            ("map", "1. CitoMap (Nodos)"),
            ("sim", "2. BioSim (Mitosis/Meiosis)"),
            ("zoom", "3. Zoom ADN → Cromosoma"),
            ("cases", "4. Biología en tu Día"),
            ("tutor", "5. BioGuía & Microscopio")
        ]
        for key, text in modes:
            btn = tk.Button(
                nav_frame, text=text, font=("Segoe UI", 10, "bold"),
                bg=BG_CARD, fg=TEXT_MAIN, activebackground=ACCENT_DNA, activeforeground=BG_MAIN,
                bd=0, padx=12, pady=6, cursor="hand2", command=lambda k=key: self.show_view(k)
            )
            btn.pack(side="left", padx=4)
            self.nav_btns[key] = btn

    def _build_views(self):
        self.container = tk.Frame(self, bg=BG_MAIN)
        self.container.pack(side="top", fill="both", expand=True)
        self.views = {}

        self._init_map_view()
        self._init_sim_view()
        self._init_zoom_view()
        self._init_cases_view()
        self._init_tutor_view()

    def show_view(self, key):
        for k, frame in self.views.items():
            frame.pack_forget()
            self.nav_btns[k].configure(bg=BG_CARD, fg=TEXT_MAIN)
        self.views[key].pack(fill="both", expand=True)
        self.nav_btns[key].configure(bg=ACCENT_DNA, fg=BG_MAIN)
        if key == "map":
            self._draw_map()
        elif key == "zoom":
            self._draw_zoom(self.zoom_slider.get())
        elif key == "tutor":
            self._render_synthetic_slide()

    # =================================================================
    # VISTA 1: CITOMAP (Mapa de Nodos Arrastrables)
    # =================================================================
    def _init_map_view(self):
        frame = tk.Frame(self.container, bg=BG_MAIN)
        self.views["map"] = frame

        self.map_canvas = tk.Canvas(frame, bg=BG_MAIN, highlightthickness=0, cursor="fleur")
        self.map_canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        self.map_canvas.bind("<ButtonPress-1>", self._on_node_press)
        self.map_canvas.bind("<B1-Motion>", self._on_node_drag)
        self.map_canvas.bind("<ButtonRelease-1>", lambda e: setattr(self, 'dragging_node', None))

        side = tk.Frame(frame, bg=BG_PANEL, width=380, highlightbackground=BORDER_COL, highlightthickness=1)
        side.pack(side="right", fill="y", padx=(0, 10), pady=10)
        side.pack_propagate(False)

        self.node_title_lbl = tk.Label(side, text="", font=("Segoe UI", 16, "bold"), bg=BG_PANEL, fg=ACCENT_DNA, wraplength=340, justify="left")
        self.node_title_lbl.pack(anchor="w", padx=20, pady=(20, 10))

        tk.Label(side, text="🔬 DEFINICIÓN CIENTÍFICA", font=("Consolas", 9, "bold"), bg=BG_PANEL, fg=TEXT_MUTED).pack(anchor="w", padx=20)
        self.node_def_lbl = tk.Label(side, text="", font=("Segoe UI", 10), bg=BG_PANEL, fg=TEXT_MAIN, wraplength=340, justify="left")
        self.node_def_lbl.pack(anchor="w", padx=20, pady=(4, 15))

        tk.Label(side, text="💡 METÁFORA COTIDIANA", font=("Consolas", 9, "bold"), bg=BG_PANEL, fg=ACCENT_CEN).pack(anchor="w", padx=20)
        self.node_meta_lbl = tk.Label(side, text="", font=("Segoe UI", 10, "italic"), bg=BG_CARD, fg=TEXT_MAIN, wraplength=320, justify="left", padx=12, pady=12)
        self.node_meta_lbl.pack(anchor="w", padx=20, pady=(4, 15), fill="x")

        tk.Label(side, text="📖 GLOSARIO INTERACTIVO", font=("Consolas", 9, "bold"), bg=BG_PANEL, fg=ACCENT_CYT).pack(anchor="w", padx=20)
        self.node_ht_lbl = tk.Label(side, text="", font=("Segoe UI", 10), bg=BG_PANEL, fg=TEXT_MUTED, wraplength=340, justify="left")
        self.node_ht_lbl.pack(anchor="w", padx=20, pady=(4, 20))

        tk.Button(
            side, text="▶ Ir a simular este proceso en BioSim", font=("Segoe UI", 10, "bold"),
            bg=ACCENT_MIT, fg=TEXT_MAIN, bd=0, padx=15, pady=10, cursor="hand2",
            command=lambda: self.show_view("sim")
        ).pack(padx=20, fill="x")

        self._update_node_panel()

    def _draw_map(self):
        c = self.map_canvas
        c.delete("all")
        for x in range(0, 900, 40):
            c.create_line(x, 0, x, 700, fill="#0f172a")
        for y in range(0, 700, 40):
            c.create_line(0, y, 900, y, fill="#0f172a")

        c.create_text(20, 20, anchor="nw", text="Arrastra los nodos con el mouse • Haz clic para ver su ficha técnica", fill=TEXT_MUTED, font=("Consolas", 10))

        for u, v in NODE_EDGES:
            x1, y1 = NODES_DATA[u]["x"], NODES_DATA[u]["y"]
            x2, y2 = NODES_DATA[v]["x"], NODES_DATA[v]["y"]
            c.create_line(x1, y1, x2, y2, fill=BORDER_COL, width=3, dash=(4, 2))

        for key, data in NODES_DATA.items():
            x, y = data["x"], data["y"]
            r = 46 if key == self.selected_node else 40
            outline = TEXT_MAIN if key == self.selected_node else data["color"]
            width = 4 if key == self.selected_node else 2
            c.create_oval(x - r, y - r, x + r, y + r, fill=BG_PANEL, outline=outline, width=width)
            c.create_text(x, y, text=data["title"], fill=TEXT_MAIN, font=("Segoe UI", 9, "bold"), width=75, justify="center")

    def _on_node_press(self, event):
        for key, data in NODES_DATA.items():
            if math.hypot(event.x - data["x"], event.y - data["y"]) <= 45:
                self.selected_node = key
                self.dragging_node = key
                self._update_node_panel()
                self._draw_map()
                break

    def _on_node_drag(self, event):
        if self.dragging_node:
            NODES_DATA[self.dragging_node]["x"] = max(50, min(780, event.x))
            NODES_DATA[self.dragging_node]["y"] = max(50, min(580, event.y))
            self._draw_map()

    def _update_node_panel(self):
        d = NODES_DATA[self.selected_node]
        self.node_title_lbl.config(text=d["title"], fg=d["color"])
        self.node_def_lbl.config(text=d["def"])
        self.node_meta_lbl.config(text=f'"{d["metaphor"]}"')
        self.node_ht_lbl.config(text=d["glossary"])

    # =================================================================
    # VISTA 2: BIOSIM (Simulador en Tiempo Real de Mitosis y Meiosis)
    # =================================================================
    def _init_sim_view(self):
        frame = tk.Frame(self.container, bg=BG_MAIN)
        self.views["sim"] = frame

        self.sim_canvas = tk.Canvas(frame, bg=BG_MAIN, highlightthickness=0)
        self.sim_canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        side = tk.Frame(frame, bg=BG_PANEL, width=380, highlightbackground=BORDER_COL, highlightthickness=1)
        side.pack(side="right", fill="y", padx=(0, 10), pady=10)
        side.pack_propagate(False)

        mode_frame = tk.Frame(side, bg=BG_PANEL)
        mode_frame.pack(fill="x", padx=20, pady=15)
        for m in ["Mitosis", "Meiosis"]:
            tk.Button(
                mode_frame, text=m, font=("Segoe UI", 10, "bold"), bg=ACCENT_MIT if m == "Mitosis" else ACCENT_MEI,
                fg=TEXT_MAIN, bd=0, padx=15, pady=6, cursor="hand2",
                command=lambda mode=m: self._set_sim_mode(mode)
            ).pack(side="left", expand=True, fill="x", padx=3)

        self.sim_phase_lbl = tk.Label(side, text="", font=("Segoe UI", 14, "bold"), bg=BG_PANEL, fg=ACCENT_DNA, wraplength=340, justify="left")
        self.sim_phase_lbl.pack(anchor="w", padx=20, pady=(5, 10))

        self.sim_count_lbl = tk.Label(side, text="", font=("Consolas", 11, "bold"), bg=BG_CARD, fg=ACCENT_CEN, padx=10, pady=6)
        self.sim_count_lbl.pack(anchor="w", padx=20, pady=(0, 15), fill="x")

        self.sim_desc_lbl = tk.Label(side, text="", font=("Segoe UI", 10), bg=BG_PANEL, fg=TEXT_MAIN, wraplength=340, justify="left")
        self.sim_desc_lbl.pack(anchor="w", padx=20, pady=(0, 20))

        ctrl = tk.Frame(side, bg=BG_PANEL)
        ctrl.pack(fill="x", padx=20, pady=10)
        tk.Button(ctrl, text="⏮ Anterior", bg=BG_CARD, fg=TEXT_MAIN, bd=0, padx=10, pady=8, command=lambda: self._step_sim(-1)).pack(side="left", padx=2)
        self.play_btn = tk.Button(ctrl, text="▶ Auto", bg=ACCENT_CYT, fg=BG_MAIN, font=("Segoe UI", 9, "bold"), bd=0, padx=14, pady=8, command=self._toggle_play)
        self.play_btn.pack(side="left", expand=True, fill="x", padx=4)
        tk.Button(ctrl, text="Siguiente ⏭", bg=BG_CARD, fg=TEXT_MAIN, bd=0, padx=10, pady=8, command=lambda: self._step_sim(1)).pack(side="left", padx=2)

        self.phase_scale = tk.Scale(side, from_=0, to=4, orient="horizontal", bg=BG_PANEL, fg=TEXT_MAIN, highlightthickness=0, troughcolor=BG_CARD, command=self._on_scale_sim)
        self.phase_scale.pack(fill="x", padx=20, pady=10)

        # Leyenda cromosómica visual
        leg = tk.Frame(side, bg=BG_CARD, padx=12, pady=12)
        leg.pack(fill="x", padx=20, pady=15)
        tk.Label(leg, text="CÓDIGO DE COLORES EN PANTALLA:", font=("Consolas", 9, "bold"), bg=BG_CARD, fg=TEXT_MUTED).pack(anchor="w")
        for col, txt in [(ACCENT_CYT, "● Membrana plasmática"), (ACCENT_DNA, "● Envoltura nuclear / Cromosoma A"), (ACCENT_MIT, "● Cromosoma homólogo B"), (ACCENT_MEI, "● Fragmento recombinado (Crossing-over)"), (ACCENT_CEN, "● Centrosomas y huso mitótico")]:
            tk.Label(leg, text=txt, font=("Segoe UI", 9), bg=BG_CARD, fg=col).pack(anchor="w", pady=1)

        self._update_sim_info()

    def _set_sim_mode(self, mode):
        self.sim_mode = mode
        self.sim_step = 0
        self.phase_scale.set(0)
        self._update_sim_info()

    def _step_sim(self, delta):
        self.sim_step = (self.sim_step + delta) % 5
        self.phase_scale.set(self.sim_step)
        self._update_sim_info()

    def _on_scale_sim(self, val):
        self.sim_step = int(val)
        self._update_sim_info()

    def _toggle_play(self):
        self.sim_playing = not self.sim_playing
        self.play_btn.config(text="⏸ Pausa" if self.sim_playing else "▶ Auto")

    def _update_sim_info(self):
        title, desc, count = SIM_PHASES[self.sim_mode][self.sim_step]
        self.sim_phase_lbl.config(text=f"[{self.sim_mode}] {title}")
        self.sim_desc_lbl.config(text=desc)
        self.sim_count_lbl.config(text=f"📊 Dotación: {count}")

    def _draw_chromosome_x(self, c, x, y, col1, col2=None, split_offset=0):
        col2 = col2 or col1
        c.create_line(x - 12 - split_offset, y - 18, x - split_offset, y, x - 12 - split_offset, y + 18, fill=col1, width=5, smooth=True)
        c.create_line(x + 12 + split_offset, y - 18, x + split_offset, y, x + 12 + split_offset, y + 18, fill=col2, width=5, smooth=True)
        if split_offset == 0:
            c.create_oval(x - 4, y - 4, x + 4, y + 4, fill=ACCENT_CEN, outline="")

    def _draw_sim_canvas(self):
        c = self.sim_canvas
        c.delete("all")
        w, h = c.winfo_width() or 750, c.winfo_height() or 600
        cx, cy = w // 2, h // 2
        wobble = math.sin(self.anim_tick * 3) * 4

        step = self.sim_step
        is_mei = (self.sim_mode == "Meiosis")

        if step < 4:
            stretch = 60 if step == 3 else 0
            c.create_oval(cx - 170 - stretch, cy - 150, cx + 170 + stretch, cy + 150, fill="#062c24", outline=ACCENT_CYT, width=4)
        else:
            if not is_mei:
                for dx in [-140, 140]:
                    c.create_oval(cx + dx - 110, cy - 110, cx + dx + 110, cy + 110, fill="#062c24", outline=ACCENT_CYT, width=4)
                    c.create_oval(cx + dx - 60, cy - 60, cx + dx + 60, cy + 60, outline=ACCENT_DNA, width=2, dash=(4, 2))
                    self._draw_chromosome_x(c, cx + dx - 20, cy + wobble, ACCENT_MIT, split_offset=8)
                    self._draw_chromosome_x(c, cx + dx + 20, cy - wobble, ACCENT_DNA, split_offset=8)
            else:
                positions = [(-160, -110), (160, -110), (-160, 110), (160, 110)]
                for idx, (dx, dy) in enumerate(positions):
                    c.create_oval(cx + dx - 85, cy + dy - 85, cx + dx + 85, cy + dy + 85, fill="#062c24", outline=ACCENT_CYT, width=3)
                    c.create_oval(cx + dx - 45, cy + dy - 45, cx + dx + 45, cy + dy + 45, outline=ACCENT_DNA, width=2, dash=(3, 2))
                    col = ACCENT_MEI if idx % 2 == 0 else ACCENT_DNA
                    self._draw_chromosome_x(c, cx + dx, cy + dy + wobble, col, ACCENT_MIT, split_offset=6)
            return

        pole_l, pole_r = cx - 140, cx + 140
        c.create_oval(pole_l - 8, cy - 8, pole_l + 8, cy + 8, fill=ACCENT_CEN)
        c.create_oval(pole_r - 8, cy - 8, pole_r + 8, cy + 8, fill=ACCENT_CEN)

        if step == 0:
            c.create_oval(cx - 95, cy - 95, cx + 95, cy + 95, fill="#082f49", outline=ACCENT_DNA, width=3, dash=(6, 4))
            if not is_mei:
                for i in range(6):
                    ang = i + self.anim_tick
                    c.create_arc(cx - 60, cy - 60, cx + 60, cy + 60, start=ang * 40, extent=110, style="arc", outline=ACCENT_DNA if i % 2 == 0 else ACCENT_MIT, width=3)
            else:
                self._draw_chromosome_x(c, cx - 18, cy + wobble, ACCENT_MIT, ACCENT_MEI)
                self._draw_chromosome_x(c, cx + 18, cy - wobble, ACCENT_DNA, ACCENT_MEI)
                c.create_text(cx, cy + 125, text="⚡ Crossing-Over (Intercambio genético en Profase I)", fill=ACCENT_MEI, font=("Segoe UI", 10, "bold"))
        elif step == 1:
            for idx, dy in enumerate([-60, -20, 20, 60]):
                c.create_line(pole_l, cy, cx, cy + dy, fill=ACCENT_CEN, dash=(3, 3))
                c.create_line(pole_r, cy, cx, cy + dy, fill=ACCENT_CEN, dash=(3, 3))
                self._draw_chromosome_x(c, cx + (wobble if idx % 2 == 0 else -wobble), cy + dy, ACCENT_MIT if idx % 2 == 0 else ACCENT_DNA, ACCENT_MEI if is_mei else None)
        elif step == 2:
            c.create_line(cx, cy - 140, cx, cy + 140, fill=BORDER_COL, dash=(4, 4))
            for idx, dy in enumerate([-75, -25, 25, 75]):
                c.create_line(pole_l, cy, cx, cy + dy, fill=ACCENT_CEN, width=2)
                c.create_line(pole_r, cy, cx, cy + dy, fill=ACCENT_CEN, width=2)
                offset = 45 if is_mei else 0
                self._draw_chromosome_x(c, cx - offset, cy + dy + wobble * 0.5, ACCENT_MIT, ACCENT_MEI if is_mei else ACCENT_MIT)
                if is_mei:
                    self._draw_chromosome_x(c, cx + offset, cy + dy - wobble * 0.5, ACCENT_DNA, ACCENT_MIT)
        elif step == 3:
            for idx, dy in enumerate([-70, -25, 25, 70]):
                c.create_line(pole_l - 40, cy, cx - 75, cy + dy, fill=ACCENT_CEN, width=2)
                c.create_line(pole_r + 40, cy, cx + 75, cy + dy, fill=ACCENT_CEN, width=2)
                self._draw_chromosome_x(c, cx, cy + dy, ACCENT_MIT, ACCENT_DNA if is_mei else ACCENT_MIT, split_offset=65 + abs(wobble))

    # =================================================================
    # VISTA 3: ZOOM ANATÓMICO (De la Molécula al Cromosoma)
    # =================================================================
    def _init_zoom_view(self):
        frame = tk.Frame(self.container, bg=BG_MAIN)
        self.views["zoom"] = frame

        top_ctrl = tk.Frame(frame, bg=BG_PANEL, pady=12)
        top_ctrl.pack(side="top", fill="x", padx=15, pady=10)

        tk.Label(top_ctrl, text="🔍 Nivel de Empaquetamiento (2 nm → 1400 nm):", font=("Segoe UI", 11, "bold"), bg=BG_PANEL, fg=ACCENT_DNA).pack(side="left", padx=15)
        self.zoom_slider = tk.Scale(top_ctrl, from_=1, to=4, orient="horizontal", bg=BG_PANEL, fg=TEXT_MAIN, length=360, highlightthickness=0, command=self._draw_zoom)
        self.zoom_slider.pack(side="left", padx=15)

        self.zoom_canvas = tk.Canvas(frame, bg=BG_MAIN, highlightthickness=0)
        self.zoom_canvas.pack(fill="both", expand=True, padx=15, pady=(0, 15))

    def _draw_zoom(self, val):
        lvl = int(val)
        c = self.zoom_canvas
        c.delete("all")
        cx, cy = 580, 250

        stages = {
            1: ("NIVEL 1: Doble Hélice de ADN (2 nm)", "Las bases nitrogenadas (A-T, C-G) forman los peldaños de una escalera en espiral.", "Analogía: Las letras y párrafos individuales de una receta de cocina."),
            2: ("NIVEL 2: Histonas y Nucleosomas (11 nm)", "El hilo de ADN da casi dos vueltas alrededor de 8 proteínas histonas (como un collar de perlas).", "Analogía: Enrollar el cable de los audífonos en un carrete organizador."),
            3: ("NIVEL 3: Fibra de Cromatina (30 - 300 nm)", "Los nucleosomas se pliegan en bucles compactos durante la Interfase dentro del núcleo.", "Analogía: Un ovillo de lana denso guardado en un cajón."),
            4: ("NIVEL 4: Cromosoma Metafásico en 'X' (1400 nm)", "Máxima condensación: 2 cromátidas hermanas idénticas sujetas por el centrómero.", "Analogía: La enciclopedia completa encuadernada con tapa dura lista para mudanza.")
        }
        title, desc, metaphor = stages[lvl]

        c.create_text(cx, 40, text=title, fill=ACCENT_DNA, font=("Segoe UI", 18, "bold"))
        c.create_text(cx, 75, text=desc, fill=TEXT_MAIN, font=("Segoe UI", 11))
        c.create_text(cx, 105, text=metaphor, fill=ACCENT_CEN, font=("Segoe UI", 11, "italic"))

        if lvl == 1:
            for i in range(-220, 220, 18):
                y1 = cy + math.sin(i * 0.03) * 65
                y2 = cy - math.sin(i * 0.03) * 65
                c.create_line(cx + i, y1, cx + i, y2, fill=ACCENT_MIT, width=3)
                c.create_oval(cx + i - 5, y1 - 5, cx + i + 5, y1 + 5, fill=ACCENT_DNA, outline="")
                c.create_oval(cx + i - 5, y2 - 5, cx + i + 5, y2 + 5, fill=ACCENT_CYT, outline="")
        elif lvl == 2:
            for i in range(-180, 200, 90):
                c.create_oval(cx + i - 30, cy - 30, cx + i + 30, cy + 30, fill=ACCENT_CEN, outline=TEXT_MAIN, width=2)
                c.create_text(cx + i, cy, text="Histona", fill=BG_MAIN, font=("Segoe UI", 8, "bold"))
                c.create_arc(cx + i - 38, cy - 38, cx + i + 38, cy + 38, start=20, extent=280, style="arc", outline=ACCENT_DNA, width=4)
        elif lvl == 3:
            pts = []
            for i in range(-240, 240, 8):
                pts.extend([cx + i, cy + math.sin(i * 0.15) * 45 + math.cos(i * 0.04) * 35])
            c.create_line(*pts, fill=ACCENT_MIT, width=10, smooth=True)
        elif lvl == 4:
            c.create_line(cx - 70, cy - 110, cx, cy, cx - 70, cy + 110, fill=ACCENT_MIT, width=28, capstyle="round", smooth=True)
            c.create_line(cx + 70, cy - 110, cx, cy, cx + 70, cy + 110, fill=ACCENT_DNA, width=28, capstyle="round", smooth=True)
            c.create_oval(cx - 22, cy - 22, cx + 22, cy + 22, fill=ACCENT_CEN, outline=TEXT_MAIN, width=3)
            c.create_text(cx + 150, cy, text="← Centrómero", fill=ACCENT_CEN, font=("Segoe UI", 11, "bold"))

    # =================================================================
    # VISTA 4: LABORATORIO DE LA VIDA COTIDIANA (Con gráficos propios)
    # =================================================================
    def _init_cases_view(self):
        frame = tk.Frame(self.container, bg=BG_MAIN)
        self.views["cases"] = frame

        cases = [
            ("skin", "🩹 El raspón que cicatriza en 5 días", "PROCESO: MITOSIS EPIDÉRMICA", ACCENT_CYT,
             "Cuando te raspas la rodilla pierdes células epidérmicas. Las células basales vecinas entran en Fase S, duplican su ADN y hacen Mitosis continua rellenando el hueco con clones exactos."),
            ("bone", "📏 El estirón de crecimiento en secundaria", "PROCESO: MITOSIS EN CARTÍLAGO", ACCENT_DNA,
             "Entre los 11 y 14 años los condrocitos en las placas de crecimiento de tus huesos se dividen rápidamente por Mitosis, empujando el hueso hacia arriba."),
            ("family", "👨‍👩‍👧‍👦 ¿Por qué no eres fotocopia de tus hermanos?", "PROCESO: MEIOSIS + CROSSING-OVER", ACCENT_MEI,
             "En la Profase I de la Meiosis los cromosomas de tus padres intercambian piezas al azar. Hay más de 70 billones de combinaciones posibles por cada gameto."),
            ("axolotl", "🦎 El ajolote que regenera su extremidad", "PROCESO: MITOSIS + BLASTEMA", ACCENT_MIT,
             "Al perder una pata, las células del ajolote se desdiferencian formando un blastema y se multiplican por Mitosis reconstruyendo hueso, nervios y piel.")
        ]

        grid = tk.Frame(frame, bg=BG_MAIN)
        grid.pack(fill="both", expand=True, padx=20, pady=15)

        for idx, (art_key, title, tag, col, body) in enumerate(cases):
            r, c_idx = divmod(idx, 2)
            card = tk.Frame(grid, bg=BG_PANEL, highlightbackground=col, highlightthickness=2, padx=16, pady=14)
            card.grid(row=r, column=c_idx, sticky="nsew", padx=10, pady=10)
            grid.grid_rowconfigure(r, weight=1)
            grid.grid_columnconfigure(c_idx, weight=1)

            top_row = tk.Frame(card, bg=BG_PANEL)
            top_row.pack(fill="x")

            # Ilustración vectorial autogenerada (Reemplaza imágenes externas)
            art = tk.Canvas(top_row, width=110, height=85, bg=BG_MAIN, highlightthickness=1, highlightbackground=BORDER_COL)
            art.pack(side="left", padx=(0, 14))
            self._draw_case_illustration(art, art_key)

            txt_box = tk.Frame(top_row, bg=BG_PANEL)
            txt_box.pack(side="left", fill="both", expand=True)
            tk.Label(txt_box, text=tag, font=("Consolas", 9, "bold"), bg=BG_PANEL, fg=col).pack(anchor="w")
            tk.Label(txt_box, text=title, font=("Segoe UI", 13, "bold"), bg=BG_PANEL, fg=TEXT_MAIN, wraplength=340, justify="left").pack(anchor="w", pady=(4, 0))

            tk.Label(card, text=body, font=("Segoe UI", 10), bg=BG_PANEL, fg=TEXT_MUTED, wraplength=480, justify="left").pack(anchor="w", pady=(12, 0))

    def _draw_case_illustration(self, c, kind):
        if kind == "skin":
            # Capas de células epidérmicas cerrando una herida
            for x in range(10, 105, 22):
                c.create_rectangle(x, 55, x + 18, 75, fill="#064e3b", outline=ACCENT_CYT)
                c.create_oval(x + 6, 61, x + 12, 67, fill=ACCENT_DNA, outline="")
            c.create_line(35, 30, 55, 50, 75, 30, fill=ACCENT_MEI, width=3)
            c.create_text(55, 16, text="Clonación 2n", fill=ACCENT_CYT, font=("Consolas", 8))
        elif kind == "bone":
            # Placa epifisaria ósea en división
            c.create_rectangle(40, 10, 70, 75, fill="#1e293b", outline=TEXT_MAIN, width=2)
            c.create_rectangle(40, 35, 70, 50, fill=ACCENT_DNA, outline="")
            c.create_text(55, 42, text="MITOSIS", fill=BG_MAIN, font=("Consolas", 7, "bold"))
        elif kind == "family":
            # Cromosomas recombinados
            self._draw_chromosome_x(c, 35, 45, ACCENT_MIT, ACCENT_MEI)
            self._draw_chromosome_x(c, 75, 45, ACCENT_DNA, ACCENT_MIT)
        elif kind == "axolotl":
            # Blastema regenerativo con células dividiéndose
            c.create_oval(20, 20, 90, 70, fill="#3b0764", outline=ACCENT_MIT, width=2)
            for dx, dy in [(40, 40), (65, 35), (55, 55)]:
                c.create_oval(dx - 7, dy - 7, dx + 7, dy + 7, outline=ACCENT_CYT, width=2)

    # =================================================================
    # VISTA 5: BIOGUÍA LOCAL + MICROSCOPIO VIRTUAL (Cero Archivos)
    # =================================================================
    def _init_tutor_view(self):
        frame = tk.Frame(self.container, bg=BG_MAIN)
        self.views["tutor"] = frame

        # Mitad Izquierda: Chatbot Local BioGuía
        chat_panel = tk.Frame(frame, bg=BG_PANEL, highlightbackground=BORDER_COL, highlightthickness=1)
        chat_panel.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        tk.Label(chat_panel, text="🤖 Tutor 'BioGuía' (Motor Local Offline)", font=("Segoe UI", 13, "bold"), bg=BG_PANEL, fg=ACCENT_DNA).pack(anchor="w", padx=15, pady=12)

        self.chat_log = tk.Text(chat_panel, bg=BG_MAIN, fg=TEXT_MAIN, font=("Segoe UI", 10), bd=0, padx=12, pady=12, wrap="word", state="disabled", height=18)
        self.chat_log.pack(fill="both", expand=True, padx=15)

        q_frame = tk.Frame(chat_panel, bg=BG_PANEL)
        q_frame.pack(fill="x", padx=15, pady=8)
        for q_txt in ["¿Qué pasa si no duplica su ADN?", "Diferencia cromátida vs cromosoma", "Mitosis vs Meiosis"]:
            tk.Button(q_frame, text=q_txt, bg=BG_CARD, fg=ACCENT_CEN, font=("Segoe UI", 8, "bold"), bd=0, padx=8, pady=5, cursor="hand2", command=lambda q=q_txt: self._ask_tutor(q)).pack(side="left", padx=3)

        inp_frame = tk.Frame(chat_panel, bg=BG_PANEL)
        inp_frame.pack(fill="x", padx=15, pady=12)
        self.chat_entry = tk.Entry(inp_frame, bg=BG_CARD, fg=TEXT_MAIN, insertbackground=TEXT_MAIN, font=("Segoe UI", 10), bd=0)
        self.chat_entry.pack(side="left", fill="x", expand=True, ipady=8, padx=(0, 8))
        self.chat_entry.bind("<Return>", lambda e: self._ask_tutor())
        tk.Button(inp_frame, text="Preguntar", bg=ACCENT_DNA, fg=BG_MAIN, font=("Segoe UI", 10, "bold"), bd=0, padx=15, pady=6, command=self._ask_tutor).pack(side="right")

        self._append_chat("BioGuía", "¡Hola! Soy tu asistente local integrado en Python. Haz clic en una pregunta rápida o escribe tu duda sobre el ciclo celular.")

        # Mitad Derecha: Microscopio Virtual con Láminas Autogeneradas
        scan_panel = tk.Frame(frame, bg=BG_PANEL, width=470, highlightbackground=BORDER_COL, highlightthickness=1)
        scan_panel.pack(side="right", fill="y", padx=(0, 10), pady=10)
        scan_panel.pack_propagate(False)

        tk.Label(scan_panel, text="🔬 Microscopio y Analizador de Muestras", font=("Segoe UI", 13, "bold"), bg=BG_PANEL, fg=ACCENT_MIT).pack(anchor="w", padx=15, pady=(12, 4))

        nav_slide = tk.Frame(scan_panel, bg=BG_PANEL)
        nav_slide.pack(fill="x", padx=15, pady=4)
        tk.Button(nav_slide, text="◀ Muestra Anterior", bg=BG_CARD, fg=TEXT_MAIN, bd=0, padx=10, pady=4, command=lambda: self._change_slide(-1)).pack(side="left")
        self.slide_title_lbl = tk.Label(nav_slide, text="", font=("Consolas", 9, "bold"), bg=BG_PANEL, fg=ACCENT_CEN)
        self.slide_title_lbl.pack(side="left", expand=True)
        tk.Button(nav_slide, text="Siguiente Muestra ▶", bg=BG_CARD, fg=TEXT_MAIN, bd=0, padx=10, pady=4, command=lambda: self._change_slide(1)).pack(side="right")

        # Visor circular de microscopio dibujado por código
        self.slide_canvas = tk.Canvas(scan_panel, width=430, height=210, bg=BG_MAIN, highlightthickness=1, highlightbackground=BORDER_COL)
        self.slide_canvas.pack(padx=15, pady=8)

        self.slide_q_lbl = tk.Label(scan_panel, text="", font=("Segoe UI", 9), bg=BG_PANEL, fg=TEXT_MUTED, wraplength=430, justify="left")
        self.slide_q_lbl.pack(anchor="w", padx=15, pady=4)

        tk.Label(scan_panel, text="Identifica la fase que muestra el lente:", font=("Segoe UI", 10, "bold"), bg=BG_PANEL, fg=TEXT_MAIN).pack(anchor="w", padx=15, pady=(6, 4))

        options = [
            "Interfase (Cromatina descondensada)",
            "Profase I de Meiosis (Crossing-Over)",
            "Metafase (Mitosis)",
            "Anafase (Separación de cromátidas)"
        ]
        for opt in options:
            tk.Button(
                scan_panel, text=f"• {opt}", bg=BG_CARD, fg=TEXT_MAIN, font=("Segoe UI", 9),
                anchor="w", bd=0, padx=10, pady=5, cursor="hand2",
                command=lambda o=opt: self._check_slide_answer(o)
            ).pack(fill="x", padx=15, pady=2)

        self.scan_result_lbl = tk.Label(scan_panel, text="Selecciona una opción para diagnosticar la lámina.", bg=BG_MAIN, fg=ACCENT_CYT, font=("Segoe UI", 9, "bold"), wraplength=420, justify="left", pady=10, padx=10)
        self.scan_result_lbl.pack(fill="x", padx=15, pady=8)

    def _change_slide(self, delta):
        self.current_slide_idx = (self.current_slide_idx + delta) % len(SYNTHETIC_SLIDES)
        self._render_synthetic_slide()

    def _render_synthetic_slide(self):
        slide = SYNTHETIC_SLIDES[self.current_slide_idx]
        self.slide_title_lbl.config(text=f"Lámina {self.current_slide_idx + 1}/{len(SYNTHETIC_SLIDES)}")
        self.slide_q_lbl.config(text=f"Pista visual: {slide['question']}")
        self.scan_result_lbl.config(text=f"Observando: {slide['name']}", fg=ACCENT_DNA)

        c = self.slide_canvas
        c.delete("all")
        cx, cy = 215, 105
        # Lente de microscopio
        c.create_oval(cx - 95, cy - 95, cx + 95, cy + 95, fill="#041f1e", outline=ACCENT_CYT, width=3)
        c.create_line(cx - 95, cy, cx - 75, cy, fill=BORDER_COL)
        c.create_line(cx + 75, cy, cx + 95, cy, fill=BORDER_COL)
        c.create_text(12, 12, anchor="nw", text="400x ÓPTICO", fill=ACCENT_CYT, font=("Consolas", 8))

        stype = slide["type"]
        if stype == "metafase":
            c.create_line(cx, cy - 80, cx, cy + 80, fill=BORDER_COL, dash=(3, 3))
            for dy in [-45, -15, 15, 45]:
                c.create_line(cx - 75, cy, cx, cy + dy, fill=ACCENT_CEN)
                c.create_line(cx + 75, cy, cx, cy + dy, fill=ACCENT_CEN)
                self._draw_chromosome_x(c, cx, cy + dy, ACCENT_MIT)
        elif stype == "anafase":
            for dy in [-40, -12, 12, 40]:
                self._draw_chromosome_x(c, cx, cy + dy, ACCENT_MIT, split_offset=42)
                c.create_line(cx - 80, cy, cx - 42, cy + dy, fill=ACCENT_CEN)
                c.create_line(cx + 80, cy, cx + 42, cy + dy, fill=ACCENT_CEN)
        elif stype == "crossing":
            self._draw_chromosome_x(c, cx - 14, cy, ACCENT_MIT, ACCENT_MEI)
            self._draw_chromosome_x(c, cx + 14, cy, ACCENT_DNA, ACCENT_MEI)
            c.create_oval(cx - 28, cy - 28, cx + 28, cy + 28, outline=ACCENT_CEN, dash=(2, 2))
        elif stype == "interfase":
            c.create_oval(cx - 55, cy - 55, cx + 55, cy + 55, fill="#082f49", outline=ACCENT_DNA, width=2)
            for i in range(5):
                c.create_arc(cx - 40, cy - 40, cx + 40, cy + 40, start=i * 70, extent=100, style="arc", outline=ACCENT_MIT if i % 2 else ACCENT_DNA, width=2)

    def _check_slide_answer(self, chosen):
        slide = SYNTHETIC_SLIDES[self.current_slide_idx]
        if chosen == slide["correct"]:
            self.scan_result_lbl.config(text=f"✅ {slide['explanation']}", fg=ACCENT_CYT)
        else:
            self.scan_result_lbl.config(text=f"❌ No exactamente. Fíjate bien en la pista visual: {slide['question']}", fg=ACCENT_MEI)

    def _append_chat(self, sender, msg):
        self.chat_log.config(state="normal")
        self.chat_log.insert("end", f"{sender}: {msg}\n\n")
        self.chat_log.see("end")
        self.chat_log.config(state="disabled")

    def _ask_tutor(self, preset_q=None):
        q = preset_q or self.chat_entry.get().strip()
        if not q:
            return
        if not preset_q:
            self.chat_entry.delete(0, "end")
        self._append_chat("Tú", q)

        q_low = q.lower()
        ans = "Pista clave: en la Interfase el ADN se duplica (Fase S), en la Mitosis se divide en 2 células clones (2n) y en la Meiosis se recombina (crossing-over) para dar 4 gametos haploides (n). Pregúntame por 'mitosis', 'meiosis', 'cromátida' o 'interfase'."
        for keywords, reply in CHAT_KNOWLEDGE:
            if any(k in q_low for k in keywords):
                ans = reply
                break
        self._append_chat("BioGuía", ans)

    # =================================================================
    # BUCLE DE ANIMACIÓN A 30 FPS
    # =================================================================
    def _animate_loop(self):
        self.anim_tick += 0.08
        if self.views["sim"].winfo_ismapped():
            if self.sim_playing and int(self.anim_tick * 10) % 45 == 0:
                self._step_sim(1)
            self._draw_sim_canvas()
        self.after(35, self._animate_loop)

if __name__ == "__main__":
    app = CitoLabApp()
    app.mainloop()