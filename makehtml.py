import json
import os
import emoji

def format_usd(usd):

    return '$' + format(usd, '.10g')

def htmlrow_wingsmessage(rows, message):
    
    row=f"""
        <tr>
	    <td><b>Wings Message</b></td>
	    <td></td>
	    <td><b>{message}</b></td>
        </tr>
        """
        
    rows.append(row)
    
def htmlrow_superchat(rows, user, usd, message):
    
    usd = format_usd(usd)
    
    row=f"""
        <tr>
	    <td>{user}</td>
	    <td>{usd}</td>
	    <td>{message}</td>
        </tr>
        """
        
    rows.append(row)    
    
def html_table(title, rows):

    html="""
    <div class="styled-header">
      <style>
          .styled-header {{
            margin: 10px 0;
            font-family: sans-serif;
          }};
      </style>
    {0}
    </div>

    <table class="styled-table">
        <thead>
          <style>
            .styled-table {{
                border-collapse: collapse;
                font-size: 0.9em;
                font-family: sans-serif;
                min-width: 400px;
                box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);
            }}
            .styled-table thead tr {{
                background-color: #009879;
                color: #ffffff;
                text-align: left;
            }}
            .styled-table th,
            .styled-table td {{
                padding: 12px 26px;
            }}
            .styled-table tbody tr {{
                border-bottom: 1px solid #dddddd;
            }}
          </style>
            <tr>
                <th>User</th>
                <th>Amount</th>
                <th>Message</th>
            </tr>
        </thead>
        <tbody>
          {1}
        </tbody>
    </table>
    """.format('<br>'.join(title), ''.join(rows))
    
    return html

def format_seconds_to_hhmmss(seconds):

    hours = seconds // (60*60)
    seconds %= (60*60)
    minutes = seconds // 60
    
    if (hours == 0):
        return '%i Minutes' % (minutes)
    if (hours == 1):
        return "%i Hour and %i Minutes" % (hours, minutes)
    
    return "%i Hours and %i Minutes" % (hours, minutes)

files = os.listdir('data/')
files = sorted(files, key=lambda x: int(x), reverse=True)

for filename in files:

    rows=[]
    total=0
    start_time=0
    end_time=0

    with open('data/' + filename, 'r', encoding='utf-8') as file:
        for event in json.load(file):
            if (event['event'] == 'wings_message'):
                htmlrow_wingsmessage(rows, emoji.emojize(event['text']))
            if (event['event'] == 'superchat'):
                htmlrow_superchat(rows, event['author'], event['usd'], emoji.emojize(event['text']))
            if (event['event'] == 'end'):
                end_time = event['time'] 
                total = event['usd']    
            if (event['event'] == 'start'):
                start_time = event['time']     
                    
    title = ['Stream duration: ' + format_seconds_to_hhmmss(end_time - start_time),
             'Superchat total: $' + str(int(round(total)))]
    page = html_table(title, rows)

    f = open('html/' + filename + '.html', "w")
    f.write(page)
    f.close()
