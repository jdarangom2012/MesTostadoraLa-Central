from django.conf import settings
from django.db import models


class Rol(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Rol'
        verbose_name_plural = 'Roles'
        ordering = ['nombre', 'id']

    def __str__(self) -> str:
        return self.nombre


class Modulo(models.Model):
    nombre = models.CharField(max_length=120)
    url = models.CharField(max_length=255)
    icono = models.CharField(max_length=120, blank=True, null=True)
    orden = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Módulo'
        verbose_name_plural = 'Módulos'
        ordering = ['orden', 'nombre', 'id']

    def __str__(self) -> str:
        return self.nombre


class Permiso(models.Model):
    codigo = models.CharField(max_length=120, unique=True)
    descripcion = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Permiso'
        verbose_name_plural = 'Permisos'
        ordering = ['codigo', 'id']

    def __str__(self) -> str:
        return self.codigo


class RolModulo(models.Model):
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE)
    modulo = models.ForeignKey(Modulo, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Rol-Módulo'
        verbose_name_plural = 'Roles-Módulos'
        constraints = [
            models.UniqueConstraint(fields=['rol', 'modulo'], name='uniq_rol_modulo'),
        ]

    def __str__(self) -> str:
        return f"{self.rol} → {self.modulo}"


class RolPermiso(models.Model):
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE)
    permiso = models.ForeignKey(Permiso, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Rol-Permiso'
        verbose_name_plural = 'Roles-Permisos'
        constraints = [
            models.UniqueConstraint(fields=['rol', 'permiso'], name='uniq_rol_permiso'),
        ]

    def __str__(self) -> str:
        return f"{self.rol} → {self.permiso}"


class PerfilUsuario(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile',
    )
    rol = models.ForeignKey(Rol, on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        verbose_name = 'Perfil de Usuario'
        verbose_name_plural = 'Perfiles de Usuario'

    def __str__(self) -> str:
        return f"Perfil {self.user}"


class PermisoCampo(models.Model):
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE)
    modelo = models.CharField(max_length=200)
    campo = models.CharField(max_length=200)
    puede_ver = models.BooleanField(default=True)
    puede_editar = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Permiso por Campo'
        verbose_name_plural = 'Permisos por Campo'
        ordering = ['modelo', 'campo', 'rol_id', 'id']
        constraints = [
            models.UniqueConstraint(fields=['rol', 'modelo', 'campo'], name='uniq_permiso_campo'),
        ]

    def __str__(self) -> str:
        return f"{self.rol} · {self.modelo}.{self.campo}"
