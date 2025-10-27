# 🗄️ COMO POPULAR O BANCO DE DADOS NO RAILWAY

**Problema**: Os livros não aparecem no site porque o banco PostgreSQL está vazio.

---

## 🚀 SOLUÇÃO - 3 Formas de Popular

### ✅ **Opção 1: Via Railway CLI (MAIS FÁCIL)**

1. **Abra o terminal do Railway:**
   - Acesse: https://railway.app/dashboard
   - Clique no seu projeto "olharliterario"
   - Clique em "View Logs"
   - Clique em "Shell" (terminal)

2. **Cole este comando:**
```bash
python manage.py shell < popular_railway_shell.py
```

3. **Aguarde a mensagem:** ✅ Pronto! Livros disponíveis no site!

---

### ✅ **Opção 2: Via Django Admin (MANUAL)**

1. **Acesse o admin:**
   - URL: https://capable-solace-production.up.railway.app/admin/
   - Login: (suas credenciais de admin)

2. **Adicione livros manualmente:**
   - Clique em "Books" → "Add Book"
   - Preencha os campos:
     * **Título**: Harry Potter e a Pedra Filosofal
     * **Autor**: J. K. Rowling
     * **Gênero**: Fantasia
     * **Sinopse**: Harry Potter descobre ser um bruxo...
     * **Páginas**: 264
     * **Idioma**: Português
     * **Ano publicação**: 2000
     * **✅ Disponível**: MARCAR
     * **✅ Destaque**: MARCAR
     * **Capa URL**: https://m.media-amazon.com/images/I/81ibfYk4qmL._SY466_.jpg

3. **Salve e repita** para outros livros

---

### ✅ **Opção 3: Via Python Shell Interativo (AVANÇADO)**

1. **No Railway Shell, digite:**
```bash
python manage.py shell
```

2. **Cole linha por linha:**
```python
from books.models import Book

Book.objects.create(
    titulo='Harry Potter e a Pedra Filosofal',
    autor='J. K. Rowling',
    editora='Rocco',
    ano_publicacao=2000,
    isbn='9788532530787',
    genero='Fantasia',
    sinopse='Harry Potter é um garoto órfão que descobre ser um bruxo aos 11 anos.',
    paginas=264,
    idioma='Português',
    disponivel=True,
    destaque=True,
    capa_url='https://m.media-amazon.com/images/I/81ibfYk4qmL._SY466_.jpg'
)

print(f"Total de livros: {Book.objects.count()}")
```

3. **Pressione Ctrl+D** para sair

---

## 🔍 VERIFICAR SE FUNCIONOU

### Via API:
```bash
curl https://capable-solace-production.up.railway.app/api/books
```

Deve retornar JSON com os livros!

### Via Navegador:
- Acesse: https://capable-solace-production.up.railway.app/
- Deve mostrar os livros na página inicial

---

## 📚 LISTA DE LIVROS PARA ADICIONAR

Se optar por adicionar manualmente no admin, use estes dados:

### 1. Harry Potter e a Pedra Filosofal
- **Autor**: J. K. Rowling
- **Gênero**: Fantasia
- **Ano**: 2000
- **Páginas**: 264
- **Capa**: https://m.media-amazon.com/images/I/81ibfYk4qmL._SY466_.jpg
- **✅ Disponível + Destaque**

### 2. A Culpa é das Estrelas
- **Autor**: John Green
- **Gênero**: Romance
- **Ano**: 2012
- **Páginas**: 288
- **Capa**: https://m.media-amazon.com/images/I/71u5f1N3xCL._SY466_.jpg
- **✅ Disponível + Destaque**

### 3. A Sutil Arte de Ligar o Foda-se
- **Autor**: Mark Manson
- **Gênero**: Autoajuda
- **Ano**: 2016
- **Páginas**: 224
- **Capa**: https://m.media-amazon.com/images/I/71QpmGcmjIL._SY466_.jpg
- **✅ Disponível + Destaque**

### 4. 1984
- **Autor**: George Orwell
- **Gênero**: Distopia
- **Ano**: 1949
- **Páginas**: 416
- **Capa**: https://m.media-amazon.com/images/I/819js3EQwbL._SY466_.jpg
- **✅ Disponível + Destaque**

### 5. O Hobbit
- **Autor**: J. R. R. Tolkien
- **Gênero**: Fantasia
- **Ano**: 1937
- **Páginas**: 336
- **Capa**: https://m.media-amazon.com/images/I/91M9xPIf10L._SY466_.jpg
- **✅ Disponível + Destaque**

### 6. O Pequeno Príncipe
- **Autor**: Antoine de Saint-Exupéry
- **Gênero**: Fábula
- **Ano**: 1943
- **Páginas**: 96
- **Capa**: https://m.media-amazon.com/images/I/71OZY035lkL._SY466_.jpg
- **✅ Disponível + Destaque**

---

## ⚠️ IMPORTANTE

**SEMPRE marque:**
- ✅ **Disponível** = `True` (senão não aparece na API)
- ✅ **Destaque** = `True` (para aparecer na página inicial)

---

## 🔧 TROUBLESHOOTING

### ❌ Livros não aparecem mesmo após adicionar?

1. **Verifique a API:**
```bash
curl https://capable-solace-production.up.railway.app/api/books
```

2. **Se retornar `[]` (vazio):**
   - Livros não foram criados OU
   - Campo `disponivel` está `False`

3. **Correção via Shell:**
```python
from books.models import Book
# Marcar TODOS os livros como disponíveis
Book.objects.all().update(disponivel=True, destaque=True)
print(f"Atualizados: {Book.objects.count()} livros")
```

---

## 📝 ARQUIVOS IMPORTANTES

- `popular_railway_shell.py` - Script para Railway Shell
- `popular_livros_railway.py` - Script com mais livros
- Este README - Instruções completas

---

**Boa sorte! 🚀**
