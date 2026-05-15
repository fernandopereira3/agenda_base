from django.db import models
from django_mongodb_backend.fields import ObjectIdAutoField


class Agendamento(models.Model):
    id = ObjectIdAutoField(primary_key=True)
    cliente_nome = models.CharField(max_length=200, verbose_name="Nome do Cliente")
    cliente_telefone = models.CharField(
        max_length=20, verbose_name="Telefone do Cliente", null=True, blank=True
    )
    data_horario = models.DateTimeField(verbose_name="Data e Horário")
    duracao = models.IntegerField(default=60, verbose_name="Duração (min)")
    observacoes = models.TextField(verbose_name="Observações", null=True, blank=True)
    finalizado = models.BooleanField(default=False, verbose_name="Finalizado")
    status = models.CharField(
        max_length=20,
        default="Pendente",
        choices=[
            ("Pendente", "Pendente"),
            ("Aguardando", "Aguardando"),
            ("Em Atendimento", "Em Atendimento"),
        ],
        verbose_name="Status",
    )

    # Nota: o campo `servicos_realizados` é gerenciado diretamente via PyMongo
    # (array de dicts com servico + data_agendamento), sem campo ORM declarado,
    # pois o django_mongodb_backend 6.0.1 tem limitações com EmbeddedModelField.

    class Meta:
        verbose_name = "Agendamento"
        verbose_name_plural = "Agendamentos"
        ordering = ["data_horario"]

    def __str__(self):
        return f"{self.cliente_nome} - {self.data_horario}"

    @property
    def cor(self):
        """Gera uma cor HSL única por cliente, baseada no hash do nome. Não salva no banco."""
        nome = self.cliente_nome or ""
        hue = hash(nome) % 360
        return f"hsl({hue}, 65%, 50%)"
