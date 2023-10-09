# Summary
Di challenge ini terdapat 3 vulnerability, yang pertama adalah File Upload, yang dimana file upload ini bisa kita manfaatkan untuk mengupload file HBS yang nantinya kita bisa manfaatkan untuk template injection.

Yang ke-2 adalah Arbitary File Read, dari HBS kita bisa menggunakan custom function include yang terdapat pada source code untuk membaca file /proc/fd/3 yang dimana ini merupakan file descriptor dari sqlite yang menyimpan admin password.

Yang ke-3 adalah Command Execution menggunakan wget dan juga rustc, untuk eksploitasinya bisa dilihat di script diatas, bisa juga menggunakan wget saja dengan options --preserver-permissions, thx to writeupnya mas @InersIn sudah menemukan teknik ini🔥
