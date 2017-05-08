#!/usr/bin/env python3
#coding: utf-8

import classes
import functs
import sys
import mylogging as log


read_json_file = functs.read_json_file
lang_handling = functs.lang_handling
encoding_string = functs.encoding_string


def select_host( lang ):
    '''Listázza a választható kiszolgálókat'''
    hosts = read_json_file( 'hosts.json' )

    while True:
        print( '\n{id:^15}{name}'.format( id=lang_handling( "identification", lang ), name=lang_handling( "host", lang ) ) )
        print( '-' * 40 )
        for host in hosts.keys():
            print( '{id:^15}{name}'.format( id=host, name=hosts[host]['host'] ) )
            
        host_id = input( '\n{ident}: '.format( ident=lang_handling( "identification", lang ) ) )

        if host_id not in hosts:
            log.warning( encoding_string( lang["errors"]["ide"].format( id=host_id ) ) )
        else:
            break

    return hosts[ host_id ]


def select_bitrate( lang ):
    while True:
        bitrate = input( '\n{bitrate}: '.format( bitrate=lang_handling( "bitrate", lang ) ) )

        if not bitrate.isdigit():
            log.warning( encoding_string( lang['errors']['num'].format( value=bitrate ) ) )
        elif int( bitrate ) < 360:
            log.warning( encoding_string( lang['errors']['sma'].format( num=bitrate ) ) )
        else:
            return bitrate


def main():
    log.debug( "Start" )
    lang = read_json_file( 'lang/hu.json' )

    try:
        bitrate = select_bitrate( lang )
        log.debug( encoding_string( lang["selected_bitrate"].format( bitrate=bitrate ) ) )

        path = 'tmp'

        host = select_host( lang )
        log.debug( encoding_string( lang["selected_host"].format( host=host['host'] ) ) )

        if "tv2.hu" in host['host']:
            obj = classes.TV2( host, lang, { 'bitrate': int( bitrate ), 'path': path } )

        obj.download_videos()
        print( obj )
    except:
        log.error( encoding_string( lang["errors"]["une"] ) )
        log.debug( sys.exc_info() )
        raise

    log.debug( "End" )
    

##############################################################################

if __name__ == "__main__":
    main()