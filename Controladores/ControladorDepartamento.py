from Repositories.DepartamentoRepository import DepartamentoRepository
from Modelos.Departamento import Departamento
class ControladorDepartamento():
    def __init__(self):
        self.DepartamentoRepository = DepartamentoRepository()

    def index(self):
        return self.DepartamentoRepository.findAll()

    def create(self,infoDepartamento):
        nuevoDepartamento=Departamento(infoDepartamento)
        return self.DepartamentoRepository.save(nuevoDepartamento)

    def show(self,id):
        elDepartamento=Departamento(self.DepartamentoRepository.findById(id))
        return elDepartamento.__dict__

    def update(self,id,infoDepartamento):
        DepartamentoActual=Departamento(self.DepartamentoRepository.findById(id))
        DepartamentoActual.nombre=infoDepartamento["nombre"]
        DepartamentoActual.descripcion = infoDepartamento["descripcion"]
        return self.DepartamentoRepository.save(DepartamentoActual)
        
    def delete(self,id):
        return self.DepartamentoRepository.delete(id)