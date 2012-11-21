nerd4python
===========

It is a python library which provides an interface to NERD http://nerd.eurecom.fr.

#### How to use the library

    from nerd import NERD
    text = read_your_text_file()
    timeout = set_timeout_seconds()
    n = NERD ('nerd.eurecom.fr', YOUR_API_KEY)
    n.extract(text, 'combined', timeout) 
