#(c) James (Jimmy) DeLano
import requests
from bs4 import BeautifulSoup
import pandas as pd

def reverse(n):
    """This function is used to turn the names from Firstname Lastname to lastname,firstname
    
    >>> reverse('Bobby Casey')
    casey,bobby
    """
    n = n.lower()
    if "jr." in n:
        return n.replace(".","").replace(" ","")
    s = n.find(" ")
    return n[s+1:]+","+n[:s]

def times_n_plays(half):
    """This function is used to 
    """
    times = []
    events = []
    for i in list(half.children)[3:-3:2]:
        times.append(list(i.children)[1].get_text())
        if "home" in str(i):
            events.append(list(i.children)[7].get_text().replace('\n', '').lower().replace(" ",""))
        else:
            events.append(list(i.children)[3].get_text().replace('\n', '').lower().replace(" ",""))
    events.append("endofhalf")
    return times, events

def time_split(times):
    """Takes the time of the plays and returns two lists: one starting at 20:00 with the start time of the plays,
    and one ending at 0:00 with the end time of the plays.
    
    >>> time_split(['15:00', '10:00', '5:00'])
    ['20:00', '15:00', '10:00', '5:00'], ['15:00', '10:00', '5:00', '0:00']
    """
    start = "20:00"
    timex = []
    timey = []
    for time in times:
        timex.append(start)
        timey.append(time)
        start = time
    timex.append(start)
    timey.append("00:00")
    return timex, timey

def convert(players, timea, timeb, event):
    """This function turns an event into a list representing the plays. 
    It returns that vector as a list along with the williams players on the court and the start/end time.
    
    >>> convert(['foehl,jake', 'delano,jimmy'], '11:24', '11:10', delano,jimmymadedunk)
    [['delano,jimmy', 'foehl,jake'],'11:24','11:10',1,'delano,jimmy',1,'delano,jimmy',0,'',0,'',1,'delano,jimmy',
    1, 'delano,jimmy',0,'',0,'',0,'',0,'',0,'',0,'',0,'',0,'',2,'delano,jimmy',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    """
#w_result = [2pt att, 'name', 2pt made, 'name', 3pt att, 'name', 3pt made, 'name', fg att, 'name', 
#            fg made, 'name', fta, 'name', ft made, 'name', oreb, 'name', dreb, 'name', assist, 'name', 
#            tov, 'name', steal, 'name', foul 'name', block, 'name', points, 'name']
    w_result = [0,'',0,'',0,'',0,'',0,'',0,'',0,'',0,'',0,'',0,'',0,'',0,'',0,'',0,'',0,'',0,'']
#opp_result = [2pt att, 2pt made, 3pt att, 3pt made, fg att, fg made, fta, ftm, oreb, 
#              dreb, assist, tov, steal, foul, block, points]
    opp_result = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    
    players.append('team')

    for p in players:
        if p in event:
            willy = p
            break
        else:
            willy = None
    players.remove('team')

    
    #field goals
    if "jumpshot" in event or "layup" in event or "dunk" in event or "tip-in" in event:
        if "3-pt." in event:
            if "made" in event:
                if willy is not None:
                    #made 3pt.
                    for i in range(4,10+1,2):
                        w_result[i] = 1
                    for i in range(5,11+1, 2):
                        w_result[i] = willy
                    w_result[-2] = 3
                    w_result[-1] = willy
                    return [sorted(players)] + [timea, timeb] + w_result + opp_result
                else:
                    #made 3pt.
                    for i in range(2,5+1):
                        opp_result[i] = 1
                    opp_result[-1] = 3
                    return [sorted(players)] + [timea, timeb] + w_result + opp_result
            
            else:
                if willy is not None:
                    #missed 3pt.
                    w_result[4] = w_result[8] = 1
                    w_result[5] = w_result[9] = willy
                    return [sorted(players)] + [timea, timeb] + w_result + opp_result
                else:
                    #missed 3pt.
                    opp_result[2] = opp_result[4] = 1
                    return [sorted(players)] + [timea, timeb] + w_result + opp_result
            
        else:
            if "made" in event:
                if willy is not None:
                    #made 2pt
                    for i in [0,2,8,10]:
                        w_result[i] = 1
                    for i in [1,3,9,11]:
                        w_result[i] = willy
                    w_result[-2] = 2
                    w_result[-1] = willy
                    return [sorted(players)] + [timea, timeb] + w_result + opp_result
                else:
                    #made 2pt
                    for i in [0,1,4,5]:
                        opp_result[i] = 1
                    opp_result[-1] = 2
                    return [sorted(players)] + [timea, timeb] + w_result + opp_result
            else:
                if willy is not None:
                    #missed 2pt
                    w_result[0] = w_result[8] = 1
                    w_result[1] = w_result[9] = willy
                    return [sorted(players)] + [timea, timeb] + w_result + opp_result
                else:
                    #missed 2pt
                    opp_result[0] = opp_result[4] = 1
                    return [sorted(players)] + [timea, timeb] + w_result + opp_result
    #free throws  
    if "freethrow" in event:
        if "made" in event:
            if willy is not None:
                #made FT
                w_result[12] = w_result[14] = w_result[-2] = 1
                w_result[13] = w_result[15] = w_result[-1] = willy
                return [sorted(players)] + [timea, timeb] + w_result + opp_result
            else:
                #made FT
                opp_result[6] = opp_result[7] = opp_result[-1] = 1
                return [sorted(players)] + [timea, timeb] + w_result + opp_result
        else:
            if willy is not None:
                #missed FT
                w_result[12] = 1
                w_result[13] = willy
                return [sorted(players)] + [timea, timeb] + w_result + opp_result
            else:
                #missed FT
                opp_result[6] = 1
                return [sorted(players)] + [timea, timeb] + w_result + opp_result
        
    #rebounds
    if "rebound" in event:
        if "offensive" in event:
            if willy is not None:
                #oreb
                w_result[16] = 1
                w_result[17] = willy
                return [sorted(players)] + [timea, timeb] + w_result + opp_result
            else:
                #oreb
                opp_result[8] = 1
                return [sorted(players)] + [timea, timeb] + w_result + opp_result
        else:
            if willy is not None:
                #dreb
                w_result[18] = 1
                w_result[19] = willy
                return [sorted(players)] + [timea, timeb] + w_result + opp_result
            else:
                #dreb
                opp_result[9] = 1
                return [sorted(players)] + [timea, timeb] + w_result + opp_result
            
    if "assist" in event:
        if willy is not None:
            #assist
            w_result[20] = 1
            w_result[21] = willy
            return [sorted(players)] + [timea, timeb] + w_result + opp_result
        else:
            #assist
            opp_result[10] = 1
            return [sorted(players)] + [timea, timeb] + w_result + opp_result
    
    if "turnoverby" in event:
        if willy is not None:
            #turnover
            w_result[22] = 1
            w_result[23] = willy
            return [sorted(players)] + [timea, timeb] + w_result + opp_result
        else:
            #turnover
            opp_result[11] = 1
            return [sorted(players)] + [timea, timeb] + w_result + opp_result
        
    if "stealby" in event:
        if willy is not None:
            #steal
            w_result[24] = 1
            w_result[25] = willy
            return [sorted(players)] + [timea, timeb] + w_result + opp_result
        else:
            #steal
            opp_result[12] = 1
            return [sorted(players)] + [timea, timeb] + w_result + opp_result
    
    if "foulby" in event:
        if willy is not None:
            #foul
            w_result[26] = 1
            w_result[27] = willy
            return [sorted(players)] + [timea, timeb] + w_result + opp_result
        else:
            #foul
            opp_result[13] = 1
            return [sorted(players)] + [timea, timeb] + w_result + opp_result
    
    if "blockby" in event:
        if willy is not None:
            #block
            w_result[28] = 1
            w_result[29] = willy
            return [sorted(players)] + [timea, timeb] + w_result + opp_result
        else:
            #block
            opp_result[14] = 1
            return [sorted(players)] + [timea, timeb] + w_result + opp_result
    else:
        return [sorted(players)] + [timea, timeb] + w_result + opp_result
    
    
def table_for_half(plays, startTimes, endTimes, starters, bench, date, half):
    """This function calls the convert function for each event in a half (the 'plays'). It returns that list along
    with the date and half played. It does not call the convert function for events that we don't care about like
    dead ball rebounds or timeouts. It swaps out lineups too and passes the correct 'starters' to convert. Any
    issues in the html where the substitutions are put in incorrectly will be highlighted by a series of many
    'cmon's being printed out.
    """
    results = []
    for event, a, b, count in zip(plays, startTimes, endTimes, range(len(plays)+2)):
        if "timeout" in event:
            continue
            
        if "deadball" in event:
            continue
            
        if "entersthegame" in event:
            for p in bench:
                if p in event:
                    starters.append(p)
                    bench.remove(p)
            continue
        if "goestothebench" in event:
            for p in starters:
                if p in event:
                    bench.append(p)
                    starters.remove(p)
            continue

        if len(starters) != 5:
            print("cmon")

        results.append([date,half] + convert(starters, a, b, event))
    return results

#game on 20181124 has an error in the play-by-play jovan jones is credited with a 
#basket to open the second half. he never comes off the court so it had to be someone else. 
#also, not inluding jones, there's 6 players that have events happening before anyone is 
#subbed out -- this game cannot be used really

#game on 20181125 has jovan jones in to start the 2nd half when he's not in the game? 
#another 6 person confusion

#game on 20181118 has marc taylor going to the bench when marc taylor enters the game
#we don't know who actually left game and it messes everything else up

games = ["https://ephsports.williams.edu/sports/mbkb/2018-19/boxscores/20181117_998b.xml?view=plays",
        "https://ephsports.williams.edu/sports/mbkb/2018-19/boxscores/20181120_bamw.xml?view=plays",
        "https://ephsports.williams.edu/sports/mbkb/2018-19/boxscores/20181129_hbpr.xml?view=plays",
        "https://ephsports.williams.edu/sports/mbkb/2018-19/boxscores/20181201_9uxu.xml?view=plays",
        "https://ephsports.williams.edu/sports/mbkb/2018-19/boxscores/20181206_ehee.xml?view=plays",
        "https://ephsports.williams.edu/sports/mbkb/2018-19/boxscores/20181208_zdhz.xml?view=plays"]
for game in games:
    #grab raw html + date of game
    link = game
    page = requests.get(link)
    soup = BeautifulSoup(page.content, 'html.parser')
    gameID = link[link.find("boxscores")+10:link.find("_")]
    
    #navigate through/deconstruct layers of html to get to play by play and starters
    layer0 = list(soup.children)[8]
                                        #print([type(item) for item in list(layer0.children)])
    layer1 = list(layer0.children)[4]
                                        #print([type(item) for item in list(layer1.children)])
    layer2 = list(layer1.children)[1]
                                        #... etc
    layer3 = list(layer2.children)[1]
    layer4 = list(layer3.children)[5]
    layer5 = list(layer4.children)[1]
    layer6 = list(layer5.children)[3]
    layer7 = list(layer6.children)[3]
    layer8 = list(layer7.children)[3]
    
    starters = list(layer8.children)[1]
    plays = list(layer8.children)[3]

    p1 = list(plays.children)[3]
    p2 = list(p1.children)[1]
    p3 = list(p2.children)[1]

    first_half = list(p3.children)[3]
    second_half = list(p3.children)[5]
    s1 = list(starters.children)[3]

    away = list(s1.children)[1]
    home = list(s1.children)[3]
    
    #home or away game -- use this bool later to select from away or home to get starters/bench
    isHome = bool()
    if list(home.children)[3].get_text() == "Williams":
        isHome = True
    
    #get away starters/bench
    away1 = list(away.children)[5]
    away2 = list(away1.children)[1]
    away3 = list(away2.children)[1]
    away4 = list(away3.children)[1]
    away_starters_html = list(away4.children)[5]
    
    away_starters = []
    for i in list(away_starters_html.children)[3::2]:
        away_starters.append(list(list(i.children)[1].children)[3].get_text())

    away_reserves_html = list(away4.children)[7]
    away_reserves = []
    for i in list(away_reserves_html.children)[3:-2:2]:
        away_reserves.append(list(list(i.children)[1].children)[3].get_text())
    
    #get home starters/bench
    home1 = list(home.children)[5]
    home2 = list(home1.children)[1]
    home3 = list(home2.children)[1]
    home4 = list(home3.children)[1]
    home_starters_html = list(home4.children)[5]
    
    home_starters = []
    for i in list(home_starters_html.children)[3::2]:
        home_starters.append(list(list(i.children)[1].children)[3].get_text())

    home_reserves_html = list(home4.children)[7]
    home_reserves = []
    for i in list(home_reserves_html.children)[3:-2:2]:
        home_reserves.append(list(list(i.children)[1].children)[3].get_text())
    
    #get williams lineup
    if isHome:
        williams = [reverse(w) for w in home_starters]
        williams_bench = [reverse(w) for w in home_reserves]
        #opponents = [reverse(o) for o in away_starters] + [reverse(o) for o in away_reserves]

    else:
        williams = [reverse(w) for w in away_starters]
        williams_bench = [reverse(w) for w in away_reserves]
        #opponents = [reverse(o) for o in home_starters] + [reverse(o) for o in home_reserves]
    #vince brookins jr is sometimes listed in the html as 'brookins,vince' instead of 'vince brookins, jr.'
    williams_bench.append('brookins,vince')
    
    #get the plays and their start/end times
    times1, events1 = times_n_plays(first_half)
    times2, events2 = times_n_plays(second_half)
    times1a, times1b = time_split(times1)
    times2a, times2b = time_split(times2)
    
    #html doesn't give 2nd half starters (and therefore bench) so we need to find them
    second_starters = []
    for e in events2:
        if len(second_starters) < 5:
            for p in williams+williams_bench:
                if (p in e) and ("entersthegame" not in e):
                    if p not in second_starters:
                        second_starters.append(p)
        else:
            break
    second_bench = [p for p in williams+williams_bench if p not in second_starters]
    
    #turn string plays into table of values
    firsthalf = table_for_half(events1, times1a, times1b, williams, williams_bench, gameID, 1)
    secondhalf = table_for_half(events2, times2a, times2b, second_starters, second_bench, gameID, 2)
    
    cols = ['Date', 'half', 'Lineup', 'timex', 'timey', '2ptA', 'name', '2ptM', 'name', '3ptA', 'name', 
        '3ptM', 'name', 'FGA', 'name', 'FGM', 'name', 'FTA', 'name', 'FTM,', 'name', 'OREB', 'name',
        'DREB', 'name', 'Asst', 'name', 'TOV', 'name', 'Steal', 'name', 'Foul', 'name', 'Block', 'name', 
        'Pts', 'name', 'opp_2ptA', 'opp_2ptM', 'opp_3ptA', 'opp_3ptM', 'opp_FGA', 'opp_FGM', 'opp_FTA', 
        'opp_FTMf', 'opp_OREB', 'opp_DREB', 'opp_Asst', 'opp_TOV', 'opp_Steal', 'opp_Foul', 'opp_Block', 'opp_Pts']

    df = pd.DataFrame(firsthalf+secondhalf, columns=cols)
    df.to_csv(gameID+".csv", index=False)
