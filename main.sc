require: common.js
    module = sys.zb-common
require: patterns.sc
    module = sys.zb-common
require: text/text.sc
    module = sys.zb-common
require: number/number.sc
    module = sys.zb-common

require: zenflow.sc
    module = sys.zfl-common

patterns:
    $hello = (start)

theme: /
    state: Start
        q!: $regex</start>
        a: Здравствуйте!
    
    state: Hello
        q!: $hello
        go!: /q8

    state: q8
        a: Какой пол мне указать в анкете?
        buttons:
            "Мужской"
            "Женский"
            "Не хочу отвечать"
            "Завершить опрос"

        state: Завершить опрос
            q: Завершить опрос
            go!: /End

        state: Не хочу отвечать
            q: Не хочу отвечать
            script:
                $session.var_sex = null
            go!: /q4

        state: a8
            intent: /sex
            script:
                $session.var_sex = $parseTree._var_sex
            go!: /q4

        state:
            event: noMatch
            go!: /q8

    state: q4
        a: Являетесь ли вы студентом?
        buttons:
            "Да, студент"
            "Нет, не студент"
            "Не хочу отвечать"
            "Завершить опрос"

        state: Завершить опрос
            q: Завершить опрос
            go!: /End

        state: Не хочу отвечать
            q: Не хочу отвечать
            script:
                $session.var_stud = null
            go!: /q1

        state: a4
            intent: /stud
            script:
                $session.var_stud = $parseTree._var_stud
            go!: /q1

        state:
            event: noMatch
            go!: /q4

    state: q1
        a: Если Вы студент, подскажите пожалуйста где проживаете в настоящее время?
        buttons:
            "в общежити"
            "снимаю квартиру"
            "проживаю с родителями"
            "Не хочу отвечать"
            "Завершить опрос"

        state: Завершить опрос
            q: Завершить опрос
            go!: /End

        state: Не хочу отвечать
            q: Не хочу отвечать
            script:
                $session.var_dom = null
            go!: /q2

        state: a1
            intent: /choose_dom
            script:
                $session.var_dom = $parseTree._var_dom
            go!: /q2

        state:
            event: noMatch
            go!: /q1

    state: q2
        a: Достаточная ли у Вас по Вашему мнению физическая активность?
        buttons:
            "Да"
            "Нет"
            "Не хочу отвечать"
            "Завершить опрос"

        state: Завершить опрос
            q: Завершить опрос
            go!: /End

        state: Не хочу отвечать
            q: Не хочу отвечать
            script:
                $session.q2 = null
            go!: /q6

        state: a2
            intent: /q2
            script:
                $session.q2 = $parseTree._q2
            go!: /q6

        state:
            event: noMatch
            go!: /q2

    state: q6
        a: Слышали ли вы от матери или отца, что они принимают лекарства от высокого давления?
        buttons:
            "Да"
            "Нет"
            "Не знаю"
            "Не хочу отвечать"
            "Завершить опрос"

        state: Завершить опрос
            q: Завершить опрос
            go!: /End

        state: Не хочу отвечать
            q: Не хочу отвечать
            script:
                $session.q6 = null
            go!: /q5

        state: a6
            intent: /q6
            script:
                $session.q6 = $parseTree._q6
            go!: /q5

        state:
            event: noMatch
            go!: /q6

    state: q5
        a: Имеется ли у матери или отца повышенное артериальное давление?
        buttons:
            "Да"
            "Нет"
            "Не знаю"
            "Не хочу отвечать"
            "Завершить опрос"

        state: Завершить опрос
            q: Завершить опрос
            go!: /End

        state: Не хочу отвечать
            q: Не хочу отвечать
            script:
                $session.q5 = null
            go!: /q7

        state: a5
            intent: /q5
            script:
                $session.q5 = $parseTree._q5
            go!: /q7

        state:
            event: noMatch
            go!: /q5

    state: q7
        a: Были ли у ваших родителей, бабушек, дедушек инфаркты, инсульты, случаи внезапной смерти в возрасте <55 лет для мужчин и в возрасте <65 лет для женщин?
        buttons:
            "Да"
            "Нет"
            "Не знаю"
            "Не хочу отвечать"
            "Завершить опрос"

        state: Завершить опрос
            q: Завершить опрос
            go!: /End

        state: Не хочу отвечать
            q: Не хочу отвечать
            script:
                $session.q7 = null
            go!: /q12

        state: a7
            intent: /q7
            script:
                $session.q7 = $parseTree._q7
            go!: /q12

        state:
            event: noMatch
            go!: /q7

    state: q12
        a: Курите ли Вы в настоящее время?
        buttons:
            "Да, курю"
            "Нет, не курю"
            "Не хочу отвечать"
            "Завершить опрос"

        state: Завершить опрос
            q: Завершить опрос
            go!: /End

        state: Не хочу отвечать
            q: Не хочу отвечать
            script:
                $session.var_smoke = null
            go!: /q13

        state: a12
            intent: /smoke
            script:
                $session.var_smoke = $parseTree._var_smoke
            go!: /q13

        state:
            event: noMatch
            go!: /q12

    state: q13
        if: $session.smoke != 'yes_smoke'
            go!: /End

        a: Вы курите сигареты или используете альтернативные системы нагревания табака?
        buttons:
            "Нет"
            "Не знаю"
            "Не хочу отвечать"
            "Завершить опрос"

        state: Завершить опрос
            q: Завершить опрос
            go!: /End

        state: Не хочу отвечать
            q: Не хочу отвечать
            script:
                $session.q13 = null
            go!: /End

        state: a13
            intent: /q13
            script:
                $session.q13 = $parseTree._q13
            go!: /End

        state:
            event: noMatch
            go!: /q13

    state: End
        a: Опрос завершён
        HttpRequest:
            url = https://functions.yandexcloud.net/d4ei2d94t39iaompfhs8
            method = POST
            body = {
                "interview_result": {
                    "user_id": "{{$session.userId}}", 
                    "answers": [ {
                        "question_of_interview_id": "8",
                        "question_id": "15",
                        "option_id": "{{$session.var_sex}}"
                        }, {
                        "question_of_interview_id": "4",
                        "question_id": "4",
                        "option_id": "{{$session.var_stud}}"
                        }, {
                        "question_of_interview_id": "1",
                        "question_id": "1",
                        "option_id": "{{$session.var_dom}}"
                        }, {
                        "question_of_interview_id": "2",
                        "question_id": "2",
                        "option_id": "{{$session.q2}}"
                        }, {
                        "question_of_interview_id": "6",
                        "question_id": "9",
                        "option_id": "{{$session.q6}}"
                        }, {
                        "question_of_interview_id": "5",
                        "question_id": "8",
                        "option_id": "{{$session.q5}}"
                        }, {
                        "question_of_interview_id": "7",
                        "question_id": "10",
                        "option_id": "{{$session.q7}}"
                        }, {
                        "question_of_interview_id": "12",
                        "question_id": "16",
                        "option_id": "{{$session.var_smoke}}"
                        }, {
                        "question_of_interview_id": "13",
                        "question_id": "17",
                        "option_id": "{{$session.q13}}"
                        }]
                    }
                }
            okState = /okState
            errorState = /errorState
            timeout = 5000
            headers = [{"name":"userId","value":"{{$session.userId}}"}]
            vars = [{"name":"data","value":"$httpResponse"}]
            useCertificates = false
            key = 
            certificate = 

    state: okState
        a: Отправлено
        go!: /showData

    state: errorState
        a: Не отправлено

    state: showData
        a: {{$session.data}}