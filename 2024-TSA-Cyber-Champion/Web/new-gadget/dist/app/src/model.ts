import { Schema, model } from "mongoose"

const noteSchema = new Schema({
    author: {
        type: Schema.Types.ObjectId,
        ref: "Author",
        require: true,
    },
    title:{
        type: String,
        required: true
    },
    value: {
        type: String,
        required: true,
    }
}, { timestamps: true });

export const Note = model("Note", noteSchema);

const authorSchema = new Schema({
    name:{
        type: String,
        required: true
    },
}, { timestamps: true });

export const Author = model("Author", authorSchema)
