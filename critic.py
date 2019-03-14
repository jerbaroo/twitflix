import urllib2, json,time,re


with open('netflix-media.json') as f:
    movies = json.load(f)
    sum = 0
    for title in movies:
        title = urllib2.quote(title)
        url="https://api.themoviedb.org/3/search/movie?api_key=d35ebd1f847888700a0a5fe82f0a1cf9&query=%s" %(title)
        response = urllib2.urlopen(url)
        data = response.read()
        data = json.loads(data)['results']
        if data == []:
         #   t = re.sub('%([a-zA-Z]|[0-9])+?','',title)
            print title
            
            sum += 1
        else:
             print data[0]['vote_average']
    print sum
