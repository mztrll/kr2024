import json
from json.encoder import INFINITY
from zipfile import ZipFile

with open('specification.json') as json_file:
  data = json.load(json_file)

with open('addition.json') as json_file:
  addData = json.load(json_file)


def make_sequence(data):
  sequence = []
  ids = []
  priority_data = {}
  for i in range(len(data)):
    priority_id = INFINITY
    question_id = -1
    for j in range(len(data)):
      if data[j]['priority'] < priority_id:
        priority_data = data[j]
        priority_id = data[j]['priority']
        question_id = data[j]['question_of_interview_id']
        data[j]['priority'] = INFINITY
    sequence.append(priority_data)
    ids.append(question_id)
  return sequence


def make_state(question, next_question_id):
  state = f"\n\n    state: q{question['question_of_interview_id']}"

  conditions_intent_id = ''
  
  if question['question_conditions']:
    operand_question_id = question['question_conditions'][0]['operand_question_id']
    for item in data:
      if item['question_of_interview_id'] == operand_question_id:
        conditions_question_id = item['question_id'] 
        for item in addData:
          if conditions_question_id == item['question_id']:
            conditions_intent_id = item['intent_id']
    
    if conditions_intent_id:
      state += f"\n        if: $session.{conditions_intent_id} != '{question['question_conditions'][0]['q_options'][0]['text']}'"
    else:
      state += f"\n        if: $session.q{question['question_conditions'][0]['operand_question_id']} != '{question['question_conditions'][0]['q_options'][0]['text']}'"
    if next_question_id != -1:
      state += f"\n            go!: /q{next_question_id}\n"
    else:
      state += "\n            go!: /End\n"

  state += f"\n        a: {question['question_name']}"

  state += "\n        buttons:"
  for option in question['question_options']:
    state += f'\n            "{option["option_text"]}"'
  state += '\n            "Не хочу отвечать"'
  state += '\n            "Завершить опрос"'

  state += "\n\n        state: Завершить опрос"
  state += "\n            q: Завершить опрос"
  state += "\n            go!: /End"

  intent_id = ''
  entity_name = ''

  for item in addData:
    if question['question_id'] == item['question_id']:
      intent_id = item['intent_id']
      entity_name = item['slots'][0]['name']

  state += "\n\n        state: Не хочу отвечать"
  state += "\n            q: Не хочу отвечать"

  if intent_id:
    state += f'\n            script:\n                $session.{entity_name} = null'
  else:
    state += f"\n            script:\n                $session.q{question['question_of_interview_id']} = null"
  if next_question_id != -1:
    state += f"\n            go!: /q{next_question_id}"
  else:
    state += "\n            go!: /End"

  state += f"\n\n        state: a{question['question_of_interview_id']}"

  if intent_id:
    state += f"\n            intent: /{intent_id}"
    state += f"\n            script:\n                $session.{entity_name} = $parseTree._{entity_name}"
  else:
    state += f"\n            intent: /q{question['question_of_interview_id']}"
    state += f"\n            script:\n                $session.q{question['question_of_interview_id']} = $parseTree._q{question['question_of_interview_id']}"
  if next_question_id != -1:
    state += f"\n            go!: /q{next_question_id}"
  else:
    state += "\n            go!: /End"
  '''for option in question['question_options']:
    state += f"\n\n        state: {option['option_text']}"
    state += f"\n            q: {option['option_text']}"
    state += f"\n            script:\n                $session.q{question['question_of_interview_id']} = $request.query"
    if next_question_id != -1:
      state += f"\n            go!: /q{next_question_id}"
    else:
      state += "\n            go!: /End"'''

  state += "\n\n        state:"
  state += "\n            event: noMatch"
  state += f"\n            go!: /q{question['question_of_interview_id']}"
  return state


def write_state_to_file(state):
  with open('src/main.sc', 'a') as file:
    file.write(state)
    file.close()


def make_entity(question):
  values = ''
  entity_name = ''

  for item in addData:
    if question['question_id'] == item['question_id']:
      values = item['slots'][0]['values']
      entity_name = item['slots'][0]['name']

  s = ' {'
  s += '\n    "entity" : {'
  s += f'\n      "id" : {question["question_of_interview_id"]},'
  if entity_name:
    s += f'\n      "name" : "{entity_name}",'
  else:
    s += f'\n      "name" : "q{question["question_of_interview_id"]}",'
  s += '\n      "enabled" : true,'
  s += '\n      "type" : "annotation",'
  s += '\n      "priority" : 1,'
  s += '\n      "noSpelling" : false,'
  s += '\n      "noMorph" : false,'
  s += '\n      "phoneticSearch" : false,'
  s += '\n      "fuzzySearch" : false,'
  s += '\n      "client" : false'
  s += '\n    },'
  s += '\n    "records" : ['

  count = 0

  for option in question['question_options']:
    s += ' {'
    s += f'\n      "id" : {option["option_id"]},'
    s += '\n      "type" : "synonyms",'
    s += f'\n      "rule" : [ "{option["option_text"]}" ],'
    s += f'\n      "value" : "{option["option_id"]}"'
    s += '\n    }'
    count += 1
    if count != len(question['question_options']):
      s += ','
  s += ' ]'
  s += '\n  }'
  return s


def make_intent(question):
  intent_id = ''
  entity_name = ''

  for item in addData:
    if question['question_id'] == item['question_id']:
      intent_id = item['intent_id']
      entity_name = item['slots'][0]['name']

  s = ' {'
  s += f'\n    "id" : {question["question_of_interview_id"]},'

  if intent_id:
    s += f'\n    "path" : "/{intent_id}",'
  else:
    s += f'\n    "path" : "/q{question["question_of_interview_id"]}",'
  s += '\n    "enabled" : true,'
  s += '\n    "businessShared" : false,'
  s += '\n    "business" : false,'
  s += '\n    "phrases" : ['
  count = 0
  for option in question['question_options']:
    count += 1
    s += ' {'
    s += f'\n      "text" : "{option["option_text"]}"'
    s += '\n    }'
    if count != len(question['question_options']):
      s += ','
  s += ' ],'
  s += '\n    "patterns" : [ ],'
  s += '\n    "slots" : [ {'

  if entity_name:
    s += f'\n      "name" : "{entity_name}",'
    s += f'\n      "entity" : "{entity_name}",'
  else:
    s += f'\n      "name" : "q{question["question_of_interview_id"]}",'
    s += f'\n      "entity" : "q{question["question_of_interview_id"]}",'
  s += '\n      "required" : true,'
  s += f'\n      "prompts" : [ "{question["question_name"]}" ]'
  s += '\n    } ]'
  s += '\n  }'
  return s


def write_main_sc(data):
  s = '''require: common.js
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
        q!: $hello'''

  count = 0
  s += f"\n        go!: /q{data[count]['question_of_interview_id']}"

  with open('src/main.sc', 'w') as file:
    file.write(s)

  for item in make_sequence(data):
    if count != len(data) - 1:
      count += 1
      write_state_to_file(
          make_state(item, data[count]['question_of_interview_id']))
    else:
      write_state_to_file(make_state(item, -1))

  with open('specification.json') as json_file:
    data = json.load(json_file)
    
  count = 0
  body = 'body = {'
  body += '''\n                "interview_result": {
                    "user_id": "{{$session.userId}}", 
                    "answers": ['''

  for item in make_sequence(data):
    body += ' {'
    body += f'\n                        "question_of_interview_id": "{item["question_of_interview_id"]}",'
    body += f'\n                        "question_id": "{item["question_id"]}",'
    
    intent_id = ''
    entity_name = ''

    for item2 in addData:
      if item['question_id'] == item2['question_id']:
        intent_id = item2['intent_id']
        entity_name = item2['slots'][0]['name']

    if intent_id:
      body += f'\n                        "option_id": "{{{{$session.{entity_name}}}}}"'
    else:
      body += f'\n                        "option_id": "{{{{$session.q{data[count]["question_of_interview_id"]}}}}}"'
    body += '\n                        }'
    if count != len(data) - 1:
      count += 1
      body += ','
    else:
      body += ']'
      body += '\n                    }'
      body += '\n                }'

  s = f'''\n\n    state: End
        a: Опрос завершён
        HttpRequest:
            url = https://functions.yandexcloud.net/d4ei2d94t39iaompfhs8
            method = POST
            {body}
            okState = /okState
            errorState = /errorState
            timeout = 5000
            headers = [{{"name":"userId","value":"{{{{$session.userId}}}}"}}]
            vars = [{{"name":"data","value":"$httpResponse"}}]
            useCertificates = false
            key = 
            certificate = 

    state: okState
        a: Отправлено
        go!: /showData

    state: errorState
        a: Не отправлено

    state: showData
        a: {{{{$session.data}}}}'''

  with open('src/main.sc', 'a') as file:
    file.write(s)
    file.close()


def write_caila_import_json(data):
  s = '''{
  "project" : {
    "id" : "",
    "name" : "",
    "folder" : "/jaicp"
  },
  "settings" : {
    "language" : "ru",
    "spellingCorrection" : false,
    "classificationAlgorithm" : "sts",
    "timezone" : "Europe/Moscow",
    "extendedSettings" : {
      "tokenizerEngine" : "default"
    },
    "businessShared" : false,
    "business" : false
  },'''
  s += '\n  "intents" : ['

  count = 0

  for item in data:
    count += 1
    s += make_intent(item)
    if count != len(data):
      s += ','

  s += ' ],'

  s += '\n  "entities" : ['

  count = 0

  for item in data:
    count += 1
    s += make_entity(item)
    if count != len(data):
      s += ','

  s += ' ],'

  s += '\n  "enabledSystemEntities" : [ "duckling.number", "duckling.time", "duckling.duration", "duckling.phone-number", "duckling.email", "duckling.url" ]'
  s += '\n}'

  with open('caila_import.json', 'w') as file:
    file.write(s)
    file.close()


def zip_files():
  zip = ZipFile("questionnaire.zip", "w")
  zip.close()
  zip = ZipFile("questionnaire.zip", "a")
  zip.write("src/main.sc")
  zip.write("caila_import.json")
  zip.write("chatbot.yaml")
  zip.write("test/test.xml")
  zip.close()


write_caila_import_json(data)
write_main_sc(data)
zip_files()
