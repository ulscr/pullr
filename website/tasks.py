from website.models import RingingName, Place, Performance, Ringer, RingerPerformance, Footnote

import json
import re
import requests
from bs4 import BeautifulSoup as Soup
from datetime import datetime, timedelta

def query_bellboard(self, user_id):
    BB_SEARCH_URL = 'http://bb.ringingworld.co.uk/export.php?ringer='
    PAGE_URL = "&page="
    user = User.objects.get(id=user_id)
    #Get a list of bellboard names
    names = RingingName.objects.filter(user=user)

    ringingnames = RingingName.objects.all()

    time_regex = re.compile("((\d+) ?[:\.h])?[ours ]*((\d+) ?[sS])?[seconds ]*((\d+)[ mM]*)?")

    added = 0
    total_count = 0
    total_performances = 0
    for ringingname in names:
        page = 1
        continue_flag = True
        name = ringingname.name
        name_added = 0
        while True:
            xml = requests.get(BB_SEARCH_URL + name + PAGE_URL + str(page) , headers={'Accept':'application/xml'})
            request_added = 0
            data = Soup(xml.text)
            performances = data.find_all("performance")
            total_performances += len(performances)
            for performance in performances:
                total_count += 1
                self.update_state(state='PROGRESS', meta={'current':total_count, 'total':total_performances})
                try:
                    perf = Performance.objects.get(bellboardId=performance['id'].replace("P",""))
                    continue
                except Performance.DoesNotExist:
                    pass

                #First, find the place and check if it exists already
                town = ""
                dedication = ""
                county = ""
                for placename in performance.find_all("place-name"):
                    if placename['type'] == "place":
                        town = unicode(placename.string)
                    if placename['type'] == "dedication":
                        dedication = unicode(placename.string)
                    if placename['type'] == "county":
                        county = unicode(placename.string)
    
                try:
                    place = Place.objects.get(name=town, dedication=dedication, county=county)
                except:
                    place = Place()
                    place.name = town
                    place.dedication = dedication
                    place.county = county
                    try:
                        place.tenor = unicode(performance.place.ring['tenor'])
                    except KeyError:
                        place.tenor = ""
                    place.type = unicode(performance.place.ring['type'])
                    place.save()
    

                perf = Performance()

                perf.bellboardId = unicode(performance['id']).replace("P","")
                perf.date = datetime.strptime(unicode(performance.date.string), '%Y-%m-%d')
                perf.changes = int(unicode(performance.title.changes.string))
                perf.method = unicode(performance.title.method.string)
                perf.association = unicode(performance.association.string)
                try:
                    perf.details = unicode(performance.details.string)
                except:
                    perf.details = ""
                try:
                    duration = unicode(performance.duration.string)
                    match = time_regex.match(duration)
                    hours = 0
                    minutes = 0
                    seconds = 0
                    if match.group(2) is not None:
                        hours = int(match.group(2))
                    if match.group(6) is not None:
                        minutes = int(match.group(6))
                    if match.group(4) is not None:
                        seconds = int(match.group(4))
                    thetimedelta = timedelta(hours=hours, minutes=minutes, seconds=seconds)
                    perf.duration = thetimedelta
                except:
                    pass
                
                try:
                    perf.composer = unicode(performance.composer.string)
                except:
                    pass #No composer here
                

                perf.place = place
                perf.save()
                added += 1
                name_added += 1
                request_added += 1
    
                for footnote in performance.find_all("footnote"):
                    fn = Footnote(value=unicode(footnote.string), performance=perf)
                    fn.save()

                #Find the ringers
                for ringer in performance.find_all('ringer'):
                    try:
                        r = Ringer.objects.get(name=unicode(ringer.string))
                    except:
                        r = Ringer()
                        r.name = unicode(ringer.string)
                    
                        r.save()

                    #Try to match with all ringingnames
                    for namestring in ringingnames:
                        nameregex = namestring.name \
                                        .replace("\\", "\\\\") \
                                        .replace(".", "\.") \
                                        .replace("*", ".*")
                        if re.match(nameregex, r.name) and not r.ringingname:
                            r.ringingname = ringingname
                            r.save()
    

                    try:
                        rp = RingerPerformance.objects.get(performance__bellboardId=unicode(performance['id']), ringer=unicode(ringer.string))
                    except:
                        rp = RingerPerformance()
                        rp.ringer = r
                        rp.performance = perf
                        rp.bell = unicode(ringer['bell'])
                        try:
                            unicode(ringer['conductor'])
                            rp.conductor = True
                        except:
                            rp.conductor = False
                        rp.save()


                

            #END FOR PERFORMANCE
            page += 1
            if request_added != 200:
                break


        #END WHILE
    
    return str(added)

