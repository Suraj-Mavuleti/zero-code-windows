import sys
import gi
import os
import json
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib, Pango

CONFIG_DIR = os.path.expanduser("~/.config/zero-code")

class ZeroCode(Gtk.Window):
    def __init__(self):
        super().__init__(title="Zero Code - Ultimate Studio")
        self.set_default_size(1300, 850)
        
        os.makedirs(CONFIG_DIR, exist_ok=True)
        
        self.header = Gtk.HeaderBar()
        self.header.set_show_close_button(True)
        self.header.props.title = ""
        self.header.get_style_context().add_class("hidden-header")
        self.set_titlebar(self.header)
        
        self.setup_css()
        
        main_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.add(main_box)
        
        # ================= SIDEBAR (Project Explorer) =================
        self.sidebar = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.sidebar.set_size_request(260, -1)
        self.sidebar.get_style_context().add_class("sidebar")
        main_box.pack_start(self.sidebar, False, False, 0)
        
        logo_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        logo = Gtk.Label(label="Z E R O C O D E")
        logo.get_style_context().add_class("sidebar-logo")
        logo_box.pack_start(logo, True, True, 0)
        self.sidebar.pack_start(logo_box, False, False, 20)
        
        lbl_proj = Gtk.Label(label="PROJECT EXPLORER")
        lbl_proj.get_style_context().add_class("section-label")
        lbl_proj.set_halign(Gtk.Align.START)
        lbl_proj.set_margin_start(20)
        self.sidebar.pack_start(lbl_proj, False, False, 10)
        
        # Fake File Tree
        self.file_list = Gtk.ListBox()
        self.file_list.get_style_context().add_class("transparent-list")
        
        files = ["📁 src/", "   📄 main.py", "   📄 utils.py", "📁 assets/", "   🖼️ logo.png", "📄 README.md", "📄 requirements.txt"]
        for f in files:
            row = Gtk.ListBoxRow()
            row.get_style_context().add_class("file-row")
            lbl = Gtk.Label(label=f)
            lbl.set_halign(Gtk.Align.START)
            lbl.set_margin_start(15)
            lbl.set_margin_top(5)
            lbl.set_margin_bottom(5)
            row.add(lbl)
            self.file_list.add(row)
            
        self.sidebar.pack_start(self.file_list, True, True, 0)
        
        # Bottom sidebar tools
        tools_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        tools_box.set_margin_start(15)
        tools_box.set_margin_end(15)
        tools_box.set_margin_bottom(15)
        
        btn_settings = Gtk.Button(label="⚙️ Settings")
        btn_settings.get_style_context().add_class("nav-btn")
        btn_git = Gtk.Button(label="🌿 Git")
        btn_git.get_style_context().add_class("nav-btn")
        tools_box.pack_start(btn_settings, True, True, 0)
        tools_box.pack_start(btn_git, True, True, 0)
        self.sidebar.pack_end(tools_box, False, False, 0)
        
        # ================= WORKSPACE =================
        self.workspace = Gtk.Paned(orientation=Gtk.Orientation.VERTICAL)
        main_box.pack_start(self.workspace, True, True, 0)
        
        # Editor Area
        editor_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        editor_box.get_style_context().add_class("workspace-bg")
        
        # Editor Tabs
        tabs_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        tabs_box.get_style_context().add_class("editor-tabs")
        tab_lbl = Gtk.Label(label="main.py")
        tab_lbl.get_style_context().add_class("active-tab")
        tabs_box.pack_start(tab_lbl, False, False, 0)
        editor_box.pack_start(tabs_box, False, False, 0)
        
        # Text View
        scroll_editor = Gtk.ScrolledWindow()
        self.textview = Gtk.TextView()
        self.textview.get_style_context().add_class("code-editor")
        self.textview.modify_font(Pango.FontDescription('monospace 13'))
        
        # Sample code
        sample_code = """def calculate_quantum_flux(mass, velocity):
    '''
    Calculates the theoretical quantum flux of a particle.
    '''
    c = 299792458
    if velocity >= c:
        raise ValueError("Velocity cannot exceed the speed of light.")
        
    gamma = 1 / ((1 - (velocity**2 / c**2)) ** 0.5)
    momentum = gamma * mass * velocity
    
    return momentum * 6.626e-34

if __name__ == '__main__':
    print(f"Flux: {calculate_quantum_flux(0.5, 100000)}")
"""
        self.textview.get_buffer().set_text(sample_code)
        
        scroll_editor.add(self.textview)
        editor_box.pack_start(scroll_editor, True, True, 0)
        
        self.workspace.pack1(editor_box, True, False)
        
        # Terminal Area
        terminal_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        terminal_box.get_style_context().add_class("terminal-box")
        
        term_header = Gtk.Label(label="TERMINAL")
        term_header.get_style_context().add_class("section-label")
        term_header.set_halign(Gtk.Align.START)
        term_header.set_margin_start(15)
        term_header.set_margin_top(5)
        term_header.set_margin_bottom(5)
        terminal_box.pack_start(term_header, False, False, 0)
        
        term_text = Gtk.TextView()
        term_text.get_style_context().add_class("terminal-text")
        term_text.modify_font(Pango.FontDescription('monospace 12'))
        term_text.get_buffer().set_text("zero-studio@archlinux ~/project $ python main.py\nFlux: 3.313e-29\nzero-studio@archlinux ~/project $ _")
        term_text.set_editable(False)
        terminal_box.pack_start(term_text, True, True, 0)
        
        self.workspace.pack2(terminal_box, False, False)
        self.workspace.set_position(600)
        
    def setup_css(self):
        css = b'''
            window { background-color: #030305; }
            .hidden-header { background: #030305; min-height: 0px; padding: 0px; border: none; box-shadow: none; }
            .sidebar { background-color: rgba(8, 10, 16, 0.95); border-right: 1px solid rgba(255, 255, 255, 0.05); }
            .sidebar-logo { color: #FFFFFF; font-size: 20px; font-weight: 900; letter-spacing: 5px; text-shadow: 0 0 15px rgba(138, 43, 226, 0.6); }
            .section-label { color: #4A5568; font-size: 11px; font-weight: 900; letter-spacing: 2px; }
            .transparent-list { background: transparent; }
            .file-row { background: transparent; color: #8B94A5; font-size: 13px; border-radius: 6px; margin: 0px 10px; border: 1px solid transparent; }
            .file-row:hover { background: rgba(255, 255, 255, 0.05); color: #FFFFFF; cursor: pointer; }
            .nav-btn { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.05); color: #8B94A5; border-radius: 12px; padding: 10px; font-weight: bold; font-size: 13px; transition: all 0.2s ease; }
            .nav-btn:hover { background: rgba(138, 43, 226, 0.1); color: #8A2BE2; border: 1px solid #8A2BE2; box-shadow: 0 0 15px rgba(138, 43, 226, 0.2); }
            .workspace-bg { background: radial-gradient(circle at top right, #10141E, #030305); }
            .editor-tabs { background: #080A10; border-bottom: 1px solid #1C2333; }
            .active-tab { background: #10141E; color: #00E5FF; padding: 10px 20px; border-top: 2px solid #00E5FF; font-family: monospace; font-size: 13px; border-right: 1px solid #1C2333; }
            .code-editor { background: transparent; color: #c9d1d9; padding: 10px; caret-color: #00E5FF; }
            .code-editor text { background: transparent; }
            .terminal-box { background: #050608; border-top: 1px solid #1C2333; }
            .terminal-text { background: transparent; color: #4AF626; padding: 10px; }
            .terminal-text text { background: transparent; }
        '''
        provider = Gtk.CssProvider()
        provider.load_from_data(css)
        Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(), provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

if __name__ == "__main__":
    win = ZeroCode()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
