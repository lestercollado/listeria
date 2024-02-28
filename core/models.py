from django.db import models

# Create your models here.
class Persona(models.Model):
    nombre = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    carnet = models.CharField(max_length=50)
    expediente = models.CharField(max_length=50)
    usuario = models.CharField(max_length=50)
    direccion = models.CharField(max_length=50)
    telefono = models.IntegerField()
    movil = models.IntegerField()
    observacion = models.TextField()    
    instructor = models.BooleanField()
    disponible = models.BooleanField()
    cargo = models.ForeignKey("Cargo", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Persona"
        verbose_name_plural = "Personas"

    def __str__(self):
        return self.nombre + " " + self.apellidos
    
class Cargo(models.Model):
    nombre = models.CharField(max_length=50)
    codigo = models.CharField(max_length=50)
    activo = models.BooleanField() 

    class Meta:
        verbose_name = "Cargo"
        verbose_name_plural = "Cargos"

    def __str__(self):
        return self.name
    
class Categoria(models.Model):
    nombre = models.CharField(max_length=50)
    codigo = models.CharField(max_length=50)
    activo = models.BooleanField() 

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"

    def __str__(self):
        return self.name
    
class Posicion(models.Model):
    nombre = models.CharField(max_length=50)
    codigo = models.CharField(max_length=50)
    activo = models.BooleanField() 

    class Meta:
        verbose_name = "Posicion"
        verbose_name_plural = "Posiciones"

    def __str__(self):
        return self.name
    
class Afectacion(models.Model):
    nombre = models.CharField(max_length=50)
    codigo = models.CharField(max_length=50)
    activo = models.BooleanField() 

    class Meta:
        verbose_name = "Afectacion"
        verbose_name_plural = "Afectaciones"

    def __str__(self):
        return self.name
    
class Turno(models.Model):
    Tipo = (
        (1, "8 horas"),
        (2, "12 horas"),
    )    
    
    nombre = models.CharField(max_length=50)
    codigo = models.CharField(max_length=50)
    tipo = models.PositiveSmallIntegerField(choices=Tipo)
    activo = models.BooleanField() 

    class Meta:
        verbose_name = "Turno"
        verbose_name_plural = "Turnos"

    def __str__(self):
        return self.name + " - " + self.tipo
    
class Vacaciones(models.Model):
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    class Meta:
        verbose_name = "Vacaciones"
        verbose_name_plural = "Vacaciones"

    def __str__(self):
        return self.persona

class AfectacionPersona(models.Model):
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)
    afectacion = models.ForeignKey(Afectacion, on_delete=models.CASCADE)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    class Meta:
        verbose_name = "Afectacion_Persona"
        verbose_name_plural = "Afectaciones_Persona"

    def __str__(self):
        return self.persona
    
class CategoriaPersona(models.Model):
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    principal = models.BooleanField()
    class Meta:
        verbose_name = "Categoria_Persona"
        verbose_name_plural = "Categoria_Persona"

    def __str__(self):
        return self.persona + self.categoria
    
class Rotacion(models.Model):
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)
    turno = models.ForeignKey(Turno, on_delete=models.CASCADE)
    posicion = models.ForeignKey(Posicion, on_delete=models.CASCADE)    
    fecha = models.DateField()
    class Meta:
        verbose_name = "Rotación"
        verbose_name_plural = "Rotaciones"

    def __str__(self):
        return self.persona
    
class Brigada(models.Model):
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)
    turno = models.ForeignKey(Turno, on_delete=models.CASCADE)
    orden = models.IntegerField()
    class Meta:
        verbose_name = "Brigada"
        verbose_name_plural = "Brigadas"

    def __str__(self):
        return self.persona