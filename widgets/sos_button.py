
import tkinter as tk

class SOSButton(tk.Canvas):
    def __init__(self, parent, command=None, bg="#ffd5c7", **kwargs):
        # Get screen width for responsive sizing
        screen_width = parent.winfo_screenwidth()
        
        # Responsive button size (30-50% of screen width, min 250, max 500)
        self.btn_w = max(150, min(350, int(screen_width * 0.4)))
        self.btn_h = int(self.btn_w * 0.28)  # Maintain aspect ratio
        self.pad = int(self.btn_h * 0.15)    # Proportional padding
        
        self.radius = self.btn_h // 2
        
        total_w = self.btn_w + self.pad * 2
        total_h = self.btn_h + self.pad * 2
        
        super().__init__(parent, width=total_w, height=total_h,
                         bg=bg, highlightthickness=0)
        self.command = command
        self.bg = bg
        
        # Store responsive fonts
        self.font_size = max(16, min(28, int(self.btn_w * 0.05)))
        
        self._draw()
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<Button-1>", self._on_click)
        
        # Bind to parent resize if needed
        self.bind("<Configure>", self._on_resize)

    def _draw_pill_filled(self, x1, y1, x2, y2, r, fill):
        """Draw a solid filled pill shape."""
        self.create_rectangle(x1 + r, y1, x2 - r, y2, fill=fill, outline="")
        self.create_rectangle(x1, y1 + r, x2, y2 - r, fill=fill, outline="")
        self.create_oval(x1, y1, x1 + r*2, y1 + r*2, fill=fill, outline="")
        self.create_oval(x2 - r*2, y1, x2, y1 + r*2, fill=fill, outline="")
        self.create_oval(x1, y2 - r*2, x1 + r*2, y2, fill=fill, outline="")
        self.create_oval(x2 - r*2, y2 - r*2, x2, y2, fill=fill, outline="")

    def _draw_pill_outline(self, x1, y1, x2, y2, r, color, width):
        """Draw only the outline of a pill shape using arcs + lines. No fill."""
        # Corner arcs using style='arc' — no fill bleed, no stray lines
        self.create_arc(x1, y1, x1 + r*2, y1 + r*2,
                        start=90, extent=90,
                        style="arc", outline=color, width=width)
        self.create_arc(x2 - r*2, y1, x2, y1 + r*2,
                        start=0, extent=90,
                        style="arc", outline=color, width=width)
        self.create_arc(x1, y2 - r*2, x1 + r*2, y2,
                        start=180, extent=90,
                        style="arc", outline=color, width=width)
        self.create_arc(x2 - r*2, y2 - r*2, x2, y2,
                        start=270, extent=90,
                        style="arc", outline=color, width=width)
        # Straight edges
        self.create_line(x1 + r, y1,   x2 - r, y1,   fill=color, width=width)  # top
        self.create_line(x1 + r, y2,   x2 - r, y2,   fill=color, width=width)  # bottom
        self.create_line(x1,     y1+r, x1,     y2-r, fill=color, width=width)  # left
        self.create_line(x2,     y1+r, x2,     y2-r, fill=color, width=width)  # right

    def _draw(self, outline_gap=0, fill="#9D1919", text_color="#f7c1c1"):
        self.delete("all")

        cx = (self.btn_w + self.pad * 2) // 2
        cy = (self.btn_h + self.pad * 2) // 2

        x1 = self.pad
        y1 = self.pad
        x2 = self.pad + self.btn_w
        y2 = self.pad + self.btn_h
        r  = self.radius

        # Outline ring — only drawn on hover
        if outline_gap > 0:
            gap = 4 + outline_gap
            # Cap ring radius so it never exceeds half the ring's own height
            ring_h = self.btn_h + gap * 2
            ring_r = min(r + gap, ring_h // 2)
            self._draw_pill_outline(
                x1 - gap, y1 - gap, x2 + gap, y2 + gap,
                ring_r, color="#e24b4a", width=4   # Thinner border for smaller screens
            )

        # Filled pill body
        self._draw_pill_filled(x1, y1, x2, y2, r, fill)

        # Label with responsive font
        self.create_text(cx, cy, text="📢 SOS  HELP",
                         fill=text_color, font=("Arial", self.font_size, "bold"))

    def _animate_in(self, step=0):
        if step > 8:
            return
        progress = step / 8
        r_val = int(0x50 + (0x79 - 0x50) * progress)
        g_val = int(0x13 + (0x1f - 0x13) * progress)
        b_val = int(0x13 + (0x1f - 0x13) * progress)
        self._draw(outline_gap=step,
                   fill=f"#{r_val:02x}{g_val:02x}{b_val:02x}",
                   text_color="white")
        self.after(18, lambda: self._animate_in(step + 1))

    def _animate_out(self, step=8):
        if step < 0:
            self._draw(outline_gap=0, fill="#9d1919", text_color="#f7c1c1")
            return
        progress = step / 8
        r_val = int(0x50 + (0x79 - 0x50) * progress)
        g_val = int(0x13 + (0x1f - 0x13) * progress)
        b_val = int(0x13 + (0x1f - 0x13) * progress)
        self._draw(outline_gap=step,
                   fill=f"#{r_val:02x}{g_val:02x}{b_val:02x}",
                   text_color="white")
        self.after(18, lambda: self._animate_out(step - 1))

    def _on_resize(self, event=None):
        """Handle resize if needed (optional)"""
        pass

    def _on_enter(self, e):
        self._animate_in()

    def _on_leave(self, e):
        self._animate_out()

    def _on_click(self, e):
        if self.command:
            self.command()