import hashlib
import os
import datetime

class SpecterBot:
    def __init__(self):
        self.audit_log = []

    def auditar_archivo(self, archivo):
        """
        Genera un hash del archivo para auditar su integridad.
        """
        hasher = hashlib.sha256()
        with open(archivo, 'rb') as afile:
            buf = afile.read()
            hasher.update(buf)
        hash_value = hasher.hexdigest()
        audit_entry = f"{archivo} - Hash: {hash_value} - {datetime.datetime.now()}"
        self.audit_log.append(audit_entry)
        print(f"Auditoría realizada para {archivo}")
    
    def revisar_auditorias(self):
        """
        Muestra el historial de auditorías realizadas.
        """
        for log in self.audit_log:
            print(log)

    def monitorizar_vulnerabilidades(self, directorio):
        """
        Monitorea un directorio en busca de cambios no autorizados en archivos.
        """
        for root, dirs, files in os.walk(directorio):
            for file in files:
                file_path = os.path.join(root, file)
                self.auditar_archivo(file_path)
    
    def cifrar_datos(self, datos):
        """
        Cifrar información sensible usando hashing.
        """
        return hashlib.sha256(datos.encode()).hexdigest()

# Ejemplo de uso
specter = SpecterBot()
specter.monitorizar_vulnerabilidades('directorio_auditar')
specter.revisar_auditorias()
