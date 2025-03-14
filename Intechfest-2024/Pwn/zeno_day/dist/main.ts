export default {
  fetch: async (req: Request) => {
    let filedesc = null;
    let temp = null;
    try {
      if (req.url.includes("..")) {
        return new Response(`403 Forbidden`, { status: 403 });
      }
      const basePath = `http://${req.headers.get("host")}`
      const pathname = req.url.replaceAll(basePath, '')
      try {
        const body = await req.formData();
        const file = body.get("file");
        if (file) {
          if (file instanceof File) {
            temp = await Deno.makeTempFile({"suffix": ".json"});
            filedesc = await Deno.open(temp, { write: true });
            await Deno.write(filedesc.rid, new Uint8Array(await file.arrayBuffer()));
          }
        }
      } catch (error) {
        console.error(error);
      }

      try {
        let path = pathname.slice(1) || "./deno.json";
        path = "./" + path;
        if (pathname === "/") {
          if (temp) {
            path = temp;
          }
        }
        const type = "application/json";
        const jsonPackage = await import(`${path}`, {
          with: {
            type: 'json'
          }
        });
        return new Response(JSON.stringify(jsonPackage), {
          headers: new Headers({
            "content-type": type,
          }),
        });
      } catch (error: unknown) {
        console.error(error);
        return new Response(`package is not a valid json`, { status: 400 });
      }
    } catch (e) {
      console.error(e);
      return new Response(`500 Internal Server Error`, { status: 500 });
    }
    finally {
      if (filedesc) {
        filedesc.close();
      }
      if (temp) {
        await Deno.remove(temp);
      }
    }
  }
}
