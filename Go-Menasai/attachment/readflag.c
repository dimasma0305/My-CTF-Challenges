#include <stdio.h>
#include <stdlib.h>
int main()
{
   char ch;
   char file_name[] = "/root/flag.txt";
   FILE *fp;

   fp = fopen(file_name, "r");

   if (fp == NULL)
   {
      perror("Error while opening the file.\n");
      exit(EXIT_FAILURE);
   }

   while((ch = fgetc(fp)) != EOF)
      printf("%c", ch);

   fclose(fp);
   return 0;
}