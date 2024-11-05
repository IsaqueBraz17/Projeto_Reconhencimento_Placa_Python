# Projeto_Reconhencimento_Placa_Python

Projeto: Sistema de Estacionamento com Reconhecimento de Placas

O Sistema de Estacionamento com Reconhecimento de Placas é uma solução desenvolvida para automatizar o controle de entrada e saída de veículos, oferecendo uma gestão mais eficiente das vagas e um processo de cobrança simplificado. Utilizando tecnologias de reconhecimento óptico de caracteres (OCR) e processamento de imagem, o sistema identifica automaticamente as placas dos veículos, eliminando a necessidade de inserção manual e aumentando a precisão e rapidez nas operações de registro.<br><br>

Funcionalidades Principais:<br><br>
Interface Gráfica: Desenvolvida com a biblioteca customTkinter, a interface é intuitiva e organizada, permitindo que os usuários registrem entradas e saídas, visualizem notificações e acessem configurações personalizáveis.

Reconhecimento Automático de Placas: Com o auxílio do OpenCV e do Tesseract OCR, o sistema processa uma imagem da placa, extrai o texto e preenche automaticamente o campo de placa na interface. Isso reduz erros e agiliza o processo de entrada.

Registro de Entrada e Saída: Quando um veículo chega, o usuário pode registrar a entrada preenchendo o nome do proprietário e utilizando o reconhecimento automático da placa. O sistema armazena a hora da entrada e exibe essa informação em uma tabela de registros. Na saída, ele calcula automaticamente o valor a ser pago com base no tempo de permanência.

Controle de Vagas: A quantidade de vagas disponíveis é monitorada em tempo real. Cada nova entrada diminui uma vaga, e cada saída confirmada restaura uma vaga, ajudando na gestão da ocupação do estacionamento.

Cálculo do Pagamento e Emissão de Comprovante: No momento da saída, o sistema abre uma aba para seleção do método de pagamento e, ao finalizar, emite um comprovante digital com as informações do usuário, veículo, horário de entrada e saída, e o valor pago.

Configurações Personalizáveis: O sistema permite configurar o número total de vagas e o valor da tarifa por hora diretamente na interface, através de uma aba de configurações.

Mensagens de Notificação: A interface exibe notificações em tempo real para informar o usuário sobre o status das operações, como confirmação de entrada, alerta para vagas indisponíveis ou erro de informações.

Funções de Manutenção: Inclui botões para limpar campos, abrir configurações e sair do sistema, mantendo a interface organizada e funcional.<br><br>

Tecnologias Utilizadas:<br><br>
Python: Linguagem de programação central para lógica e interface.<br><br>
customTkinter: Biblioteca para construção de uma interface gráfica moderna e personalizável.<br><br>
OpenCV: Processamento de imagens para melhorar a qualidade da imagem da placa antes do reconhecimento.<br><br>
Tesseract OCR: Realiza o reconhecimento de texto nas imagens de placas.<br><br>
datetime: Calcula o tempo de permanência do veículo no estacionamento.<br><br><br>
Apresentação do Funcionamento:<br><br>
Ao iniciar o sistema, o operador vê uma interface amigável, onde pode registrar a entrada de um veículo com um simples clique. Usando uma câmera ou uma imagem de placa, o sistema detecta automaticamente o número da placa, o que torna o processo muito mais rápido e confiável. O sistema armazena as informações do veículo e atualiza a quantidade de vagas disponíveis. No momento da saída, o operador seleciona o método de pagamento e o sistema calcula automaticamente o valor com base no tempo de permanência, emitindo um comprovante digital para o usuário.

Este sistema é ideal para estacionamentos que desejam reduzir a intervenção manual, aumentar a precisão nos registros e oferecer um serviço de alta qualidade e eficiência aos usuários.
