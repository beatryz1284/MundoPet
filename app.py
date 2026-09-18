from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect, text
import os
import uuid

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mundo_pet.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

UPLOAD_FOLDER = os.path.join(
    app.root_path,
    "static",
    "img",
    "pets"
)

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

EXTENSOES_PERMITIDAS = {"png", "jpg", "jpeg", "webp"}


def arquivo_permitido(nome):
    return (
        "." in nome
        and nome.rsplit(".", 1)[1].lower()
        in EXTENSOES_PERMITIDAS
    )


# =========================
# MODELO DOS PETS
# =========================

class Pet(db.Model):
    __tablename__ = "pet"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    especie = db.Column(db.String(50), nullable=False)
    raca = db.Column(db.String(100))
    idade = db.Column(db.Integer)
    unidade_idade = db.Column(db.String(20), default="anos")
    sexo = db.Column(db.String(20))
    porte = db.Column(db.String(30))
    cidade = db.Column(db.String(100))
    descricao = db.Column(db.Text)
    tutor = db.Column(db.String(100), nullable=False)
    imagem = db.Column(db.String(255))
    destaque = db.Column(db.Boolean, default=False)


# =========================
# MODELO DAS ADOÇÕES
# =========================

class Adocao(db.Model):
    __tablename__ = "adocao"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    telefone = db.Column(db.String(30), nullable=False)
    mensagem = db.Column(db.Text)
    pet_id = db.Column(db.Integer, db.ForeignKey("pet.id"), nullable=False)

    pet = db.relationship("Pet", backref="adocoes")


# =========================
# ATUALIZAÇÃO DO BANCO
# =========================

def atualizar_banco():
    db.create_all()

    inspetor = inspect(db.engine)

    # Verifica se a tabela pet existe
    tabelas = inspetor.get_table_names()

    if "pet" in tabelas:
        colunas_existentes = {
            coluna["name"]
            for coluna in inspetor.get_columns("pet")
        }

        novas_colunas = {
            "unidade_idade": 'VARCHAR(20) DEFAULT "anos"',
            "sexo": "VARCHAR(20)",
            "porte": "VARCHAR(30)",
            "cidade": "VARCHAR(100)",
            "descricao": "TEXT",
            "imagem": "VARCHAR(255)",
            "destaque": "BOOLEAN DEFAULT 0"
        }

        for nome_coluna, tipo_coluna in novas_colunas.items():

            if nome_coluna not in colunas_existentes:

                db.session.execute(
                    text(
                        f"""
                        ALTER TABLE pet
                        ADD COLUMN {nome_coluna}
                        {tipo_coluna}
                        """
                    )
                )

        db.session.commit()


# =========================
# SALVAR IMAGEM
# =========================

def salvar_imagem(arquivo):

    if not arquivo or not arquivo.filename:
        return None

    if not arquivo_permitido(arquivo.filename):
        return None

    extensao = arquivo.filename.rsplit(".", 1)[1].lower()

    nome_arquivo = f"{uuid.uuid4().hex}.{extensao}"

    caminho = os.path.join(
        app.config["UPLOAD_FOLDER"],
        nome_arquivo
    )

    arquivo.save(caminho)

    return nome_arquivo


# =========================
# PÁGINA INICIAL
# =========================

@app.route("/")
def inicio():

    pets = Pet.query.order_by(Pet.id.desc()).all()

    pet_destaque = Pet.query.filter_by(
        destaque=True
    ).first()

    return render_template(
        "index.html",
        pets=pets,
        pet_destaque=pet_destaque
    )


# =========================
# GALERIA DE ADOÇÃO
# =========================

@app.route("/galeria")
def galeria():

    pets = Pet.query.order_by(
        Pet.id.desc()
    ).all()

    return render_template(
        "galeria.html",
        pets=pets
    )


# =========================
# CADASTRO DE PET
# =========================

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():

    if request.method == "POST":

        arquivo = request.files.get("imagem")

        nome_imagem = salvar_imagem(arquivo)

        idade_texto = request.form.get(
            "idade",
            ""
        ).strip()

        if idade_texto:

            try:
                idade = int(idade_texto)

            except ValueError:
                idade = None

        else:
            idade = None

        destaque = (
            request.form.get("destaque") == "on"
        )

        if destaque:
            Pet.query.update(
                {Pet.destaque: False}
            )

        novo_pet = Pet(

            nome=request.form.get(
                "nome",
                ""
            ).strip(),

            especie=request.form.get(
                "especie",
                ""
            ).strip(),

            raca=request.form.get("raca"),

            idade=idade,

            unidade_idade=request.form.get(
                "unidade_idade",
                "anos"
            ),

            sexo=request.form.get("sexo"),

            porte=request.form.get("porte"),

            cidade=request.form.get("cidade"),

            descricao=request.form.get(
                "descricao"
            ),

            tutor=request.form.get(
                "tutor",
                ""
            ).strip(),

            imagem=nome_imagem,

            destaque=destaque
        )

        db.session.add(novo_pet)

        db.session.commit()

        return redirect(
            url_for("galeria")
        )

    return render_template(
        "cadastro.html"
    )


# =========================
# GERENCIAR PETS
# =========================

@app.route("/pets")
def pets():

    lista_pets = Pet.query.order_by(
        Pet.id.desc()
    ).all()

    return render_template(
        "pets.html",
        pets=lista_pets
    )


# =========================
# EDITAR PET
# =========================

@app.route(
    "/editar/<int:id>",
    methods=["GET", "POST"]
)
def editar(id):

    pet = Pet.query.get_or_404(id)

    if request.method == "POST":

        pet.nome = request.form.get(
            "nome",
            ""
        ).strip()

        pet.especie = request.form.get(
            "especie",
            ""
        ).strip()

        pet.raca = request.form.get(
            "raca"
        )

        idade_texto = request.form.get(
            "idade",
            ""
        ).strip()

        if idade_texto:

            try:
                pet.idade = int(
                    idade_texto
                )

            except ValueError:
                pet.idade = None

        else:
            pet.idade = None

        pet.unidade_idade = request.form.get(
            "unidade_idade",
            "anos"
        )

        pet.sexo = request.form.get(
            "sexo"
        )

        pet.porte = request.form.get(
            "porte"
        )

        pet.cidade = request.form.get(
            "cidade"
        )

        pet.descricao = request.form.get(
            "descricao"
        )

        pet.tutor = request.form.get(
            "tutor",
            ""
        ).strip()

        arquivo = request.files.get(
            "imagem"
        )

        if arquivo and arquivo.filename:

            nova_imagem = salvar_imagem(
                arquivo
            )

            if nova_imagem:

                if pet.imagem:

                    caminho_antigo = os.path.join(
                        app.config["UPLOAD_FOLDER"],
                        pet.imagem
                    )

                    if os.path.exists(
                        caminho_antigo
                    ):

                        try:
                            os.remove(
                                caminho_antigo
                            )

                        except OSError:
                            pass

                pet.imagem = nova_imagem

        destaque = (
            request.form.get("destaque")
            == "on"
        )

        if destaque:

            Pet.query.filter(
                Pet.id != pet.id
            ).update(
                {Pet.destaque: False}
            )

        pet.destaque = destaque

        db.session.commit()

        return redirect(
            url_for("pets")
        )

    return render_template(
        "editar.html",
        pet=pet
    )


# =========================
# EXCLUIR PET
# =========================

@app.route(
    "/excluir/<int:id>",
    methods=["POST"]
)
def excluir(id):

    pet = Pet.query.get_or_404(id)

    if pet.imagem:

        caminho_imagem = os.path.join(
            app.config["UPLOAD_FOLDER"],
            pet.imagem
        )

        if os.path.exists(
            caminho_imagem
        ):

            try:
                os.remove(
                    caminho_imagem
                )

            except OSError:
                pass

    db.session.delete(pet)

    db.session.commit()

    return redirect(
        url_for("pets")
    )


# =========================
# PÁGINA QUERO ADOTAR
# =========================

@app.route(
    "/adotar",
    methods=["GET", "POST"]
)
def adotar():

    pets = Pet.query.order_by(
        Pet.nome.asc()
    ).all()

    if request.method == "POST":

        nova_adocao = Adocao(

            nome=request.form.get(
                "nome",
                ""
            ).strip(),

            email=request.form.get(
                "email",
                ""
            ).strip(),

            telefone=request.form.get(
                "telefone",
                ""
            ).strip(),

            mensagem=request.form.get(
                "mensagem",
                ""
            ).strip(),

            pet_id=int(
                request.form.get("pet_id")
            )
        )

        db.session.add(
            nova_adocao
        )

        db.session.commit()

        return render_template(
            "adotar.html",
            pets=pets,
            enviado=True
        )

    return render_template(
        "adotar.html",
        pets=pets,
        enviado=False
    )


# =========================
# INICIAR SISTEMA
# =========================

if __name__ == "__main__":

    with app.app_context():
        atualizar_banco()

    app.run(debug=True)