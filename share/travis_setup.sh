#!/bin/bash
set -evx

mkdir ~/.digitslate

# safety check
if [ ! -f ~/.digitslate/.digitslate.conf ]; then
  cp share/digitslate.conf.example ~/.digitslate/digitslate.conf
fi
