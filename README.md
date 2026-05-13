# App Prestadores de Serviços

## 1. Visão Geral
Este projeto é uma aplicação web para **cadastro, busca e gerenciamento de prestadores de serviços**. O objetivo é facilitar o encontro de profissionais (ex.: eletricista, pedreiro, encanador) por meio de uma interface simples e um banco de dados local.

## 2. Funcionalidades
- Cadastro de prestadores de serviço
- Listagem de prestadores cadastrados
- Busca/filtragem por tipo de serviço e/ou cidade (quando disponível)
- Edição de dados cadastrados
- Exclusão de registros

## 3. Tecnologias Utilizadas
- **Backend:** Python (ex.: Flask)
- **Frontend:** HTML e CSS
- **Banco de Dados:** SQLite (arquivo local)
- **Versionamento:** Git e GitHub

> **Observação:** Os nomes exatos de arquivos, rotas e comandos podem variar conforme a implementação do repositório.

## 4. Estrutura do Projeto (exemplo)
A estrutura abaixo ilustra uma organização comum para aplicações web em Python:

```text
app-prestadores/
├── app.py               # Arquivo principal (inicialização do app)
├── routes.py            # Rotas / controllers (se existir)
├── models.py            # Modelos / entidades do banco (se existir)
├── templates/           # Páginas HTML
├── static/              # CSS/JS/imagens
├── requirements.txt     # Dependências Python
└── (banco).db           # Banco SQLite (pode variar de nome)
```

## 5. Banco de Dados (modelo sugerido)
A aplicação tipicamente utiliza uma tabela para armazenar dados do prestador:

**Prestador**
- `id` (inteiro) — identificador
- `nome` (texto) — nome do prestador
- `servico` (texto) — tipo de serviço
- `telefone` (texto) — contato
- `cidade` (texto) — localização

## 6. Instalação e Execução (Passo a Passo)

### 6.1 Clonar o repositório
```bash
git clone https://github.com/Univesp-Projeto1/app-prestadores.git
cd app-prestadores
```

### 6.2 Criar e ativar ambiente virtual (recomendado)
```bash
python -m venv .venv
```

**Windows**
```bash
.venv\Scripts\activate
```

**Linux/macOS**
```bash
source .venv/bin/activate
```

### 6.3 Instalar dependências
```bash
pip install -r requirements.txt
```

### 6.4 Executar o projeto
Escolha **um** dos comandos abaixo (depende de como o projeto foi implementado):

**Opção A — execução direta**
```bash
python app.py
```

**Opção B — Flask**
```bash
flask run
```

### 6.5 Acessar no navegador
Normalmente o projeto fica disponível em:
- `http://127.0.0.1:5000`

## 7. Como Usar (Manual Rápido)
1. Abra a página inicial no navegador.
2. Acesse a área de **Prestadores** para visualizar a lista.
3. Use a opção **Cadastrar** para inserir um novo prestador.
4. Utilize **Editar** para atualizar informações.
5. Utilize **Excluir** para remover um cadastro.
6. Caso exista busca/filtro, selecione o serviço e/ou cidade para encontrar prestadores com mais rapidez.

## 8. Rotas/Endpoints (exemplo)
> Esta seção é um modelo. Ajuste conforme as rotas reais do seu projeto.

- `GET /` — Página inicial
- `GET /prestadores` — Listagem
- `GET /prestadores/novo` — Formulário de cadastro
- `POST /prestadores` — Criação
- `GET /prestadores/<id>` — Detalhes
- `POST/PUT /prestadores/<id>` — Atualização
- `POST/DELETE /prestadores/<id>` — Remoção

## 9. Limitações Conhecidas
- Banco local (SQLite) pode não ser ideal para muitos usuários simultâneos.
- Pode não haver autenticação/autorização (login) dependendo da versão.

## 10. Melhorias Futuras (sugestões)
- Login e perfis (usuário/administrador)
- Validações mais completas (telefone, campos obrigatórios)
- Deploy em nuvem (Render, Railway, Vercel + API)
- Interface mais moderna e responsiva

---

## Licença
Defina a licença do projeto (ex.: MIT) ou informe “Uso acadêmico”.
