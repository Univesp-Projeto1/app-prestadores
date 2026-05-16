# App Prestadores de Serviços

## Visão geral

O **App Prestadores de Serviços** é uma aplicação web em Flask criada para conectar clientes a profissionais de serviços domésticos e gerais. A proposta evolui a base já iniciada pela equipe para uma experiência próxima de plataformas como Parafuzo e GetNinjas: o cliente encontra profissionais, filtra por localização, consulta contatos, agenda serviços e acompanha seus dados de perfil.

A implementação atual preserva a estrutura original do projeto e amplia o visual e o fluxo de navegação sem substituir a ideia construída pela equipe.

## Funcionalidades principais

| Área | Funcionalidade |
|---|---|
| Login e cadastro | Autenticação com e-mail e senha, cadastro como cliente ou prestador. |
| Tela inicial | Central de navegação para busca, localização, contatos, agendamentos e perfil. |
| Feed de prestadores | Cards de profissionais com busca por nome, especialidade ou descrição. |
| Perfil do prestador | Modal com descrição, avaliação simulada, contador de serviços, contato e agendamento. |
| Localização | Filtro por cidade e bairro usando os dados cadastrados. |
| Meus contatos | Mini agenda com WhatsApp e e-mail dos profissionais contratados. |
| Agendamentos | Lista de serviços reservados com detalhes expansíveis, status, valor e pagamento simulado. |
| Meu perfil | Exibição e edição de nome, e-mail, CEP, cidade, bairro, contato, especialidade e foto. |

## Tecnologias utilizadas

| Camada | Tecnologia |
|---|---|
| Backend | Python 3 e Flask |
| Servidor de produção | Gunicorn |
| Frontend | HTML, CSS e JavaScript simples |
| Banco de dados | SQLite |
| Deploy | Preparado para Render/Railway ou hospedagem Python compatível com `Procfile` |

## Dados demonstrativos

Ao iniciar o projeto, se ainda não existir nenhum prestador cadastrado, o sistema cria automaticamente alguns profissionais de exemplo, como diarista, eletricista, montadora de móveis e encanador. Isso facilita a apresentação do marketplace sem apagar cadastros reais já existentes.

| Tipo | E-mail | Senha | Observação |
|---|---|---|---|
| Prestador demonstrativo | `ana.diarista@example.com` | `123456` | Criado apenas se não houver prestadores no banco. |
| Prestador demonstrativo | `carlos.eletricista@example.com` | `123456` | Criado apenas se não houver prestadores no banco. |
| Prestador demonstrativo | `marina.montadora@example.com` | `123456` | Criado apenas se não houver prestadores no banco. |
| Prestador demonstrativo | `joao.encanador@example.com` | `123456` | Criado apenas se não houver prestadores no banco. |

## Como executar localmente

```bash
git clone https://github.com/Univesp-Projeto1/app-prestadores.git
cd app-prestadores
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
pip install -r requirements.txt
python app.py
```

No Windows, a ativação do ambiente virtual pode ser feita com:

```bash
.venv\Scripts\activate
```

Depois, acesse no navegador:

```text
http://127.0.0.1:5000
```

## Como publicar como site permanente

O projeto agora possui os arquivos necessários para publicação em plataformas de hospedagem Python:

| Arquivo | Finalidade |
|---|---|
| `requirements.txt` | Lista Flask, Werkzeug e Gunicorn. |
| `Procfile` | Define o comando de produção: `web: gunicorn app:app`. |
| `render.yaml` | Permite criar um serviço web no Render a partir do repositório GitHub. |

### Opção recomendada para apresentação acadêmica: Render

1. Envie as alterações para o GitHub.
2. Acesse [Render](https://render.com/).
3. Crie um novo **Web Service** conectado ao repositório `Univesp-Projeto1/app-prestadores`.
4. Use os comandos abaixo:

| Campo | Valor |
|---|---|
| Build Command | `pip install -r requirements.txt` |
| Start Command | `gunicorn app:app` |
| Environment | Python |

5. Configure a variável de ambiente `SECRET_KEY` com qualquer texto seguro.
6. Publique o serviço e use a URL gerada pela plataforma.

## Observação importante sobre permanência dos dados

A aplicação usa **SQLite**, que é adequado para protótipo, demonstração e projeto acadêmico. Em hospedagens gratuitas, o arquivo do banco pode não ser ideal para produção real com muitos usuários. Para uma versão final mais robusta, recomenda-se migrar o banco para PostgreSQL ou MySQL.

## Estrutura do projeto

```text
app-prestadores/
├── app.py
├── requirements.txt
├── Procfile
├── render.yaml
├── templates/
│   ├── login.html
│   ├── cadastro.html
│   ├── home.html
│   ├── feed.html
│   ├── prestadores.html
│   ├── contatos.html
│   ├── agendamentos.html
│   └── perfil.html
├── static/
│   └── style.css
└── uploads/
```

## Próximas melhorias sugeridas

| Prioridade | Melhoria |
|---|---|
| Alta | Migrar SQLite para PostgreSQL/MySQL em produção. |
| Alta | Criar fluxo real de orçamento entre cliente e prestador. |
| Média | Adicionar avaliações reais após serviço concluído. |
| Média | Adicionar categorias oficiais de serviços. |
| Média | Melhorar controle de permissões entre cliente e prestador. |
| Baixa | Integrar pagamento real em ambiente seguro. |

---

Uso acadêmico.
