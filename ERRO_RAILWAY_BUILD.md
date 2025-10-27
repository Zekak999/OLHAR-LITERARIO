# 🔴 ERRO DE BUILD NO RAILWAY - NIXPACKS FAILED

**Data**: 27/10/2025  
**Status**: Corrigindo configuração de build

---

## ❌ PROBLEMA IDENTIFICADO

O Railway está falhando no build com "Nixpacks build failed" porque:

1. **Estrutura de diretórios**: O projeto Django está em `olhar_literario_django/` mas o Railway tenta fazer build na raiz
2. **Configuração incompleta**: Nixpacks precisa de instruções explícitas sobre onde estão os arquivos

---

## ✅ CORREÇÕES APLICADAS

### 1. Criado `nixpacks.toml`

Arquivo de configuração do Nixpacks com instruções claras:

```toml
[phases.setup]
nixPkgs = ["python311"]

[phases.install]
cmds = ["pip install -r requirements.txt"]

[phases.build]
cmds = ["cd olhar_literario_django && python manage.py collectstatic --noinput"]

[start]
cmd = "cd olhar_literario_django && gunicorn olhar_literario_django.wsgi:application --bind 0.0.0.0:$PORT --workers 3 --threads 2 --timeout 300"
```

**O que faz:**
- ✅ Especifica Python 3.11
- ✅ Instala dependências do `requirements.txt` (na raiz)
- ✅ Entra em `olhar_literario_django/` para collectstatic
- ✅ Inicia gunicorn no diretório correto

---

### 2. Simplificado `railway.json`

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "cd olhar_literario_django && python manage.py migrate && gunicorn olhar_literario_django.wsgi:application --bind 0.0.0.0:$PORT --workers 3",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

**Mudanças:**
- ✅ Removido `collectstatic` do startCommand (já feito no build)
- ✅ Simplificado comando gunicorn
- ✅ Mantido `cd olhar_literario_django` para garantir

---

## 📋 ESTRUTURA DO PROJETO

```
olharliterario-master/
├── requirements.txt          ← Dependências aqui (raiz)
├── Procfile                 ← Comando alternativo
├── runtime.txt              ← Python 3.11
├── railway.json             ← Configuração Railway
├── nixpacks.toml            ← NOVO - Configuração Nixpacks
└── olhar_literario_django/  ← Projeto Django aqui
    ├── manage.py
    ├── olhar_literario_django/
    │   ├── settings.py
    │   ├── wsgi.py
    │   └── urls.py
    └── books/
```

---

## 🚀 PRÓXIMOS PASSOS

1. **Commit e push** dos arquivos corrigidos
2. **Railway fará novo deploy automaticamente**
3. **Aguardar build completar** (2-3 minutos)
4. **Verificar se deploy funcionou**

---

## 🔍 POSSÍVEIS CAUSAS ADICIONAIS

Se ainda falhar após essas correções, pode ser:

1. **Problema no requirements.txt**: Alguma dependência incompatível
2. **Problema no settings.py**: Configuração errada para produção
3. **Problema de memória**: Build precisa de mais recursos

---

## 📊 ARQUIVOS MODIFICADOS

- ✅ `nixpacks.toml` - CRIADO
- ✅ `railway.json` - SIMPLIFICADO

---

**Status**: Aguardando commit e redeploy
