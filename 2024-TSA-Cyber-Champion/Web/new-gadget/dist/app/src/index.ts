import { Elysia } from "elysia";
import mongoose from "mongoose"
import { Note, Author } from "./model";

mongoose.connect(process.env.MONGO_URL || "mongodb://localhost:27017/app")

function safeMerge(target: any, source: any): any {
  for (const key in source) {
    if (key === '__proto__') {
      continue;
    }
    if (Array.isArray(source[key])) {
      target[key] = source[key]
    }
    else if (source[key] && typeof source[key] === 'object') {
      if (!target[key]) {
        target[key] = {};
      }
      safeMerge(target[key], source[key]);
    }
    else {
      target[key] = source[key];
    }
  }
  return target;
}


const app = new Elysia()
  .all("/login", () => Bun.file("public/login.html"))
  .all("/api/v1/login", async ({ request, cookie: { name } }) => {
    const data = await request.json()
    const author = await new Author(data).save()
    name.value = author._id.toString()
    name.path = "/"
    return { "message": "success" }
  })
  .derive(async ({ cookie: { name } }) => {
    return { session: await Author.findById(name.value).exec() }
  })
  .onBeforeHandle(async ({ session, query, set, request }) => {
    if (!session) {
      return set.redirect = "/login"
    }
    const json = await request.json().catch(() => { })
    safeMerge(query, json)
  })
  .all("/", async () => Bun.file("public/index.html"))
  .all("/api/v1/note", async ({ query }) => {
    return Note.findOne(query).exec()
  })
  .all("/api/v1/note", async ({ query, cookie: { name } }) => {
    query["author"] = name.value
    await new Note(query).save()
    return { "message": "success" }
  })
  .all("/api/v1/note/:_id", async ({ params }) => {
    await Note.deleteOne(params).exec()
    return { "message": "success" }
  })
  .all("/api/v1/notes", async ({ cookie: { name } }) => {
    const note = await Note.find({ author: name.value }).populate('author').exec()
    return note
  })
  .listen(3000);

console.log(
  `🦊 Elysia is running at ${app.server?.hostname}:${app.server?.port}`
);
