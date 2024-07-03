from database.DAO import DAO
from model.model import Model

result = DAO.getAllObjects()
print(len(result))

model = (Model())
model.creaGrafo()
connessioni = DAO.getAllConnessioni(model._idMap)
print(len(connessioni))
