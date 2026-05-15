from django.db import models
from django_mongodb_backend.fields import ObjectIdAutoField


# ─── SERVIÇOS / RECEITAS ────────────────────────────────────────────────────
class Servicos(models.Model):
    FORMA_PAGAMENTO_CHOICES = [
        ("dinheiro", "Dinheiro"),
        ("cartao_debito", "Cartão Débito"),
        ("cartao_credito", "Cartão Crédito"),
        ("pix", "PIX"),
        ("transferencia", "Transferência"),
        ("boleto", "Boleto"),
        ("a_prazo", "A Prazo"),
    ]

    STATUS_CHOICES = [
        ("pago", "Pago"),
        ("pendente", "Pendente"),
        ("cancelado", "Cancelado"),
        ("estornado", "Estornado"),
    ]

    id = ObjectIdAutoField(primary_key=True)

    descricao = models.CharField(
        max_length=200, verbose_name="Descrição", null=False, blank=False
    )

    servico = models.CharField(
        max_length=200, verbose_name="Serviço", null=True, blank=True
    )

    valor = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Valor", null=False, blank=False
    )

    data = models.DateField(verbose_name="Data", null=False, blank=False)

    forma_pagamento = models.CharField(
        max_length=20,
        choices=FORMA_PAGAMENTO_CHOICES,
        verbose_name="Forma de Pagamento",
        null=False,
        blank=False,
    )

    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="pago", verbose_name="Status"
    )

    observacoes = models.TextField(verbose_name="Observações", null=True, blank=True)

    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Data de Cadastro"
    )

    updated_at = models.DateTimeField(auto_now=True, verbose_name="Última Atualização")

    class Meta:
        db_table = "financeiro_servicos"
        verbose_name = "Serviço Financeiro"
        verbose_name_plural = "Serviços Financeiros"
        ordering = ["-data", "-created_at"]
        indexes = [
            models.Index(fields=["-data"]),
            models.Index(fields=["status"]),
        ]

    def __str__(self):
        return f"Receita: {self.descricao} - R$ {self.valor}"


class Fluxo(models.Model):
    descricao = models.CharField(
        max_length=200, verbose_name="Descrição", null=False, blank=False, default=""
    )

    servico = models.CharField(
        max_length=200, verbose_name="Serviço", null=True, blank=True
    )

    valor = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Valor", null=False, blank=False
    )

    data = models.DateField(verbose_name="Data", null=False, blank=False)

    forma_pagamento = models.CharField(
        max_length=20,
        choices=Servicos.FORMA_PAGAMENTO_CHOICES,
        verbose_name="Forma de Pagamento",
        null=False,
        blank=False,
    )

    tipo = models.CharField(max_length=50, verbose_name="Tipo", null=True, blank=True)

    class Meta:
        db_table = "financeiro_fluxo"
        verbose_name = "Fluxo Financeiro"
        verbose_name_plural = "Fluxos Financeiros"
        ordering = ["-data"]
        indexes = [
            models.Index(fields=["-data"]),
        ]

    def __str__(self):
        return f"Fluxo: {self.descricao} - R$ {self.valor}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
