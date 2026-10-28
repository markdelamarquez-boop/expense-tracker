from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.graphics import Color, RoundedRectangle, Ellipse

class GlassCard(BoxLayout):
    """Modern Clean White Card Container"""
    def __init__(self, bg_color=(1, 1, 1, 1), radius=16, border_color=(0.85, 0.88, 0.92, 1), **kwargs):
        super().__init__(**kwargs)
        self.bg_color = bg_color
        self.radius = radius
        self.border_color = border_color
        
        with self.canvas.before:
            if self.border_color:
                Color(*self.border_color)
                self.border_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[self.radius])
            Color(*self.bg_color)
            self.rect = RoundedRectangle(
                pos=(self.pos[0] + 1, self.pos[1] + 1) if self.border_color else self.pos,
                size=(self.size[0] - 2, self.size[1] - 2) if self.border_color else self.size,
                radius=[self.radius]
            )
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, instance, value):
        if self.border_color:
            self.border_rect.pos = instance.pos
            self.border_rect.size = instance.size
            self.rect.pos = (instance.pos[0] + 1, instance.pos[1] + 1)
            self.rect.size = (instance.size[0] - 2, instance.size[1] - 2)
        else:
            self.rect.pos = instance.pos
            self.rect.size = instance.size


class ModernButton(Button):
    """Custom Styled Action Button (Clean Theme)"""
    def __init__(self, bg_color=(0.15, 0.45, 0.95, 1), text_color=(1, 1, 1, 1), radius=12, **kwargs):
        super().__init__(**kwargs)
        self.background_color = (0, 0, 0, 0)
        self.bg_color = bg_color
        self.color = text_color
        self.radius = radius
        
        with self.canvas.before:
            Color(*self.bg_color)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[self.radius])
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


class ModernInput(TextInput):
    """Sleek Styled Light Input Field"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_active = ''
        self.background_color = (0.95, 0.97, 1, 1)
        self.foreground_color = (0.1, 0.15, 0.25, 1)
        self.hint_text_color = (0.5, 0.55, 0.65, 1)
        self.cursor_color = (0.15, 0.45, 0.95, 1)
        self.padding = [14, 12, 14, 12]


class LogoBadge(BoxLayout):
    """Custom Modern Circular Logo Badge"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint = (None, None)
        self.size = (70, 70)
        self.pos_hint = {'center_x': 0.5}
        
        with self.canvas.before:
            Color(0.15, 0.45, 0.95, 1)
            self.circle = Ellipse(pos=self.pos, size=self.size)
            
        self.bind(pos=self.update_circle, size=self.update_circle)
        
        lbl = Label(
            text="$", 
            font_size='36sp', 
            bold=True, 
            color=(1, 1, 1, 1),
            halign='center',
            valign='middle'
        )
        self.add_widget(lbl)

    def update_circle(self, instance, value):
        self.circle.pos = instance.pos
        self.circle.size = instance.size


def show_custom_popup(title, message):
    content = BoxLayout(orientation='vertical', padding=20, spacing=15)
    
    # Nilagyan ng solid white background at rounded rectangle para hindi maging itim
    with content.canvas.before:
        Color(1, 1, 1, 1)  # Pure White
        self_rect = RoundedRectangle(pos=content.pos, size=content.size, radius=[16])
    content.bind(pos=lambda inst, val: setattr(self_rect, 'pos', val),
                 size=lambda inst, val: setattr(self_rect, 'size', val))

    msg_lbl = Label(
        text=message, 
        color=(0.1, 0.15, 0.25, 1),  # Dark text para madaling basahin
        font_size='14sp',
        halign='center',
        valign='middle'
    )
    msg_lbl.bind(size=msg_lbl.setter('text_size'))
    content.add_widget(msg_lbl)
    
    btn = ModernButton(
        text="OK", 
        bg_color=(0.15, 0.45, 0.95, 1), 
        size_hint_y=None, 
        height=45,
        bold=True
    )
    content.add_widget(btn)
    
    popup = Popup(
        title=title, 
        content=content, 
        size_hint=(0.8, 0.28),
        background=''
    )
    btn.bind(on_press=popup.dismiss)
    popup.open()