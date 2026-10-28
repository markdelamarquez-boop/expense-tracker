from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window

from screens import LoginScreen, RegisterScreen, DashboardScreen

# Set smooth window size and clean light background
Window.size = (390, 700)
Window.clearcolor = (0.96, 0.97, 0.99, 1)  # Clean Modern Light Theme Background

# --- MAIN APP ---
class ExpenseApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(RegisterScreen(name="register"))
        sm.add_widget(DashboardScreen(name="dashboard"))
        return sm

if __name__ == '__main__':
    ExpenseApp().run()