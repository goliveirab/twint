import twint
import json
import gitlab
import sys
from datetime import datetime

# Configure
gl = gitlab.Gitlab('https://gitlab.com', private_token='TOKEN')
p = gl.projects.get('PROJECT ID')

accounts = [line.rstrip() for line in open("twitter_account.txt", "r")]
words = [line.rstrip() for line in open("words.txt", "r")]
if not len(sys.argv) > 1:
     raise Exception("No hay una fecha definida")
today = datetime.strptime(sys.argv[1], '%Y-%m-%d').strftime('%Y-%m-%d')
open("result.json", "w").close()

for account in accounts:
    t = twint.Config()
    t.Username = account
    t.Since = today
    t.Store_json = True
    t.Output = 'result.json'

    for word in words:
        t.Search = word
        twint.run.Search(t)

with open("result.json", "r") as result:
    for line in result:
        data = json.loads(line)
        title = ": ".join((data['name'], data['tweet'][0:50].rstrip()))
        if title not in [i.title for i in p.issues.list(state='opened')]:
            p.issues.create({
                'title': title,
                'description': " | ".join((data['tweet'], data['link'], data['date'])),
                'labels': ["automatic", "support"]
            })
