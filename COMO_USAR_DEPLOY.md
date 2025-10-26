# 🎯 Como Usar o Deploy Automático

## Para Usuários Iniciantes (Mais Fácil)

### ✨ Método 1: Duplo Clique (Recomendado)

```
1. Faça suas alterações nos arquivos do projeto
2. Dê duplo clique no arquivo: deploy-rapido.bat
3. Uma janela vai abrir perguntando a mensagem do commit
4. Digite algo como: "Corrigi o bug da busca"
5. Pressione Enter
6. Pronto! ✅
```

**Tempo total**: ~30 segundos

---

## Para Usuários Avançados

### 🖥️ Método 2: Via PowerShell

Abra o PowerShell na pasta do projeto e execute:

```powershell
.\deploy.ps1 -mensagem "Sua mensagem aqui"
```

Ou simplesmente:

```powershell
.\deploy.ps1
```

---

## 📊 O Que Acontece Quando Você Faz Deploy?

```
┌─────────────────────────────────────────┐
│  1. Git Add (Adiciona arquivos)        │
│     ⬇️                                  │
│  2. Git Commit (Salva alterações)      │
│     ⬇️                                  │
│  3. Git Push (Envia para GitHub)       │
│     ⬇️                                  │
│  4. Railway Deploy (Atualiza site)     │
└─────────────────────────────────────────┘
```

---

## ⏱️ Quanto Tempo Demora?

| Etapa | Tempo |
|-------|-------|
| Commit local | 2-5 segundos |
| Push para GitHub | 5-10 segundos |
| Deploy no Railway | 2-3 minutos |
| **TOTAL** | **~3 minutos** |

---

## 🔍 Como Acompanhar o Deploy?

1. Acesse: https://railway.app
2. Faça login
3. Clique no projeto "olharliterario"
4. Vá em "Deployments"
5. Veja o progresso em tempo real

### Status do Deploy:
- 🟡 **Building**: Construindo a aplicação
- 🔵 **Deploying**: Fazendo o deploy
- 🟢 **Success**: Deploy concluído! 🎉
- 🔴 **Failed**: Algo deu errado (veja os logs)

---

## 💡 Exemplos de Mensagens de Commit

### ✅ BOM
```
Fix: Corrigir erro na busca de livros
Feature: Adicionar filtro por autor
Update: Melhorar design da página inicial
Refactor: Otimizar código da biblioteca
Docs: Atualizar documentação
Style: Ajustar cores do tema
```

### ❌ RUIM
```
att
fix
teste
update
```

**Dica**: Seja específico sobre o que você mudou!

---

## 🚨 Problemas Comuns

### Problema: "Nenhuma alteração detectada"
**Solução**: Você não modificou nenhum arquivo. Faça alguma alteração primeiro.

### Problema: "Erro ao fazer push"
**Solução**: 
- Verifique sua conexão de internet
- Confirme que o Git está instalado
- Tente novamente

### Problema: "Deploy falhou no Railway"
**Solução**:
1. Acesse os logs no Railway
2. Veja qual foi o erro
3. Corrija o problema
4. Faça deploy novamente

---

## 📱 Testando Depois do Deploy

Depois que o deploy terminar (status "Success" no Railway):

1. Espere ~30 segundos
2. Acesse o site hospedado
3. Pressione `Ctrl + F5` para recarregar sem cache
4. Teste as alterações

---

## 🎓 Tutorial em Vídeo (Passo a Passo)

**1. Abrir o projeto**
- Navegue até a pasta do projeto no Windows Explorer

**2. Fazer suas alterações**
- Edite os arquivos que precisa (HTML, CSS, JS, Python)
- Salve os arquivos

**3. Executar o deploy**
- Dê duplo clique em `deploy-rapido.bat`
- Digite a mensagem do commit
- Pressione Enter

**4. Acompanhar**
- Abra https://railway.app
- Veja o deploy em andamento

**5. Testar**
- Acesse seu site
- Verifique se as alterações estão lá

---

## 🔐 Segurança

- ✅ O token do GitHub já está configurado
- ✅ Não precisa digitar senha toda vez
- ⚠️ Não compartilhe o arquivo `.git/config` com ninguém

---

## 💻 Comandos Úteis

```powershell
# Ver status do Git
git status

# Ver histórico de commits
git log --oneline

# Ver diferenças não commitadas
git diff

# Desfazer última alteração (CUIDADO!)
git reset --hard HEAD~1
```

---

## 🆘 Precisa de Ajuda?

1. Leia este arquivo novamente 📖
2. Verifique o arquivo `DEPLOY_AUTOMATICO.md` 📄
3. Confira os logs no Railway 🔍
4. Teste localmente antes de fazer deploy 🧪

---

**Criado em**: 26 de Outubro de 2025  
**Versão**: 1.0
