#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Copyright (c) 2019 Paolo D'Emilio
#
# This file is part of Bulker.
#
# Bulker is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Bulker is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Bulker.  If not, see <https://www.gnu.org/licenses/>.

import argparse
import fnmatch
import io
import os
import locale
try:  # Python 2.X
    from Tkinter import *
    import tkFileDialog as filedialog, tkMessageBox as messagebox
except ImportError:  # Python 3.X
    from tkinter import *
    from tkinter import filedialog, messagebox


licenses = {"0": "Creative Commons 0", "by": "Attribution", "nc": "Attribution Noncommercial"}


class GuiArgs:
    """
    This class allows the create_csv module function to work both with the command line arguments and with the ones
    derived from the GUI, as it offers the same syntax as the object created by argparse's parse_args
    """
    dir_name = ""
    pattern = ""
    desc_file = ""
    encoding = ""
    tags = ""
    name_tags = False
    name_sep = "_"
    geotag = ""
    license = ""
    pack_name = ""
    explicit = False
    output_file = ""
    

class App:

    def __init__(self, master):
        """
        Sets up the GUI and the default values.
        :param master: the parent for the created widgets
        """

        self.args = GuiArgs()
        self.dir_name = StringVar()
        self.dir_name.set("")
        self.pattern = StringVar()
        self.desc_file = StringVar()
        self.encoding = StringVar()
        self.license = StringVar()
        self.license.set("0")
        self.name_tags = BooleanVar()
        self.name_tags.set(False)
        self.name_sep = StringVar()
        self.explicit = BooleanVar()
        self.explicit.set(False)
        self.output_file = StringVar()

        w = Label(master, text="Directory of sounds")
        w.grid(row=0, sticky=E)
        self.t_dir = Entry(master, width=50, textvariable=self.dir_name)
        self.t_dir.grid(row=0, column=1, sticky=W+E)
        self.b_dir = Button(master, text="...", command=self.pick_sound_dir)
        self.b_dir.grid(row=0, column=2, sticky=W)
        w = Label(master, text="  Pattern")
        w.grid(row=0, column=3, sticky=E)
        self.t_pat = Entry(master, width=10, textvariable=self.pattern)
        self.pattern.set("*")
        self.t_pat.grid(row=0, column=4)

        w = Label(master, text="Pack name")
        w.grid(row=1, sticky=E)
        self.t_name = Entry(master)
        self.t_name.grid(row=1, column=1, sticky=W+E)
        w = Label(master, text="  License")
        w.grid(row=1, column=2, sticky=E)
        r_0 = Radiobutton(master, text="CC 0", variable=self.license, value="0")
        r_0.grid(row=1, column=3)
        r_by = Radiobutton(master, text="Attribution", variable=self.license, value="by")
        r_by.grid(row=1, column=4)
        r_nc = Radiobutton(master, text="Non Commercial", variable=self.license, value="nc")
        r_nc.grid(row=1, column=5)

        w = Label(master, text="Geotag")
        w.grid(row=2, sticky=E)
        self.t_geo = Entry(master)
        self.t_geo.grid(row=2, column=1, sticky=W+E)
        c_exp = Checkbutton(master, text="Mark as explicit content", variable=self.explicit)
        c_exp.deselect()
        c_exp.grid(row=2, column=3, columnspan=2, sticky=W)

        w = Label(master, text="Description file")
        w.grid(row=3, sticky=E)
        self.t_desc = Entry(master, textvariable=self.desc_file)
        self.t_desc.grid(row=3, column=1, sticky=W+E)
        self.b_desc = Button(master, text="...", command=self.pick_desc_file)
        self.b_desc.grid(row=3, column=2, sticky=W)
        w = Label(master, text="Text encoding")
        w.grid(row=3, column=3, sticky=E)
        self.t_enc = Entry(master, textvariable=self.encoding)
        self.t_enc.grid(row=3, column=4, sticky=W)

        w = Label(master, text="Tags")
        w.grid(row=4, sticky=E)
        self.t_tag = Entry(master)
        self.t_tag.grid(row=4, column=1, sticky=W+E)
        self.c_atag = Checkbutton(master, text="Add tags from the file name", variable=self.name_tags)
        self.c_atag.deselect()
        self.c_atag.grid(row=4, column=3, columnspan=2, sticky=W)
        w = Label(master, text="  Separator")
        w.grid(row=4, column=5, sticky=E)
        self.t_sep = Entry(master, width=5, textvariable=self.name_sep)
        self.name_sep.set("_")
        self.t_sep.grid(row=4, column=6, sticky=W)

        w = Label(master, text="Output file")
        w.grid(row=5, sticky=E)
        self.t_out = Entry(master, textvariable=self.output_file)
        self.t_out.grid(row=5, column=1, sticky=W+E)
        self.b_out = Button(master, text="...", command=self.pick_csv_file)
        self.b_out.grid(row=5, column=2, sticky=W)

        frame_but = Frame(master)
        frame_but.grid(row=100, column=3, columnspan=2)
        self.quit = Button(frame_but, text="QUIT", command=master.quit)
        self.quit.pack(side=LEFT)
        self.csv = Button(frame_but, text="Create CSV", command=self.create_csv)
        self.csv.pack(side=LEFT)

        master.grid_columnconfigure(1, weight=1)
        master.grid_columnconfigure(2, weight=1)

    def pick_sound_dir(self):
        """
        Lets the user choose the directory with the sounds via dialog and sets the value in the corresponding entry.
        """
        dir_name = filedialog.askdirectory()
        if dir_name:
            self.dir_name.set(dir_name)

    def pick_desc_file(self):
        """
        Lets the user choose the description file via dialog and sets the value in the corresponding entry.
        """
        desc_file = filedialog.askopenfilename(initialdir=self.dir_name or "/", title="Select description file",
                                               filetypes=(("text files", "*.txt"), ("all files", "*.*")))
        if desc_file:
            self.desc_file.set(desc_file)

    def pick_csv_file(self):
        """
        Lets the user choose the output file via dialog and sets the value in the corresponding entry.
        """
        output_file = filedialog.asksaveasfilename(initialdir=self.output_file or "/", title="Select output file",
                                                   filetypes=(("csv files", "*.csv"), ("all files", "*.*")))
        if output_file:
            self.output_file.set(output_file)

    def create_csv(self):
        """
        Gets the options from the GUI and, if they're valid, creates the csv.
        """
        self.args.dir_name = self.t_dir.get()
        self.args.pattern = self.t_pat.get()
        self.args.desc_file = self.t_desc.get()
        self.args.tags = self.t_tag.get()
        self.args.name_tags = self.name_tags.get()
        self.args.name_sep = self.t_sep.get()
        self.args.geotag = self.t_geo.get()
        self.args.license = self.license.get()
        self.args.pack_name = self.t_name.get()
        self.args.explicit = self.explicit.get()
        self.args.output_file = self.t_out.get()
        print("args: ", self.args.dir_name, self.args.pattern, self.args.desc_file, self.args.tags, self.args.name_tags,
              self.args.name_sep, self.args.geotag, self.args.license, self.args.pack_name, self.args.explicit,
              self.args.output_file)
        if args_ok(self.args, gui=True):
            create_csv(self.args, gui=True)


def quote(text):
    """
    Puts the specified non-empty text in double quotes.
    :param str text: the text to quote
    :return str: the quoted text if text is non-empty, an empty string otherwise
    """
    if text:
        try:
            return '"' + text + '"'
        except TypeError:
            return ""
    else:
        return ""


def add_tags_from_name(tags, name, sep):
    """
    Splits the sound name into words according to the separator, and adds them as tags to the tag list, eliminating
    eventual duplicates.
    :param str tags: the current tags (space-separated string)
    :param str name: the sound name
    :param str sep: the separator character or string
    :return list: the updated tag list
    """
    tag_list = list(set(tags.split(" ") + os.path.splitext(name)[0].split(sep)))
    return quote(" ".join(tag_list))


def is_geotag_valid(geotag):
    """
    Checks the validity of the geotag, according to the constraints in Freesound's FAQ here:
    https://freesound.org/help/faq/#i-have-many-sounds-to-upload-is-there-a-way-to-describe-many-sounds-in-bulk
    :param str geotag: the geotag to check
    :return bool: True if the tag is valid, False otherwise
    """
    if geotag is None or geotag == '':
        return True
    try:
        data = geotag.split(", ")
        if len(data) != 3:
            return False
        if abs(float(data[0])) > 90.0 or abs(float(data[1])) > 180.0 or int(float(data[2])) not in range(11, 22):
            return False
    except ValueError:
        return False
    return True


def warn(title, msg, gui):
    """
    Shows a message to the user, either in console or in a graphical message box.
    :param str title: the title for the message box (ignored in the command line case)
    :param str msg: the message
    :param bool gui: indicates if using the GUI or not
    """
    if gui:
        messagebox.showinfo(title, msg)
    else:
        print(msg)


def get_encodings(text_encoding):
    """
    Returns a list of encodings, starting with the current locale and, if specified, the one from the options.
    :param str text_encoding: user specified text_encoding
    :return list: the list of encodings
    """
    # Refer to https://docs.python.org/2/library/codecs.html#standard-encodings to add more at will
    encodings = ["UTF-8"]
    loc = locale.getlocale()[1]
    if loc not in encodings:
        encodings = [loc] + encodings
    if text_encoding and text_encoding != "UTF-8":  # if one is specified by command-line argument, always try it first
        encodings = [text_encoding] + encodings
    return encodings


def read_desc_file(desc_file, text_encoding="UTF-8"):
    """
    Reads the description file, using the specified encoding.
    :param str desc_file: the description file path
    :param str text_encoding: the specified encoding
    :return list: the list of text lines with the description
    """
    try:  # Python 3.X
        with open(desc_file, mode="r", newline=None, encoding=text_encoding) as f:
            desc = f.read()
    except TypeError:  # Python 2.X
        with io.open(desc_file, mode="rU", encoding=text_encoding) as f:
            desc = f.read()
    desc = '"' + desc.replace('"', '\\"') + '"'
    return desc


def get_desc(desc_file, text_encoding):
    """
    Reads the description file, trying the available encodings and the user specified encoding, if present.
    :param str desc_file: the description file path
    :param text_encoding: the user specified encoding
    :return list: the list of text lines with the description
    """
    for encoding in get_encodings(text_encoding):
        try:
            return read_desc_file(desc_file, text_encoding=encoding)
        except UnicodeDecodeError:
            pass
    return None


def create_csv(args, gui):
    """
    Creates the csv and saves it into the output file if specified, or prints it to the console.
    :param args: the arguments, specified either via command line or via GUI
    :param bool gui: indicates if using the GUI or not
    """
    desc = get_desc(args.desc_file, args.encoding)
    if not desc:
        warn("Attention", "Description file text encoding not supported.", gui)
        return
    csv = [u"audio_filename,name,tags,geotag,description,license,pack_name,is_explicit\n"]
    files = os.listdir(args.dir_name)
    for file_name in files:
        if fnmatch.fnmatch(file_name, args.pattern):
            if args.name_tags:
                tags = add_tags_from_name(args.tags, file_name, args.name_sep)
            else:
                tags = quote(args.tags)
            line = ",".join([file_name, file_name, tags, quote(args.geotag), desc, licenses[args.license.lower()],
                             args.pack_name or '', str(int(args.explicit))]) + "\n"
            csv.append(line)
    if args.output_file:
        if os.path.exists(args.output_file) and not gui:
            try:  # Python 2.X
                choice = raw_input("Destination file " + args.output_file + " exists. Overwrite? [y/N] ")
            except NameError:  # Python 3.X
                choice = input("Destination file " + args.output_file + " exists. Overwrite? [y/N] ")
            if str(choice).lower() != 'y':
                return
        try:
            with io.open(args.output_file, "w", encoding="utf8") as f:
                f.writelines(csv)
        except IOError:
            warn("Attention", "Error: writing file " + args.output_file + " failed.", gui)
    else:
        for line in csv:
            print(line[:-1])


def args_ok(args, gui):
    """
    Checks the validity of the arguments, showing messages in case of errors.
    :param args: the arguments, specified either via command line or via GUI
    :param gui: indicates if using the GUI or not
    :return bool:
    """
    result = True
    if not os.path.exists(args.dir_name):
        warn("Attention", "Error: directory of sounds " + args.dir_name + " not found.", gui)
        result = False
    if not os.path.exists(args.desc_file):
        warn("Attention", "Error: description file " + args.desc_file + " not found.", gui)
        result = False
    if not args.tags:
        warn("Attention", "Error: missing tags.", gui)
        result = False
    if not is_geotag_valid(args.geotag):
        warn("Attention", "Error: geotag " + args.geotag + " not valid.", gui)
        result = False
    return result


def handle_command_line():
    """
    Handles the command line arguments and, if they're valid, creates the csv.
    """
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     epilog="Run bulker without arguments to show its GUI.")
    parser.add_argument("-d", "--dir", dest="dir_name", metavar="DIR", required=True, help="directory of sounds")
    parser.add_argument("-p", "--pattern", default="*",
                        help="optional pattern of files to describe, e.g. -p \"sample*.wav\" (used with -d)")
    parser.add_argument("-n", "--name", dest="pack_name", help="pack name")
    parser.add_argument("-l", "--license", choices=["0", "by", "nc"], required=True, default="0", help="license")
    parser.add_argument("-g", "--geotag", help="geotag in double quotes, e.g. \"41.40348, 2.189420, 18\"")
    parser.add_argument("-x", "--explicit", action="store_true", help="mark sounds as explicit content")
    parser.add_argument("-df", "--desc", dest="desc_file", required=True, help="text file with the description")
    parser.add_argument("-e", "--encoding", help="encoding of the text file with the description")
    parser.add_argument("-t", "--tags", required=True, help="tags in double quotes, e.g. \"tag1 tag2\"")
    parser.add_argument("-nt", "--name_tags", action="store_true", help="make extra tags from words in the file name")
    parser.add_argument("-ns", "--name_sep", default="_", help="name separator e.g. \"-\" (used with -nt)")
    parser.add_argument("-o", "--output_file", help="output file name, standard output used if omitted")
    args = parser.parse_args()
    if args_ok(args, gui=False):
        create_csv(args, gui=False)


def show_gui():
    """
    Shows the Tk GUI.
    """
    try:
        root = Tk()
        root.title("Bulker")
        app = App(root)
        root.mainloop()
        root.destroy()
    except TclError:
        print("The GUI can only be shown in a graphical environment.")


def main():
    """
    Shows the GUI if no arguments are provided, handles the command line otherwise.
    """
    if len(sys.argv) == 1:
        show_gui()
    else:
        handle_command_line()


if __name__ == "__main__":
    main()
