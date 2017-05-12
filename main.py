#!/usr/bin/env python3
#coding: utf-8

import sys
from lib import classes
from lib import functs
from lib import mylogging as log
from lib import config as cfg


# Create shortcut functions
read_json_file = functs.read_json_file
lang_handling = functs.lang_handling
error_handling = functs.error_handling
encoding_string = functs.encoding_string

# Default paths
DOWNLOAD_PATH = cfg.DOWNLOAD_PATH
LANG_PATH = cfg.LANG_PATH


def select_host( lang ):
    '''Lists the optional hosts.

    Returns to the selected host data from the hosts.json file.'''
    hosts = read_json_file( 'hosts.json' )

    while True:
        print( '\n{id:^15}{name}'.format( id=lang_handling( "identification", lang ), name=lang_handling( "host", lang ) ) )
        print( '-' * 40 )
        for host in range( len( hosts ) ):
            print( '{id:^15}{name}'.format( id=host, name=hosts[host]['host'] ) )
            
        host_id = input( '\n{ident}: '.format( ident=lang_handling( "select_host", lang ) ) )

        if not host_id.isdigit() or int( host_id ) >= len( hosts ) or int( host_id ) < 0:
            log.warning( error_handling( "ide", lang, { "id": host_id } ) )
        else:
            break

    return hosts[ int( host_id ) ]


def select_bitrate( lang ):
    '''Specify the desired bitrate'''

    bitrates = [
        1080,
        720,
        480,
        360,
        240,
        180,
        144
    ]

    while True:
        print( '\n{id:^15}'.format( id=lang_handling( "bitrate", lang ) ) )
        print( '-' * 40 )

        for rate in bitrates:
            print( '{id:^15}'.format( id=rate ) )
        bitrate = input( '\n{bitrate}: '.format( bitrate=lang_handling( "select_bitrate", lang ) ) )

        if not bitrate.isdigit():
            log.warning( error_handling( "num", lang, { "value": bitrate } ) )
        elif int( bitrate ) not in bitrates:
            log.warning( error_handling( "bie", lang, { "bitrate": bitrate } ) )
        else:
            return bitrate


def select_option( lang ):
    '''What should be the downloads and'''
    while True:
        print( '\n{id:^15}{name}'.format( id=lang_handling( "identification", lang ), name=lang_handling( "option", lang ) ) )
        print( '-' * 40 )
        for i in range( len( lang['options'] ) ):
            print( '{id:^15}{name}'.format( id=i, name=lang[ 'options' ][i] ) )
        print( '{id:^15}{name}'.format( id="exit", name=lang_handling( "exit", lang ) ) )

        start = input( "\n{what}: ".format( what=lang_handling( "select_option", lang ) ) )

        if start != "exit" and ( not start.isdigit() or int( start ) not in range( len( lang['options'] ) ) ):
            log.warning( error_handling( "ide", lang, { "id": start } ) )
        else:
            return start


def main():
    log.debug( "Start" )

    lang = read_json_file( LANG_PATH )

    try:
        start = 0
        while True:
            if int( start ) == 0:
                bitrate = select_bitrate( lang )
                log.debug( lang_handling( "selected_bitrate", lang, { "bitrate": bitrate } ) )

                host = select_host( lang )
                log.debug( lang_handling( "selected_host", lang, { "host": host['host'] } ) )

                # select class
                if "tv2.hu" in host['host']:
                    obj = classes.TV2( host, lang, { 'bitrate': int( bitrate ), 'path': DOWNLOAD_PATH } )

            # download controller
            obj.download_videos( int( start ) )

            start = select_option( lang )
            if start == "exit":
                break
    except:
        log.error( error_handling( "une", lang ) )
        log.debug( sys.exc_info() )
        raise

    log.debug( "End" )
    

##############################################################################

if __name__ == "__main__":
    main()