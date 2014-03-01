#!/usr/bin/python

import subprocess
import os
import string
from argparse import ArgumentParser

parser = ArgumentParser(description="Page fetcher")
parser.add_argument(
    '--name', type=str,
    help=("Name of the Webpages.pages file, " +
          "which contains URLs to fetch and save to the " +
          "Webpages/ directory."))
args = parser.parse_args()

def sanitize_file(file):
  "Turn a URL into a valid filename."
  valid = "-_.() %s%s" % (string.ascii_letters, string.digits)
  return ''.join(c for c in file if c in valid)

def delete_dir(dir):
  with open('/dev/null', 'w+') as null:
    subprocess.Popen("rm -r %s" % dir, shell=True,
                     stdout=null, stderr=null).wait()


if __name__ == '__main__':
  internetdir = os.getcwd() + '/Internet'
  cachedir = os.getcwd() + '/cache'
  outdir = os.getcwd() + '/' + args.name
  fetchlogdir = outdir + '.fetchlog'

  pages = []
  with open(args.name + '.pages', 'r') as namefile:
    pages = namefile.readlines()
  pages = [p.strip() for p in pages if len(p.strip()) != 0]

  for d in [outdir, fetchlogdir]:
    delete_dir(d)
    os.makedirs(d)

  try:
    for page in pages:
      print "Fetching %s" % page
      delete_dir(internetdir)
      delete_dir(cachedir)
      command = ('DISPLAY=:1 ' + os.getcwd() + '/test_shell ' +
                 '--stats --save_files %s') % page
      logfile = fetchlogdir + '/' + sanitize_file(page)
      with open(logfile, 'w+') as log:
        subprocess.Popen(command, shell=True,
                         stdout=log, stderr=log).wait()
      subprocess.Popen('cp -R %s/* %s/' % (internetdir, outdir),
                       shell=True).wait()
  finally:
    delete_dir(internetdir)
    delete_dir(cachedir)
