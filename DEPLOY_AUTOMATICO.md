# 🚀 Deploy Automático - Olhar Literário

Este projeto possui scripts de deploy automático que facilitam o envio de alterações para o GitHub e Railway.

## 📋 Arquivos de Deploy

### 1. `deploy-rapido.bat` (Recomendado)
Script interativo que faz todo o processo de deploy.

**Como usar:**
1. Faça suas alterações no código
2. Dê duplo clique em `deploy-rapido.bat`
3. Digite uma mensagem descritiva do que foi alterado (ou pressione Enter para usar mensagem padrão)
4. Aguarde o processo finalizar

### 2. `deploy.ps1`
Script PowerShell que realiza o deploy completo.

**Como usar via linha de comando:**
```powershell
.\deploy.ps1 -mensagem "Sua mensagem de commit aqui"
```

Ou simplesmente:
```powershell
.\deploy.ps1
```

## 🔄 O que os scripts fazem?

1. **Verificam alterações** - Detectam arquivos modificados
2. **Fazem commit** - Salvam as alterações no Git local
3. **Fazem push** - Enviam para o GitHub
4. **Disparam deploy** - O Railway detecta automaticamente e inicia o deploy

## ⏱️ Tempo de Deploy

- **Commit e Push**: ~5-10 segundos
- **Deploy no Railway**: ~2-3 minutos

## 📝 Exemplos de Mensagens de Commit

Boas mensagens de commit:
- ✅ "Fix: Corrigir bug na busca de livros"
- ✅ "Feature: Adicionar filtro por gênero"
- ✅ "Update: Melhorar design da página inicial"
- ✅ "Refactor: Otimizar código de busca"

Mensagens ruins:
- ❌ "alterações"
- ❌ "fix"
- ❌ "update"

## 🛠️ Troubleshooting

### Erro: "git: command not found"
**Solução**: Instale o Git ou adicione-o ao PATH do sistema

### Erro ao fazer push
**Solução**: Verifique sua conexão com internet e credenciais do GitHub

### Deploy não inicia no Railway
**Solução**: 
1. Acesse o dashboard do Railway
2. Verifique se o repositório está conectado corretamente
3. Confira os logs de deploy

## 🔐 Segurança

O token de acesso GitHub já está configurado no repositório remoto. Não compartilhe este token publicamente.

## 📱 Deploy via VS Code

Se preferir usar o VS Code, você pode usar o terminal integrado:

```powershell
# No terminal do VS Code (PowerShell)
.\deploy.ps1 -mensagem "Sua mensagem aqui"
```

## 🌐 Verificar Deploy no Railway

Após o deploy:
1. Acesse: https://railway.app/dashboard
2. Selecione seu projeto "olharliterario"
3. Vá em "Deployments" para ver o progresso
4. Quando aparecer "Success", seu site está atualizado!

## 📞 Suporte

Em caso de dúvidas ou problemas:
1. Verifique os logs do Railway
2. Confirme que o push foi enviado ao GitHub
3. Teste localmente antes de fazer deploy

---

**Última atualização**: 26 de outubro de 2025
