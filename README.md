# gallagher-card-hacking
A repo for a working PoC of the Gallagher card exploit documented here: https://github.com/megabug/gallagher-research

This script only works with Mifare Classic (currently) and does not acount for MES.

## Why are you releasing this?

It was a culmination of the process of making my own PoC from documentation and was fairly interesting. The reading of these cards is already [implemented in FlipperZero firmware](https://github.com/flipperdevices/flipperzero-firmware/blob/dev/applications/main/nfc/plugins/supported_cards/gallagher.c)... so this poses little extra risk.

## Decoding
```
$ python3 gallagher-decode.py -h
usage: gallagher-decode.py [-h] [--read-proxmark] [-b BLOCK] [-k KEY] [hex_strings ...]

Gallagher Decoder by sealldev

positional arguments:
  hex_strings        Hex strings to process

options:
  -h, --help         show this help message and exit
  --read-proxmark    Read from proxmark card
  -b, --block BLOCK  Read from proxmark card block
  -k, --key KEY      Read from proxmark card key
```

The Proxmark can be used with `--read-proxmark` (though the device may need to be changed from `/dev/tty.usbmodemiceman1` depending on your device).

## Encoding

For whatever card you are working with, dump it with the Proxmark (with ALL keys) and store it as `base-dump.json`

```
$ python3 gallagher-encode.py -h
usage: gallagher-encode.py [-h] [-i] [--write-proxmark] [--emulate-proxmark] [-b BLOCK] [-k KEY] [--CN CN] [--FC FC] [--RC RC] [--UB UB] [--UE UE] [--UC UC] [--UD UD] [--IL IL]

Gallagher Encoder by sealldev

options:
  -h, --help          show this help message and exit
  -i, --interactive   Run in interactive mode
  --write-proxmark    Write encoded data to Proxmark3
  --emulate-proxmark  Emulate encoded data to Proxmark3
  -b, --block BLOCK   Block to write or emulate to when using Proxmark3
  -k, --key KEY       Key to read original data with using Proxmark3
  --CN CN             Value for CN
  --FC FC             Value for FC
  --RC RC             Value for RC
  --UB UB             Value for UB
  --UE UE             Value for UE
  --UC UC             Value for UC
  --UD UD             Value for UD
  --IL IL             Value for IL
```

The Proxmark can be used with `--emulate-proxmark` or `--write-proxmark` (though the device may need to be changed from `/dev/tty.usbmodemiceman1` depending on your device).

## Bruteforce
The `gallagher-bf.sh` uses the Proxmark with the `gallagher-encode.py` script to rotate through numbers sequentially. Every time the user presses the button on the Proxmark, it rotates to the next number.

## Features?
Feel free to PR or make issues. If you want a change make it yourself yada yada... I'll try to respond to issues, but it comes out of my own time, so please be respectful.