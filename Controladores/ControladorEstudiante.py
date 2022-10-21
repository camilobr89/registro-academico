from Modelos.Estudiante import Estudiante
from Repositories.EstudianteRepository import EstudianteRepository

class ControladorEstudiante():
    def __init__(self):
        #print("Creando ControladorEstudiante")
        self.estudianteRepository = EstudianteRepository()

    def index(self):
        print("Listar todos los estudiantes")
        # unEstudiante={
        #     "_id":"abc123",
        #     "cedula":"123",
        #     "nombre":"Juan",
        #     "apellido":"Perez"
        # }
        return self.estudianteRepository.findAll()
        
    def create(self,infoEstudiante):
        print("Crear un estudiante")
        # elEstudiante = Estudiante(infoEstudiante)
        # return elEstudiante.__dict__
        nuevoEstudiante = Estudiante(infoEstudiante)
        return self.estudianteRepository.save(nuevoEstudiante)

    def show(self,id):
        print("Mostrando un estudiante con id ",id)
        # elEstudiante = {
        #     "_id": id,
        #     "cedula": "123",
        #     "nombre": "Juan",
        #     "apellido": "Perez"
        # }
        # return elEstudiante
        elEstudiante = Estudiante(self.estudianteRepository.findById(id))
        return elEstudiante.__dict__

    def update(self,id,infoEstudiante):
        print("Actualizando estudiante con id ",id)
        # elEstudiante = Estudiante(infoEstudiante)
        # return elEstudiante.__dict__
        estudianteActual = Estudiante(self.estudianteRepository.findById(id))
        estudianteActual.cedula = infoEstudiante["cedula"]
        estudianteActual.nombre = infoEstudiante["nombre"]
        estudianteActual.apellido = infoEstudiante["apellido"]
        estudianteActual.direccion = infoEstudiante["direccion"]
        estudianteActual.celular = infoEstudiante["celular"]
        return self.estudianteRepository.save(estudianteActual)

    def delete(self,id):
        print("Elimiando estudiante con id ",id)
        # return {"deleted_count":1}
        return self.estudianteRepository.delete(id)