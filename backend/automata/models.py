from django.db import models

class AutomataModel(models.Model):
    """
    Modelo para guardar autómatas en la base de datos.
    """
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    automata_type = models.CharField(max_length=10, choices=[
        ('AFND', 'AFND'),
        ('AFD', 'AFD'),
    ])
    nodes = models.JSONField()
    edges = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.automata_type})"
    
    @property
    def to_dict(self):
        """Convierte el modelo a un diccionario para la API."""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'automataType': self.automata_type,
            'nodes': self.nodes,
            'edges': self.edges,
            'createdAt': self.created_at.isoformat(),
            'updatedAt': self.updated_at.isoformat(),
        }