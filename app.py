from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.graphics import Color, RoundedRectangle, Rectangle
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp
import speech_recognition as sr
import threading
from fuzzywuzzy import process

# ------------------- BASE DE CONHECIMENTO (perguntas frequentes dos meus familiares) -------------------
base_conhecimento = {

    # --- interação inicial ---
    "olá": "Olá! Espero que esteja bem! Quer ajuda com algo específico?",
    "tudo bem?": "Tudo ótimo por aqui! E com você?",
    "bom dia": "Bom dia! Como posso te ajudar hoje?",
    "boa tarde": "Boa tarde! Tem alguma dúvida que eu possa resolver?",
    "boa noite": "Boa noite! Está precisando de alguma ajuda?",
    "oi chat": "Oiee! Qual é a sua dúvida hoje?",

    # --- Celular ---
    "meu celular está com vírus": (
        "1. Não entre em pânico.\n\n"
        "2. Reinicie o celular.\n\n"
        "3. Instale um antivírus confiável.\n\n"
        "4. Evite baixar apps de sites desconhecidos.\n\n"
        "5. Mantenha o sistema atualizado.\n\n"
        "6. Faça backup de arquivos importantes.\n\n"
        "7. Se continuar, verifique com Alice ou Aline."
    ),
    "celular travando": (
        "1. Reinicie o celular.\n\n"
        "2. Feche apps em segundo plano.\n\n"
        "3. Libere espaço interno.\n\n"
        "4. Atualize o sistema e os apps.\n\n"
        "5. Se continuar, verifique com Alice ou Aline."
    ),
    "celular não carrega": (
        "1. Verifique se o cabo e o carregador estão funcionando.\n\n"
        "2. Limpe a entrada de carga.\n\n"
        "3. Reinicie o celular.\n\n"
        "4. Experimente carregar em outra tomada.\n\n"
        "5. Se não resolver, verifique com Alice ou Aline."
    ),
    "wifi não conecta": (
        "1. Certifique-se de que o Wi-Fi está ligado.\n\n"
        "2. Esqueça a rede e reconecte digitando a senha novamente.\n\n"
        "3. Reinicie o roteador.\n\n"
        "4. Reinicie o celular.\n\n"
        "5. Teste outros dispositivos na mesma rede.\n\n"
        "6. Se não funcionar, verifique com Alice ou Aline."
    ),
    "celular lento": (
        "1. Feche apps em segundo plano.\n\n"
        "2. Limpe cache e arquivos temporários.\n\n"
        "3. Remova apps desnecessários.\n\n"
        "4. Atualize sistema e apps.\n\n"
        "5. Se continuar, verifique com Alice ou Aline."
    ),
    "apps fechando sozinhos": (
        "1. Reinicie o celular.\n\n"
        "2. Atualize o app e o sistema.\n\n"
        "3. Limpe cache do app.\n\n"
        "4. Reinstale o app.\n\n"
        "5. Se não resolver, verifique com Alice ou Aline."
    ),

    # --- Redes sociais ---
    "como recuperar senha do instagram": (
        "1. Verifique se a senha está anotada em algum lugar.\n\n"
        "2. Confira se a senha está salva no seu e-mail.\n\n"
        "3. Tente lembrar com dicas de senha antiga.\n\n"
        "4. Use 'Esqueci minha senha' no Instagram.\n\n"
        "5. Se não conseguir, verifique com Alice ou Aline."
    ),
     # --- Redes sociais ---
    "meu instagram esta com problema": (
        'Talvez você tenha esquecido a senha\n\n'
        "1. Verifique se a senha está anotada em algum lugar.\n\n"
        "2. Confira se a senha está salva no seu e-mail.\n\n"
        "3. Tente lembrar com dicas de senha antiga.\n\n"
        "4. Use 'Esqueci minha senha' no Instagram.\n\n"
        "5. Se não conseguir, verifique com Alice ou Aline."
    ),
     # --- Redes sociais ---
    "meu instagram esta com problema, não consigo entrar": (
        "1. Verifique se a senha está anotada em algum lugar.\n\n"
        "2. Confira se a senha está salva no seu e-mail.\n\n"
        "3. Tente lembrar com dicas de senha antiga.\n\n"
        "4. Use 'Esqueci minha senha' no Instagram.\n\n"
        "5. Se não conseguir, verifique com Alice ou Aline."
    ),
    "como recuperar senha do tiktok": (
        "1. Verifique se a senha está anotada em algum lugar.\n\n"
        "2. Confira se a senha está salva no seu e-mail.\n\n"
        "3. Tente lembrar com dicas de senha antiga.\n\n"
        "4. Use 'Esqueci minha senha' no TikTok.\n\n"
        "5. Se não conseguir, verifique com Alice ou Aline."
    ),
    "como postar no instagram": (
        "1. Abra o Instagram.\n\n"
        "2. Clique em '+' ou 'Adicionar'.\n\n"
        "3. Escolha a foto ou vídeo.\n\n"
        "4. Adicione legenda ou marcações.\n\n"
        "5. Clique em 'Compartilhar'."
    ),
    "como salvar fotos do instagram": (
        "1. Abra a foto.\n\n"
        "2. Clique nos três pontinhos e 'Salvar'.\n\n"
        "3. Se não aparecer, verifique com Alice ou Aline."
    ),
    "whatsapp não envia mensagens": (
        "1. Verifique sua conexão com a internet.\n\n"
        "2. Reinicie o WhatsApp.\n\n"
        "3. Atualize o aplicativo.\n\n"
        "4. Confira se não há restrições de dados.\n\n"
        "5. Se continuar, verifique com Alice ou Aline."
    ),
    "facebook não abre": (
        "1. Verifique a internet.\n\n"
        "2. Limpe cache do navegador ou app.\n\n"
        "3. Atualize o aplicativo.\n\n"
        "4. Tente abrir em outro dispositivo.\n\n"
        "5. Se não abrir, verifique com Alice ou Aline."
    ),
    "youtube não carrega vídeos": (
        "1. Verifique a internet.\n\n"
        "2. Reinicie o app ou navegador.\n\n"
        "3. Limpe cache e cookies.\n\n"
        "4. Atualize o app.\n\n"
        "5. Se não carregar, verifique com Alice ou Aline."
    ),

    # --- Produtividade / organização ---
    "como organizar senhas": (
        "1. Use um caderno ou app confiável de senhas.\n\n"
        "2. Nunca compartilhe suas senhas.\n\n"
        "3. Atualize senhas regularmente.\n\n"
        "4. Habilite autenticação de dois fatores.\n\n"
        "5. Se precisar, verifique com Alice ou Aline."
    ),
    "como liberar espaço no celular": (
        "1. Apague arquivos desnecessários.\n\n"
        "2. Limpe cache de apps.\n\n"
        "3. Transfira fotos e vídeos para nuvem ou PC.\n\n"
        "4. Desinstale apps pouco usados.\n\n"
        "5. Se precisar de ajuda, verifique com Alice ou Aline."
    ),
    "como fazer backup de fotos e arquivos": (
        "1. Use serviços de nuvem (Google Drive, OneDrive, iCloud).\n\n"
        "2. Conecte o celular ao computador e copie arquivos.\n\n"
        "3. Faça backup regularmente.\n\n"
        "4. Se tiver dúvidas, verifique com Alice ou Aline."
    ),
}

# ------------------- FUNÇÃO DE BUSCA -------------------
def buscar_resposta(pergunta):
    melhor_match, score = process.extractOne(pergunta.lower(), base_conhecimento.keys())
    if score > 60:
        return base_conhecimento[melhor_match]
    else:
        return "Desculpe, não sei responder essa pergunta ainda."

# ------------------- CHAT LAYOUT -------------------
class ChatLayout(BoxLayout):

    class RoundedButton(Button):
        def __init__(self, **kwargs):
            bg_color = kwargs.pop('background_color', (1, 1, 1, 1))
            super().__init__(**kwargs)
            self.bg_color = bg_color
            self.background_normal = ''
            self.background_down = ''
            self.bind(pos=self.update_rect, size=self.update_rect)
            with self.canvas.before:
                Color(*self.bg_color)
                self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[20])

        def update_rect(self, *args):
            self.rect.pos = self.pos
            self.rect.size = self.size

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'

        # Fundo geral
        with self.canvas.before:
            Color(228/255, 227/255, 255/255, 1)  # lilás claro
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect, size=self.update_rect)
        

        # ===== ÁREA DO CHAT (SCROLLVIEW) =====
        self.scroll = ScrollView(size_hint=(1, 1))
        self.chat_box = BoxLayout(orientation='vertical', size_hint_y=None, padding=dp(10), spacing=dp(5))
        self.chat_box.bind(minimum_height=self.chat_box.setter('height'))
        self.scroll.add_widget(self.chat_box)
        self.add_widget(self.scroll)

       # ===== BARRA DE ENVIO =====
        barra_envio = BoxLayout(
            size_hint_y=None,
            height=50,
            spacing=5,
            padding=5
        )

        # Campo de texto onde o usuário digita sua mensagem
        self.user_input = TextInput(
            size_hint_x=0.6,
            multiline=False,
            background_color=(1, 1, 1, 1),          # fundo branco
            foreground_color = (0.5, 0.5, 0.5, 1),  # cinza claro
            font_name="Roboto-BoldItalic",
            font_size=15
        )
        barra_envio.add_widget(self.user_input)

        # Função auxiliar para criar botões arredondados
        def criar_botao(texto, cor_fundo, cor_texto, funcao):
            btn = Button(
                text=texto,
                size_hint_x=0.2,
                background_normal='',          # remove a imagem padrão
                background_color=cor_fundo,
                color=cor_texto,
                font_name="Roboto-BoldItalic",
                font_size=18
            )
            btn.bind(on_press=funcao)
            
            # Bordas arredondadas usando canvas
            with btn.canvas.before:
                Color(*cor_fundo)
                btn.rect = RoundedRectangle(pos=btn.pos, size=btn.size, radius=[15])
            
            btn.bind(pos=lambda instance, value: setattr(btn.rect, 'pos', value))
            btn.bind(size=lambda instance, value: setattr(btn.rect, 'size', value))
            return btn

        # Botão de enviar mensagem
        send_button = criar_botao(
            texto="Enviar",
            cor_fundo=(0.705, 0.431, 1, 1),          # roxo
            cor_texto=(0.941, 0.941, 0.941, 1),     # quase branco
            funcao=self.enviar_mensagem
        )
        barra_envio.add_widget(send_button)

        # Botão para iniciar gravação de áudio
        audio_button = criar_botao(
            texto="Falar",
            cor_fundo=(180/255, 110/255, 1, 1),     # roxo 
            cor_texto=(240/255, 240/255, 240/255, 1),
            funcao=self.iniciar_audio
        )
        barra_envio.add_widget(audio_button)

        # Adiciona a barra completa ao layout principal do chat
        self.add_widget(barra_envio)


    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    # ------------------- TEXTO -------------------
    def enviar_mensagem(self, instance):
        mensagem = self.user_input.text.strip()
        if not mensagem:
            return
        self.adicionar_balao(mensagem, usuario=True)
        resposta = buscar_resposta(mensagem)
        self.adicionar_balao(resposta, usuario=False)
        self.user_input.text = ""

    def adicionar_balao(self, texto, usuario=True):
        """
        Funcionalidades:
        - Balão se adapta à largura máxima e altura automática do texto.
        - Um único balão por mensagem, independente do tamanho.
        - Balão alinhado à direita (usuário) ou esquerda (bot).
        - Mantém cores, fonte e formatação.
        - Scroll automático para o último balão.
        """

        anchor = AnchorLayout(
            anchor_x='right' if usuario else 'left',
            size_hint_y=None,
            padding=(dp(20), dp(10), dp(40), dp(10))  # (esquerda, cima, direita, baixo)
        )

        # - Branco para usuário, roxo para chat
        cor = (1, 1, 1, 1) if usuario else (180/255, 110/255, 255/255, 1)

        # 3️⃣ Criar o Label que vai conter o texto da mensagem
        label = Label(
            text=texto,                   # Conteúdo da mensagem
            size_hint=(None, None),       # Largura e altura definidas manualmente
            text_size=(dp(300), None),    # Largura máxima, altura ajusta automaticamente
            halign='left',                # Alinhamento horizontal do texto
            valign='top',                 # Alinhamento vertical do texto
            markup=True,                  # Permite tags de formatação
            font_name="Roboto-BoldItalic",# Fonte personalizada
            font_size=15,                 # Tamanho da fonte
            color=(0.5, 0.5, 0.5, 1) if usuario else (1, 1, 1, 1) # Cor do texto
        )

        # Definir largura fixa do label para corresponder ao text_size
        label.width = dp(300)

        def atualizar_altura(inst, val):
            # val[1] é a altura do texto renderizado
            inst.height = val[1] + dp(12)  # adiciona padding interno
            anchor.height = inst.height     # faz o anchor crescer junto

        # Conectar a função ao evento de alteração de tamanho do texto
        label.bind(texture_size=atualizar_altura)

        with label.canvas.before:
            Color(*cor)
            # Adiciona padding interno do balão
            label.bg_rect = RoundedRectangle(
                size=(label.width + dp(20), label.height + dp(14)),  # largura + padding horizontal, altura + padding vertical
                pos=(label.x - dp(10), label.y - dp(7)),            # desloca para respeitar padding
                radius=[15]
            )

        # Atualizar a posição e tamanho do RoundedRectangle quando o label se mover ou redimensionar
        label.bind(pos=lambda inst, val: setattr(label.bg_rect, 'pos', (val[0] - dp(10), val[1] - dp(7))))
        label.bind(size=lambda inst, val: setattr(label.bg_rect, 'size', (val[0] + dp(20), val[1] + dp(14))))


        anchor.add_widget(label)
        self.chat_box.add_widget(anchor)
        Clock.schedule_once(lambda dt: self.scroll.scroll_to(anchor), 0.01)

    # ------------------- ÁUDIO -------------------
    def iniciar_audio(self, instance):
        # Criar balão temporário "Ouvindo..." centralizado
        ouvindo_anchor = AnchorLayout(
            anchor_x='center',
            size_hint_y=None,
            padding=(dp(15), dp(7))
        )
        label = Label(
            text="Ouvindo...",
            size_hint=(None, None),
            text_size=(dp(250), None),
            halign='center',
            valign='middle',
            markup=True,
            font_name="Roboto-BoldItalic",
            font_size=16,
            color=(0, 0, 0, 1)
        )
        label.width = dp(250)
        label.height = dp(30)
        ouvindo_anchor.height = label.height + dp(10)

        ouvindo_anchor.add_widget(label)
        self.chat_box.add_widget(ouvindo_anchor)
        Clock.schedule_once(lambda dt: self.scroll.scroll_to(ouvindo_anchor), 0.01)

        # Iniciar thread para ouvir
        threading.Thread(target=self.reconhecer_audio, args=(ouvindo_anchor,), daemon=True).start()

    def reconhecer_audio(self, ouvindo_anchor):
        rec = sr.Recognizer()
        try:
            with sr.Microphone() as mic:
                audio = rec.listen(mic, timeout=5, phrase_time_limit=5)
                texto = rec.recognize_google(audio, language="pt-BR")
                # Remover balão "Ouvindo..."
                Clock.schedule_once(lambda dt: self.chat_box.remove_widget(ouvindo_anchor), 0)
                # Atualizar chat com o que o usuário falou
                self.atualizar_chat(texto, usuario=True)
        except sr.UnknownValueError:
            Clock.schedule_once(lambda dt: self.chat_box.remove_widget(ouvindo_anchor), 0)
            self.atualizar_chat("Não entendi o que você falou", usuario=False)
        except sr.RequestError:
            Clock.schedule_once(lambda dt: self.chat_box.remove_widget(ouvindo_anchor), 0)
            self.atualizar_chat("Erro ao conectar com o serviço", usuario=False)
        except sr.WaitTimeoutError:
            Clock.schedule_once(lambda dt: self.chat_box.remove_widget(ouvindo_anchor), 0)
            self.atualizar_chat("Tempo esgotado, tente novamente", usuario=False)

    def atualizar_chat(self, texto, usuario=True):
        """
        Atualiza o chat com balão do usuário ou do bot.
        - Se usuario=True: adiciona balão do usuário e imediatamente processa a resposta do bot.
        - Se usuario=False: adiciona balão do bot.
        """
        def update(dt):
            if usuario:
                # 1. Balão do usuário
                self.adicionar_balao(texto, usuario=True)
                # 2. Processar resposta do bot
                resposta = buscar_resposta(texto)
                # 3. Balão do bot
                self.adicionar_balao(resposta, usuario=False)
            else:
                # Balão do bot (caso precise adicionar isoladamente)
                self.adicionar_balao(texto, usuario=False)
        Clock.schedule_once(update)


# ------------------- APP -------------------
class ChatApp(App):
    def build(self):
        return ChatLayout()


if __name__ == "__main__":
    ChatApp().run()
