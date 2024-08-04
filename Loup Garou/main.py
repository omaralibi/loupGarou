from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen
import random

class ModernTextInput(TextInput):
    def __init__(self, **kwargs):
        super(ModernTextInput, self).__init__(**kwargs)
        self.background_color = (1, 1, 1, 0.8)
        self.foreground_color = (0, 0, 0, 1)
        self.hint_text_color = (0.5, 0.5, 0.5, 1)
        self.padding = [10, 10]
        self.width = 100
        self.height = 40  # Ajuster la hauteur du TextInput


class ModernLabel(Label):
    def __init__(self, **kwargs):
        super(ModernLabel, self).__init__(**kwargs)
        self.font_size = 24
        self.color = (1,1,1, 1)  # Text color
        self.bold = True

class BackgroundScreen(Screen):
    def __init__(self, **kwargs):
        super(BackgroundScreen, self).__init__(**kwargs)
        self.fond = FloatLayout()
        self.img1 = Image(source='bg.png', allow_stretch=True, keep_ratio=False, size_hint=(1, 1))
        self.fond.add_widget(self.img1)
        self.add_widget(self.fond)

    def create_button(self, text, on_press_callback):
        button = Button(
            text=text,
            size_hint=(None, None),
            size=(200, 60),
            background_normal='',
            background_color=(0.1, 0.6, 0.8, 1),
            color=(1, 1, 1, 1),
            font_size=24,
            bold=True,
            pos_hint={'center_x': 0.5}
        )
        button.bind(on_press=on_press_callback)
        return button


class InputScreen(BackgroundScreen):
    def __init__(self, **kwargs):
        super(InputScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', size_hint=(0.8, 0.8), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        layout.add_widget(Image(source='logo.png', size_hint=(1, 0.2)))
        instructions = ModernLabel(text="Entrez le nombre de joueurs\n", halign='center', size_hint=(1, 0.2),pos_hint={'center_y': 0.3})
        layout.add_widget(instructions)
        self.nb_joueurs_input = ModernTextInput(
            hint_text='Nombre de joueurs',
            multiline=False,
            input_filter='int',
            size_hint=(0.5, None),  # Ajuster la taille
            height=40,  # Ajuster la hauteur
            pos_hint={'center_x': 0.5}
        )
        layout.add_widget(self.nb_joueurs_input)
        button = self.create_button('Entrer les Noms', self.ouvrir_popup_joueurs)
        layout.add_widget(button)
        self.fond.add_widget(layout)

    def show_popup(self, title, message):
        popup = Popup(
            title=title,
            content=Label(text=message),
            size_hint=(0.6, 0.4)
        )
        popup.open()

    def ouvrir_popup_joueurs(self, instance):
        try:
            self.nb_joueurs = int(self.nb_joueurs_input.text)
        except ValueError:
            self.show_popup('Erreur', 'Veuillez entrer un nombre valide pour les joueurs.')
            return
        self.joueurs = []
        self.popup_index = 0
        self.afficher_popup_nom_joueur()

    def afficher_popup_nom_joueur(self):
        if self.popup_index < self.nb_joueurs:
            layout = BoxLayout(orientation='vertical')
            label = ModernLabel(text=f"Nom du Joueur {self.popup_index + 1}:")
            self.joueur_input = ModernTextInput(multiline=False)
            submit_button = self.create_button('Suivant', self.enregistrer_joueur)
            layout.add_widget(label)
            layout.add_widget(self.joueur_input)
            layout.add_widget(submit_button)
            self.joueur_popup = Popup(
                title='Entrer le nom du joueur',
                content=layout,
                size_hint=(0.75, 0.5)
            )
            self.joueur_popup.open()
        else:
            self.afficher_popup_roles()

    def enregistrer_joueur(self, instance):
        nom_joueur = self.joueur_input.text.strip()
        if nom_joueur:
            self.joueurs.append(nom_joueur)
            self.popup_index += 1
            self.joueur_popup.dismiss()
            self.afficher_popup_nom_joueur()
        else:
            self.show_popup('Erreur', 'Le nom du joueur ne peut pas être vide.')

    def afficher_popup_roles(self):
        self.roles = []
        self.popup_index = 0
        self.afficher_popup_role()

    def afficher_popup_role(self):
        if self.popup_index < self.nb_joueurs:
            layout = BoxLayout(orientation='vertical')
            label = ModernLabel(text=f"Rôle {self.popup_index + 1}:")
            self.role_input = ModernTextInput(multiline=False)
            submit_button = self.create_button('Suivant', self.enregistrer_role)
            layout.add_widget(label)
            layout.add_widget(self.role_input)
            layout.add_widget(submit_button)
            self.role_popup = Popup(
                title='Entrer le rôle',
                content=layout,
                size_hint=(0.75, 0.5)
            )
            self.role_popup.open()
        else:
            roles_assignes = assignerRoles(self.joueurs, self.roles)
            self.afficher_roles_un_par_un(roles_assignes)

    def enregistrer_role(self, instance):
        role = self.role_input.text.strip()
        if role:
            self.roles.append(role)
            self.popup_index += 1
            self.role_popup.dismiss()
            self.afficher_popup_role()
        else:
            self.show_popup('Erreur', 'Le rôle ne peut pas être vide.')

    def afficher_roles_un_par_un(self, roles_assignes):
        sm = self.manager
        sm.clear_widgets()  # Nettoie les anciens écrans

        for joueur, role in roles_assignes.items():
            screen = RoleScreen(name=joueur)
            screen.afficher_role(joueur, role)
            sm.add_widget(screen)

        final_screen = ResultScreen(name='result')
        final_screen.afficher_resultats(roles_assignes, self.joueurs, self.roles)
        sm.add_widget(final_screen)

        sm.current = list(roles_assignes.keys())[0]

class RoleScreen(BackgroundScreen):
    def __init__(self, **kwargs):
        super(RoleScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')
        self.role_label = ModernLabel(text='', halign='center', valign='top')
        self.layout.add_widget(self.role_label)
        button = self.create_button('Suivant', self.pass_next)
        self.layout.add_widget(button)
        self.fond.add_widget(self.layout)

    def afficher_role(self, joueur, role):
        self.role_label.text = f"{joueur} : {role}"

    def pass_next(self, instance):
        sm = self.manager
        screens = sm.screens
        current_index = screens.index(self)
        next_index = (current_index + 1) % len(screens)
        sm.current = screens[next_index].name

class ResultScreen(BackgroundScreen):
    def __init__(self, **kwargs):
        super(ResultScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', size_hint=(1, 1))

        # Layout for result label
        result_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.8), padding=[20, 10])
        self.resultat_label = ModernLabel(text='', halign='center', valign='top')
        result_layout.add_widget(self.resultat_label)
        self.layout.add_widget(result_layout)

        # Layout for buttons
        button_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.2), padding=[20, 10])
        
        # Button for "Nouveau Jeu" on the left
        self.nouveau_jeu_button = self.create_button('Nouveau Jeu', self.nouveau_jeu)
        button_layout.add_widget(self.nouveau_jeu_button)
        
        # Spacer to push the button "Nouvelle Partie" to the right
        spacer = Label(size_hint_x=1)  # Spacer takes up the remaining space
        button_layout.add_widget(spacer)
        
        # Button for "Nouvelle Partie" on the right
        self.nouvelle_partie_button = self.create_button('Nouvelle Partie', self.nouvelle_partie)
        button_layout.add_widget(self.nouvelle_partie_button)

        self.layout.add_widget(button_layout)
        self.fond.add_widget(self.layout)

    def afficher_resultats(self, roles_assignes, joueurs, roles):
        resultat = "\nRôles assignés :\n"
        for joueur, role in roles_assignes.items():
            resultat += f"{joueur} : {role}\n"
        self.resultat_label.text = resultat
        self.roles = roles
        self.joueurs = joueurs

    def nouveau_jeu(self, instance):
        sm = self.manager
        sm.current = 'input'

    def nouvelle_partie(self, instance):
        roles_assignes = assignerRoles(self.joueurs, self.roles)
        sm = self.manager
        sm.clear_widgets()
        for joueur, role in roles_assignes.items():
            screen = RoleScreen(name=joueur)
            screen.afficher_role(joueur, role)
            sm.add_widget(screen)
        final_screen = ResultScreen(name='result')
        final_screen.afficher_resultats(roles_assignes, self.joueurs, self.roles)
        sm.add_widget(final_screen)
        sm.current = list(roles_assignes.keys())[0]


class LoupGarouApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(InputScreen(name='input'))
        sm.add_widget(RoleScreen(name='role'))
        sm.add_widget(ResultScreen(name='result'))
        return sm

def choisirRoleAleatoire(listeR):
    if not listeR:
        return None
    index = random.randint(0, len(listeR) - 1)
    role = listeR.pop(index)
    return role

def assignerRoles(joueurs, roles):
    roles_assignes = {}
    roles_restants = roles.copy()
    for joueur in joueurs:
        role = choisirRoleAleatoire(roles_restants)
        roles_assignes[joueur] = role
    return roles_assignes

if __name__ == '__main__':
    LoupGarouApp().run()
