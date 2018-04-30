# Monitor de Repositórios - Hackaton Dashboard

Desenvolvido para monitorar e acompanhar os projetos do *3ª Hackaton da Faculdade Católica do Tocantins*

Disponível em [dashboard-hackton](https://dashboard-hackton.herokuapp.com)


## Configuração

Para utilizar basta atualizar a lista de repositórios no método `repositories`

        def repositories():
            return [
                'https://api.github.com/repos/felipegomesgit13/ConQuest',
                'https://api.github.com/repos/brunomoraisti/AppMedigo',
                'https://api.github.com/repos/SkyList/Hackathon-prototipo',
                'https://api.github.com/repos/brunnosales/argos2',
                'https://api.github.com/repos/vilmarferreira/Triagem-AVC',
                'https://api.github.com/repos/juleow/projeto_hackathon',
                'https://api.github.com/repos/DanielArrais/snitchdedoduro',
                'https://api.github.com/repos/BersonCrios/HeavyBattleSpace',
                'https://api.github.com/repos/saviossmg/RageAttack',
                'https://api.github.com/repos/Adailsonacj/OvelhaRunner'
            ]

Criar a `client_id` e `client_secret` para acesso a [GitHub REST API v3](https://developer.github.com/v3/)

E configurar as três variaveis de ambiente no [Heroku](http://herokuapp.com/)

        client_id=XXXXXXXXXXX
        client_secret=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
        FLASK_APP=app.py