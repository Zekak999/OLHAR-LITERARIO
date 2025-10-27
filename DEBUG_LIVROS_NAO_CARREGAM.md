# 🔍 DEBUG: Livros não estão carregando

**Data**: 27/10/2025  
**Problema**: Nenhum livro aparece na página inicial

---

## 🎯 DIAGNÓSTICO

### Possíveis Causas:

1. **❓ Banco de dados vazio** - Não há livros cadastrados
2. **❓ Filtro muito restritivo** - Estava buscando apenas `destaque=true`
3. **❓ Erro na API** - `/api/books` retornando erro
4. **❓ Problema no JavaScript** - Erro ao renderizar cards

---

## ✅ CORREÇÕES APLICADAS

### 1️⃣ **Adicionados logs de debug extensivos**

```javascript
async function carregarLivrosDjango() {
    try {
        // Buscar TODOS os livros (removido filtro de destaque)
        console.log('🔍 Buscando livros da API...');
        const res = await fetch('/api/books');
        
        console.log('📡 Resposta da API:', res.status, res.statusText);
        
        if (!res.ok) {
            console.error('❌ Erro ao carregar livros:', res.status);
            return;
        }
        
        const livros = await res.json();
        console.log('📚 Livros recebidos:', livros.length, 'livros');
        console.log('📋 Dados dos livros:', livros);
        
        if (!Array.isArray(livros) || livros.length === 0) {
            console.warn('⚠️ Nenhum livro encontrado!');
            console.log('💡 Execute: python manage.py shell < popular_livros.py');
            return;
        }
        
        const grid = $('#booksGrid');
        if (!grid) {
            console.error('❌ Elemento #booksGrid não encontrado!');
            return;
        }
        
        console.log('✅ Grid encontrado, limpando cards...');
        grid.innerHTML = '';
        
        console.log('📖 Adicionando', livros.length, 'livros...');
        // ... resto do código
    }
}
```

### 2️⃣ **Removido filtro de destaque temporariamente**

**ANTES:**
```javascript
const res = await fetch('/api/books?destaque=true');
```

**DEPOIS:**
```javascript
const res = await fetch('/api/books');
```

Isso mostra TODOS os livros, não apenas os em destaque.

---

## 🔎 COMO VERIFICAR O PROBLEMA

### Opção 1: Console do Navegador

1. Abra o site no navegador
2. Pressione `F12` para abrir DevTools
3. Vá na aba **Console**
4. Recarregue a página
5. Veja os logs:

```
🔍 Buscando livros da API...
📡 Resposta da API: 200 OK
📚 Livros recebidos: 0 livros
⚠️ Nenhum livro encontrado!
💡 Execute: python manage.py shell < popular_livros.py
```

Se aparecer **"0 livros"** = Banco de dados vazio!

---

## 💡 SOLUÇÕES

### Se banco estiver vazio:

#### Opção 1: Popular via Script (RECOMENDADO)
```bash
cd olhar_literario_django
python manage.py shell < popular_livros.py
```

#### Opção 2: Popular via Admin Django
1. Acesse: `https://seu-site.railway.app/admin/`
2. Login com credenciais admin
3. Clique em "Books"
4. Clique em "Add Book"
5. Preencha:
   - ✅ Título
   - ✅ Autor
   - ✅ Gênero
   - ✅ Sinopse
   - ✅ Páginas
   - ✅ Idioma
   - ✅ Ano publicação
   - ✅ **Disponível**: Marcar checkbox
   - ✅ **Destaque**: Marcar checkbox (opcional)
   - ✅ **Capa URL**: Cole URL do Google Drive ou deixe vazio
6. Salve

#### Opção 3: Popular via API
```bash
curl -X POST https://seu-site.railway.app/api/books \
  -H "Content-Type: application/json" \
  -d '{
    "titulo": "Dom Casmurro",
    "autor": "Machado de Assis",
    "genero": "Romance",
    "sinopse": "Clássico da literatura brasileira",
    "paginas": 256,
    "idioma": "Português",
    "ano_publicacao": 1899,
    "disponivel": true,
    "destaque": true
  }'
```

---

## 📋 CHECKLIST DE VERIFICAÇÃO

- [ ] Railway deployment funcionando?
- [ ] API `/api/books` retorna 200?
- [ ] Banco de dados PostgreSQL conectado?
- [ ] Migrations aplicadas?
- [ ] Livros cadastrados no banco?
- [ ] Console mostra logs de debug?
- [ ] Elemento `#booksGrid` existe no HTML?
- [ ] JavaScript sem erros?

---

## 🎯 PRÓXIMOS PASSOS

1. **Aguarde Railway fazer redeploy** (2-3 min)
2. **Abra o site e pressione F12**
3. **Veja o que aparece no console**
4. **Me envie print dos logs**
5. **Vou ajudar a popular o banco se necessário**

---

## 📊 STATUS

✅ **Logs de debug adicionados**  
✅ **Filtro de destaque removido temporariamente**  
✅ **Push realizado para 3 repositórios**  
⏳ **Aguardando Railway redeploy**  
⏳ **Aguardando verificação do console**

---

**Commit**: `62fae1a`  
**Mensagem**: "🐛 DEBUG: Adiciona logs extensivos para debugar carregamento de livros"
