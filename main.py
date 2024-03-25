import pandas as pd


class MatrizPD:
    def __init__(self) -> None:
        self.heuristicaHearder = ["nome", "heuristica"]
        self.grafoHeader = ["origem", "destino", "distancia"]
        self.openGrafo()
        self.openHeuristica()

    def openGrafo(self):
        self.grafoTable = pd.read_csv("Grafo.txt", names=self.grafoHeader, sep=";")

    def openHeuristica(self):
        self.heuristicaTable = pd.read_csv(
            "Heuristica.txt", names=self.heuristicaHearder, sep=";", index_col="nome"
        )

    def showTables(self):
        print(self.grafoTable)
        print("-----------------------------------------------------")
        print(self.heuristicaTable)

    def getGrafoTable(self):
        return self.grafoTable

    def getHeuristicaTable(self):
        return self.heuristicaTable


class Edge:

    def __init__(self, origem="", destino="", g_distancia=0, h_origem=0, h_destino=0):
        self.origem = origem
        self.destino = destino
        self.g_distancia = g_distancia
        self.h_origem = h_origem
        self.h_destino = h_destino
        self.path = []


class Grafo:
    def __init__(self, grafoTable, hTable) -> None:
        self.grafoTable = grafoTable
        self.hTable = hTable
        self.dic = {}

        for indice, citys in self.grafoTable.iterrows():
            self.addEdge(
                citys["origem"],
                citys["destino"],
                citys["distancia"],
                self.hTable.loc[citys["origem"]][0],
                self.hTable.loc[citys["destino"]][0],
            )
            # self.hTable.loc[citys["origem"]]: localizo a city em que estou criando um nó na tabela dos valores da heuristica; [0]: pego o valor da heuristica

    # TODO: name: origem, distName: city de destino, g: custo entre as citys, h: heuristica
    def addEdge(self, name, distName, g, h, h_dest):

        edge = Edge(name, distName, g, h, h_dest)
        edgeDest = Edge(distName, name, g, h_dest, h)

        if name in self.dic:
            # Este 0 representao o g acumulado (g_accumulate)
            self.dic[name].append(edge)
            # self.dic[name].append([distName, g, h_dest, 0])

            if distName in self.dic:
                self.dic[distName].append(edgeDest)
                # self.dic[distName].append([name, g, h, 0])
            else:
                self.dic[distName] = [edgeDest]
                # self.dic[distName] = [[name, g, h, 0]]
        else:
            self.dic[name] = [edgeDest]
            # self.dic[name] = [[distName, g, h_dest, 0]]
            self.dic[distName] = [edgeDest]
            # self.dic[distName] = [[name, g, h, 0]]

    def getGrafo(self):
        return self.dic



class EstrelaA:
    def __init__(self, grafo) -> None:
        self.grafo = grafo
        self.startSearch("Arad", "Bucareste")

    def cityAleartyFounded(self, current_city, cadidate, city_visiteds) -> bool:
        for city in self.grafo[current_city]:
            if city[0] == cadidate:
                if cadidate in city_visiteds:
                    print(f"city {cadidate} já descoberta!\n")
                    return True
        return False

    def calc_g_amount(self, edge: Edge):
        g_amount = 0
        current_edge = edge

        for p in reversed(edge.path):
            for c in self.grafo[p]:
                if c.destino == current_edge.origem:
                    g_amount += c.g_distancia
                    current_edge = c
                    break
            

        return g_amount

    def showOptions(self, g_options_all):
        for o in g_options_all:
            print(f"{o[0].origem} --{o[1]}--> {o[0].destino}")

    def startSearch(self, source, destiny):
        n = 0
        current_city = source
        current_edge = Edge()
        lastCity = ""
        g_options_all = []  # nome f g_accumulate
        min_result = []
        path = []

        while True:
            print(
                "\n---------------------------------------------------------------------------\n"
                f"PASSO: {n}"
                "\n---------------------------------------------------------------------------\n"
            )
            n += 1

            if current_city == destiny:
                path = current_edge                
                break

            # nextCity[3]: g_accumulate, nextCity[2]: valor de h, nextCity[1]:  custo g, nextCity[0]: nome destino
            for nextCity in self.grafo[current_city]:
                nextCity: Edge
                
                if nextCity.destino in nextCity.path:
                    continue

                g_accumulate = self.calc_g_amount(nextCity)

                custoTotal = nextCity.g_distancia + g_accumulate
                f = custoTotal + nextCity.h_destino

                

                nextCity.path.append(nextCity.origem)

                # Verifico se já não tem uma opção ou se uma opção já foi visitada
                # if (not nextCity[0] in [nome[0] for nome in g_options_all] and not nextCity[0] in city_visiteds):
                g_options_all.append([nextCity, f])

            # min_result = min(g_options_all, key=lambda x: x[1])
            self.showOptions(g_options_all)

            lastCity = current_city
            print(f"Origem: {lastCity}")

            cityBestCost = min(g_options_all, key=lambda x: x[1])
            current_city = cityBestCost[0].destino
            current_edge = cityBestCost[0]

            if len(g_options_all) > 0:
                indexCityChoice = [
                    indice
                    for indice, city in enumerate(g_options_all)
                    if city[0] == current_edge
                ]
                g_options_all.pop(indexCityChoice[0])

            # Verificar que ja foi descoberto
            # if not self.cityAleartyFounded(current_city, min_result[0], city_visiteds):
            #     current_city = min_result[0]
            #     path.append([current_city, min_result[3]])
            #     city_visiteds.append(current_city)

            #     if len(g_options_all) > 0:
            #         indexCityChoice = [indice for indice, city in enumerate(g_options_all) if city[0] == current_city]
            #         g_options_all.pop(indexCityChoice[0])
            #     g_options.clear()
            # else:
            #     current_city = min_result[0]
            #     min_result = min(g_options_all, key=lambda x: x[1])

            print(f"city escolhida: {current_city}")
            for c in self.grafo[current_city]:
                c.path = current_edge.path.copy() #Ele tava compartilhando o mesmo local de memoria

        print(
            "\n---------------------------------------------------------------------------\n"
            f"Melhor Caminho: {path.path} -> {path.destino}\n"
            f"Custo Total: {self.calc_g_amount(nextCity) + path.g_distancia}"
            "\n---------------------------------------------------------------------------\n"
        )


matriz = MatrizPD()
# matriz.showTables()
grafo = Grafo(matriz.getGrafoTable(), matriz.getHeuristicaTable())
caminho = EstrelaA(grafo.getGrafo())
print("Busca Concluida!")
