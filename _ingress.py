p = '/home/hermes/.cloudflared/config-jax-briefs.yml'
s = open(p).read()
if 'quicksilver.dreytools.com' not in s:
    nl = chr(10)
    rule = '  - hostname: quicksilver.dreytools.com' + nl + '    service: http://127.0.0.1:8794'
    idx = s.find('ingress:')
    s = s[:idx + len('ingress:')] + nl + rule + s[idx + len('ingress:'):]
    open(p, 'w').write(s)
    print('rule added')
else:
    print('already present')
