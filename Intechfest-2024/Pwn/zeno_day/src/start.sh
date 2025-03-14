echo $GZCTF_FLAG > /root/flag.txt
chmod 400 /root/flag.txt

su - deno -c '
  while true; do
    deno task start
  done
'
