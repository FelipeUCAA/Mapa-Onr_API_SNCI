🧭 Automação de Consulta SNCI – Mapa ONR
Este projeto é uma automação em Python que realiza consultas no site mapa.onr.org.br utilizando o código SNCI de imóveis rurais certificados. A automação interage com a interface do mapa, ativa a camada de certificação e realiza a busca geográfica pelo código informado.

⚙️ Funcionalidades
Validação de código SNCI via input ou argumento de terminal

Abertura automatizada do navegador com configurações antidetecção

Navegação pelo site do Mapa ONR via Selenium

Seleção da camada “SNCI - Certificação” dentro do grupo “Imóveis Rurais”

Busca geográfica pelo código SNCI informado

Interação com o mapa para exibir o imóvel

Exibição de mensagem final via popup

🛠️ Tecnologias Utilizadas
Python 3

Selenium WebDriver

WebDriver Manager

Tkinter (para input e mensagens)

Chrome (via ChromeDriver)

🚀 Como usar
1. Instale as dependências
bash
pip install selenium webdriver-manager
2. Execute o script
Você pode passar o código SNCI como argumento:

bash
python script.py 081008000136-89
Ou deixar que o script solicite via popup:

bash
python script.py
3. Resultado
O navegador será aberto, a camada será ativada e o imóvel será localizado no mapa. Ao final, uma janela informará que a consulta foi concluída.

📌 Observações
O código SNCI deve ter no mínimo 10 caracteres.

O script pode ser adaptado para rodar em servidores ou agendado via cron.

A automação foi testada com o site oficial do Mapa ONR e pode estar sujeita a mudanças na estrutura da página.

📄 Licença
Este projeto está sob a licença APACHE.
