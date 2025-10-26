# 🔍 Guia de Diagnóstico - Problema na Barra de Pesquisa

## 📋 Problema Relatado

**Sintomas:**
1. Quando pesquisa qualquer livro, aparece **todos** os livros
2. Quando pressiona **Enter**, sempre abre **Harry Potter**

---

## ✅ Correções Aplicadas

### 1. **Prevenção de Buscas Múltiplas**
- Adicionada flag `buscaEmAndamento` para evitar chamadas simultâneas
- Previne que Enter e Click disparem múltiplas buscas ao mesmo tempo

### 2. **Logs de Debug Adicionados**
Agora o console mostra:
- 🔍 Termo de busca digitado
- 📂 Tipo de busca selecionado (livros/autores/editoras)
- 🌐 URL da API chamada
- 📚 Quantidade e lista de livros encontrados
- ✅ Para qual livro está redirecionando

### 3. **Normalização do Tipo de Busca**
- Converte o texto do botão para lowercase
- Garante comparação correta (livros/autores/editoras)

---

## 🧪 Como Testar

### Teste 1: Console do Navegador

1. **Abra o site** hospedado no Railway
2. **Pressione F12** para abrir DevTools
3. **Vá na aba Console**
4. **Digite algo na busca** (ex: "Harry")
5. **Pressione Enter** ou clique no ícone de busca

**O que você DEVE ver no console:**
```
🔍 Termo de busca: Harry
📂 Tipo de busca: livros
🔎 Buscando: Harry em livros
🌐 URL da busca: /api/books?q=Harry
📚 Livros encontrados: 1 [{id: 1, titulo: "Harry Potter", ...}]
✅ Redirecionando para: Harry Potter
```

**Se aparecer:**
```
📚 Livros encontrados: 10 [...]
```
→ **Problema**: Backend está retornando todos os livros

### Teste 2: Teste Direto da API

1. **Abra uma nova aba**
2. **Digite na URL:**
   ```
   https://SEU-SITE.railway.app/api/books?q=Harry
   ```
3. **Analise o JSON retornado**

**Resultado esperado:**
- Deve retornar APENAS livros com "Harry" no título
- Se retornar todos os livros → Problema no backend

### Teste 3: Tipos de Busca

1. **Teste busca por autor:**
   - Clique no dropdown "livros"
   - Selecione "autores"
   - Digite um autor (ex: "Rowling")
   - Pressione Enter

2. **Verifique no console:**
```
📂 Tipo de busca: autores
🌐 URL da busca: /api/books?autor=Rowling
```

---

## 🔍 Possíveis Causas do Problema

### Causa 1: Backend Ignorando Parâmetro `q`
**Sintoma:** Retorna todos os livros independente da busca

**Solução:** Verificar `views.py`:
```python
busca = request.GET.get('q')
if busca:
    books = books.filter(titulo__icontains=busca) | books.filter(autor__icontains=busca)
```

### Causa 2: Cache do Navegador
**Sintoma:** Código atualizado mas comportamento antigo

**Solução:**
1. Pressione `Ctrl + Shift + R` (hard reload)
2. Ou limpe o cache do navegador
3. Ou abra em aba anônima

### Causa 3: Script Antigo Carregado
**Sintoma:** Logs de debug não aparecem no console

**Solução:**
1. Verifique se o collectstatic rodou no Railway
2. Confirme que o deploy foi concluído
3. Force reload com `Ctrl + F5`

### Causa 4: Dropdown Resetando
**Sintoma:** Tipo de busca volta para "livros" automaticamente

**Solução:**
Verificar se há código que reseta o dropdown após a busca

---

## 🛠️ Como Coletar Mais Informações

### Opção 1: Copiar Logs do Console
1. Faça uma busca
2. Clique com botão direito no console
3. "Save as..." ou copie os logs
4. Compartilhe os logs

### Opção 2: Inspecionar Requisição
1. **F12 → Aba Network**
2. **Marque "Preserve log"**
3. **Digite algo e pressione Enter**
4. **Clique na requisição "/api/books?..."**
5. **Veja a aba "Response"**

**Exemplo:**
```
Request URL: https://site.railway.app/api/books?q=Harry
Response: [{"id": 1, "titulo": "Harry Potter", ...}]
```

---

## 📊 Checklist de Diagnóstico

- [ ] Deploy concluído no Railway (status "Success")
- [ ] Cache do navegador limpo (Ctrl + Shift + R)
- [ ] Console aberto (F12)
- [ ] Logs de debug aparecendo no console
- [ ] URL da API está correta (/api/books?q=...)
- [ ] Response da API contém apenas livros filtrados
- [ ] Não há erros 404 ou 500 no console

---

## 🚑 Solução Rápida

Se o problema persistir:

1. **Teste a API diretamente:**
   ```
   https://SEU-SITE/api/books?q=teste
   ```

2. **Se a API retornar TUDO:**
   - Problema é no backend (views.py)
   - Verificar filtro de busca

3. **Se a API retornar CORRETO mas site errado:**
   - Problema é no frontend (script.js)
   - Verificar se script correto está carregado

4. **Se sempre abre Harry Potter:**
   - Provavelmente é o primeiro livro no banco
   - Verificar ordem no backend

---

## 📱 Teste Também

- [ ] Busca funciona em diferentes navegadores
- [ ] Busca funciona no mobile
- [ ] Sugestões aparecem ao digitar
- [ ] Modal de resultados aparece para múltiplos livros
- [ ] Redirecionamento funciona para 1 livro

---

## 🆘 Precisa de Ajuda?

**Compartilhe:**
1. Screenshots dos logs do console
2. URL que está sendo chamada (visível no console)
3. Response da API (JSON retornado)
4. Em qual navegador está testando

---

**Atualizado**: 26 de Outubro de 2025  
**Versão**: 2.0 (com logs de debug)
