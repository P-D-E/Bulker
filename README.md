# Bulker
Bulker is a command-line tool written in Python that helps you create a CSV file for bulk description of files uploaded to Freesound ( https://freesound.org ).


## Usage
Running bulker.py with -h or --help will tell you this:

usage: bulker.py [-h] -d DIR [-p PATTERN] [-n PACK_NAME] -l {0,by,nc}
                 [-g GEOTAG] [-x] -df DESC_FILE -t TAGS [-nt] [-ns NAME_SEP]
                 [-o OUTPUT_FILE]

optional arguments:
  -h, --help            show this help message and exit

  -d DIR, --dir DIR     directory of sounds (default: None)

  -p PATTERN, --pattern PATTERN
                        optional pattern of files to describe, e.g. -p
                        "sample*.wav" (used with -d) (default: *)

  -n PACK_NAME, --name PACK_NAME
                        pack name (default: None)

  -l {0,by,nc}, --license {0,by,nc}
                        license (default: None)

  -g GEOTAG, --geotag GEOTAG
                        geotag in double quotes, e.g. "41.40348, 2.189420, 18"
                        (default: None)

  -x, --explicit        mark sounds as explicit content (default: False)

  -df DESC_FILE, --desc DESC_FILE
                        text file with the description (default: None)

  -t TAGS, --tags TAGS  tags in double quotes, e.g. "tag1 tag2" (default:
                        None)

  -nt, --name_tags      make extra tags from words in the file name (default:
                        False)

  -ns NAME_SEP, --name_sep NAME_SEP
                        name separator e.g. "-" (used with -nt) (default: _)

  -o OUTPUT_FILE, --output_file OUTPUT_FILE
                        output file name, standard output used if omitted
                        (default: None)

Run bulker without arguments to show its GUI.


## Assorted notes
The name_tags option splits the file name based on the "_" character (unless specified otherwise with the -ns option), so the name Standup_Bass_Normal_F4.wav will add the tags "standup bass normal f4" to the ones specified with the --tags option, eliminating eventual duplicates.

The geotag syntax is checked according to Freesound's FAQ here:
https://freesound.org/help/faq/#i-have-many-sounds-to-upload-is-there-a-way-to-describe-many-sounds-in-bulk


## Requirements
At the current version, Bulker only relies on core modules, and it runs both on Python 2.X and 3.X; the only requirement is Python itself.


## Acknowledgements
- Freesound ( https://freesound.org ) for being an awesome sound resource for everyone.
- Phillip Jay Cohen ( https://freesound.org/people/pjcohen/ ) for inspiring the creation of Bulker.
