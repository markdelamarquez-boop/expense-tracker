import sqlite3
from datetime import datetime

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import Screen, FadeTransition
from kivy.graphics import Color, RoundedRectangle

from database import conn, cursor
from components import GlassCard, ModernButton, ModernInput, LogoBadge, show_custom_popup

# --- SCREENS ---

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        main_layout = BoxLayout(orientation='vertical', padding=[30, 40, 30, 40], spacing=20)

        header_box = BoxLayout(orientation='vertical', spacing=10, size_hint_y=0.35)
        header_box.add_widget(LogoBadge())
        
        header_box.add_widget(Label(
            text="Expense Tracker", 
            font_size='26sp', 
            bold=True, 
            color=(0.1, 0.15, 0.25, 1),
            size_hint_y=0.3
        ))
        header_box.add_widget(Label(
            text="Manage your personal budget wisely", 
            font_size='13sp', 
            color=(0.4, 0.48, 0.58, 1),
            size_hint_y=0.2
        ))
        main_layout.add_widget(header_box)

        form_card = GlassCard(
            orientation='vertical', 
            padding=18, 
            spacing=12, 
            size_hint_y=0.38,
            bg_color=(1, 1, 1, 1),
            border_color=(0.85, 0.88, 0.92, 1)
        )

        self.username_input = ModernInput(hint_text="Username", multiline=False)
        self.password_input = ModernInput(hint_text="Password", password=True, multiline=False)

        form_card.add_widget(self.username_input)
        form_card.add_widget(self.password_input)

        btn_login = ModernButton(
            text="SIGN IN", 
            bg_color=(0.15, 0.45, 0.95, 1), 
            bold=True,
            font_size='15sp'
        )
        btn_login.bind(on_press=self.do_login)
        form_card.add_widget(btn_login)

        main_layout.add_widget(form_card)

        actions_box = BoxLayout(orientation='vertical', spacing=10, size_hint_y=0.2)
        btn_register = ModernButton(
            text="Don't have an account? Sign Up", 
            bg_color=(0.9, 0.93, 0.98, 1), 
            text_color=(0.15, 0.45, 0.95, 1),
            font_size='13sp'
        )
        btn_register.bind(on_press=self.go_to_register)
        actions_box.add_widget(btn_register)

        main_layout.add_widget(actions_box)
        self.add_widget(main_layout)

    def do_login(self, instance):
        u = self.username_input.text.strip()
        p = self.password_input.text.strip()

        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (u, p))
        if cursor.fetchone():
            self.manager.transition = FadeTransition(duration=0.25)
            self.manager.current = "dashboard"
            self.manager.get_screen("dashboard").load_data()
        else:
            show_custom_popup("Authentication Error", "Invalid username or password.")

    def go_to_register(self, instance):
        self.manager.transition = FadeTransition(duration=0.25)
        self.manager.current = "register"


class RegisterScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        main_layout = BoxLayout(orientation='vertical', padding=[30, 40, 30, 40], spacing=20)

        header_box = BoxLayout(orientation='vertical', spacing=6, size_hint_y=0.25)
        header_box.add_widget(Label(
            text="Create Account", 
            font_size='24sp', 
            bold=True, 
            color=(0.1, 0.15, 0.25, 1)
        ))
        header_box.add_widget(Label(
            text="Start tracking your cashflow today", 
            font_size='13sp', 
            color=(0.4, 0.48, 0.58, 1)
        ))
        main_layout.add_widget(header_box)

        form_card = GlassCard(
            orientation='vertical', 
            padding=18, 
            spacing=12, 
            size_hint_y=0.45,
            bg_color=(1, 1, 1, 1),
            border_color=(0.85, 0.88, 0.92, 1)
        )

        self.new_user_input = ModernInput(hint_text="Choose Username", multiline=False)
        self.new_pass_input = ModernInput(hint_text="Choose Password", password=True, multiline=False)

        form_card.add_widget(self.new_user_input)
        form_card.add_widget(self.new_pass_input)

        btn_reg = ModernButton(
            text="CREATE ACCOUNT", 
            bg_color=(0.15, 0.45, 0.95, 1), 
            bold=True,
            font_size='15sp'
        )
        btn_reg.bind(on_press=self.do_register)
        form_card.add_widget(btn_reg)

        main_layout.add_widget(form_card)

        btn_back = ModernButton(
            text="← Back to Sign In", 
            bg_color=(0.9, 0.93, 0.98, 1), 
            text_color=(0.15, 0.45, 0.95, 1),
            size_hint_y=0.1
        )
        btn_back.bind(on_press=self.go_back)
        main_layout.add_widget(btn_back)

        self.add_widget(main_layout)

    def do_register(self, instance):
        u = self.new_user_input.text.strip()
        p = self.new_pass_input.text.strip()

        if not u or not p:
            show_custom_popup("Warning", "All fields are required!")
            return

        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (u, p))
            conn.commit()
            show_custom_popup("Success", "Account created successfully!")
            self.go_back(None)
        except sqlite3.IntegrityError:
            show_custom_popup("Error", "Username already taken!")

    def go_back(self, instance):
        self.manager.transition = FadeTransition(duration=0.25)
        self.manager.current = "login"


class DashboardScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.monthly_budget = 0.0

        main_layout = BoxLayout(orientation='vertical', padding=[16, 20, 16, 16], spacing=12)

        header = BoxLayout(orientation='horizontal', size_hint_y=0.07)
        header.add_widget(Label(
            text="Dashboard", 
            font_size='22sp', 
            bold=True, 
            color=(0.1, 0.15, 0.25, 1), 
            halign='left',
            valign='middle'
        ))
        
        btn_logout = ModernButton(
            text="Logout", 
            bg_color=(0.95, 0.85, 0.85, 1), 
            text_color=(0.8, 0.2, 0.2, 1),
            size_hint_x=0.25,
            font_size='12sp'
        )
        btn_logout.bind(on_press=self.logout)
        header.add_widget(btn_logout)
        main_layout.add_widget(header)

        self.card = GlassCard(
            orientation='vertical',
            padding=16,
            spacing=6,
            size_hint_y=0.25,
            bg_color=(1, 1, 1, 1),
            border_color=(0.85, 0.88, 0.92, 1)
        )

        self.lbl_budget = Label(text="Budget: PHP 0.00", font_size='13sp', color=(0.4, 0.48, 0.58, 1), halign='left')
        self.lbl_total = Label(text="PHP 0.00", font_size='28sp', bold=True, color=(0.85, 0.25, 0.25, 1), halign='left')
        self.lbl_remaining = Label(text="Remaining: PHP 0.00", font_size='13sp', color=(0.1, 0.65, 0.35, 1), halign='left')

        btn_set_budget = ModernButton(
            text="SET BUDGET", 
            bg_color=(0.15, 0.45, 0.95, 1), 
            bold=True,
            font_size='12sp',
            size_hint_y=0.35
        )
        btn_set_budget.bind(on_press=self.open_budget_popup)

        self.card.add_widget(self.lbl_budget)
        self.card.add_widget(self.lbl_total)
        self.card.add_widget(self.lbl_remaining)
        self.card.add_widget(btn_set_budget)

        main_layout.add_widget(self.card)

        input_card = GlassCard(
            orientation='vertical',
            padding=12,
            spacing=8,
            size_hint_y=0.28,
            bg_color=(1, 1, 1, 1),
            border_color=(0.85, 0.88, 0.92, 1)
        )

        self.desc_input = ModernInput(hint_text="Item Description (e.g. Dinner)", multiline=False)
        self.amt_input = ModernInput(hint_text="Amount", multiline=False, input_filter='float')

        btn_add = ModernButton(
            text="+ Add Expense", 
            bg_color=(0.15, 0.75, 0.45, 1), 
            bold=True, 
            font_size='14sp'
        )
        btn_add.bind(on_press=self.add_expense)

        input_card.add_widget(self.desc_input)
        input_card.add_widget(self.amt_input)
        input_card.add_widget(btn_add)

        main_layout.add_widget(input_card)

        main_layout.add_widget(Label(
            text="Recent Transactions", 
            font_size='14sp', 
            bold=True, 
            color=(0.4, 0.48, 0.58, 1), 
            size_hint_y=0.04,
            halign='left'
        ))

        self.scroll = ScrollView(size_hint_y=0.36)
        self.expense_list = GridLayout(cols=1, spacing=8, size_hint_y=None)
        self.expense_list.bind(minimum_height=self.expense_list.setter('height'))
        self.scroll.add_widget(self.expense_list)

        main_layout.add_widget(self.scroll)
        self.add_widget(main_layout)

    def load_data(self):
        cursor.execute("SELECT value FROM settings WHERE key='budget'")
        row = cursor.fetchone()
        self.monthly_budget = row[0] if row else 0.0
        self.load_expenses()

    def open_budget_popup(self, instance):
        content = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        with content.canvas.before:
            Color(1, 1, 1, 1)
            self_rect = RoundedRectangle(pos=content.pos, size=content.size, radius=[16])
        content.bind(pos=lambda inst, val: setattr(self_rect, 'pos', val),
                     size=lambda inst, val: setattr(self_rect, 'size', val))

        content.add_widget(Label(
            text="Enter Monthly Budget (PHP):", 
            color=(0.1, 0.15, 0.25, 1), 
            font_size='14sp',
            halign='left'
        ))

        input_budget = ModernInput(
            text=str(self.monthly_budget) if self.monthly_budget > 0 else "",
            hint_text="Enter budget amount", 
            multiline=False, 
            input_filter='float'
        )
        content.add_widget(input_budget)
        
        btn_save = ModernButton(
            text="SAVE BUDGET", 
            bg_color=(0.15, 0.45, 0.95, 1), 
            bold=True,
            size_hint_y=None,
            height=45
        )
        content.add_widget(btn_save)

        popup = Popup(
            title="Set Budget", 
            content=content, 
            size_hint=(0.85, 0.35),
            background=''
        )

        def save_budget(btn_inst):
            val = input_budget.text.strip()
            if val:
                new_b = float(val)
                self.monthly_budget = new_b
                cursor.execute("INSERT OR REPLACE INTO settings (key, value) VALUES ('budget', ?)", (new_b,))
                conn.commit()
                self.load_expenses()
            popup.dismiss()

        btn_save.bind(on_press=save_budget)
        popup.open()

    def add_expense(self, instance):
        desc = self.desc_input.text.strip()
        amt = self.amt_input.text.strip()
        date_str = datetime.now().strftime("%b %d")

        if not desc or not amt:
            return

        cursor.execute("INSERT INTO expenses (description, amount, category, date) VALUES (?, ?, ?, ?)",
                       (desc, float(amt), "General", date_str))
        conn.commit()

        self.desc_input.text = ""
        self.amt_input.text = ""
        
        self.load_expenses()

    def load_expenses(self):
        self.expense_list.clear_widgets()
        cursor.execute("SELECT id, description, amount, category, date FROM expenses ORDER BY id DESC")
        rows = cursor.fetchall()

        total = 0.0
        for row in rows:
            exp_id, desc, amt, cat, dt = row
            total += amt
            
            item_card = GlassCard(
                orientation='horizontal', 
                size_hint_y=None, 
                height=52, 
                padding=[12, 6, 12, 6], 
                spacing=10,
                bg_color=(1, 1, 1, 1),
                border_color=(0.9, 0.92, 0.95, 1)
            )

            info_box = BoxLayout(orientation='vertical', spacing=2)
            lbl_title = Label(
                text=f"{desc}", 
                font_size='13sp', 
                bold=True,
                color=(0.1, 0.15, 0.25, 1),
                halign='left'
            )
            lbl_sub = Label(
                text=f"{dt}", 
                font_size='10sp', 
                color=(0.5, 0.55, 0.65, 1),
                halign='left'
            )
            info_box.add_widget(lbl_title)
            info_box.add_widget(lbl_sub)

            lbl_amt = Label(
                text=f"-₱{amt:.2f}", 
                font_size='13sp', 
                bold=True,
                color=(0.85, 0.25, 0.25, 1),
                size_hint_x=0.3
            )

            btn_del = ModernButton(
                text="X", 
                size_hint_x=0.12, 
                bg_color=(0.95, 0.85, 0.85, 1),
                text_color=(0.8, 0.2, 0.2, 1),
                radius=8
            )
            btn_del.bind(on_press=lambda inst, e_id=exp_id: self.delete_expense(e_id))

            item_card.add_widget(info_box)
            item_card.add_widget(lbl_amt)
            item_card.add_widget(btn_del)
            
            self.expense_list.add_widget(item_card)

        self.lbl_budget.text = f"Budget: PHP {self.monthly_budget:,.2f}"
        self.lbl_total.text = f"PHP {total:,.2f}"
        
        remaining = self.monthly_budget - total
        rem_color = (0.1, 0.65, 0.35, 1) if remaining >= 0 else (0.85, 0.25, 0.25, 1)
        self.lbl_remaining.color = rem_color
        self.lbl_remaining.text = f"Remaining: PHP {remaining:,.2f}"

    def delete_expense(self, exp_id):
        cursor.execute("DELETE FROM expenses WHERE id=?", (exp_id,))
        conn.commit()
        self.load_expenses()

    def logout(self, instance):
        self.manager.transition = FadeTransition(duration=0.25)
        self.manager.current = "login"