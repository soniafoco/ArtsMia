import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handleAnalizzaOggetti(self, e):
        self._model.creaGrafo()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato:"))
        self._view.txt_result.controls.append(ft.Text(f"Grafo contiene {self._model.getNumNodes()} nodi"))
        self._view.txt_result.controls.append(ft.Text(f"Grafo contiene {self._model.getNumEdges()} archi"))
        self._view.update_page()

    def handleCompConnessa(self,e):
        id_added = self._view._txtIdOggetto.value

        try:
            int_id = int(id_added)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Il valore inserito è errato"))

        if self._model.checkExistence(int_id):
            self._view.txt_result.controls.append(ft.Text(f"L'oggetto {int_id} è presente nel grafo"))
        else:
            self._view.txt_result.controls.append(ft.Text(f"L'oggetto {int_id} non è presente nel grafo"))

        sizeConnessa = self._model.getConnessa(int_id)

        self._view.txt_result.controls.append(ft.Text(f"la componente connessa che contine {int_id} ha dimensione {sizeConnessa}"))

        # Fill dd
        self._view._ddLun.disabled = False
        self._view._btnCercaPercorso.disabled = False
        options = range(2, sizeConnessa)
        for op in options:
            self._view._ddLun.options.append(ft.dropdown.Option(op))
        #listOptions = list(map(lambda x: ft.dropdown.Option(x), options))

        self._view.update_page()

    def handleCercaPercorso(self, e):
        v0 = int(self._view._txtIdOggetto.value)
        lenght = int(self._view._ddLun.value)
        path, peso = self._model.getBestPath(lenght, self._model.getObjectFromId(v0))
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Percorso trovato con peso migliore = {peso}:"))
        for v in path:
            self._view.txt_result.controls.append(ft.Text(v))
        self._view.update_page()




