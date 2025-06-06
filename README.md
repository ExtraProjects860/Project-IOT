# Project-IOT
Este projeto é um trabalho acadêmico focado na aplicação de conceitos de Cloud Computing, Internet das Coisas (IoT) e Indústria 4.0. O objetivo principal é desenvolver uma solução para monitoramento e controle de temperatura de ambientes, especificamente para garantir o bem-estar de animais de estimação em momentos sem supervisão. A problemática identificada foi a falta de controle de temperatura no local onde o cão de uma cliente passava os dias, o que poderia gerar riscos como desidratação, insolação, exaustão térmica, letargia, vômitos, dificuldades respiratórias e, em casos extremos, morte.

A solução desenvolvida visa oferecer uma plataforma confiável, intuitiva e segura para registro e controle de temperatura, permitindo o monitoramento em tempo real e o acionamento automático de um ventilador para baixar a sensação térmica. O projeto alinha-se aos objetivos acadêmicos de desenvolver habilidades em resolução de problemas, aplicar tecnologia da informação e promover inovação e responsabilidade sociaL.
## Tecnologias Utilizadas

### Ferramentas de Desenvolvimento:
- **Visual Studio Code**: Utilizado como ambiente de desenvolvimento integrado (IDE) para escrever e depurar o código.
- **Figma**: Ferramenta para design de interfaces e prototipagem rápida.
- **SQLite**: Utilizado para alocação, administração e design do banco de dados local e leve, garantindo operações rápidas.
- **Postman**: Utilizado para testes da API.
- **Lucidchart**: Utilizado para criação da documentação UML.

### Softwares Organizacionais:
- **Trello**: Utilizado para organização e planejamento do projeto.
- **Discord**: Plataforma para comunicação em tempo real, facilitando reuniões e discussões, além de planejamento e acompanhamento do progresso.
- **GitHub**: Serviço para controle de versão e gerenciamento do código, proporcionando acesso colaborativo.
- **Microsoft Word**: Utilizado para criação da documentação do projeto

### Linguagens de Programação, Frameworks e Equipamentos de IOT:
- **Arduíno**: Utilizado como microcontrolador, escolhido por sua popularidade, facilidade de uso e baixo custo.
- **Nodemcu**: Utilizado como placa de desenvolvimento e ponte WiFi para conexão com APIs externas, além de enviar dados do sensor de temperatura obtidos pelo Arduino.
- **Sensor de temperatura DHT22**: Utilizado para captura de dados e transformação deles em temperatura, umidade e sensação térmica dentro do sistema.
- **Protoboard, Jumpers, Relé**: Componentes utilizados para a montagem do protótipo físico, conectando dispositivos e permitindo o acionamento elétrico (como o ventilador).
- **React, JavaScript e Tailwind**: Utilizados para a construção da interface do usuário e lógica de front-end, com foco em estabilidade, modularidade e eficiência nas atualizações em tempo real.
- **Python/FastAPI**: Utilizados para o desenvolvimento do back-end, trabalhar com assincronicidade, registrar métricas do Arduino e permitir acesso rápido aos dados, sendo compatível com a abordagem RAD (Rapid Application Development).
- **C/C++**: Utilizado para programar no Arduino.
- **API’s Externas**: Utilizadas para auxílio na construção do projeto, com acesso/autenticação segura.
- **Arduino Cloud**: Plataforma integrada utilizada para a comunicação com o NodeMCU, possibilitando acesso remoto em tempo real.

## Funcionalidades
O sistema oferece diversas funcionalidades para o monitoramento e controle ambiental e a proteção do animal:
- **Monitoramento em Tempo Real**: Captação e exibição em tempo real da temperatura, umidade e sensação térmica do ambiente por meio de sensores.
- **Controle Automático de Temperatura**: Gatilho automático para acionamento de um regulador de temperatura (ex: ventilador) caso a temperatura atinja um valor acima do limite predefinido.
- **Notificações por E-mail**: Envio automático de e-mails de notificação para o usuário em caso de temperatura elevada ou acionamento do ventilador.
- **Histórico de Temperaturas**: O sistema oferece um histórico dos horários em que a temperatura ultrapassou o limite pré-definido para acompanhamento pelo cliente.
- **Registro de Eventos Anormais**: Registro de eventos de temperatura anormal (acima de um limite definido) detectada pelo sensor.
- **Cálculo da Temperatura Média**: Cálculo e exibição da temperatura média do ambiente, possivelmente utilizando a combinação de temperatura e umidade.
- **Interface Intuitiva**: Plataforma simples e de fácil manuseio para acompanhamento das informações e operação do sistema.
- **Visualização de Dados**: Exibição da temperatura atual na página inicial e apresentação dos dados registrados em uma tabela com barra de pesquisa e filtros.
- **Prevenção de Riscos**: Ajuda a reduzir riscos de insolação, desidratação e exaustão térmica no animal.
- **Redução de Custos**: Contribui para a redução de custos veterinários ao evitar tratamentos emergenciais.
- **Automação e Segurança**: Opera de forma autônoma, minimizando falhas humanas e servindo como registro de cuidados prestados ao animal.

## Diagrama de Classes UML
- Visão Geral:
![Visão Geral](https://github.com/ExtraProjects860/Project-IOT/blob/master/imgs/Vis%C3%A3o%20Geral.jpg)

- Parte 1 do Diagrama:
![Parte 1 do Diagrama](https://github.com/ExtraProjects860/Project-IOT/blob/master/imgs/Parte-1.jpg)

- Parte 2 do Diagrama:
![Parte 2 do Diagrama](https://github.com/ExtraProjects860/Project-IOT/blob/master/imgs/Parte-2.jpg)

## Esboços do Projeto
- Tela Principal:
![Tela Princippal](https://github.com/ExtraProjects860/Project-IOT/blob/master/imgs/Tela%20Principal.png)

- Tela Principal com Carregamento:
![Teça Principal com Carregamento](https://github.com/ExtraProjects860/Project-IOT/blob/master/imgs/Tela%20Principal%20com%20Carregamento.png)

## Equipe
Este Projeto está sendo desenvolvido pela equipe:

- [Davi Nascimento](https://github.com/zedark860) - Desenvolvedor Backend e criação/controle do Banco de Dados;
- [Gustavo Rodrigues](https://github.com/Gvcrodrigues99) - Realização de Testes e criação/controle da Documentação do Projeto;
- [Jamil Salomão](https://github.com/jamilsalomao) - Desenvolvedor Frontend e UI/UX;
- [Tarcísio Alves](https://github.com/Tarcisio1234) - Prototipação do Projeto e Testes.
- [Alana Karine](https://github.com/AlanaK2) - Desenvolvedor Frontend e UI/UX;

## Licença
Este projeto está sob a licença [MIT License]. Consulte o arquivo [LICENSE](LICENSE) para mais detalhes.
