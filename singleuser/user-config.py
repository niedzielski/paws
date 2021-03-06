import os

mylang = 'test'
family = 'wikipedia'


custom_path = os.path.expanduser('~/user-config.py')
if os.path.exists(custom_path):
    with open(custom_path, 'rb') as f:
        exec(compile(f.read(), custom_path, 'exec'), globals())

    del f
# Clean up temp variables, since pwb issues a warning otherwise
# to help people catch misspelt config
del custom_path

# Things that should be non-easily-overridable
usernames[family]['*'] = os.environ['JPY_USER']

# If OAuth integration is available, take it
if 'CLIENT_ID' in os.environ:
    authenticate['*'] = (
        os.environ['CLIENT_ID'],
        os.environ['CLIENT_SECRET'],
        os.environ['ACCESS_KEY'],
        os.environ['ACCESS_SECRET']
    )
