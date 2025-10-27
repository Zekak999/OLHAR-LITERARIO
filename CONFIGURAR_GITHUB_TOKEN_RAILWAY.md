# 🔑 Configurar GitHub Token no Railway

## 📋 Visão Geral
Para que o sistema de upload de avatares funcione corretamente em produção (Railway), é necessário configurar um **GitHub Personal Access Token**. Este token permite que a aplicação faça upload automático de imagens para o repositório GitHub.

---

## 🎯 Passo a Passo

### **1️⃣ Criar GitHub Personal Access Token**

#### **Acessar GitHub**
1. Acesse: https://github.com/settings/tokens
2. Clique em **"Generate new token"** → **"Generate new token (classic)"**

#### **Configurar Permissões**
| Campo | Valor |
|-------|-------|
| **Note** | `Railway - Olhar Literário Upload` |
| **Expiration** | `No expiration` (sem expiração) |
| **Scopes** | ✅ `repo` (Full control of private repositories) |

#### **Copiar Token**
⚠️ **IMPORTANTE**: Copie o token **AGORA** - você não poderá vê-lo novamente!
```
Exemplo: ghp_1234567890abcdefghijklmnopqrstuvwxyz
```

---

### **2️⃣ Configurar no Railway**

#### **Acessar Railway Dashboard**
1. Acesse: https://railway.app/
2. Selecione o projeto **"Olhar Literário"**
3. Clique na aba **"Variables"**

#### **Adicionar Variável de Ambiente**
| Nome | Valor | Descrição |
|------|-------|-----------|
| `GITHUB_TOKEN` | `ghp_seu_token_aqui` | Token copiado no passo anterior |
| `GITHUB_REPO` | `vidafacilnohard/olharliterario` | Repositório do projeto |

#### **Salvar**
1. Clique em **"Add"** ou **"Save"**
2. Railway vai **reiniciar** a aplicação automaticamente

---

### **3️⃣ Testar Upload**

#### **Acessar Aplicação em Produção**
```
https://capable-solace-production.up.railway.app/
```

#### **Fazer Login**
```
Email: zekak@zekak.com (admin)
Senha: [sua senha]
```

#### **Testar Upload de Avatar**
1. Acesse **Perfil** (canto superior direito)
2. Clique em **"📷 Enviar Foto"**
3. Selecione uma imagem (JPG, PNG, GIF, WebP - máx 5MB)
4. Observe os logs no Railway

---

## 🔍 Verificar Logs no Railway

### **Acessar Logs**
1. No Railway Dashboard, clique em **"Deployments"**
2. Selecione o último deployment
3. Clique em **"View Logs"**

### **Logs Esperados (Sucesso)**
```
📸 Upload de avatar - Usuário: usuario@email.com
📋 FILES: <MultiValueDict: {'file': [<InMemoryUploadedFile: foto.jpg (image/jpeg)>]}>
📁 Arquivo recebido: foto.jpg - Tamanho: 50000 bytes
✅ Perfil encontrado: Perfil de usuario@email.com
✅ Arquivo avatars/foto.jpg enviado para o GitHub!
🌐 URL: https://cdn.jsdelivr.net/gh/vidafacilnohard/olharliterario@main/olhar_literario_django/media/avatars/foto.jpg
✅ Avatar salvo com sucesso!
```

### **Logs Esperados (Erro - Token Não Configurado)**
```
⚠️ GITHUB_TOKEN não configurado. Salvando localmente...
```
⚠️ Se aparecer este log, o token **NÃO** está configurado corretamente!

---

## 🛠️ Troubleshooting

### **❌ Problema: "GITHUB_TOKEN não configurado"**

#### **Causa**
- Token não foi adicionado no Railway
- Nome da variável está errado

#### **Solução**
1. Verifique se o nome é **exatamente** `GITHUB_TOKEN` (case-sensitive)
2. Verifique se o valor começa com `ghp_`
3. Reinicie o deployment no Railway

---

### **❌ Problema: "401 Unauthorized" ao fazer upload**

#### **Causa**
- Token inválido ou expirado
- Permissões insuficientes

#### **Solução**
1. Gerar novo token com permissão `repo`
2. Atualizar variável `GITHUB_TOKEN` no Railway
3. Aguardar reinicialização automática

---

### **❌ Problema: "404 Not Found" ao fazer upload**

#### **Causa**
- Repositório não existe
- Nome do repositório está errado

#### **Solução**
1. Verificar se `GITHUB_REPO=vidafacilnohard/olharliterario` está correto
2. Verificar se o repositório existe: https://github.com/vidafacilnohard/olharliterario
3. Verificar se o branch é `main` (não `master`)

---

## 📊 Como Funciona

### **Fluxo de Upload**

```mermaid
graph LR
    A[Usuário faz upload] --> B{GITHUB_TOKEN configurado?}
    B -->|Sim| C[Upload via GitHub API]
    B -->|Não| D[Salvar localmente - TEMPORÁRIO]
    C --> E[Commit automático no GitHub]
    E --> F[CDN JSDelivr]
    F --> G[Imagem disponível globalmente]
    D --> H[⚠️ Arquivo será perdido no próximo deploy]
```

### **Vantagens do GitHub Storage**
- ✅ **Persistente**: Arquivos não são perdidos no deploy
- ✅ **CDN Gratuito**: JSDelivr serve arquivos com cache
- ✅ **Versionamento**: Histórico completo no Git
- ✅ **Backup Automático**: Tudo salvo no repositório

---

## 🔐 Segurança

### **✅ Boas Práticas**
- ✅ Nunca commitar o token no código
- ✅ Usar variáveis de ambiente (Railway)
- ✅ Token com escopo mínimo necessário (`repo`)
- ✅ Renovar token periodicamente

### **❌ NÃO FAZER**
- ❌ Colocar token em `settings.py`
- ❌ Commitar arquivo `.env` com token
- ❌ Compartilhar token publicamente
- ❌ Usar token pessoal em produção (criar token dedicado)

---

## 📝 Checklist de Configuração

### **Antes do Deploy**
- [ ] Token criado no GitHub
- [ ] Token copiado (começa com `ghp_`)
- [ ] Permissão `repo` marcada

### **No Railway**
- [ ] Variável `GITHUB_TOKEN` adicionada
- [ ] Variável `GITHUB_REPO` adicionada
- [ ] Deployment reiniciado automaticamente

### **Teste em Produção**
- [ ] Upload de avatar testado
- [ ] Logs verificados (sem "⚠️ GITHUB_TOKEN não configurado")
- [ ] Imagem acessível via CDN
- [ ] URL no formato: `https://cdn.jsdelivr.net/gh/...`

---

## 🆘 Suporte

### **Logs de Debug**
Se algo não funcionar, **sempre** verifique os logs no Railway:
```bash
# Procure por:
✅ Arquivo {nome} enviado para o GitHub!
⚠️ Erro ao fazer upload para o GitHub: {erro}
⚠️ GITHUB_TOKEN não configurado. Salvando localmente...
```

### **URLs de Referência**
- **GitHub Tokens**: https://github.com/settings/tokens
- **Railway Dashboard**: https://railway.app/dashboard
- **JSDelivr CDN**: https://www.jsdelivr.com/github
- **GitHub API Docs**: https://docs.github.com/en/rest/repos/contents

---

## ✅ Conclusão

Com o GitHub Token configurado, o sistema de avatares funcionará perfeitamente em produção:

1. ✅ Usuário faz upload de avatar
2. ✅ Imagem é enviada para o GitHub via API
3. ✅ Commit automático no repositório
4. ✅ Imagem disponível via CDN (JSDelivr)
5. ✅ URL persistente mesmo após novos deploys

**Status**: 🟢 **Pronto para uso em produção!**

---

**Última atualização**: Outubro 2025
