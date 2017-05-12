import requests
import json
from datetime import date
from lxml import html
from lib import mylogging as log
from lib import functs


# Create shortcut functions
lang_handling = functs.lang_handling
error_handling = functs.error_handling
replace_accent = functs.replace_accent
download = functs.download


class seriesDownloader:
    def get_data( self, link, xpath_desc ):
        '''Finding data from the link with xpath_desc'''
        try:
            page = requests.get( link )
        except requests.exceptions.InvalidURL:
            log.error( error_handling( "url", self.lang, { "link": link } ) )
            return False
        except requests.exceptions.ConnectionError:
            log.error( error_handling( "con", self.lang, { "link": link } ) )
            return False

        tree = html.fromstring( page.content )
        return tree.xpath( xpath_desc )


    def print_series( self, series ):
        '''Prints the optional series and saves to the selected one.'''
        while True:

            print( '\n{id:^15}{name}'.format( id=lang_handling( "identification", self.lang ), name=lang_handling( "series", self.lang ) ) )
            print( '-' * 40 )
            for i in range( len( series ) ):
                print( '{id:^15}{name}'.format( id=i, name=series[i][0].capitalize() ) )
            
            series_id = input('\n{ident}: '.format( ident=lang_handling( "select_series", self.lang ) ) )

            if not series_id.isdigit() or int( series_id ) >= len( series ) or int( series_id ) < 0:
                log.warning( error_handling( "ide", self.lang, { "id": series_id } ) )
            else:
                break

        self.settings['show_id'] = series[ int(series_id) ][1]
        self.settings['show_name'] = series[int(series_id)][0].capitalize()

        log.debug( lang_handling( "selected_series", self.lang, { "series": series[int(series_id)][0] } ) )
        log.debug( lang_handling( "selected_series_id", self.lang, { "id": series[int(series_id)][1] } ) )


    def valid_episodes( self, episodes ):
        '''Examine the list being delivered.'''
        for value in episodes:
            if not value.isdigit():
                log.warning( error_handling( "num", self.lang, { "value": value } ) )
                return False
        return True


    def get_episodes(self):
        '''It generates a list (or range) of items to download according to the input'''
        while True:
            episodes = input( '\n{down} ( 1-10 | 1,5,30 | 11 ): '.format( down=lang_handling( "download_episodes", self.lang ) ) )
            episodes = episodes.replace(' ','')

            if ',' in episodes and '-' in episodes:
                log.warning( error_handling( "poz", self.lang ) )
                continue

            if ',' in episodes:
                episodes = episodes.strip(',')
                episodes = episodes.split(',')

                if self.valid_episodes(episodes):
                    episodes = set(episodes)
                    self.settings['episodes'] = sorted( [ int(ep) for ep in episodes ] )
                    log.debug( lang_handling( 'selected_episodes', self.lang, { "episodes": str( self.settings['episodes'] ) } ) )
                    return True
                else:
                    continue

            if '-' in episodes:
                episodes = episodes.strip('-')
                episodes = episodes.split('-')

                if len( episodes ) != 2:
                    log.warning( error_handling( "int", self.lang ) )
                    continue
                if self.valid_episodes(episodes):
                    episodes[0] = int( episodes[0] )
                    episodes[1] = int( episodes[1] )
                    self.settings['episodes'] = range( min(episodes), max(episodes) + 1 )
                    log.debug( lang_handling( 'selected_episodes', self.lang, { "episodes": str( self.settings['episodes'] ) } ) )
                    return True
                else:
                    continue

            if episodes.isdigit():
                self.settings['episodes'] = [ int( episodes ) ]
                log.debug( lang_handling( 'selected_episodes', self.lang, { "episodes": str( self.settings['episodes'] ) } ) )
                return True
            else:
                log.warning( error_handling( "num", self.lang, { "value": episodes } ) )


class TV2( seriesDownloader ):
    def __init__( self, host, lang, settings={ 'bitrate': 720, 'path': 'tmp' } ):
        self.host_settings = host
        self.host_settings['date_end'] = date.today().strftime("%Y-%m-%d")

        self.settings = settings

        self.lang = lang


    def get_series(self):
        '''Returns all series of the host in a sorted list'''
        series_l = []
        host = self.host_settings['host']
        xpath_desc = self.host_settings['series_xpath']

        print( '\n{load}...'.format( load=lang_handling( "load", self.lang ) ), end='' )

        series = self.get_data( '{host}/search.php'.format( host=host ), xpath_desc )
        if not series:
            return False

        for value in series:
            key = value.xpath('text()')[0].lower().strip()
            val = value.xpath('@value')[0]

            if val != '0': #0 - Műsor (default menu item)
                series_l.append( ( key, val ) )

        print( '{ready}'.format( ready=lang_handling( "ready", self.lang ) ) )

        return sorted( series_l, key=lambda series_l: replace_accent( series_l[0] ) )


    def search_series( self, series ):
        '''Finds the specified keyword in the series'''
        hit_series = []

        while True:
            keyword = input( '\n{search}: '.format( search=lang_handling( "series_search", self.lang ) ) )

            if len( keyword ) < 3:
                log.warning( error_handling( "min", self.lang ) )
                continue
            else:
                break

        for ser in series:
            if keyword.lower() in ser[0]:
                hit_series.append( ser )

        if len( hit_series ) == 0:
            log.warning( error_handling( "non", self.lang, { "key": keyword } ) )
            return False

        return hit_series


    def get_episode_links( self, ep ):
        '''Saves a list of slices of an episode'''
        xpath_desc = self.host_settings['episodes_xpath']
        host = self.host_settings['host']
        link = '{host}/search/{episode}/oldal1?&datumtol={date_start}&datumig={date_end}&musorid={show_id}'.format( host=host, episode=ep, date_start=self.host_settings['date_start'], date_end=self.host_settings['date_end'], show_id=self.settings['show_id'] )

        pager = self.get_data( link, self.host_settings['pager_xpath'] )
        if pager == False:
            return False

        if pager:
            if 'utolsó' in pager[-1].xpath( 'text()' )[0]:
                link = host + pager[-1].xpath( '@href' )[0]
            else:
                link = host + pager[-2].xpath( '@href' )[0]

            videos = self.get_data( link, xpath_desc )
            if not videos:
                return False
        else:
            videos = self.get_data( link, xpath_desc )

        valid_episodes = [
            ' {episode}. '.format( episode=ep ),
            ' {episode}/1. '.format( episode=ep ),
            ' {episode}/2. '.format( episode=ep ),
            ' {episode}/3. '.format( episode=ep )
        ]

        ep_links = []

        for ep_link in videos:
            for string in valid_episodes:
                if string in ep_link.xpath( 'text()' )[0]:
                    ep_links.append( ( host + ep_link.xpath( '@href' )[0], ep_link.xpath( 'text()' )[0] ) )
                    break

        return ep_links


    def get_json_url( self, link ):
        '''Returns the json file path'''
        xpath_desc = self.host_settings['script_xpath']

        scripts = self.get_data( link, xpath_desc )
        if not scripts:
            return False

        start = 'jsonUrl'
        end = '&type=json'
        jsonUrl = ''

        for script in scripts:
            result = script.find( start )
            if result != -1:
                jsonUrl = ''.join( script[ result : ].split(" ") )
                jsonUrl_result = jsonUrl.find( end )
                jsonUrl = jsonUrl[ len( start ) + 2 : jsonUrl_result + len( end ) ]
                break
                
        return jsonUrl


    def get_json_dict( self, link ):
        '''Returns a dictionary from the json file'''
        link = "http://{link}".format( link=link.lstrip("//") )

        jsonText = self.get_data( link, '//text()' )
        if not jsonText:
            return False
        else:
            jsonText = jsonText[0]
        
        return json.loads( jsonText )


    def select_bitrate( self, dictionary ):
        '''Specify the specified resolution or the nearest to the specified one'''
        bitrates = dictionary['mp4Labels']
        del bitrates[0]

        for i in range( len( bitrates ) ):
            if self.settings['bitrate'] >= int( bitrates[i].rstrip('p') ):
                break

        self.settings['tmp'] = bitrates[i]

        videoLinks = dictionary['bitrates']['mp4']

        return videoLinks[i + 1]

    def download_videos( self, start ):
        '''Download controller'''
        if start >= 0 and start < 2:
            series = self.get_series()
            if not series:
                return False

            while True:
                series_hit = self.search_series( series )
                if series_hit:
                    break

            self.print_series( series_hit )

        self.get_episodes()

        total = len( self.settings['episodes'] )
        process = 0

        for ep in self.settings['episodes']:
            log.info( '\n[{progress:3.0f}%] {ep}. {episode}'.format( progress=(100 * process / total), ep=ep, episode=lang_handling( 'episode', self.lang ) ) )
            process += 1
            ep_links = self.get_episode_links( ep )
            if not ep_links:
                log.warning( error_handling( "not", self.lang ) )
                continue

            for ep_link, ep_name in ep_links:
                jsonUrl = self.get_json_url( ep_link )
                if not jsonUrl:
                    continue

                if jsonUrl != '':
                    jsonDict = self.get_json_dict( jsonUrl )
                    if not jsonDict:
                        continue

                    link = 'http:{url}'.format( url=self.select_bitrate( jsonDict ) )
                    log.info( '[{ep} {bit}]'.format( ep=ep_name, bit=self.settings['tmp'] ) )
                    log.debug( link )
                    try:
                        download( link, "{ep}_{bit}".format( ep=ep_name, bit=self.settings['tmp'] ), self.settings['path'] )
                        log.debug( lang_handling( 'done', self.lang ) )
                    except:
                        log.error( error_handling( "dow", self.lang ) )

        print("")
        log.info( "[100%] {done}".format( done=lang_handling( "download_done", self.lang ) ) )


    def __str__( self ):
        return str( self.settings )