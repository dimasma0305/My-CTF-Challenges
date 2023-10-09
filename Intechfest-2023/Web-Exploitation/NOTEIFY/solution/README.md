solvernya akan menggenerate id note yang bisa kirim ke bot untuk mendapatkan XSS di akun admin dan membaca credensial akun admin di localStorage yang berisi flag
ada beberapa vulnerability yang menarik di challenge ini
Yang pertama adalah Dom Clobring, dan yang kedua adalah JSONP injection di endpoint /api/healthcheck
