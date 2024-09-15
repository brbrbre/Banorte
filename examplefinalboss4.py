from tkinter import *
from tkinter import messagebox, filedialog, ttk
from PIL import Image, ImageTk
import webbrowser  # Importar el módulo webbrowser
import webview

import requests
from tkcalendar import DateEntry
from io import BytesIO
from tkinter import scrolledtext
import cv2

class App(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.config(bg="#FF0000", cursor="heart")
        self.geometry("400x700")
        self.title("Banorte Onboarding")

        url = "https://i.pinimg.com/474x/93/9c/15/939c150a2059216c97e8026d43f375f8.jpg"
        response = requests.get(url)
        img_data = response.content
        img = Image.open(BytesIO(img_data))
        photo = ImageTk.PhotoImage(img)

        # Imagen del chatbot
        url = "https://richestsoft.com/wp-content/themes/richnew/images/chatbot-images/intro-img.webp"
        response = requests.get(url)
        img_data = response.content
        img = Image.open(BytesIO(img_data))
        img = img.resize((60, 60), Image.LANCZOS)  # Redimensionar la imagen
        self.robot = ImageTk.PhotoImage(img)

        
                       
        # Crear el label con la imagen y sin borde
        label = Label(self, image=photo, highlightthickness=0, bd=0)
        label.image = photo  # Mantener una referencia a la imagen
        label.place(x=20, y=150)

        #esta variable de usuarios es un diccionario de python y estara simulando una base de datos de la vida real.
        self.usuarios = {
            #user,contraseña,si realizo test inicia, tipo de personalidad, nombre, objetivo,saldo,ahorros
            "steffanylars": ["qwertyuiop", False, "Haz tu test con el chatbot.","Steffany","",0,0]
        }

        self.colors = {  # para los botoncitos
            "primary": "#FF0000",  # Rojo
            "secondary": "#8B0000",  # Rojo oscuro
            "white": "#FFFFFF",
            "selected": "#B22222"  # Rojo más oscuro para botón seleccionado
        }

        #SE INICIALIZA PARA EL USO DE LA BARRA DE CARGA
        self.nav_buttons = {}  # Inicializar el diccionario de botones de navegación
        self.progress_var = DoubleVar()
        # Definir el conjunto de módulos visitados
        self.modulos_visitados = set()

        self.images = {
                "modulo_1": ImageTk.PhotoImage(Image.open(BytesIO(requests.get("https://via.placeholder.com/300x150.png/007BFF/FFFFFF?text=Bienestar+Financiero").content)).resize((300, 150), Image.LANCZOS)),
                "modulo_2": ImageTk.PhotoImage(Image.open(BytesIO(requests.get("https://via.placeholder.com/300x150.png/28A745/FFFFFF?text=Tarjeta+de+Crédito").content)).resize((300, 150), Image.LANCZOS)),
                "modulo_3": ImageTk.PhotoImage(Image.open(BytesIO(requests.get("https://via.placeholder.com/300x150.png/FFC107/FFFFFF?text=Planeando+mi+Futuro").content)).resize((300, 150), Image.LANCZOS)),
                "modulo_4": ImageTk.PhotoImage(Image.open(BytesIO(requests.get("https://via.placeholder.com/300x150.png/17A2B8/FFFFFF?text=Estrategias+de+Ahorro").content)).resize((300, 150), Image.LANCZOS))
            }

        self.nav_buttons = {}  # Inicializar el diccionario de botones de navegación

        # Mostrar pantalla de login después de 4 segundos
        self.after(2000, self.show_priv)

        self.estado_conversacion = "inicio"
        self.tema_actual = ""
    
    def show_priv(self):
        # Limpiar la pantalla actual
        for widget in self.winfo_children():
            widget.destroy()

        self.config(bg="#FFFFFF")

        # Descargar la imagen del candado
        url_candado = "https://cdn-icons-png.flaticon.com/512/345/345735.png"
        response = requests.get(url_candado)
        img_data = response.content
        img = Image.open(BytesIO(img_data))
        img = img.resize((100, 100), Image.Resampling.LANCZOS)  # Ajustar el tamaño de la imagen
        profile_pic = ImageTk.PhotoImage(img)

        # Icono del candado
        label_icon = Label(self, image=profile_pic, bg="#FFFFFF")
        label_icon.image = profile_pic  # Mantener la referencia de la imagen
        label_icon.pack(pady=30)

        # Crear las etiquetas de seguridad
        Label(self, text="• Banorte cuida tus datos como si fueran nuestros", 
              font=("Arial", 12), bg="#FFFFFF").pack(pady=5)
        Label(self, text="• Todo está cifrado y protegido", font=("Arial", 12), bg="#FFFFFF").pack(pady=5)
        Label(self, text="• Solo tú puedes acceder a tu cuenta", font=("Arial", 12), bg="#FFFFFF").pack(pady=5)
        Label(self, text="• Activa el reconocimiento facial para seguridad extra", 
              font=("Arial", 12), bg="#FFFFFF").pack(pady=5)
        Label(self, text="• Si ves algo raro, avísanos rápido", font=("Arial", 12), bg="#FFFFFF").pack(pady=5)

        # Botón siguiente que redirige al login
        Button(self, text="Siguiente", font=("Arial", 14), bg="#FFFFFF", fg="#FF0000", width=20,
               command=self.login).place(x=100, y=480)

    def obtener_respuesta(self, texto):
        texto = texto.lower()  # Convertir todo el texto a minúsculas

        # Iniciar el test de personalidad
        if texto == "identifica mi personalidad":
            self.estado_conversacion = "instrucciones_test"
            self.user_input.config(state="normal")  # Habilitar el campo de entrada
            return (
                "Para identificar tu personalidad financiera, te haré 20 preguntas. "
                "Responde con un número del 1 al 10 para indicar qué tanto estás de acuerdo con cada afirmación "
                "(1 = Nada de acuerdo, 10 = Totalmente de acuerdo). "
                "Si en cualquier momento deseas salir del test, escribe 'terminar'. "
                "¿Estás listo/a para comenzar?"
            )

        # Dar instrucciones y comenzar el test
        if self.estado_conversacion == "instrucciones_test":
            if "sí" or "si" in texto or "listo" in texto:
                return self.iniciar_test_personalidad()
            elif "terminar" in texto:
                self.estado_conversacion = "inicio"
                return "Test cancelado. ¿En qué más te puedo ayudar?"
            else:
                return "Por favor, responde con 'sí' para comenzar o 'terminar' para salir del test."

        # Proceso del test de personalidad
        if self.estado_conversacion == "test_personalidad":
            if "terminar" in texto:
                self.estado_conversacion = "inicio"
                return "Test cancelado. ¿En qué más te puedo ayudar?"
            try:
                puntuacion = int(texto)
                if 1 <= puntuacion <= 10:
                    self.respuestas_personalidad.append(puntuacion)
                    self.pregunta_actual += 1
                    if self.pregunta_actual < len(self.preguntas_personalidad):
                        return self.preguntas_personalidad[self.pregunta_actual]
                    else:
                        return self.clasificar_personalidad()
                else:
                    return "Por favor, responde con un número del 1 al 10."
            except ValueError:
                return "Por favor, responde con un número del 1 al 10."

        # Flujo de conversación existente (otros temas, etc.)
        if self.estado_conversacion == "inicio":
            # Aquí continuarías con el manejo de otros temas según lo que ya tienes implementado.
            pass

        return "Lo siento, no tengo información sobre ese tema. Puedes preguntarme sobre ahorro, inversión, presupuesto, deuda, y más."


    def iniciar_test_personalidad(self):
        # Preguntas del test de personalidad
        self.preguntas_personalidad = [
            "¿Me siento cómodo/a tomando decisiones financieras importantes sin consultar a nadie?",
            "¿Estoy constantemente buscando nuevas formas de invertir mi dinero?",
            "¿Prefiero opciones financieras que ofrezcan seguridad, aunque el rendimiento sea bajo?",
            "¿Me gusta interactuar con otras personas para discutir ideas financieras o de negocios?",
            "¿Estoy dispuesto/a a asumir riesgos financieros para obtener altos rendimientos?",
            "¿Prefiero crear un plan detallado antes de tomar decisiones financieras?",
            "¿Me considero una persona creativa cuando se trata de gestionar mis finanzas?",
            "¿Valoro más la estabilidad financiera que las oportunidades de crecimiento incierto?",
            "¿Disfruto construyendo y manteniendo relaciones que me ayuden a mejorar mis finanzas?",
            "¿Me gusta liderar proyectos o inversiones nuevas y asumir la responsabilidad del resultado?",
            "¿Me siento más seguro/a cuando tengo un plan financiero claro y definido?",
            "¿Me emociona la idea de innovar en mis estrategias financieras o de inversión?",
            "¿La seguridad de mi dinero es más importante que buscar ganancias rápidas?",
            "¿Creo que mi éxito financiero depende en gran medida de mi capacidad para relacionarme con otros?",
            "¿Me motiva iniciar y liderar nuevos proyectos o negocios?",
            "¿Prefiero analizar todas las opciones antes de tomar una decisión financiera?",
            "¿Estoy dispuesto/a a explorar ideas no convencionales para aumentar mi patrimonio?",
            "¿Considero que es esencial proteger mis inversiones frente a posibles pérdidas?",
            "¿Prefiero discutir y compartir ideas financieras con otros antes de actuar?",
            "¿Me gusta enfrentar nuevos desafíos financieros y estoy dispuesto/a a asumir riesgos?"
        ]

        # Preguntas de personalización
        self.preguntas_personalizacion = [
            "¿Cuál es tu edad?",
            "¿Cuál es tu ocupación?",
            "¿Cuál consideras que es tu nivel de educación financiera (bajo, medio, alto)?",
            "¿Qué tipo de plataformas digitales prefieres (banca móvil, aplicaciones de inversión, etc.)?"
        ]

        # Combinar ambas listas
        self.preguntas_totales = self.preguntas_personalidad + self.preguntas_personalizacion

        self.respuestas_personalidad = []
        self.respuestas_personalizacion = {}  # Para guardar respuestas de personalización
        self.pregunta_actual = 0
        self.estado_conversacion = "test_personalidad"
        return self.preguntas_totales[self.pregunta_actual]

    def siguiente_pregunta(self, respuesta):
        # Si la pregunta es de personalización, la guarda en el diccionario
        if self.pregunta_actual >= len(self.preguntas_personalidad):
            pregunta_personalizacion = self.preguntas_totales[self.pregunta_actual]
            self.respuestas_personalizacion[pregunta_personalizacion] = respuesta
        else:
            # Guardar respuestas del test de personalidad
            self.respuestas_personalidad.append(int(respuesta))  # Suponiendo que las respuestas son en formato numérico

        # Avanzar a la siguiente pregunta
        self.pregunta_actual += 1

        if self.pregunta_actual < len(self.preguntas_totales):
            return self.preguntas_totales[self.pregunta_actual]
        else:
            # Una vez terminadas las preguntas, clasificar la personalidad
            return self.clasificar_personalidad()

    def clasificar_personalidad(self):
        num_tipos = 5
        preguntas_por_tipo = len(self.respuestas_personalidad) // num_tipos  # Debería ser 4, ya que hay 20 preguntas y 5 tipos

        # Inicializa una lista para sumar los puntajes por tipo de personalidad
        puntajes_personalidad = [0] * num_tipos

        # Itera sobre cada respuesta y la asigna a su correspondiente tipo de personalidad
        for i in range(len(self.respuestas_personalidad)):
            tipo_index = i % num_tipos  # Esto asegura que las respuestas se distribuyan entre los tipos
            puntajes_personalidad[tipo_index] += self.respuestas_personalidad[i]

        # Encuentra el tipo de personalidad con el puntaje más alto
        max_puntaje = max(puntajes_personalidad)
        indice_personalidad = puntajes_personalidad.index(max_puntaje)

        # Define los tipos de personalidad
        tipos_personalidad = ["El Estratega", "El Innovador", "El Guardián", "El Comunicador", "El Emprendedor"]
        self.estado_conversacion = "inicio" 

        # Modificar la "base de datos" para añadir la personalidad y la personalización
        self.usuarios[self.username][2] = tipos_personalidad[indice_personalidad]
        self.usuarios[self.username][1] = True

        # Agregar respuestas de personalización al perfil
        self.usuarios[self.username].extend([self.respuestas_personalizacion])

        return f"Tu tipo de personalidad es: {tipos_personalidad[indice_personalidad]}. ¡Gracias por completar el test!"
    def show_chatbot(self):
        self.clear_main_frame()

        # Agregar un frame superior con la imagen del chatbot
        top_frame = Frame(self.main_frame, bg=self.colors["primary"], height=100)
        top_frame.pack(fill=X)
        
        
        # Label para mostrar la imagen
        img_label = Label(top_frame, image=self.robot, bg=self.colors["primary"])
        img_label.image = self.robot  # Necesario para mantener la referencia a la imagen
        img_label.pack(side=LEFT, padx=20, pady=20)

        # Nombre del chatbot
        Label(top_frame, text="¡Hola, soy Forti!", font=("Arial", 18, "bold"), bg=self.colors["primary"], fg=self.colors["white"]).pack(side=LEFT, pady=20)

        # Frame para mostrar la conversación con estilo de burbujas
        conversation_frame = Frame(self.main_frame, bg="#f0f0f0")
        conversation_frame.pack(expand=True, fill=BOTH, padx=10, pady=10)

        # Agregar un ScrolledText para las conversaciones
        self.chat_display = scrolledtext.ScrolledText(conversation_frame, wrap=WORD, bg="#f0f0f0", fg="#000000", font=("Arial", 12), borderwidth=0, highlightthickness=0)
        self.chat_display.pack(expand=True, fill=BOTH)
        self.chat_display.insert(END, "Bot: Hola, ¿en qué puedo ayudarte hoy?\n\n")
        self.chat_display.configure(state='disabled')

        # Hacer que se desplace automáticamente hacia abajo cuando se agrega texto
        self.chat_display.yview(END)

        # Frame para la entrada de texto y el botón de enviar
        entry_frame = Frame(self.main_frame, bg="#f0f0f0")
        entry_frame.pack(fill=X, padx=10, pady=10)

        self.user_input = Entry(entry_frame, font=("Arial", 14), width=20, borderwidth=2, relief="groove")
        self.user_input.pack(side=LEFT, fill=X, expand=True, padx=(0, 10))

        # Verificar si ya hizo el test personalizado
        if not (self.usuarios[self.username][1]): 
            self.user_input.insert(0, "Identifica mi personalidad")
            self.user_input.config(state="disabled")
        else:
            self.user_input.config(state="normal")

        send_button = Button(entry_frame, text="Enviar", font=("Arial", 14), bg="#FF4500", fg=self.colors["white"], command=self.get_response, width=10, borderwidth=0)
        send_button.pack(side=RIGHT)

        self.update_nav_button("chatbot")

    def get_response(self):
        user_input = self.user_input.get()
        if user_input:
            self.chat_display.config(state=NORMAL)
            self.chat_display.insert(END, f"Tú: {user_input}\n")
            response = self.obtener_respuesta(user_input)
            self.chat_display.insert(END, f"Bot: {response}\n")

            # Desplazarse automáticamente hacia el final del texto
            self.chat_display.yview(END)

            self.chat_display.config(state=DISABLED)
            self.user_input.delete(0, END)

    def crear_cuenta_paso1(self):
        # Limpiar la ventana
        for widget in self.winfo_children():
            widget.destroy()

        Label(self, text="Crea tu cuenta", font=("Arial", 24, "bold"), bg="#FF0000", fg="#FFFFFF").place(x=100, y=60)

        # Campos de entrada
        Label(self, text="Nombre(s):", font=("Arial", 14), bg="#FF0000", fg="#FFFFFF").place(x=30, y=150)
        self.nombre_entry = Entry(self, font=("Arial", 14), width=30)
        self.nombre_entry.place(x=30, y=180)

        Label(self, text="Apellidos:", font=("Arial", 14), bg="#FF0000", fg="#FFFFFF").place(x=30, y=230)
        self.apellido_entry = Entry(self, font=("Arial", 14), width=30)
        self.apellido_entry.place(x=30, y=260)

        Label(self, text="Fecha de nacimiento:", font=("Arial", 14), bg="#FF0000", fg="#FFFFFF").place(x=30, y=310)
        self.fecha_entry = DateEntry(self, font=("Arial", 14), width=28, background="red", foreground="white", bd=2)
        self.fecha_entry.place(x=30, y=340)

        Label(self, text="Correo electrónico:", font=("Arial", 14), bg="#FF0000", fg="#FFFFFF").place(x=30, y=390)
        self.email_entry = Entry(self, font=("Arial", 14), width=30)
        self.email_entry.place(x=30, y=420)

        Button(self, text="Siguiente", font=("Arial", 14), bg="#FFFFFF", fg="#FF0000", width=20,
               command=self.crear_cuenta_paso2).place(x=100, y=480)
        
        Button(self, text="Atras", font=("Arial", 14), bg="#FFFFFF", fg="#FF0000", width=10,
               command=self.login).place(x=250, y=540)

    def crear_cuenta_paso2(self):
        # Limpiar la ventana
        for widget in self.winfo_children():
            widget.destroy()

        Label(self, text="Crea tu cuenta", font=("Arial", 24, "bold"), bg="#FF0000", fg="#FFFFFF").place(x=100, y=60)

        # Campos de entrada
        Label(self, text="Usuario:", font=("Arial", 14), bg="#FF0000", fg="#FFFFFF").place(x=30, y=150)
        self.usuario_entry = Entry(self, font=("Arial", 14), width=30)
        self.usuario_entry.place(x=30, y=180)

        Label(self, text="Contraseña:", font=("Arial", 14), bg="#FF0000", fg="#FFFFFF").place(x=30, y=230)
        self.password_entry = Entry(self, font=("Arial", 14), show="*", width=30)
        self.password_entry.place(x=30, y=260)

        Label(self, text="Confirma contraseña:", font=("Arial", 14), bg="#FF0000", fg="#FFFFFF").place(x=30, y=310)
        self.confirm_password_entry = Entry(self, font=("Arial", 14), show="*", width=30)
        self.confirm_password_entry.place(x=30, y=340)

        Label(self, text="ID oficial:", font=("Arial", 14), bg="#FF0000", fg="#FFFFFF").place(x=30, y=390)
        Button(self, text="Cargar imagen", font=("Arial", 14), bg="#FFFFFF", fg="#FF0000", width=20, command=self.subir_foto).place(x=30, y=420)

        Button(self, text="Crear Cuenta", font=("Arial", 14), bg="#FFFFFF", fg="#FF0000", width=20,command=self.verificar_datos).place(x=30, y=480)
        Button(self, text="Atras", font=("Arial", 14), bg="#FFFFFF", fg="#FF0000", width=10,
               command=self.crear_cuenta_paso1).place(x=250, y=540)
    def verificar_datos(self):
        prueba_usuario = self.usuario_entry.get().strip()
        prueba_password = self.password_entry.get().strip()

        if not prueba_usuario or not prueba_password:
            messagebox.showinfo("Error de input","Llena todas las entradas")
            self.crear_cuenta_paso2
        else:
            if (self.password_entry.get() == self.confirm_password_entry.get()):
                messagebox.showinfo("Listo","Cuenta creada con éxito.")
                new_user_detail = [self.password_entry.get(),False,"Haz tu Test con el chatbot",self.usuario_entry.get(),"",0,0]
                self.usuarios[self.usuario_entry.get()] = new_user_detail
                self.login()
            else:
                messagebox.showinfo("Error","Contraseñas no coinciden")
                self.crear_cuenta_paso2

    def pantalla_principal(self):
        # Limpiar la ventana y mostrar pantalla principal
        for widget in self.winfo_children():
            widget.destroy()

        self.config(bg=self.colors["white"])  # Fondo blanco para la pantalla principal

        # Crear un frame principal para mostrar el contenido de las páginas
        self.main_frame = Frame(self, bg=self.colors["white"])
        self.main_frame.pack(fill=BOTH, expand=True)

        # Crear barra de navegación inferior
        self.create_bottom_nav()
        # Página principal por defecto
        self.show_home()

    
    
    def show_module_detail(self, titulo, descripcion):
        self.clear_main_frame()

        Label(self.main_frame, text=titulo, font=("Arial", 15), bg=self.colors["white"]).pack(pady=20)
        Label(self.main_frame, text=descripcion, font=("Arial", 12), bg=self.colors["white"], wraplength=400).pack(pady=20)

        Button(self.main_frame, text="Regresar", font=("Arial", 12), bg=self.colors["primary"], fg=self.colors["white"], command=self.show_home).pack(pady=20)

        self.update_nav_button("home")

    def complete_module(self, module_number):
        # Simula la finalización del módulo y actualiza el progreso
        self.progreso += 1
        self.progress["value"] = self.progreso

        # Calcular el porcentaje completado y actualizar el label
        percentage = int((self.progreso / self.progress["maximum"]) * 100)
        self.percentage_label.config(text=f"{percentage}%")

        if self.progreso >= self.progress["maximum"]:
            print("Todos los módulos completados")

        # Mostrar el detalle del módulo
        modulos = ["Módulo 1. Bienestar Financiero", "Módulo 2. Conociendo mi tarjeta de \ncrédito", "Módulo 3. Planeando mi futuro", "Módulo 4. Estrategias de Ahorro"]
        descripciones = [
            "Aprende a manejar tus finanzas personales de manera efectiva.",
            "Descubre todo lo que necesitas saber sobre el uso de tarjetas de crédito.",
            "Estrategias para planificar y asegurar un futuro próspero.",
            "Mejores prácticas para ahorrar dinero de manera inteligente."
        ]
        self.show_module_detail(modulos[module_number-1], descripciones[module_number-1])


    def clear_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def show_media(self):
        self.clear_main_frame()

        # Crear frames para las diferentes vistas
        self.selection_frame = Frame(self.main_frame)
        self.selection_frame.pack(fill="both", expand=True)

        self.video_frame = Frame(self.main_frame)
        self.video_frame.pack_forget()  # Ocultar el frame de video al inicio

        # Título con el estilo "A un Click"
        Label(self.selection_frame, text="A un Click", font=("Arial", 24, "bold"), bg=self.colors["primary"], fg=self.colors["white"]).pack(pady=20, fill=X)

        # Botones para elegir entre los videos con el mismo estilo que el botón "Enviar"
        Button(self.selection_frame, text="¿Cómo ahorrar con poco dinero?", font=("Arial", 14), bg=self.colors["primary"], fg=self.colors["white"], command=self.play_video1).pack(pady=10)
        Button(self.selection_frame, text="Plan financiero a largo plazo", font=("Arial", 14), bg=self.colors["primary"], fg=self.colors["white"], command=self.play_video2).pack(pady=10)
        Button(self.selection_frame, text="Tarjeta de débito o crédito", font=("Arial", 14), bg=self.colors["primary"], fg=self.colors["white"], command=self.play_video3).pack(pady=10)


    def play_video1(self):
         # URL of the YouTube video with the specific video ID
        video_url = 'https://www.youtube.com/watch?v=1MEn0n9Hd-w'
        # Open a webview window that will display the YouTube video
        webview.create_window('YouTube Video', url=video_url, width=800, height=600)
        webview.start(gui='qt')

    def play_video2(self):
        # URL of the YouTube video with the specific video ID
        video_url = 'https://www.youtube.com/watch?v=1CJE2X7Tmxo'
        # Open a webview window that will display the YouTube video
        webview.create_window('YouTube Video', url=video_url, width=800, height=600)
        webview.start(gui='qt')

    def play_video3(self):
        # URL of the YouTube video with the specific video ID
        video_url = 'https://www.youtube.com/watch?v=z3Ha78V9ZnQ'
        # Open a webview window that will display the YouTube video
        webview.create_window('YouTube Video', url=video_url, width=800, height=600)
        webview.start(gui='qt')

    def play_video(self, video_path):
        """ Reproducir un video y cambiar al frame de video. """
        self.switch_to_video_frame()  # Cambiar al frame de video

        # Si ya hay un video corriendo, lo detenemos antes de cargar el nuevo
        self.stop_video()

        # Cargar el nuevo video
        self.cap = cv2.VideoCapture(video_path)
        if not self.cap.isOpened():
            print(f"Error: No se puede abrir el archivo {video_path}")
            return
        self.video_running = True
        self.stop_update = False  # Reiniciar la actualización de frames
        self.current_video = video_path  # Guardar el video actual
        self.update_video_frame()

    def update_video_frame(self):
        """ Actualizar los frames del video que se está reproduciendo. """
        if self.video_running and self.cap.isOpened() and not self.stop_update:
            ret, frame = self.cap.read()
            if ret:
                # Convertir el frame de OpenCV (BGR) a PIL (RGB)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)
                imgtk = ImageTk.PhotoImage(image=img)
                self.label_video.imgtk = imgtk
                self.label_video.configure(image=imgtk)

                # Volver a llamar a update_video_frame después de 20ms
                self.update_id = self.after(20, self.update_video_frame)
            else:
                self.cap.release()
                self.video_running = False

    def toggle_like(self):
        """ Alternar entre el estado de corazón vacío o lleno (like o no like). """
        if self.liked:
            self.like_button.config(image=self.heart_empty)  # Cambiar a corazón vacío
            self.liked = False
        else:
            self.like_button.config(image=self.heart_full)  # Cambiar a corazón lleno
            self.liked = True

    def toggle_share(self):
        """ Alternar entre el estado de compartir vacío o lleno (share o no share). """
        if self.shared:
            self.share_button.config(image=self.share_empty)  # Cambiar a compartir vacío
            self.shared = False
        else:
            self.share_button.config(image=self.share_full)  # Cambiar a compartir lleno
            self.shared = True

    def toggle_save(self):
        """ Alternar entre el estado de guardar vacío o lleno (save o no save). """
        if self.saved:
            self.save_button.config(image=self.save_empty)  # Cambiar a guardar vacío
            self.saved = False
        else:
            self.save_button.config(image=self.save_full)  # Cambiar a guardar lleno
            self.saved = True

    def switch_to_video_frame(self):
        """ Cambiar de la vista de selección al frame de video. """
        self.selection_frame.pack_forget()  # Ocultar el menú de selección
        self.video_frame.pack(fill="both", expand=True)  # Mostrar la vista de video

    def back_to_menu(self):
        """ Regresar al menú de selección de video. """
        self.stop_video()  # Detener el video antes de regresar
        self.video_frame.pack_forget()  # Ocultar el frame de video
        self.selection_frame.pack(fill="both", expand=True)  # Mostrar el menú de selección

    def stop_video(self):
        """ Detener el video actual si está en reproducción. """
        if self.cap is not None:
            self.stop_update = True  # Detener la actualización de frames
            self.video_running = False
            self.cap.release()
            self.label_video.config(image='')  # Limpiar el video anterior

    def show_user(self):
        self.clear_main_frame()

        # Título en la parte superior
        Label(self.main_frame, text=f"¡Hola, {self.usuarios[self.username][3]}!", font=("Arial", 18, "bold"), bg=self.colors["white"], fg="#000000").pack(pady=10)

        # Descargar y mostrar la foto de perfil desde el enlace
        url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT-HmAlYRaMiTx6PqSGcL9ifkAFxWHVPvhiHQ&s"
        response = requests.get(url)
        img_data = response.content
        img = Image.open(BytesIO(img_data))
        img = img.resize((100, 100), Image.Resampling.LANCZOS)  # Ajustar el tamaño de la imagen
        profile_pic = ImageTk.PhotoImage(img)

        profile_label = Label(self.main_frame, image=profile_pic, bg=self.colors["white"])
        profile_label.image = profile_pic  # Mantener la referencia de la imagen
        profile_label.pack(pady=10)

        # Texto debajo de la foto de perfil
       
        # Espacio para los datos del usuario
        # Primero, define un diccionario para almacenar los Entry widgets
        self.entry_fields = {}

        # Luego, al crear cada Entry, guarda la referencia en el diccionario
        fields = ["Personalidad:", "Objetivo:", "Saldo:", "Ahorros:"]
        for field in fields:
            Label(self.main_frame, text=field, font=("Arial", 12), bg=self.colors["white"], anchor="w").pack(fill=X, padx=20, pady=5)
            entry = Entry(self.main_frame, font=("Arial", 12), bg="#f0f0f0")
            entry.pack(fill=X, padx=20, pady=5)
            self.entry_fields[field] = entry  # Guarda la referencia en el diccionario

        # Ahora, cuando desees cambiar el valor de un Entry, puedes hacerlo así:
        # Por ejemplo, para cambiar el valor del Entry de "Saldo:"
        self.entry_fields["Personalidad:"].delete(0, END)  # Elimina cualquier texto existente
        self.entry_fields["Personalidad:"].insert(0, self.usuarios[self.username][2])  # Inserta el nuevo valor
        self.entry_fields["Personalidad:"].configure(state='disabled')
        self.entry_fields["Objetivo:"].insert(0, self.usuarios[self.username][4]) 
        self.entry_fields["Saldo:"].insert(0, self.usuarios[self.username][5]) 
        self.entry_fields["Ahorros:"].insert(0, self.usuarios[self.username][6]) 
        #guardar los datos frame de user
        Button(self.main_frame, text="Guardar", font=("Arial", 12), bg="#FF0000", fg="#FFFFFF", bd=0,command=self.guardarDatosUser).pack(pady=10,padx=20)

        # Sección de tarjeta o préstamo
        Label(self.main_frame, text="¿Te interesa un préstamo o una tarjeta?", font=("Arial", 12, "bold"), bg=self.colors["white"], fg="#8B0000").pack(pady=20)
        Button(self.main_frame, text="Me interesa", font=("Arial", 12), bg="#FF0000", fg="#FFFFFF", bd=0,command=self.show_tarjeta).pack(pady=10)
        Button(self.main_frame, text="Cerrar Sesión", font=("Arial", 12), bg="#FF0000", fg="#FFFFFF", bd=0,command=self.login).pack(pady=10,padx=50)

        # Actualiza los botones de navegación
        self.update_nav_button("user")

  
    def show_tarjeta(self):
        self.clear_main_frame()

        # Título en la parte superior
        top_frame = Frame(self.main_frame, bg=self.colors["white"])
        top_frame.pack(fill=X)

        Label(top_frame, text="Solicitud de tarjeta", font=("Arial", 18, "bold"), bg=self.colors["white"], fg="#000000").pack(side=LEFT, pady=10, padx=10)

        # Botón de regresar en la esquina superior derecha
        Button(top_frame, text="Regresar", font=("Arial", 10), bg=self.colors["primary"], fg="#FFFFFF", command=self.show_user).pack(side=RIGHT, pady=10, padx=10)

        # Título de la sección
        Label(self.main_frame, text="¿Te interesa una tarjeta de débito o crédito?", font=("Arial",12, "bold"), bg=self.colors["white"], fg="#000000").pack(pady=20)

        # Tarjeta de débito
        Label(self.main_frame, text="Tarjeta de débito:", font=("Arial", 13, "bold"), bg=self.colors["white"], fg="#8B0000").pack(anchor="w", padx=20)
        Label(self.main_frame, text="1. Ingresa al sitio web oficial de Banorte o descarga nuestra app móvil.", font=("Arial", 12), bg=self.colors["white"], fg="#000000", wraplength=350).pack(anchor="w", padx=20)

        # Enlace clicable
        link = Label(self.main_frame, text="https://www.banorte.com/", font=("Arial", 12), bg=self.colors["white"], fg="#0000FF", cursor="hand2", wraplength=350)
        link.pack(anchor="w", padx=20)
        link.bind("<Button-1>", lambda e: webbrowser.open("https://www.banorte.com/"))

        # Continuar con las instrucciones
        Label(self.main_frame, text="2. Ve a la sección de 'Abrir cuenta en línea' o busca las cuentas de débito disponibles.", font=("Arial", 12), bg=self.colors["white"], fg="#000000", wraplength=350).pack(anchor="w", padx=20)
        Label(self.main_frame, text="3. Completa los formularios con tus datos personales, identificación y comprobante de domicilio.", font=("Arial", 12), bg=self.colors["white"], fg="#000000", wraplength=350).pack(anchor="w", padx=20)
        Label(self.main_frame, text="4. Una vez aprobada la cuenta, recibirás tu tarjeta física por correo o en una sucursal.", font=("Arial", 12), bg=self.colors["white"], fg="#000000", wraplength=350).pack(anchor="w", padx=20)

        # Espacio entre secciones
        Label(self.main_frame, bg=self.colors["white"]).pack(pady=10)

        # Tarjeta de crédito
        Label(self.main_frame, text="Tarjeta de crédito:", font=("Arial", 12, "bold"), bg=self.colors["white"], fg="#8B0000").pack(anchor="w", padx=20)
        Label(self.main_frame, text="1. Ve al sitio web oficial de Banorte y selecciona la tarjeta de crédito que deseas.", font=("Arial", 12), bg=self.colors["white"], fg="#000000", wraplength=350).pack(anchor="w", padx=20)
        
        # Otro enlace clicable
        link_credito = Label(self.main_frame, text="https://www.banorte.com/", font=("Arial", 12), bg=self.colors["white"], fg="#0000FF", cursor="hand2", wraplength=350)
        link_credito.pack(anchor="w", padx=20)
        link_credito.bind("<Button-1>", lambda e: webbrowser.open("https://www.banorte.com/"))

        # Continuar con las instrucciones
        Label(self.main_frame, text="2. Completa el formulario de solicitud con tus datos personales y financieros.", font=("Arial", 12), bg=self.colors["white"], fg="#000000", wraplength=350).pack(anchor="w", padx=20)
        Label(self.main_frame, text="3. En algunos casos, puedes obtener aprobación en línea, aunque pueden requerir documentos adicionales.", font=("Arial", 12), bg=self.colors["white"], fg="#000000", wraplength=350).pack(anchor="w", padx=20)
        Label(self.main_frame, text="4. La tarjeta llegará a tu domicilio si es aprobada.", font=("Arial", 12), bg=self.colors["white"], fg="#000000", wraplength=350).pack(anchor="w", padx=20)

        # Botón para conocer productos
        Button(self.main_frame, text="Conoce nuestros productos", font=("Arial", 12), bg="#FF0000", fg="#FFFFFF", bd=0, command=lambda: webbrowser.open("https://www.banorte.com/wps/portal/banorte/Home/cuentas-y-tarjetas/tarjetas-de-credito")).pack(pady=20)

        # Botón para cerrar
        Button(self.main_frame, text="Cerrar", font=("Arial", 12), bg="#FF0000", fg="#FFFFFF", bd=0, command=self.show_user).pack(pady=10)

    def show_home(self):
        self.clear_main_frame()

        # Definir el progreso inicial basado en módulos completados
        if not hasattr(self, 'progreso'):
            self.progreso = 0

        if not self.usuarios[self.username][1]:
            Label(self.main_frame, text="Módulos personalizados", font=("Arial", 24), bg=self.colors["white"]).pack(pady=50, fill=X)
            Label(self.main_frame, text="Haz tu test de personalidad \ncon el chatbot para acceder a \nlos módulos acorde a ti.", font=("Arial", 16), bg=self.colors["white"]).pack(pady=50, fill=X)
        else:
            Label(self.main_frame, text="Módulos adaptados a ti", font=("Arial", 24), bg=self.colors["white"]).pack(pady=10, fill=X)
            
            # Barra de progreso y porcentaje
            self.progress = ttk.Progressbar(self.main_frame, orient="horizontal", length=300, mode="determinate")
            self.progress.pack(pady=10)
            self.progress["maximum"] = 4  # Número total de módulos
            self.progress["value"] = self.progreso

            self.percentage_label = Label(self.main_frame, text=f"{int((self.progreso / 4) * 100)}%", font=("Arial", 14), bg=self.colors["white"])
            self.percentage_label.pack()

            # Crear un canvas para poder hacer scroll
            canvas = Canvas(self.main_frame, bg=self.colors["white"])
            scrollbar = Scrollbar(self.main_frame, orient="vertical", command=canvas.yview)
            scrollable_frame = Frame(canvas, bg=self.colors["white"])

            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(
                    scrollregion=canvas.bbox("all")
                )
            )

            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)

            # Cargar las imágenes solo una vez
            self.images = {
                "modulo_1": ImageTk.PhotoImage(Image.open(BytesIO(requests.get("https://via.placeholder.com/300x150.png/007BFF/FFFFFF?text=Bienestar+Financiero").content)).resize((300, 150), Image.LANCZOS)),
                "modulo_2": ImageTk.PhotoImage(Image.open(BytesIO(requests.get("https://via.placeholder.com/300x150.png/28A745/FFFFFF?text=Tarjeta+de+Crédito").content)).resize((300, 150), Image.LANCZOS)),
                "modulo_3": ImageTk.PhotoImage(Image.open(BytesIO(requests.get("https://via.placeholder.com/300x150.png/FFC107/FFFFFF?text=Planeando+mi+Futuro").content)).resize((300, 150), Image.LANCZOS)),
                "modulo_4": ImageTk.PhotoImage(Image.open(BytesIO(requests.get("https://via.placeholder.com/300x150.png/17A2B8/FFFFFF?text=Estrategias+de+Ahorro").content)).resize((300, 150), Image.LANCZOS))
            }

            # Lista de módulos con títulos y descripciones
            modulos = [
                {"titulo": "Módulo 1. Bienestar Financiero", "imagen": self.images["modulo_1"], "descripcion": "Aprende a manejar tus finanzas personales de manera efectiva.", "comando": lambda: self.complete_module(1)},
                {"titulo": "Módulo 2. Conociendo mi tarjeta de \ncrédito", "imagen": self.images["modulo_2"], "descripcion": "Descubre todo lo que necesitas saber sobre el uso de tarjetas de crédito.", "comando": lambda: self.complete_module(2)},
                {"titulo": "Módulo 3. Planeando mi futuro", "imagen": self.images["modulo_3"], "descripcion": "Estrategias para planificar y asegurar un futuro próspero.", "comando": lambda: self.complete_module(3)},
                {"titulo": "Módulo 4. Estrategias de Ahorro", "imagen": self.images["modulo_4"], "descripcion": "Mejores prácticas para ahorrar dinero de manera inteligente.", "comando": lambda: self.complete_module(4)},
            ]

            # Agregar cada módulo al scrollable_frame
            for modulo in modulos:
                module_frame = Frame(scrollable_frame, bg=self.colors["white"], pady=10)
                module_frame.pack(fill="x", expand=True)
                Label(module_frame, text=modulo["titulo"], font=("Arial", 16), bg=self.colors["white"]).pack(anchor="w")
                Button(module_frame, image=modulo["imagen"], command=modulo["comando"], bd=0).pack(pady=5)
                module_frame.image = modulo["imagen"]  # Para mantener la referencia

            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

        self.update_nav_button("home")

    def show_module_detail(self, titulo, descripcion):
        self.clear_main_frame()

        Label(self.main_frame, text=titulo, font=("Arial", 15), bg=self.colors["white"]).pack(pady=20)
        Label(self.main_frame, text=descripcion, font=("Arial", 12), bg=self.colors["white"], wraplength=400).pack(pady=20)

        Button(self.main_frame, text="Regresar", font=("Arial", 12), bg=self.colors["primary"], fg=self.colors["white"], command=self.show_home).pack(pady=20)

        self.update_nav_button("home")

    def complete_module(self, module_number):
        # Simula la finalización del módulo y actualiza el progreso
        self.progreso += 1
        self.progress["value"] = self.progreso

        # Calcular el porcentaje completado y actualizar el label
        percentage = int((self.progreso / self.progress["maximum"]) * 100)
        self.percentage_label.config(text=f"{percentage}%")

        if self.progreso >= self.progress["maximum"]:
            print("Todos los módulos completados")

        # Mostrar el detalle del módulo
        modulos = ["Módulo 1. Bienestar Financiero", "Módulo 2. Conociendo mi tarjeta de crédito", "Módulo 3. Planeando mi futuro", "Módulo 4. Estrategias de Ahorro"]
        descripciones = [
            "Aprende a manejar tus finanzas personales de manera efectiva.",
            "Descubre todo lo que necesitas saber sobre el uso de tarjetas de crédito.",
            "Estrategias para planificar y asegurar un futuro próspero.",
            "Mejores prácticas para ahorrar dinero de manera inteligente."
        ]
        self.show_module_detail(modulos[module_number-1], descripciones[module_number-1])


    def guardarDatosUser(self):
        # Obtén la información de los Entry fields
        objetivo = self.entry_fields["Objetivo:"].get()
        saldo = self.entry_fields["Saldo:"].get()
        ahorros = self.entry_fields["Ahorros:"].get()

        # Actualiza los valores en el diccionario self.usuarios
        self.usuarios[self.username][4] = objetivo
        self.usuarios[self.username][5] = saldo
        self.usuarios[self.username][6] = ahorros

        # Muestra un mensaje de confirmación
        messagebox.showinfo("Datos guardados", "¡Tu información ha sido guardada exitosamente!")

    def create_bottom_nav(self):
        nav_frame = Frame(self, bg=self.colors["primary"], height=60)
        nav_frame.pack(side=BOTTOM, fill=X)

        # Crear botones de navegación y almacenarlos en el diccionario
        self.nav_buttons["home"] = Button(nav_frame, text="🏠", font=("Arial", 14), bg=self.colors["primary"], fg=self.colors["white"], bd=0, command=self.show_home)
        self.nav_buttons["home"].pack(side=LEFT, expand=True, fill=BOTH)

        self.nav_buttons["media"] = Button(nav_frame, text="▶", font=("Arial", 14), bg=self.colors["primary"], fg=self.colors["white"], bd=0, command=self.show_media)
        self.nav_buttons["media"].pack(side=LEFT, expand=True, fill=BOTH)

        self.nav_buttons["chatbot"] = Button(nav_frame, text="🤖", font=("Arial", 14), bg=self.colors["primary"], fg=self.colors["white"], bd=0, command=self.show_chatbot)
        self.nav_buttons["chatbot"].pack(side=LEFT, expand=True, fill=BOTH)

        self.nav_buttons["user"] = Button(nav_frame, text="👤", font=("Arial", 14), bg=self.colors["primary"], fg=self.colors["white"], bd=0, command=self.show_user)
        self.nav_buttons["user"].pack(side=LEFT, expand=True, fill=BOTH)

    def update_nav_button(self, selected):
        # Restaurar color de fondo de todos los botones
        for key, button in self.nav_buttons.items():
            button.config(bg=self.colors["primary"])

        # Cambiar color del botón seleccionado
        if selected in self.nav_buttons:
            self.nav_buttons[selected].config(bg=self.colors["selected"])

    def subir_foto(self):
        # Seleccionar imagen
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if file_path:
            self.id_image_path = file_path
            messagebox.showinfo("Éxito", "Imagen cargada con éxito.")
        else:
            messagebox.showerror("Error", "No se seleccionó ninguna imagen.")

    def base_de_datos(self, user, pswrd, identificador):

        if identificador == 1:  # para el login
            if self.usuarios.get(user) and self.usuarios[user][0].lower() == pswrd:
                self.username = user
                self.pantalla_principal()
            else:
                messagebox.showinfo("Error", "Usuario y/o contraseña incorrecto")

    def login(self):
        # Limpiar la ventana
        for widget in self.winfo_children():
            widget.destroy()

        # Cambiar el fondo de la ventana
        self.config(bg="#FF0000")

        # Crear label y campos de texto para el login
        Label(self, text="Iniciar Sesión", font=("Arial", 18), bg="#FF0000", fg="#FFFFFF").pack(pady=20)

        Label(self, text="Usuario", font=("Arial", 12), bg="#FF0000", fg="#FFFFFF").pack(pady=5)
        username_entry = Entry(self, font=("Arial", 12))
        username_entry.pack(pady=5)

        Label(self, text="Contraseña", font=("Arial", 12), bg="#FF0000", fg="#FFFFFF").pack(pady=5)
        password_entry = Entry(self, font=("Arial", 12), show="*")
        password_entry.pack(pady=5)

        self.loginButton = Button(self, text="Iniciar sesión", font=("Arial", 10), bg="#FF0000", fg="#FFFFFF", width=15, command=lambda: self.base_de_datos(username_entry.get(), password_entry.get(),1))
        self.loginButton.pack(pady=20)

        Button(self, text="Verificación Facial", font=("Arial", 10), bg="#FFFFFF", fg="#0000FF", width=15, command=self.verificacion_facial).pack(pady=10)

        # Opción de crear una cuenta
        Label(self, text="¿No tienes cuenta?", font=("Arial", 10), bg="#FF0000").pack(pady=5)
        Button(self, text="Crear cuenta", font=("Arial", 10), bg="#FFFFFF", fg="#FF0000", width=15, command=self.crear_cuenta_paso1).pack(pady=5)
    
    def verificacion_facial(self):
        # Crear etiqueta de estado para la verificación facial
        self.label_status = Label(self, text="", font=("Arial", 24, "bold"), width=15, height=2)
        self.label_status.pack(pady=10)

        # Crear una etiqueta para mostrar el video (traqueo)
        self.label_video = Label(self)
        self.label_video.pack(pady=10)

        # Capturar el video desde la cámara web para la verificación facial
        self.cap = cv2.VideoCapture(0)

        # Verificar si la cámara se abrió correctamente
        if not self.cap.isOpened():
            messagebox.showerror("Error", "No se puede acceder a la cámara")
            return

        # Iniciar la actualización de frames
        self.update_frame()

        # Opción de crear una cuenta (aquí agregamos el botón de Crear cuenta)
        Label(self, text="¿No tienes cuenta?", font=("Arial", 10), bg="#FF0000").pack(pady=5)
        
    def update_frame(self):
        # Leer un frame del video
        ret, frame = self.cap.read()
        
        if not ret:
            print("Error: No se pudo leer el frame")
            return

        # Convertir el frame a escala de grises para la detección de caras
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Cargar el clasificador preentrenado de Haar Cascade para la detección de caras
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        # Detectar las caras en el frame
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)

        if len(faces) > 0:
            # Si se detecta una cara, mostrar "VERIFICADO" con fondo verde
            self.label_status.config(text="VERIFICADO", bg="green", fg="white")
            self.loginButton.config(state=NORMAL)  # Habilitar el botón de inicio de sesión
        else:
            # Si no se detectan caras, mostrar "ERROR" con fondo rojo
            self.label_status.config(text="ERROR", bg="red", fg="white")
            self.loginButton.config(state=DISABLED)  # Deshabilitar el botón de inicio de sesión

        # Dibujar un rectángulo alrededor de cada cara detectada
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Convertir el frame de OpenCV (BGR) a PIL (RGB) para mostrarlo en Tkinter
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)
        imgtk = ImageTk.PhotoImage(image=img)

        # Actualizar el label de video existente con el nuevo frame
        self.label_video.imgtk = imgtk
        self.label_video.configure(image=imgtk)

        # Volver a llamar a update_frame después de 20ms para crear un bucle de actualización de video
        self.after(20, self.update_frame)

    def stop_video(self):
        """ Detener el video y liberar la cámara al salir de la pantalla de login. """
        if self.cap is not None:
            self.cap.release()
            self.cap = None


App().mainloop()