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
        self._initialize()
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
                        "Compromisos": {
                            "file": "compromisos.csv",
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
                        "Incidencias": {
                            "file": "incidencias.csv",

                            }
                        }
                    }
                })

    def read(self):
        super().read(self, self.config_file)

    def write(self):
        with open(self.config_file, "wb") as config_file:
            super().write(config_file)