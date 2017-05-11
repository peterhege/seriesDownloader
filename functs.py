import json
import mylogging as log
import sys
import requests

def read_json_file( link ):
    '''Read a json file'''
    try:
        with open( link ) as f:
            return json.load( f )
    except FileNotFoundError:
        log.error( "No such file or directory: '{file}'".format( file=link ) )
        sys.exit(0)


def encoding_string( s ):
    '''Coding accurate characters'''
    text = s
    d = {
        "Ã¡": "á",
        "Ã©": "é",
        "Ã­": "í",
        "Ã³": "ó",
        "Ã¶": "ö",
        "Å‘": "ő",
        "Ãº": "ú",
        "Ã¼": "ü",
        "Å±": "ű",
        "Ã‰": "É"
    }

    for c, to in d.items():
        if c in text:
            text = text.replace( c, to )

    return text


def lang_handling( code, lang, lang_dict=False ):
    '''Returning the language texts'''
    if lang_dict:
        return encoding_string( lang[ code ].format( **lang_dict ) )
    return encoding_string( lang[ code ] )


def error_handling( code, lang, lang_dict=False ):
    '''Returning the error texts'''
    if lang_dict:
        return encoding_string( lang['errors'][ code ].format( **lang_dict ) )
    return encoding_string( lang['errors'][ code ] )


def replace_accent(s):
    '''Change the accented characters in a string'''
    d = {
        'á':'a',
        'é':'e',
        'í':'i',
        'ó':'o',
        'ö':'o',
        'ő':'o',
        'ú':'u',
        'ü':'u',
        'ű':'u',
    }

    new = []
    for c in s:
        if c in d:
            new.append(d[c])
        else:
            new.append(c)

    return ''.join( new )


def download( link, name, path ):
    '''Download an mp4 file with progress'''
    down_name = replace_accent( name.replace(" ","_").replace('.','').replace('/','_').replace('-','_').lower() )
    file_name = "{path}/{file_name}.mp4".format( path=path, file_name=down_name )
    progress_length = 50

    with open( file_name, "wb" ) as f:
        response = requests.get(link, stream=True)
        total_length = response.headers.get('content-length')

        if total_length is None: # no content length header
            f.write( response.content )
        else:
            dl = 0
            total_length = int( total_length )
            for data in response.iter_content( chunk_size=4096 ):
                dl += len( data )
                f.write(data)
                done = int( progress_length * dl / total_length )
                print( "\r[{1}{2}] [{2:5.1f}%]".format( '=' * done, ' ' * ( progress_length - done ), 100 * dl / total_length ), end='' )
            print("")