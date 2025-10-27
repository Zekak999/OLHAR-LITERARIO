import sys
import os

print("Tentando importar books.apps...")

# Adicionar o diretório ao path
sys.path.insert(0, r"C:\Users\zekak\Desktop\olharliterario-master\olharliterario-master\olhar_literario_django")

try:
    # Configurar Django settings
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'olhar_literario_django.settings')
    
    # Tentar importar books.apps
    print("Importando books.apps.BooksConfig...")
    from books.apps import BooksConfig
    print("[OK] books.apps importado com sucesso!")
    
    # Tentar setup do Django
    print("\nTentando django.setup()...")
    import django
    django.setup()
    print("[OK] Django setup completo!")
    
except Exception as e:
    print(f"[ERRO] {e}")
    import traceback
    traceback.print_exc()
