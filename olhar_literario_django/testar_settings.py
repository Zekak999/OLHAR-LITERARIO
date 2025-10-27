import sys
import importlib.util

print("Testando import direto do settings.py...")

# Carregar o arquivo settings.py como módulo
spec = importlib.util.spec_from_file_location(
    "settings",
    r"C:\Users\zekak\Desktop\olharliterario-master\olharliterario-master\olhar_literario_django\olhar_literario_django\settings.py"
)
settings_module = importlib.util.module_from_spec(spec)

try:
    print("Executando settings.py...")
    spec.loader.exec_module(settings_module)
    print("✅ Settings carregado com sucesso!")
    print(f"INSTALLED_APPS: {settings_module.INSTALLED_APPS}")
except Exception as e:
    print(f"❌ Erro ao carregar settings: {e}")
    import traceback
    traceback.print_exc()
