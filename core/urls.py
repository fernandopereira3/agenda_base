from django.urls import path
from agenda.views import (
    agenda,
    editar_agendamento,
    excluir_agendamento,
    get_agendamento,
    finalizar_atendimento,
    finalizar_mobile_page,
    visualizar_atendimento,
    buscar_clientes,
    alterar_status_agendamento,
)

urlpatterns = [
    path("", agenda, name="agenda"),
    path("agenda/editar/<str:id>/", editar_agendamento, name="editar_agendamento"),
    path("agenda/excluir/<str:id>/", excluir_agendamento, name="excluir_agendamento"),
    path("agenda/get/<str:id>/", get_agendamento, name="get_agendamento"),
    path(
        "agenda/finalizar/<str:id>/",
        finalizar_atendimento,
        name="finalizar_atendimento",
    ),
    path(
        "agenda/finalizar-mobile/<str:id>/",
        finalizar_mobile_page,
        name="finalizar_mobile_page",
    ),
    path(
        "agenda/visualizar/<str:id>/",
        visualizar_atendimento,
        name="visualizar_atendimento",
    ),
    path("agenda/buscar-clientes/", buscar_clientes, name="buscar_clientes"),
    path(
        "agenda/status/<str:id>/",
        alterar_status_agendamento,
        name="alterar_status_agendamento",
    ),
]
