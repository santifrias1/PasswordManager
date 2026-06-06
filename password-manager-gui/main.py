import customtkinter as ctk
import requests
import random
import string

# Configuración básica de la ventana
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# --- VENTANA PRINCIPAL (DASHBOARD) ---
class PanelPrincipal(ctk.CTk):
    def __init__(self, user_id):
        super().__init__()

        self.user_id = user_id
        self.credenciales_guardadas = [] # Guardamos la lista en memoria para el buscador

        self.title("Gestor de Contraseñas - Mis Credenciales")
        self.geometry("800x550")
        self.resizable(False, False)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # --- BARRA LATERAL (Menú) ---
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(4, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar, text="Panel de Control", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 30))

        self.btn_agregar = ctk.CTkButton(self.sidebar, text="Agregar Contraseña", fg_color="#1f538d", hover_color="#14375e", command=self.abrir_ventana_agregar)
        self.btn_agregar.grid(row=1, column=0, padx=20, pady=10)

        self.btn_refrescar = ctk.CTkButton(self.sidebar, text="Refrescar Lista", command=self.cargar_credenciales)
        self.btn_refrescar.grid(row=2, column=0, padx=20, pady=10)

        self.btn_salir = ctk.CTkButton(self.sidebar, text="Cerrar Sesión", fg_color="#8d1f1f", hover_color="#5e1414", command=self.cerrar_sesion)
        self.btn_salir.grid(row=5, column=0, padx=20, pady=20)

        # --- ÁREA CENTRAL ---
        self.main_frame = ctk.CTkScrollableFrame(self, corner_radius=10)
        self.main_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        self.label_bienvenida = ctk.CTkLabel(self.main_frame, text="Tus Credenciales Guardadas", font=("Arial", 20, "bold"))
        self.label_bienvenida.pack(pady=(10, 10))

        # --- BUSCADOR ---
        self.frame_busqueda = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.frame_busqueda.pack(fill="x", padx=10, pady=(0, 15))

        self.entry_buscador = ctk.CTkEntry(self.frame_busqueda, placeholder_text="Buscar sitio...", width=250)
        self.entry_buscador.pack(side="left", padx=(0, 10))

        # Vinculamos el evento de presionar una tecla (KeyRelease) a la función de filtrar
        self.entry_buscador.bind("<KeyRelease>", self.filtrar_credenciales)

        # Frame contenedor para la grilla
        self.grilla_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.grilla_frame.pack(fill="x", padx=10)

        self.cargar_credenciales()

    def cargar_credenciales(self):
        url = f"http://localhost:8080/api/credentials/{self.user_id}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                self.credenciales_guardadas = response.json() # Guardamos en memoria
                self.dibujar_grilla(self.credenciales_guardadas)
            else:
                self.mostrar_mensaje_grilla("Error al cargar credenciales", "red")
        except requests.exceptions.ConnectionError:
            self.mostrar_mensaje_grilla("Sin conexión al servidor", "red")

    def filtrar_credenciales(self, event=None):
        texto_busqueda = self.entry_buscador.get().lower()
        if not texto_busqueda:
            # Si borró todo, mostramos la lista completa
            self.dibujar_grilla(self.credenciales_guardadas)
            return

        # Filtramos buscando coincidencias en el sitio web
        credenciales_filtradas = [c for c in self.credenciales_guardadas if texto_busqueda in c['site'].lower()]
        self.dibujar_grilla(credenciales_filtradas)

    def dibujar_grilla(self, lista_credenciales):
        # 1. Limpiamos la grilla
        for widget in self.grilla_frame.winfo_children():
            widget.destroy()

        # 2. Dibujamos las cabeceras
        ctk.CTkLabel(self.grilla_frame, text="Sitio Web", font=("Arial", 14, "bold"), width=150, anchor="w").grid(row=0, column=0, padx=5, pady=5)
        ctk.CTkLabel(self.grilla_frame, text="Usuario", font=("Arial", 14, "bold"), width=150, anchor="w").grid(row=0, column=1, padx=5, pady=5)
        ctk.CTkLabel(self.grilla_frame, text="Acciones", font=("Arial", 14, "bold"), width=180).grid(row=0, column=2, columnspan=2, padx=5, pady=5)

        if not lista_credenciales:
            self.mostrar_mensaje_grilla("No se encontraron credenciales.", "gray")
            return

        # 3. Llenamos la tabla con los datos
        for index, cred in enumerate(lista_credenciales, start=1):
            ctk.CTkLabel(self.grilla_frame, text=cred['site'], width=150, anchor="w").grid(row=index, column=0, padx=5, pady=5)
            ctk.CTkLabel(self.grilla_frame, text=cred['username'], width=150, anchor="w").grid(row=index, column=1, padx=5, pady=5)
            
            btn_copiar = ctk.CTkButton(self.grilla_frame, text="Copiar", width=80, fg_color="#2b7a4b", hover_color="#1e5434",
                                       command=lambda p=cred['encryptedPassword']: self.copiar_al_portapapeles(p))
            btn_copiar.grid(row=index, column=2, padx=5, pady=5)

            btn_eliminar = ctk.CTkButton(self.grilla_frame, text="Eliminar", width=80, fg_color="#8d1f1f", hover_color="#5e1414",
                                         command=lambda cid=cred['id']: self.eliminar_credencial(cid))
            btn_eliminar.grid(row=index, column=3, padx=5, pady=5)

    def mostrar_mensaje_grilla(self, texto, color):
        for widget in self.grilla_frame.winfo_children():
            widget.destroy()
        ctk.CTkLabel(self.grilla_frame, text=texto, text_color=color).grid(row=1, column=0, columnspan=4, pady=20)

    def copiar_al_portapapeles(self, texto):
        self.clipboard_clear()
        self.clipboard_append(texto)
        self.update()
        print("¡Contraseña copiada al portapapeles!")

    def eliminar_credencial(self, credencial_id):
        url = f"http://localhost:8080/api/credentials/{credencial_id}"
        try:
            response = requests.delete(url)
            if response.status_code == 200:
                self.cargar_credenciales() 
            else:
                print(f"Error al eliminar la credencial. Código: {response.status_code}")
        except requests.exceptions.ConnectionError:
            print("Sin conexión al servidor al intentar eliminar.")

    def abrir_ventana_agregar(self):
        ventana = ctk.CTkToplevel(self)
        ventana.title("Nueva Contraseña")
        ventana.geometry("380x450")
        ventana.resizable(False, False)
        ventana.focus()

        ctk.CTkLabel(ventana, text="Guardar Credencial", font=("Arial", 20, "bold")).pack(pady=15)

        entry_sitio = ctk.CTkEntry(ventana, placeholder_text="Sitio Web", width=280)
        entry_sitio.pack(pady=10)

        entry_usuario = ctk.CTkEntry(ventana, placeholder_text="Usuario o Email", width=280)
        entry_usuario.pack(pady=10)

        # --- GENERADOR DE CONTRASEÑAS ---
        frame_pass = ctk.CTkFrame(ventana, fg_color="transparent")
        frame_pass.pack(pady=10)

        entry_password = ctk.CTkEntry(frame_pass, placeholder_text="Contraseña", width=190)
        entry_password.pack(side="left", padx=(0, 10))

        def generar_clave():
            caracteres = string.ascii_letters + string.digits + "!@#$%&*"
            clave_segura = ''.join(random.choice(caracteres) for _ in range(14))
            entry_password.delete(0, 'end')
            entry_password.insert(0, clave_segura)

        btn_generar = ctk.CTkButton(frame_pass, text="Generar", width=80, fg_color="#1f538d", hover_color="#14375e", command=generar_clave)
        btn_generar.pack(side="left")
        # --------------------------------

        entry_notas = ctk.CTkEntry(ventana, placeholder_text="Notas (Opcional)", width=280)
        entry_notas.pack(pady=10)

        label_error = ctk.CTkLabel(ventana, text="", text_color="red")
        label_error.pack(pady=5)

        def guardar():
            sitio = entry_sitio.get()
            usuario = entry_usuario.get()
            password = entry_password.get()
            notas = entry_notas.get()

            if not sitio or not usuario or not password:
                label_error.configure(text="Completá Sitio, Usuario y Contraseña.")
                return

            url = f"http://localhost:8080/api/credentials/{self.user_id}"
            payload = {"site": sitio, "username": usuario, "password": password, "notes": notas}

            try:
                response = requests.post(url, json=payload)
                if response.status_code == 201:
                    ventana.destroy()
                    self.cargar_credenciales()
                else:
                    label_error.configure(text="Error al guardar en el servidor.")
            except requests.exceptions.ConnectionError:
                label_error.configure(text="Sin conexión al servidor.")

        btn_guardar = ctk.CTkButton(ventana, text="Guardar", fg_color="#2b7a4b", hover_color="#1e5434", command=guardar)
        btn_guardar.pack(pady=10)

    def cerrar_sesion(self):
        self.destroy()
        app = LoginWindow()
        app.mainloop()

# --- VENTANA DE LOGIN ---
class LoginWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Gestor de Contraseñas")
        self.geometry("400x550") # La hicimos un poco más alta para que entre el botón
        self.resizable(False, False)

        self.label_titulo = ctk.CTkLabel(self, text="Iniciar Sesión", font=("Arial", 28, "bold"))
        self.label_titulo.pack(pady=(50, 30))

        self.entry_usuario = ctk.CTkEntry(self, placeholder_text="Usuario", width=250, height=40)
        self.entry_usuario.pack(pady=10)

        self.entry_password = ctk.CTkEntry(self, placeholder_text="Contraseña Maestra", show="*", width=250, height=40)
        self.entry_password.pack(pady=10)

        self.btn_login = ctk.CTkButton(self, text="Entrar", command=self.iniciar_sesion, width=250, height=40, font=("Arial", 14, "bold"))
        self.btn_login.pack(pady=20)

        self.label_mensaje = ctk.CTkLabel(self, text="", text_color="red", font=("Arial", 12))
        self.label_mensaje.pack(pady=5)

        # --- BOTÓN PARA REGISTRARSE ---
        self.btn_registrar = ctk.CTkButton(self, text="Crear cuenta nueva", fg_color="transparent", border_width=1, text_color="gray", command=self.abrir_ventana_registro, width=250, height=35)
        self.btn_registrar.pack(pady=(10, 20))

    def iniciar_sesion(self):
        usuario = self.entry_usuario.get()
        password = self.entry_password.get()

        if not usuario or not password:
            self.label_mensaje.configure(text="Por favor, completá todos los campos.", text_color="red")
            return

        url = "http://localhost:8080/api/auth/login"
        payload = {"username": usuario, "masterPassword": password}

        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                user_id = response.text
                self.destroy()
                panel = PanelPrincipal(user_id)
                panel.mainloop()
            elif response.status_code == 401:
                self.label_mensaje.configure(text="Credenciales inválidas.", text_color="red")
            else:
                self.label_mensaje.configure(text=f"Error del servidor: {response.status_code}", text_color="red")
        except requests.exceptions.ConnectionError:
            self.label_mensaje.configure(text="No se pudo conectar al servidor.", text_color="red")

    # --- MÉTODO PARA LA VENTANA DE REGISTRO ---
    def abrir_ventana_registro(self):
        ventana_reg = ctk.CTkToplevel(self)
        ventana_reg.title("Nueva Cuenta")
        ventana_reg.geometry("350x420")
        ventana_reg.resizable(False, False)
        ventana_reg.focus()

        ctk.CTkLabel(ventana_reg, text="Registrar Usuario", font=("Arial", 20, "bold")).pack(pady=20)

        entry_nuevo_usu = ctk.CTkEntry(ventana_reg, placeholder_text="Nuevo Usuario", width=250)
        entry_nuevo_usu.pack(pady=10)

        entry_nueva_pass = ctk.CTkEntry(ventana_reg, placeholder_text="Contraseña Maestra", show="*", width=250)
        entry_nueva_pass.pack(pady=10)

        entry_confirm_pass = ctk.CTkEntry(ventana_reg, placeholder_text="Confirmar Contraseña", show="*", width=250)
        entry_confirm_pass.pack(pady=10)

        label_err_reg = ctk.CTkLabel(ventana_reg, text="", text_color="red")
        label_err_reg.pack(pady=5)

        def registrar():
            usu = entry_nuevo_usu.get()
            pas = entry_nueva_pass.get()
            conf = entry_confirm_pass.get()

            if not usu or not pas or not conf:
                label_err_reg.configure(text="Completá todos los campos.")
                return
            
            # Validación simple para que no se equivoquen al tipear su clave maestra
            if pas != conf:
                label_err_reg.configure(text="Las contraseñas no coinciden.")
                return

            # Petición al backend
            url = "http://localhost:8080/api/auth/register"
            payload = {"username": usu, "masterPassword": pas}

            try:
                response = requests.post(url, json=payload)
                if response.status_code == 201:
                    # Registro exitoso: avisa en la pantalla de login y cierra el modal
                    self.label_mensaje.configure(text="¡Cuenta creada! Ya podés iniciar sesión.", text_color="green")
                    ventana_reg.destroy()
                else:
                    # El backend tira error si el nombre de usuario ya existe
                    label_err_reg.configure(text="Error: El usuario ya existe o hubo un fallo.")
            except requests.exceptions.ConnectionError:
                label_err_reg.configure(text="Sin conexión al servidor.")

        btn_guardar_reg = ctk.CTkButton(ventana_reg, text="Registrarse", fg_color="#2b7a4b", hover_color="#1e5434", command=registrar)
        btn_guardar_reg.pack(pady=15)

if __name__ == "__main__":
    app = LoginWindow()
    app.mainloop()