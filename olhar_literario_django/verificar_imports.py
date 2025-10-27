import sys
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'olhar_literario_django.settings')

print("=" * 60)
print("Verificando sys.path e módulos...")
print("=" * 60)
print("\nsys.path:")
for i, p in enumerate(sys.path, 1):
    print(f"{i}. {p}")

print("\n" + "=" * 60)
print("Tentando importar Django...")
try:
    import django
    django.setup()
    print("✅ Django importado com sucesso!")
except Exception as e:
    print(f"❌ Erro ao importar Django: {e}")
    import traceback
    traceback.print_exc()
