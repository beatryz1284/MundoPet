# 🐾 MundoPet

## 📌 Sobre o projeto

O **MundoPet** é uma aplicação web desenvolvida para facilitar o cadastro, o gerenciamento e a adoção de animais de estimação.

O sistema é voltado para cães e gatos e permite cadastrar informações dos pets, consultar os animais disponíveis, editar e excluir registros, além de apresentar uma galeria para adoção e um formulário para pessoas interessadas em adotar.

O projeto foi desenvolvido utilizando **Python e Flask** no back-end, **SQLite e SQLAlchemy** para armazenamento e manipulação dos dados, e **HTML5, CSS3 e Bootstrap 5** para a interface.

---

## 🎯 Objetivo

O objetivo do MundoPet é criar uma aplicação web organizada e intuitiva para auxiliar no gerenciamento e na adoção responsável de animais.

Com o sistema, é possível:

- 🐶 Cadastrar cães e gatos
- 🐾 Consultar pets cadastrados
- ✏️ Editar informações dos animais
- 🗑️ Excluir registros
- 🖼️ Adicionar imagens aos pets
- ⭐ Destacar um **Pet da Semana**
- 🔎 Pesquisar e filtrar animais na galeria
- 🧡 Demonstrar interesse em adotar um pet
- 📋 Armazenar os dados utilizando banco de dados SQLite

---

## 💻 Tecnologias utilizadas

- **Python 3**
- **Flask**
- **Flask-SQLAlchemy**
- **SQLAlchemy**
- **SQLite**
- **HTML5**
- **CSS3**
- **Bootstrap 5**
- **Jinja2**

---

## ⚙️ Funcionalidades

### 🐾 Cadastro de pets

O sistema permite cadastrar informações como:

- Nome
- Espécie
- Raça
- Idade
- Unidade da idade
- Sexo
- Porte
- Cidade
- Descrição
- Tutor
- Imagem
- Pet da Semana

### 🔎 Consulta e galeria

Os animais cadastrados são apresentados em uma galeria de adoção, permitindo visualizar suas principais informações.

A galeria também possui recursos de pesquisa e filtros.

### ✏️ Edição

É possível alterar as informações de um pet já cadastrado através da página de gerenciamento.

### 🗑️ Exclusão

O sistema permite excluir um pet cadastrado quando necessário.

### 🧡 Adoção

A aplicação possui um formulário para pessoas interessadas em adotar um animal.

O formulário permite informar:

- Nome
- E-mail
- Telefone
- Pet escolhido
- Mensagem

Os dados da solicitação de adoção são armazenados no banco de dados.

### ⭐ Pet da Semana

O sistema permite destacar um animal como **Pet da Semana**, dando maior destaque ao animal na página inicial.

---

## 🗄️ Banco de dados

O projeto utiliza **SQLite** para armazenamento dos dados e **SQLAlchemy** para realizar a comunicação entre a aplicação Flask e o banco de dados.

O sistema possui os seguintes modelos principais:

### Pet

Responsável pelo armazenamento das informações dos animais cadastrados.

### Adocao

Responsável pelo armazenamento das informações das pessoas interessadas em adotar um pet.

---

## 🛣️ Principais rotas

| Rota | Função |
|---|---|
| `/` | Página inicial |
| `/galeria` | Galeria de pets para adoção |
| `/cadastro` | Cadastro de um novo pet |
| `/pets` | Gerenciamento dos pets |
| `/editar/<id>` | Edição de um pet |
| `/excluir/<id>` | Exclusão de um pet |
| `/adotar` | Formulário de adoção |

---

## 🔄 Operações CRUD

O MundoPet utiliza as operações básicas de CRUD:

- **Create (Criar):** cadastro de novos pets
- **Read (Consultar):** visualização dos pets cadastrados
- **Update (Atualizar):** edição das informações
- **Delete (Excluir):** remoção de registros

---

## 📁 Estrutura do projeto

```text
MundoPet/
│
├── app.py
├── README.md
├── requirements.txt
├── .gitignore
│
├── static/
│   ├── style.css
│   └── img/
│       ├── cachorro.jpg
│       ├── gato.jpg
│       ├── logo-cachorrinho.png
│       └── pets/
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── galeria.html
│   ├── cadastro.html
│   ├── pets.html
│   ├── editar.html
│   └── adotar.html
│
├── instance/
│   └── mundo_pet.db
│
└── venv/