import mechanize
import time

# Get some input from the user
print '> Enter users profile'
user = raw_input('> ')
print '> Enter text to ask'
q = raw_input('> ')
print '> How many times should the query be preformed?'
times = raw_input('> ')
print ''

# Submit form inputted number of times with 2 second pauses
n = 0
while n < int(times):
    # Set up mechanize
    br = mechanize.Browser()
    br.open("http://ask.fm/" + user)

    # Find the right form for submitting our query
    for form in br.forms():
        if form.attrs['id'] == 'question_form':
            br.form = form
            break

    # Put some text in the forms textarea
    br.form['question[question_text]'] = q
    # Submit the form
    br.submit()
   
    # Keep track of how many queries we've submitted, then wait a few seconds to continue
    # Waiting a couple of seconds to preform queries will prevent the servers from blocking our IP for spamming
    n = n + 1
    time.sleep(2)
    print '> Query \'' + q + '\' submitted.'

# Tell the users some info and exit
print ''
print '> Operation complete, exiting script.'
