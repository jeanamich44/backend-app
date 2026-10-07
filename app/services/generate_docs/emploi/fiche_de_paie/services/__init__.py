from . import calculs, ecriture, informations, orchestration

# ----------------------------------------------------------------------

service_ecriture = ecriture
service_informations = informations
service_calculs = calculs
service_orchestration = orchestration

__all__ = [
    "calculs",
    "ecriture",
    "informations",
    "orchestration",
    "service_calculs",
    "service_ecriture",
    "service_informations",
    "service_orchestration",
]
