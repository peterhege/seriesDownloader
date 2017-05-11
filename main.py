#!/usr/bin/env python3
#coding: utf-8

import classes
import functs
import sys
import mylogging as log


# Create shortcut functions
read_json_file = functs.read_json_file
lang_handling = functs.lang_handling
error_handling = functs.error_handling
encoding_string = functs.encoding_string

# Default paths
DOWNLOAD_PATH = 'tmp'
LANG_PATH = 'lang/hu.json'


def select_host( lang ):
    '''Lists the optional hosts.

    Returns to the selected host data from the hosts.json file.'''
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
    '''Specify the desired bitrate'''
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

    lang = read_json_file( LANG_PATH )

    try:
        bitrate = select_bitrate( lang )
        log.debug( lang_handling( "selected_bitrate", lang, { "bitrate": bitrate } ) )

        host = select_host( lang )
        log.debug( lang_handling( "selected_host", lang, { "host": host['host'] } ) )

        # select class
        if "tv2.hu" in host['host']:
            obj = classes.TV2( host, lang, { 'bitrate': int( bitrate ), 'path': DOWNLOAD_PATH } )

        # download controller
        obj.download_videos()
    except:
        log.error( error_handling( "une", lang ) )
        log.debug( sys.exc_info() )
        raise

    log.debug( "End" )
    

##############################################################################

if __name__ == "__main__":
    main()