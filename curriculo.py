from flask import Flask

crcl = Flask(__name__)

@crcl.route('/')
def decorator():
    return'''
                <!DOCTYPE html>
            <html lang="pt-BR">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Currículo - [Seu Nome]</title>
                <style>
                    a { color: #9f743c;}
                    body { font-family: Arial, sans-serif; background: #2b2825; line-height: 1.6; color: #cf974e; max-width: 800px; margin: 0 auto; padding: 20px; }
                    h1 { color: #cf974e; text-align: center; }
                    h2 { color: #cf974e; border-bottom: 2px solid #cf974e; padding-bottom: 10px; }
                    .info { text-align: center; margin-bottom: 20px; }
                    .secao { margin-bottom: 20px; }
                    .experiencia, .educacao { margin-bottom: 15px; }
                    h3 { margin-bottom: 5px; }
                    .data { font-style: italic; color: #7f8c8d; }
                </style>
            </head>
            <body>

                <header>
                    <h1>Victor Josias Parreiras Peluzo</h1>
                    <div class="info">
                        <p>[Estudante] | [Belo Hozonte, Minas Gerais]</p>
                        <p>(00)9999-9999 | <a href="mailto:[12401609@aluno.cotemig.com.br]">12401609@aluno.cotemig.com.br</a></p>
                        <p><a href="[Seu Link LinkedIn]" target="_blank">LinkedIn</a> | <a href="[Seu Link Portfólio]" target="_blank">Portfólio</a></p>
                    </div>
                </header>

                <section class="secao">
                    <h2>Resumo Profissional</h2>
                    <p>[Escreva um breve resumo sobre sua trajetória, habilidades principais e objetivos.]</p>
                </section>

                <section class="secao">
                    <h2>Experiência Profissional</h2>
                    <div class="experiencia">
                        <h3>[Cotemig] - [Estudante]</h3>
                        <p class="data">[Mês/Ano] – [Mês/Ano ou Atual]</p>
                        <ul>
                            <li>[Responsabilidade ou conquista principal 1]</li>
                            <li>[Responsabilidade ou conquista principal 2]</li>
                        </ul>
                    </div>
                    <!-- Adicione mais experiências aqui -->
                </section>

                <section class="secao">
                    <h2>Formação Acadêmica</h2>
                    <div class="educacao">
                        <h3>[Nome do Curso]</h3>
                        <p>[Nome da Instituição] - [Ano de Conclusão]</p>
                    </div>
                </section>

                <section class="secao">
                    <h2>Habilidades</h2>
                    <ul>
                        <li>[Habilidade 1, ex: HTML/CSS]</li>
                        <li>[Habilidade 2, ex: Gestão de Projetos]</li>
                        <li>[Habilidade 3]</li>
                    </ul>
                </section>

            </body>
            </html>

          '''

if __name__ == '__main__':
    crcl.run(debug=True)