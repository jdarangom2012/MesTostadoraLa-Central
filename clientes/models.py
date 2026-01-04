from django.db import models


class Cliente(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)
    id_tipo_cliente = models.ForeignKey('tipo_clientes.TipoCliente', models.SET_NULL, db_column='IdtipoCliente', null=True, blank=True)
    id_tipo_identificacion = models.ForeignKey('tipo_identificacion.TipoIdentificacion', models.SET_NULL, db_column='IdTipoIdentificacion', null=True, blank=True)
    id_estado_cliente = models.ForeignKey('estados_clientes.EstadoCliente', models.SET_NULL, db_column='IdEstadoCliente', null=True, blank=True)
    codigo = models.CharField(db_column='Codigo', max_length=25, blank=True, null=True)
    nombre = models.CharField(db_column='Nombre', max_length=50, blank=True, null=True)
    apellidos = models.CharField(db_column='Apellidos', max_length=50, blank=True, null=True)
    telefono = models.CharField(db_column='Telefono', max_length=30, blank=True, null=True)
    direccion = models.CharField(db_column='Direccion', max_length=35, blank=True, null=True)
    email = models.CharField(db_column='Email', max_length=30, blank=True, null=True)
    representante_legal = models.CharField(db_column='RepresentanteLegal', max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(db_column='created_at', blank=True, null=True)
    updated_at = models.DateTimeField(db_column='updated_at', blank=True, null=True)

    class Meta:
        db_table = 'tblClientes'
        indexes = [
            models.Index(fields=['codigo'], name='idx_cliente_codigo'),
            models.Index(fields=['nombre'], name='idx_cliente_nombre'),
        ]

    def __str__(self):
        return f'{self.nombre} {self.apellidos}' if self.nombre else f'Cliente {self.id}'