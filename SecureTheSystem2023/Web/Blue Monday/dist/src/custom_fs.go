package main

import "io/fs"

type PublicFS struct {
	fsys fs.FS
}

func newPublicFS(fsys fs.FS) *PublicFS {
	return &PublicFS{fsys}
}

func (pf *PublicFS) Open(name string) (fs.File, error) {
	return public.Open("public/" + name)
}
