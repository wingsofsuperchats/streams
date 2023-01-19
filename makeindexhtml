import json
import os
import datetime
from dateutil import tz

def format_starttime(start_time):

    return datetime.datetime.fromtimestamp(start_time, tz=tz.gettz('US/Eastern')).strftime('%Y-%m-%d %H:%M:%S')

def format_usd(usd):

    return '$' + format(usd, '.10g')

def format_seconds_to_hhmmss(seconds):

    hours = seconds // (60*60)
    seconds %= (60*60)
    minutes = seconds // 60
    
    if (hours == 0):
        return '%i Minutes' % (minutes)
    if (hours == 1):
        return "%i Hour and %i Minutes" % (hours, minutes)
    
    return "%i Hours and %i Minutes" % (hours, minutes)
   
def htmlrow_stream(rows, start_time, duration, usd, filename):
    
    start_time = format_starttime(start_time)
    duration = format_seconds_to_hhmmss(duration)
    usd = format_usd(usd)
    
    row=f"""
        <tr>
	    <td>{start_time}</td>
	    <td>{duration}</td>
	    <td>{usd}</td>
	    <td><a href="{filename}.html">View</a></td>
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
                <th>Start Time (EST)</th>
                <th>Duration</th>
                <th>Superchats</th>
                <th>View</th>
            </tr>
        </thead>
        <tbody>
          {1}
        </tbody>
    </table>
    """.format('<br>'.join(title), ''.join(rows))
    
    return html    

rows=[]
title = ''
total=0
start_time=0
end_time=0

files = os.listdir('data/')
files = sorted(files, key=lambda x: int(x), reverse=True)

for filename in files:
    with open('data/' + filename, 'r', encoding='utf-8') as file:
        for event in json.load(file):
            if (event['event'] == 'end'):
                end_time = event['time'] 
                total = event['usd']    
            if (event['event'] == 'start'):
                start_time = event['time']

    htmlrow_stream(rows, start_time, end_time-start_time, total, filename) 
  
title = ['Wings stream history']
page = html_table(title, rows)

f = open('html/index.html', "w")
f.write(page)
f.close()  
