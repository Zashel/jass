import os
import configparser as cp

class Config(cp.ConfigParser):
    def __init__(self):
        super().__init__()
        self.this_path = os.path.dirname(os.path.abspath(__file__))
        self.root_path = os.path.split(self.this_path)[0]
        self.local_path = os.path.join(os.environ["LOCALAPPDATA"], "jassbxi")
        if not os.path.exists(self.local_path):
            os.makedirs(self.local_path)
            self.write()
        self.config_file = os.path.join(self.local_path, "config.ini")
        self.read()

    def _initialize(self):
        super().read_dict({
                "uAgent": {
                        "version": "7.5",
                        "server": "tresma81",
                        "port": 1500,
                        "campaign": "OB_JAZ_BXI",
                        "user": os.environ["USERNAME"],
                        "pwd": "",
                        "extension": ""
                        },
                "JAss": {
                    "location": "location_spanish",
                    "remote": r"app/jassbxi",
                    "data": {
                        "remote": r"app/jassbxi/data",
                        "commitments": {
                            "file": "commitments.csv",
                            "fields": [
                                "unique_id",
                                "batch_name",
                                "year",
                                "user",
                                "customer_id",
                                "contact_phone",
                                "day",
                                "hour",
                                "type",
                                "status",
                                "comment"
                                ],
                            "index": [
                                "unique_id",
                                "batch_name",
                                "year",
                                "user",
                                "customer_id",
                                "contact_phone",
                                "day",
                                "hour",
                                "type",
                                "status"
                                ],
                            "location_spanish": {
                                "commitments": "Compromisos",
                                "unique_id": "ID",
                                "batch_name": "Nombre Campaña",
                                "year": "Año",
                                "user": "Usuario",
                                "customer_id": "NIF",
                                "contact_phone": "Teléfono de Contacto",
                                "day": "Día",
                                "hour": "Hora",
                                "type": "Tipo",
                                "status": "Estado",
                                "comment": "Comentario"
                                },
                            "location_english": {
                                "commitments": "Commitments",
                                "unique_id": "ID",
                                "batch_name": "Campaign Name",
                                "year": "Year",
                                "user": "User",
                                "customer_id": "Customer ID",
                                "contact_phone": "Contact Phone",
                                "day": "Day",
                                "hour": "Hour",
                                "type": "Type",
                                "status": "Status",
                                "comment": "Comment"
                                },
                            "selectors": {
                                "type": {
                                    "tc": {
                                        "location_spanish": "Pago TC",
                                        "location_english": "Credit Card Payment"
                                        },
                                    "tr": {
                                        "location_spanish": "Pago Transferencia",
                                        "location_english": "Bank Transfer Payment"
                                        }
                                    },
                                "status": {
                                    "pending": {
                                        "location_spanish": "Pendiente",
                                        "location_english": "Pending"
                                        },
                                    "updated": {
                                        "location_spanish": "Al Corriente",
                                        "location_english": "Updated"
                                        },
                                    "partial_payment": {
                                        "location_spanish": "Pago Parcial",
                                        "location_english": "Partial Payment"
                                        },
                                    "refusal": {
                                        "location_spanish": "Negativa de Pago",
                                        "location_english": "Refusal of Payment"
                                        },
                                    "no-answer": {
                                        "location_spanish": "No Contesta",
                                        "location_english": "No Answer"
                                        },
                                    }
                                }
                            },
                        "complaints": {
                            "file": "complaints.csv",
                            "fields": [
                                "unique_id",
                                "batch_name",
                                "year",
                                "user",
                                "customer_id",
                                "contact_phone",
                                "day",
                                "reason",
                                "comment"
                                ],
                            "index": [
                                "unique_id",
                                "batch_name",
                                "year",
                                "user",
                                "customer_id",
                                "contact_phone",
                                "day",
                                "reason"
                                ],
                            "location_spanish": {
                                "complaints": "Incidencias",
                                "unique_id": "ID",
                                "batch_name": "Nombre Campaña",
                                "year": "Año",
                                "user": "Usuario",
                                "customer_id": "NIF",
                                "contact_phone": "Teléfono de Contacto",
                                "day": "Día",
                                "reason": "Motivo",
                                "comment": "Comentario"
                                },
                            "location_english": {
                                "complaints": "Complaints",
                                "unique_id": "ID",
                                "batch_name": "Campaign Name",
                                "year": "Year",
                                "user": "User",
                                "customer_id": "Customer ID",
                                "contact_phone": "Contact Phone",
                                "day": "Day",
                                "reason": "Reason",
                                "comment": "Comment"
                                },
                            "selectors": {
                                "type": {
                                    "unit_not_redelivered": {
                                        "location_spanish": "No Devolución Equipo",
                                        "location_english": "Unit Not Redelivered"
                                        },
                                    "unattended_cancellation": {
                                        "location_spanish": "Baja No Cursada",
                                        "location_english": "Unattended Cancellation"
                                        },
                                    "unaplied_discount": {
                                        "location_spanish": "Descuento No Aplicado",
                                        "location_english": "Unaplied Discount"
                                        },
                                    "suscripted_sms": {
                                        "location_spanish": "SMS Suscripción",
                                        "location_english": "Suscripted SMS"
                                        },
                                    "special_services_800": {
                                        "location_spanish": "Servicios Especiales 800",
                                        "location_english": "Special Servicies 800"
                                        },
                                    "supplementary_installation": {
                                        "location_spanish": "Instalación Adicional",
                                        "location_english": "Supplementary Installation"
                                        },
                                    "demise": {
                                        "location_spanish": "Fallecimiento",
                                        "location_english": "Demise"
                                        },
                                    "unacknowledged_service": {
                                        "location_spanish": "Línea No Reconocida",
                                        "location_english": "Unacknowledged Service"
                                        },
                                    "other_reason": {
                                        "location_spanish": "Otros",
                                        "location_english": "Other Reason"
                                        },
                                    },
                                }
                            }
                        }
                    },
                "VirtualGPIO": {
                    "remote": r"app/jassbxi/communication",
                    },
                "WebSocket": {
                    "dir": "127.0.0.1",
                    "port": 5277
                    },
                })

    def read(self):
        self._initialize()
        super().read(self, self.config_file)

    def write(self):
        with open(self.config_file, "wb") as config_file:
            super().write(config_file)