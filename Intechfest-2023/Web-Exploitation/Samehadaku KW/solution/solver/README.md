1. Obtain the secret by using a zip symlink to read /proc/self/environ.
2. Use the secret key to create your own cookie with the 'is_admin' flag set to true.
3. Now you can exploit the tar vulnerability to gain arbitrary file write.
   - Bypass the ".." by using the tar symlink to create a symlink of the parent directory.
4. Write your "yaml deserialization vuln" payload into the `config` file.
5. Trigger the yaml vulnerability by tampering with your cookie. Add the "config file" path to your cookie and then access the homepage to trigger the yaml deserialization vulnerability.
