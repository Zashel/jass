import os
import configparser as cp
import json

class Config(cp.ConfigParser):
    def __init__(self):
        super().__init__()
        self.this_path = os.path.dirname(os.path.abspath(__file__))
        self.root_path = os.path.split(self.this_path)[0]
        self.local_path = os.path.join(os.environ["LOCALAPPDATA"], "jassbxi")
        self.config_file = os.path.join(self.local_path, "config.ini")
        if not os.path.exists(self.local_path):
            os.makedirs(self.local_path)
            self.write()
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
                    },
                "data": {
                    "remote": r"app/jassbxi/data",
                    },
                "commitments": {
                    "file": "commitments.csv",
                    "fields": "unique_id|batch_name|year|user|customer_id|contact_phone|day|hour|type|status|comment",
                    "index": "unique_id|batch_name|year|user|customer_id|contact_phone|day|hour|type|status",
                    },
                "commitments_selectors": {
                    "type": "tc|tr",
                    "status": "pending|updated|partial_payment|refusal|no-answer"
                    },
                "complaints": {
                    "file": "complaints.csv",
                    "fields": "unique_id|batch_name|year|user|customer_id|contact_phone|day|reason|comment",
                    "index": "unique_id|batch_name|year|user|customer_id|contact_phone|day|reason",
                    },
                "complaints-selectors": {
                    "type":
                        "unit_not_redelivered|unattended_cancellation|unaplied_discount|suscripted_sms|"+
                        "special_services_800|supplementary_installation|demise|unacknowledged_service|other_reason",
                    },
                "VirtualGPIO": {
                    "remote": r"app/jassbxi/communication",
                    },
                "WebSocket": {
                    "dir": "127.0.0.1",
                    "port": 5277,
                    "html": r"jassbxi.html"
                    },
                })

    def read(self):
        self._initialize()
        super().read(self.config_file)

    def write(self):
        with open(self.config_file, "wb") as config_file:
            super().write(config_file)

class Locale():
    def __init__(self, lang):
        self._language = lang
        self._localization = {
            "tc": {
                "location_spanish": "Pago TC",
                "location_english": "Credit Card Payment"
                },
            "tr": {
                "location_spanish": "Pago Transferencia",
                "location_english": "Bank Transfer Payment"
                },
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
            "commitments": {
                "location_spanish": "Compromisos",
                "location_english": "Commitments",
            },
            "unique_id": {
                "location_spanish": "ID",
                "location_english": "ID",
                },
            "batch_name": {
                "location_spanish": "Nombre Campaña",
                "location_english": "Campaign Name",
                },
            "year": {
                "location_spanish": "Año",
                "location_english": "Year",
                },
            "user": {
                "location_spanish": "Usuario",
                "location_english": "User",
                },
            "customer_id": {
                "location_spanish": "NIF",
                "location_english": "Customer ID",
                },
            "contact_phone": {
                "location_spanish": "Teléfono de Contacto",
                "location_english": "Contact Phone",
                },
            "day": {
                "location_spanish": "Día",
                "location_english": "Day",
                },
            "hour": {
                "location_spanish": "Hora",
                "location_english": "Hour",
                },
            "type": {
                "location_spanish": "Tipo",
                "location_english": "Type",
                },
            "status": {
                "location_spanish": "Estado",
                "location_english": "Status",
                },
            "comment": {
                "location_spanish": "Comentario",
                "location_english": "Comment",
                },
            "complaints": {
                "location_spanish": "Incidencias",
                "location_english": "Complaints",
                },
            "reason": {
                "location_spanish": "Motivo",
                "location_english": "Reason",
                },
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
            }

    @property
    def language(self):
        return self._language

    def __getkey__(self, key):
        return self._localization[key][self.language]

    def __getattr__(self, attr):
        if attr in self._localization:
            return self._localization[attr][self.language]

    def to_dict(self):
        final = dict()
        for item in self._localization:
            final[item] = self._localization[item][self.language]
        return final

    def to_json(self):
        return json.dumps(self.to_dict())
