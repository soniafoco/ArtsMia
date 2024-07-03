import copy

import networkx as nx
from database.DAO import DAO

class Model:
    def __init__(self):
        self._artObjects = DAO.getAllObjects()
        self._grafo = nx.Graph() #grafo pesato, semplice e non orientato
        self._grafo.add_nodes_from(self._artObjects)
        self._idMap = {}
        for v in self._artObjects:
            self._idMap[v.object_id] = v

        self._solBest = []
        self._pesoBest = 0

    def creaGrafo(self):
        self.addEdges()

    def getNumNodes(self):
        return len(self._grafo.nodes)

    def getNumEdges(self):
        return len(self._grafo.edges)

    def addEdges(self):
        #self._grafo.edges.clear()

        """
        #SOLUZIONE 1: ciclare sui nodi e fare singola query --> più semplice da scrivere, ma complessità MOLTO grande (da usare solo se i nodi sono pochi)
        for u in self._artObjects:
            for v in self._artObjects:
                peso = DAO.getPeso(u, v)
                self._grafo.add_edge(u, v, weight=peso)
        """

        # SOLUZIONE 2:
        allEdges = DAO.getAllConnessioni(self._idMap)
        for e in allEdges:
            self._grafo.add_edge(e.v1, e.v2, weight=e.peso)
        print(self._grafo)


    def checkExistence(self, idOggetto):
        return idOggetto in self._idMap

    def getConnessa(self, v0_id):
        v0 = self._idMap[v0_id]

        # METODO 1: successori di v0 in DFS
        successors = nx.dfs_successors(self._grafo, v0) #dizionario {nodo : lista di nodi successori del nodo}
        allSuccessors = []
        for v in successors.values():
            allSuccessors.extend(v)
        print(f"Metodo 1 (successori): {len(allSuccessors)}")
        # SBAGLIATO print(f"Metodo 1 (successori): {len(successors.values())}") perchè non prende tutti i successori

        # METODO 2: predecessori di v0 in DFS
        predecessors = nx.dfs_predecessors(self._grafo, v0)  # dizionario {nodo : lista di nodi predecessori del nodo}
        print(f"Metodo 2 (predecessori): {len(predecessors.values())}")

        # METODO 3: conto i nodi dell'albero di visita (il risultato sarà 1 in più perchè considera anche l'origine)
        tree = nx.dfs_tree(self._grafo, v0)  # grafo
        print(f"Metodo 3 (tree): {len(tree.nodes())}")

        # METODO 4: node_connector_component (il risultato sarà 1 in più perchè considera anche l'origine)
        connComponent = nx.node_connected_component(self._grafo, v0)  # lista di nodi
        print(f"Metodo 4 (connected component): {len(connComponent)}")

        return len(connComponent)

    def getObjectFromId(self, idOggetto):
        return self._idMap[idOggetto]

    def getBestPath(self, lenght, v0):
        self._solBest = []
        self._pesoBest = 0

        parziale = [v0]
        for v in self._grafo.neighbors(v0):
            if v.classification == v0.classification:
                parziale.append(v)
                self.ricorsione(parziale,lenght)
                parziale.pop()

        return(self._solBest, self._pesoBest)

    def ricorsione(self, parziale, lenght):
        #Controllo soluzione parziale
        if len(parziale) == lenght:
            if self.peso(parziale) > self._pesoBest:
                self._pesoBest = self.peso(parziale)
                self._solBest = copy.deepcopy(parziale)
            return
        else:
            for v in self._grafo.neighbors(parziale[-1]): #vicini dell'ultimo elemento di parziale
                if v not in parziale and v.classification == parziale[0].classification:
                    parziale.append(v)
                    self.ricorsione(parziale, lenght)
                    parziale.pop()


    def peso(self, parziale):
        peso = 0
        for i in range(len(parziale)-1): #sommo i pesi degli archi successivi
            peso += self._grafo[parziale[i]][parziale[i+1]]["weight"]
        return peso