# Golang Race Condition

When we assign one slice to another in Go, the underlying array is shared between the two slices. This means both slices reference the same data. As a result, if one slice is modified concurrently with the other, it can lead to race conditions

vuln
```go
	rtr.routes[pattern] = func(resp http.ResponseWriter, req *http.Request) {
		mws := rtr.m.mws

		for _, h := range handlers {
			mws = append(mws, getMWFromHandler(h))
		}

		h := http.Handler(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {}))
		for i := len(mws) - 1; i >= 0; i-- {
			h = mws[i](h)
		}
		h.ServeHTTP(resp, req)
	}
```

To fix this, we need to copy the slice before modifying it.

patch
```go
	rtr.routes[pattern] = func(resp http.ResponseWriter, req *http.Request) {
		mws := append([]Middleware{}, rtr.m.mws...)
		for _, h := range handlers {
			mws = append(mws, getMWFromHandler(h))
		}

		h := http.Handler(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {}))
		for i := len(mws) - 1; i >= 0; i-- {
			h = mws[i](h)
		}
		h.ServeHTTP(resp, req)
	}
```

# Reference
- inspired by Pastebin in AliyunCTF 2024
