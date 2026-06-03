import tkinter as tk
import random
import time

# =====================
# CONSTANTS
# =====================
CANVAS_WIDTH = 500
CANVAS_HEIGHT = 600

PADDLE_WIDTH = 80
PADDLE_HEIGHT = 12
PADDLE_Y = CANVAS_HEIGHT - 40
PADDLE_COLOR = "#FFFFFF"

BALL_RADIUS = 10
BALL_COLOR = "#FFFFFF"

BRICK_ROWS = 10
BRICKS_PER_ROW = 10
BRICK_GAP = 4
BRICK_HEIGHT = 12
BRICK_TOP_OFFSET = 50
BRICK_WIDTH = (CANVAS_WIDTH - BRICK_GAP * (BRICKS_PER_ROW + 1)) / BRICKS_PER_ROW

BRICK_COLORS = [
    "#FF3B3B", "#FF3B3B",
    "#FF8C00", "#FF8C00",
    "#FFD700", "#FFD700",
    "#39D353", "#39D353",
    "#00CFFF", "#00CFFF",
]

NUM_TURNS = 3
BALL_SPEED_X = 4
BALL_SPEED_Y = 5
FRAME_DELAY = 10  # ms


class Breakout:
    def __init__(self, root):
        self.root = root
        self.root.title("Breakout")
        self.root.resizable(False, False)
        self.root.configure(bg="#0a0a0f")

        # Canvas con fondo oscuro
        self.canvas = tk.Canvas(
            root,
            width=CANVAS_WIDTH,
            height=CANVAS_HEIGHT,
            bg="#0a0a0f",
            highlightthickness=0
        )
        self.canvas.pack(padx=20, pady=20)

        # Estado del juego
        self.bricks = []
        self.bricks_remaining = 0
        self.turn = 0
        self.mouse_x = CANVAS_WIDTH / 2
        self.running = False
        self.ball_x = 0
        self.ball_y = 0
        self.change_x = 0
        self.change_y = 0
        self.paddle = None
        self.ball = None
        self.message = None
        self.score_text = None
        self.lives_text = None

        # Rastrear mouse
        self.canvas.bind("<Motion>", self.on_mouse_move)

        self.setup_game()

    def on_mouse_move(self, event):
        self.mouse_x = event.x

    def setup_game(self):
        """Configura el estado inicial del juego."""
        self.canvas.delete("all")
        self.bricks = []
        self.turn = 0

        self.draw_background_grid()
        self.create_bricks()
        self.bricks_remaining = len(self.bricks)
        self.paddle = self.create_paddle()
        self.ball = self.create_ball()

        self.score = 0
        self.score_text = self.canvas.create_text(
            10, 8, anchor="nw",
            text="SCORE: 0",
            fill="#555577", font=("Courier", 10, "bold")
        )
        self.lives_text = self.canvas.create_text(
            CANVAS_WIDTH - 10, 8, anchor="ne",
            text=f"VIDAS: {NUM_TURNS}",
            fill="#555577", font=("Courier", 10, "bold")
        )

        self.show_message("BREAKOUT", "Haz clic para comenzar", "#00CFFF")
        self.canvas.bind("<Button-1>", self.start_turn)

    def draw_background_grid(self):
        """Dibuja una grilla sutil de fondo."""
        for x in range(0, CANVAS_WIDTH, 40):
            self.canvas.create_line(x, 0, x, CANVAS_HEIGHT, fill="#111122", width=1)
        for y in range(0, CANVAS_HEIGHT, 40):
            self.canvas.create_line(0, y, CANVAS_WIDTH, y, fill="#111122", width=1)

    def create_bricks(self):
        for row in range(BRICK_ROWS):
            color = BRICK_COLORS[row]
            for col in range(BRICKS_PER_ROW):
                x1 = BRICK_GAP + col * (BRICK_WIDTH + BRICK_GAP)
                y1 = BRICK_TOP_OFFSET + row * (BRICK_HEIGHT + BRICK_GAP)
                x2 = x1 + BRICK_WIDTH
                y2 = y1 + BRICK_HEIGHT
                # Sombra / glow sutil
                self.canvas.create_rectangle(
                    x1 + 1, y1 + 1, x2 + 1, y2 + 1,
                    fill="", outline=color, stipple="gray25"
                )
                brick = self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=color, outline="#0a0a0f", width=1
                )
                self.bricks.append(brick)

    def create_paddle(self):
        px = (CANVAS_WIDTH - PADDLE_WIDTH) / 2
        # Brillo del paddle
        self.canvas.create_rectangle(
            px, PADDLE_Y, px + PADDLE_WIDTH, PADDLE_Y + 2,
            fill="#AADDFF", outline=""
        )
        return self.canvas.create_rectangle(
            px, PADDLE_Y,
            px + PADDLE_WIDTH, PADDLE_Y + PADDLE_HEIGHT,
            fill=PADDLE_COLOR, outline="#88BBDD", width=1
        )

    def create_ball(self):
        self.ball_x = CANVAS_WIDTH / 2
        self.ball_y = CANVAS_HEIGHT / 2
        return self.canvas.create_oval(
            self.ball_x - BALL_RADIUS,
            self.ball_y - BALL_RADIUS,
            self.ball_x + BALL_RADIUS,
            self.ball_y + BALL_RADIUS,
            fill=BALL_COLOR, outline="#AAEEFF", width=1
        )

    def show_message(self, title, subtitle="", color="#FFFFFF"):
        """Muestra un mensaje centrado."""
        if self.message:
            for item in self.message:
                self.canvas.delete(item)

        items = []
        t1 = self.canvas.create_text(
            CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2 - 16,
            text=title, fill=color,
            font=("Courier", 22, "bold"), anchor="center"
        )
        items.append(t1)
        if subtitle:
            t2 = self.canvas.create_text(
                CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2 + 14,
                text=subtitle, fill="#888899",
                font=("Courier", 11), anchor="center"
            )
            items.append(t2)
        self.message = items

    def clear_message(self):
        if self.message:
            for item in self.message:
                self.canvas.delete(item)
            self.message = None

    def start_turn(self, event=None):
        """Inicia un turno nuevo."""
        if self.running:
            return
        self.canvas.unbind("<Button-1>")
        self.clear_message()

        # Resetear pelota al centro
        self.ball_x = CANVAS_WIDTH / 2
        self.ball_y = CANVAS_HEIGHT / 2
        self.canvas.coords(
            self.ball,
            self.ball_x - BALL_RADIUS, self.ball_y - BALL_RADIUS,
            self.ball_x + BALL_RADIUS, self.ball_y + BALL_RADIUS
        )

        # Velocidad aleatoria en x, siempre hacia abajo
        self.change_x = random.choice([-1, 1]) * BALL_SPEED_X
        self.change_y = BALL_SPEED_Y

        self.running = True
        self.game_loop()

    def game_loop(self):
        if not self.running:
            return

        self.move_ball()
        self.move_paddle()
        self.check_collisions()

        self.root.after(FRAME_DELAY, self.game_loop)

    def move_ball(self):
        self.ball_x += self.change_x
        self.ball_y += self.change_y

        self.canvas.coords(
            self.ball,
            self.ball_x - BALL_RADIUS, self.ball_y - BALL_RADIUS,
            self.ball_x + BALL_RADIUS, self.ball_y + BALL_RADIUS
        )

    def move_paddle(self):
        # Clampear para no salirse
        px = self.mouse_x - PADDLE_WIDTH / 2
        px = max(0, min(CANVAS_WIDTH - PADDLE_WIDTH, px))
        self.canvas.coords(
            self.paddle,
            px, PADDLE_Y,
            px + PADDLE_WIDTH, PADDLE_Y + PADDLE_HEIGHT
        )

    def check_collisions(self):
        bx, by = self.ball_x, self.ball_y

        # --- Pared izquierda / derecha ---
        if bx - BALL_RADIUS <= 0:
            self.ball_x = BALL_RADIUS
            self.change_x = abs(self.change_x)
        elif bx + BALL_RADIUS >= CANVAS_WIDTH:
            self.ball_x = CANVAS_WIDTH - BALL_RADIUS
            self.change_x = -abs(self.change_x)

        # --- Pared superior ---
        if by - BALL_RADIUS <= 0:
            self.ball_y = BALL_RADIUS
            self.change_y = abs(self.change_y)

        # --- Pared inferior → pierde turno ---
        if by + BALL_RADIUS >= CANVAS_HEIGHT:
            self.running = False
            self.turn_lost()
            return

        # --- Colisión con objetos ---
        collider = self.get_collider()

        if collider is None:
            return

        paddle_coords = self.canvas.coords(self.paddle)

        if collider == self.paddle:
            # Rebotar hacia arriba, reposicionar encima del paddle
            self.change_y = -abs(self.change_y)
            self.ball_y = PADDLE_Y - BALL_RADIUS - 1
            # Variar ángulo según dónde golpeó el paddle
            paddle_center = (paddle_coords[0] + paddle_coords[2]) / 2
            offset = (self.ball_x - paddle_center) / (PADDLE_WIDTH / 2)
            self.change_x = offset * BALL_SPEED_X * 1.5

        elif collider in self.bricks:
            self.canvas.delete(collider)
            self.bricks.remove(collider)
            self.bricks_remaining -= 1
            self.change_y = -self.change_y

            # Actualizar score
            self.score += 10
            self.canvas.itemconfig(self.score_text, text=f"SCORE: {self.score}")

            if self.bricks_remaining == 0:
                self.running = False
                self.game_won()

    def get_collider(self):
        """Revisa las 4 esquinas del bounding box de la pelota."""
        bx, by = self.ball_x, self.ball_y
        r = BALL_RADIUS
        corners = [
            (bx - r, by - r),
            (bx + r, by - r),
            (bx - r, by + r),
            (bx + r, by + r),
        ]
        for (cx, cy) in corners:
            items = self.canvas.find_overlapping(cx, cy, cx, cy)
            for item in items:
                if item != self.ball:
                    return item
        return None

    def turn_lost(self):
        self.turn += 1
        remaining = NUM_TURNS - self.turn

        self.canvas.itemconfig(self.lives_text, text=f"VIDAS: {remaining}")

        if self.turn >= NUM_TURNS:
            self.game_over()
        else:
            self.show_message(
                f"¡PERDISTE LA PELOTA!",
                f"Te quedan {remaining} vida(s) — Clic para continuar",
                "#FF8C00"
            )
            self.canvas.bind("<Button-1>", self.start_turn)

    def game_over(self):
        self.show_message("GAME OVER", f"Score final: {self.score}  — Clic para reiniciar", "#FF3B3B")
        self.canvas.bind("<Button-1>", lambda e: self.setup_game())

    def game_won(self):
        self.show_message("¡GANASTE! 🎉", f"Score: {self.score}  — Clic para reiniciar", "#39D353")
        self.canvas.bind("<Button-1>", lambda e: self.setup_game())


def main():
    root = tk.Tk()
    game = Breakout(root)
    root.mainloop()


if __name__ == "__main__":
    main()
